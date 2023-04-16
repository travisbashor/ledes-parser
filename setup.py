from setuptools import setup, find_packages

def read_version():
    with open("./VERSION", "r") as version_file:
        return version_file.read().strip()

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
