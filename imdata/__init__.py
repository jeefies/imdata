import codecs # use codecs to encode or decode a string or a bytes
import base64 # turn all bytes into ascii codes
import zlib # compress the bytes in
import math # for auto choosing the size

import numpy as np # the array for the im
import imageio # to save the image


class ImData:
    "A class to save the string data by img, can format in tiff, tif, png, bmp."

    content = None
    imdata = None

    format = 'bmp'

    def __init__(self, content = None):
        self.content = content

    def save(self, filename = None, content = None, **kwargs):
        """
        filename can be str, pathlib.Path or file object
        kwargs is for bytes_pix that will use in this function
        self.content will update to content given after using this
        """
        self.content = ctt = content if content else self.content
        if not ctt:
            raise TypeError("no content given in")

        return imageio.imsave(filename, self.bytes_pix(ctt, **kwargs), format=self.format)

    def read(self, filename = None):
        """
        filename can be a str, pathlib.Path or file object
        also can be plain bytes data (im data)
        """

        self.imdata = imageio.imread(filename, format=self.format)
        self.content = self.pix_bytes(self.imdata)

    @property
    def data(self):
        if self.content is not None:
            return self.bytes_pix(self.content)
        return None


    @staticmethod
    def to_bytes(s, code='utf-8'):
        "Change param s into bytes, according to encode(default 'utf-8')"
        if isinstance(s, bytes):
            return s # if it's bytes, return the raw arg
        try:
            return codecs.encode(s, code) # try to encode the string according to given encode
        except TypeError:
            try:
                return codecs.encode(s, 'utf-8') # use default encode to try again
            except:
                pass
            try:
                return bytes(s) # just use bytes to turn it into bytes
            except:
                raise TypeError('Not a right object to change into bytes') # Final error

    @staticmethod
    def to_string(b, code='utf-8'):
        "Change param b into string, according to encode(default 'utf-8')"
        if isinstance(b, str):
            return b # if it's str, return the raw string
        try:
            return codecs.decode(b, code) # try to decode the bytes according to gievn encode
        except TypeError:
            try:
                return codecs.decode(b, 'utf-8') # use default encode to try again
            except TypeError:
                try:
                    return str(b) # Just use str to turn it
                except:
                    raise TypeError("Not a right object to change into string") # final error

    def bytes_pix(self, bs = None, size = None, encode='utf-8', matrix = None, matrix_compress = False):
        """
        turn bytes into pixel info
        
        Args:
            bs = None: The bytes or the string you wish to turn to imdata
            size = None: 
                you can set the size your self, or it will use _autosize to get the size from length 
                Notice that there's 5 place should be remained for info
            matrix = None: 
                the list or list-like object (get content by index), if it's given, bs is no use anymore
                remember every number should smaller than 256 (exculde 256)
        """
        if not matrix:
            base = base64.b85encode(zlib.compress(self.to_bytes(bs, encode))) # change to base85 string, only use ascii letters
            imtype = 0
        else:
            base = matrix
            imtype = 1
            if matrix_compress:
                base = zlib.compress(bytes(matrix))
                imtype = 2

        if size:
            size = (*size, 3) # get the im size
            length = self._size(size) # get max data length
            if len(base) + 5 > length:
                raise SizeError('size not enough for data, please use bigger size.')
        else:
            size = self._autosize(len(base) + 5)
            length =  self._size(size)
        im = np.zeros(length, dtype='uint8') # create lear data


        # predata, has a chuck data place
        # 数据头，记录数据大小
        # 1 place (8 bits) for type, 4 place (32 bits) for size
        # 8 bits 记录数据类型，32 bits 记录数据长度
        # 8 bits 占一位
        # type 0 for bs, type 1 for plain matrix, type 2 for bs matrix
        # 类型0 为单纯的字符数据，类型1 是数组数据，类型2 是压缩过后的数组数据
        # type 3 for chencode, it's an extra lib
        # more see github.com/jeefies/chencode main.py function to_imdata_pixels
        # 类型3 是checode里的一中加密方式，是一个额外的库(也是我写的^_^)
        # 详见 github.com/jeefies/chencode main.py to_imdata_pixels
        im[0] =  imtype
        content_length = len(base)
        for i in range(4):
            im[1 + i] = content_length & (0xff << (i * 8))

        for index, lt in enumerate(base): # notice enumerate would change the bytes into numbers automaticly
            im[index + 5] = lt
        return im.reshape(size).astype('uint8')

    @classmethod
    def _size(cls, size):
        "get the pixel numbers"
        if isinstance(size, int):
            return size
        res = 1
        for i in iter(size):
            res *= cls._size(i)
        return res

    def pix_bytes(self, pix):
        """
        turn pixels into bytes or matrix data
        notice the matrix data would turn to numpy.array type
        plain text data would turn to bytes
        把图像数据转为实际数据，
        """
        # 将三维图像数组转为一维
        row = pix.reshape(-1)
        # 获取图像类型，字符串，还是字节数组
        imtype = row[0]
        
        # 获取余下的信息
        length = 0
        for i in range(4):
            length |= row[1 + i] << (i * 8)

        # imtype:
        # 0 for base and zlib
        # 1 for plain matrix
        # 2 for zlib + matrix
        if imtype == 1:
            # 数组就直接返回
            return row[5 : length + 5]
        elif imtype == 2:
            ctx = zlib.decompress(bytes(row[5 : length + 5]))
            return np.array(ctx, dtype="uint8")
        elif imtype == 0:
            # 字符串拼接只后会返回bytes
            stri = bytes(row[5 : length + 5])
            return zlib.decompress(base64.b85decode(stri))
        else:
            # error
            pass
    
    @staticmethod
    def _autosize(length, w = 4, h = 3):
        """
        auto generate the size of the imdata
        w, h is not the true width, but the ratio of true im size
        """
        # 先获取到需要的像素数
        length = math.ceil(length / 3)
        # 获取至少需要多少块(w, h)的像素块
        m = length / (w * h)
        # 然后获取横竖需要的块数
        # 两者应相等，这样才能保证两者比不变
        cell = math.sqrt(m)
        size = (cell * w, cell * h, 3)
        # 在这里取整，可以减少一点误差，但不能完全保证绝对横竖比
        return tuple(math.ceil(i) for i in size)

class SizeError(Exception): pass
