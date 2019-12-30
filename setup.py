from setuptools import setup,Extension
from codecs import open
from os import path
from Cython.Build import cythonize, build_ext
import os

macros = [("CYTHON_TRACE", "1")]

# extension sources
macros = []

if macros:
    from Cython.Compiler.Options import get_directive_defaults

    directive_defaults = get_directive_defaults()
    directive_defaults['linetrace'] = True
    directive_defaults['binding'] = True

dir_path = os.path.dirname(os.path.realpath(__file__))
include_dirs = [dir_path + "/PyFastNER"]
print("include dir", include_dirs)
extensions = [
    # Extension(
    #     "quicksect", ["PyFastNER/quicksectx.pyx"],
    #     define_macros=macros,
    #     include_dirs=include_dirs),
]

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyFastNER',
    packages=['PyFastNER'],  # this must be the same as the name above
    package_dir={'PyFastNER': 'PyFastNER'},
    cmdclass={'build_ext': build_ext},
    version='1.0.8.dev3',
    description='A fast implementation of dictionary based named entity recognition.',
    author='Jianlin',
    author_email='jianlinshi.cn@gmail.com',
    url='https://github.com/jianlins/PyFastNER',  # use the URL to the github repo
    download_url='https://github.com/jianlins/PyFastNER/archive/1.0.8.dev2.zip',
    keywords=['PyFastNER', 'ner', 'regex'],
    long_description=long_description,
    ext_modules=cythonize(extensions, language_level=2),
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
        'quicksectx'
    ],
    tests_require=[
        'intervaltree',
        'kerneltree',
    ],
    data_files=[('demo_data', ['conf/crule_test.tsv'])],
    package_data={'': ['*.pyx', '*.pxd']},
    include_dirs=["."]
)
