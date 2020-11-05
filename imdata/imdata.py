import codecs # use codecs to encode or decode a string or a bytes
import base64 # turn all bytes into ascii codes

import numpy as np # the array for the im
import imageio # to save the image


class ImData:
    "A class to save the string data by img, can format in tiff, tif, png type."
    @staticmethod
    def to_bytes(s, encode='utf-8'):
        "Change param s into bytes, according to encode(default 'utf-8')"
        if isinstance(s, bytes):
            return s # if it's bytes, return the raw arg
        try:
            return codecs.encode(s, encode) # try to encode the string according to given encode
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
    def to_string(b, encode='utf-8'):
        "Change param b into string, according to encode(default 'utf-8')"
        if isinstance(b, str):
            return b # if it's str, return the raw string
        try:
            return codecs.decode(b, encode) # try to decode the bytes according to gievn encode
        except TypeError:
            try:
                return codecs.decode(b, 'utf-8') # use default encode to try again
            except TypeError:
                try:
                    return str(b) # Just use str to turn it
                except:
                    raise TypeError("Not a right object to change into string") # final error

    def bytes_pix(self, bs, size = (400, 600), encode='utf-8'):
        "turn bytes into pixel info"
        base = base64.b85encode(self.to_bytes(bs, encode)) # change to base85 string, only use ascii letters
        size = (*size, 3) # get the im size
        length = self._size(size) # get max data length
        if len(base) > length:
            raise SizeError('size not enough for data, please use bigger size.')
        im = np.zeros(length, dtype='uint8') # create lear data
        for index, lt in enumerate(base): # notice enumerate would change the bytes into numbers automaticly
            im[index] = lt
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

    def pix_bytes(self, pix, encode='utf-8'):
        row = pix.reshape(-1)
        stri = ''.join(chr(code) for code in row[:] if code)
        return base64.b85decode(self.to_bytes(stri, encode))


class SizeError(Exception): pass
