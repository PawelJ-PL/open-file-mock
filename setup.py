from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()


setup(
    name='open_mock_file',
    use_scm_version=True,
    description='Smart object for mocking open file calls, depends on file path',
    long_description=long_description,
    url='https://github.com/PawelJ-PL/open-file-mock',
    author='Pawel',
    author_email='inne.poczta@gmail.com',
    maintainer='Pawel',
    maintainer_email='inne.poczta@gmail.com',
    license='MIT',
    keywords='Python mock open file',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
    packages=find_packages(),
    extras_require={
        'test': ['coverage', 'nose', 'flake8'],
    },
    tests_require=['nose', 'coverage'],
    setup_requires=['setuptools_scm', 'wheel', 'twine'],
    python_requires='>=3',
    test_suite='nose.collector',
)
