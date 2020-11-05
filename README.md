# ImData

**Author: Jeef**  
**Email: jeefy163@163.com**

----------
## Installation
Use _git_ to clone it for the github.com.  
See [Github](https://github.com/jeefies/imdata)  
Or see [PyPI](https://pypi.org/project/imdata) to install  
`pip install imdata`.

-------------
## Usage
the main class is ImData.  
_Dependeces: imageio_  
_Advice: Use python that later than 3.5, no support for 2.7_

Imdata.bytes_pix(bs, size, encode='utf-8')
> if bs is a string, use 'encode' to encode the string.  
> size is the size of the img, such as (40, 80).  
> size is not for the length of the bs, it's about 1.4 bigger than the length.  
> for eample, if bytes is like b'my bytes', size at least should be (3,4) instead of (2,4)

ImData.pix_bytes(pix, encode='utf-8')
> The pix is the np.array object. Use `import numpy as np; pix = np.array(...)`.  
> encode for the bytes type, is want a string.  

ImData.read(uri)
> Read from the image, notice that do not read a unsupport picture.

ImData.save(uri, bytes=None, size, format)
> Save the bytes to the image.  
> format can only be in 'tif', 'tiff', 'png' but not for 'jpg', 'jpeg', 'gif' and so on.  