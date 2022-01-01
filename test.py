from imdata import ImData, SizeError

imd = ImData()

matrix = list(range(100))
ctx = "fuck it bitch" * 20

matrix_dt = imd.bytes_pix(matrix=matrix)
ctx_dt = imd.bytes_pix(ctx)


matrix_o = imd.pix_bytes(matrix_dt)
ctx_o = imd.pix_bytes(ctx_dt)

print(matrix_o, ctx_o, sep='\n')

with open("test.bmp", 'wb') as f:
    imd.save(f, ctx)

with open('test.bmp', 'rb') as f:
    imd.read(f)
    print(imd.content)
