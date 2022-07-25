from setuptools import setup

# from blog.csdn.net/tcy23456/article/details/91886555

with open('README.md') as f:
    long_des=f.read()

with open('requirements.txt') as f:
    reqs = f.read().strip().split()

setup(
        name = 'imdata',
        author = 'Jeefy',
        version = '0.0.4',
        packages = ['imdata'],
        author_email = 'jeefy163@163.com',
        description = 'A easy class for save the data by the img',
        python_requires = '>3.4',
        url = 'https://github.com/jeefies/imdata',
        long_description = long_des,
        long_description_content_type = 'text/markdown',
        # install_requires = [reqs]
        )
