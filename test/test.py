import pandas as pd

# df=pd.read_csv('../conf/crule_test.tsv', header=0, sep='\t')
# print(df)
from nlp.IOUtils import IOUtils

ioutils = IOUtils('../conf/crule_test.tsv')
print(ioutils.initiations)


# for value in ioutils.rule_cells.values():
# 	print(value)


class Test:
	@staticmethod
	def assign(value):
		Test.value = value

	@classmethod
	def cls_assign(cls, value):
		Test.value = value

	def inst_assign(self, value):
		self.value = value


t = Test()
Test.assign(1)
print(Test.value)
print(t.value)
Test.cls_assign(2)
print(Test.value)
print(t.value)
t.inst_assign(3)
print(Test.value)
print(t.value)
Test.cls_assign(4)
print(Test.value)
print(t.value)


print(type('ste') is str)
a = {}
a[1] = str
print(type('ste') is a[1])

a='ddkdjoaidao'
print(a[2])
print(a[-1])
a=chr(160)
print('ord 160 is space: '+str(a.isspace()))
print('\\n is space: '+str('\n'.isspace()))

print(not False and False)
print('a'<'b')