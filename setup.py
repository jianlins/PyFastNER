from distutils.core import setup

setup(
	name='PyFastNER',
	packages=['PyFastNER'],  # this must be the same as the name above
	version='1.0dev1',
	description='A fast implementation of dictionary based named entity recognition.',
	author='Jianlin',
	author_email='jianlinshi.cn@gmail.com',
	url='https://github.com/jianlins/PyFastNER',  # use the URL to the github repo
	download_url='https://github.com/jianlins/PyFastNER/archive/1.0dev1.tar.gz',  # I'll explain this in a second
	keywords=['PyFastNER', 'ner', 'regex'],  # arbitrary keywords
	license='Apache License, Version 2.0',
	classifiers=[
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Development Status :: 0.1 - Beta",
		"Intended Audience :: Developers",
		"License :: Apache License, Version 2.0",
		"Operating System :: OS Independent",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Text Processing :: Linguistic :: Natural Language Processing",
	],
	install_requires=[
		'intervaltree',
	],
	data_files=[('demo_data', ['conf/crule_test.tsv'])],
)
