from imdata import ImData, SizeError

# init with data
# 初始化的数据
imd = ImData("origin things here")

matrix = list(range(100))
ctx = "hello world " * 20

# 三种方式转换为像素数组
# three ways to convert to digital data
# 第一种，将字符串，字节，经压缩转换
# first one, convert string, bytes, .etc with compress
ctx_dt = imd.bytes_pix(ctx)
# 第二种，将数组信息直接转为图像信息
# 注意，数组里不能出现大于等于256的数字，且只能为整数
# second, convert num array directly into imdata
# notice, there shouldn't be any number more than 256 (256 included), and every one should be a int
matrix_dt = imd.bytes_pix(matrix=matrix)
# 第三种，将数组信息压缩后转换
# third, compress the array data and convert into imdata
cmatrix_dt = imd.bytes_pix(matrix=matrix, matrix_compress=True)

# 还原数据，注意返回的数据类型
# 数组会返回 numpy.ndarray, 字符会返回 bytes
# get the original data, notice the type returned
# matrix would turn into numpy.ndarray array, string or bytes data would turn into bytes data
matrix_o = imd.pix_bytes(matrix_dt)
ctx_o = imd.pix_bytes(ctx_dt)
cmatrix_o = imd.pix_bytes(matrix_dt)

print(matrix_o, ctx_o, cmatrix_o, sep='\n')
# imd.data是一个property，每次使用都会重新生成图像像素数据
# imd.data is a property, every time use would generate the image data according to imdata.content
# that means use it often can lower the speed of the program!
print("imdata's data:\n", imd.data)

# the way to save or read a image's data
with open("test.bmp", 'wb') as f:
    imd.save(f, ctx)
# the same as
# imd.save("test.bmp", ctx)
# also
# imd = ImData(ctx)
# imd.save("test.bmp")

with open("test.bmp", 'rb')  as f:
    imd.read(f)
# the same as
# imd.read("test.bmp")

# result save in imd.content
print(imd.content)
