from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

VERSION = '1.0.0'
# TODO: version should be generated

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()


setup(
    name='open_mock_file',
    version=VERSION,
    description='Smart object for mocking open file calls, depends on file path',
    long_description=long_description,
    url='https://github.com/PawelJ-PL/open_file_mock',
    author='Pawel',
    author_email='inne.poczta@gmail.com',
    license='MIT',
    keywords='Python mock open file',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
    packages=find_packages(exclude=['tests']),
    extras_require={
        'test': ['coverage'],
    },
    python_requires='>=3',

)