from setuptools import setup
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='PyFastNER',
    packages=['PyFastNER'],  # this must be the same as the name above
    version='1.0.dev1',
    description='A fast implementation of dictionary based named entity recognition.',
    author='Jianlin',
    author_email='jianlinshi.cn@gmail.com',
    url='https://github.com/jianlins/PyFastNER',  # use the URL to the github repo
    download_url='https://github.com/jianlins/PyFastNER/archive/1.0.dev1.zip',  # I'll explain this in a second
    keywords=['PyFastNER', 'ner', 'regex'],
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    install_requires=[
        'intervaltree'
    ],
    data_files=[('demo_data', ['conf/crule_test.tsv'])],
)
