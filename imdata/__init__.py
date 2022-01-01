import codecs # use codecs to encode or decode a string or a bytes
import base64 # turn all bytes into ascii codes
import zlib # compress the bytes in
import math # for auto choosing the size

import numpy as np # the array for the im
import imageio # to save the image


class ImData:
    "A class to save the string data by img, can format in tiff, tif, png type."

    content = None
    imdata = None

    format = 'bmp'

    def __init__(self, content = None):
        if content:
            self.content = content
            self.imdata = self.bytes_pix(content)

    def save(self, filename = None, content = None):
        """
        filename can be str, pathlib.Path or file object
        """
        ctt = content if content else self.content
        if not ctt:
            raise TypeError("no content given in")

        if self.imdata:
            return imageio.imsave(filename, self.imdata, format=self.format)
        else:
            return imageio.imsave(filename, self.bytes_pix(ctt), format=self.format)

    def read(self, filename = None):
        """
        filename can be a str, pathlib.Path or file object
        also can be plain bytes data (im data)
        """

        self.imdata = imageio.imread(filename, format=self.format)
        self.content = self.pix_bytes(self.imdata)


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

    def bytes_pix(self, bs = None, size = None, encode='utf-8', matrix = None):
        """
        turn bytes into pixel info
        
        Args:
            bs = None: The bytes or the string you wish to turn to imdata
            size = None: you can set the size your self, or it will use _autosize to get the size from length 
            matrix = None: the list or list-like object (get content by index), if it's given, bs is no use anymore
        """
        if not matrix:
            base = base64.b85encode(zlib.compress(self.to_bytes(bs, encode))) # change to base85 string, only use ascii letters
        else:
            base = matrix

        if size:
            size = (*size, 3) # get the im size
            length = self._size(size) # get max data length
            if len(base) > length:
                raise SizeError('size not enough for data, please use bigger size.')
        else:
            size = self._autosize(len(base))
            length =  self._size(size)
        im = np.zeros(length, dtype='uint8') # create lear data


        # predata, has a chuck data place
        # 1 for type, 4 for size
        # type 0 for  bs, type 1 for plain matrix
        im[0] =  1 if matrix else 0
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
        """
        row = pix.reshape(-1)
        rtype = row[0]
        
        length = 0
        for i in range(4):
            length |= row[1 + i] << (i * 8)

        if rtype == 1:
            return row[5 : length + 5]
        else:
            stri = ''.join(chr(code) for code in row[5 : length + 5])
            return zlib.decompress(base64.b85decode(self.to_bytes(stri)))
    
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
        # 在这里取整，可以减少一点误差，但不能完全保证横竖比
        return tuple(math.ceil(i) for i in size)

class SizeError(Exception): pass
