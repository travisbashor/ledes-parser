from setuptools import setup, find_packages

def read_version():
    return '1.0.1'

setup(
    name='ledes-parser',
    version=read_version(),
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    author='Travis Bashor',
    author_email='travis.bashor@gmail.com',
    description='A package for parsing LEDES format files',
    url='https://github.com/travisbashor/ledes-parser',
)
