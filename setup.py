from setuptools import setup, Extension
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
include_dirs = [dir_path + "/PyFastNER", dir_path]
print("include dir", include_dirs)
extensions = [
    # Extension(
    #     "PyFastNER", ["PyFastNER/CFastCNER.pyx"],
    #     define_macros=macros,
    #     include_dirs=include_dirs),
]


def get_version():
    for line in open(os.path.join(os.path.dirname(__file__), 'PyFastNER', '__init__.py')).read().splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def parse_requirements(requirements_file):
    requirements=open(os.path.join(os.path.dirname(__file__), requirements_file)).read().split('\n')
    requirements=[r.strip() for r in requirements]
    requirements=[r for r in requirements if len(r)>0 and not r.startswith('#')]
    return requirements

build_version=get_version()
install_reqs = parse_requirements('requirements.txt')

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyFastNER',
    packages=['PyFastNER'],  # this must be the same as the name above
    package_dir={'PyFastNER': 'PyFastNER'},
    cmdclass={'build_ext': build_ext},
    version=build_version,
    description='A fast implementation of dictionary based named entity recognition.',
    author='Jianlin',
    author_email='jianlinshi.cn@gmail.com',
    url='https://github.com/jianlins/PyFastNER',  # use the URL to the github repo
    keywords=['PyFastNER', 'ner', 'regex'],
    license='Apache License',
    long_description='PyFastNER is the python implementation of FastNER, which is orginally developed using Java. It uses hash function to process multiple rules at the same time. Similar to FastNER, PyFastNER supports token-based rules (FastNER--under developing) and character-based rules (FastCNER). It is licensed under the Apache License, Version 2.0.',
    ext_modules=cythonize(extensions, compiler_directives={'language_level': "3"}),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    install_requires=parse_requirements('requirements.txt'),
    tests_require=parse_requirements('dev-requirements.txt'),
    data_files=[('demo_data', ['conf/crule_test.tsv'])],
    package_data={'': ['*.pyx', '*.pxd']},
    include_dirs=include_dirs
)
