import string
from nlp import FastCNER

class WildCardFunctions:
	def __init__(self, processRulesFunc):
		self.wildcard_funcs = dict()
		self.initWildCardFuncs(self.wildcard_funcs)
		self.processRules = processRulesFunc
		pass

	def initWildCardFuncs(self, wildcard_funs):
		wildcard_funs['s'] = self.processWildCard_s
		wildcard_funs['n'] = self.processWildCard_n
		wildcard_funs['('] = self.processWildCard_openParan
		wildcard_funs[')'] = self.processWildCard_closeParan
		wildcard_funs['d'] = self.processWildCard_d
		wildcard_funs['C'] = self.processWildCard_C
		wildcard_funs['c'] = self.processWildCard_c
		wildcard_funs['p'] = self.processWildCard_p
		wildcard_funs['+'] = self.processWildCard_plus
		wildcard_funs['\\'] = self.processWildCard_backSlash
		wildcard_funs['a'] = self.processWildCard_a
		wildcard_funs['u'] = self.processWildCard_u
		wildcard_funs['w'] = self.processWildCard_w
		pass

	def processWildCard_s(self, text, rule_map, match_begin, match_end, current_position, matches,
						  this_char):
		if this_char == ' ' or this_char == '\t' or ord(this_char) == 160:
			self.processRules(text, rule_map['s'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 's')
		pass

	def processWildCard_n(self, text, rule_map, match_begin, match_end, current_position, matches,
						  this_char):
		if this_char == '\n' or this_char == '\r':
			self.processRules(text, rule_map['n'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'n')
		pass

	def processWildCard_openParan(self, text, rule_map, match_begin, match_end, current_position, matches,
								  this_char):
		if this_char == '(':
			self.processRules(text, rule_map['('], match_begin, match_end, current_position + 1, matches,
							  this_char, True, '(')
		pass

	def processWildCard_closeParan(self, text, rule_map, match_begin, match_end, current_position, matches,
								   this_char):
		if this_char == ')':
			self.processRules(text, rule_map[')'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, ')')
		pass

	def processWildCard_d(self, text, rule_map, match_begin, match_end, current_position, matches,
						  this_char):
		if this_char.isdigit():
			self.processRules(text, rule_map['d'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'd')
		pass

	def processWildCard_C(self, text, rule_map, match_begin, match_end, current_position, matches,
						  this_char):
		if this_char.isupper():
			self.processRules(text, rule_map['C'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'C')
		pass

	def processWildCard_c(self, text, rule_map, match_begin, match_end, current_position, matches,
						  this_char):
		if this_char.islower():
			self.processRules(text, rule_map['c'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'c')
		pass

	def processWildCard_p(self, text, rule_map, match_begin, match_end, current_position, matches,
						  this_char):
		if this_char in string.punctuation:
			self.processRules(text, rule_map['p'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'p')
		pass

	def processWildCard_plus(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char):
		if this_char.islower():
			self.processRules(text, rule_map['c'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'c')
		pass

	def processWildCard_backSlash(self, text, rule_map, match_begin, match_end, current_position, matches,
								  this_char):
		if this_char == '\\':
			self.processRules(text, rule_map['\\'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, '\\')

	def processWildCard_a(self, text, rule_map, match_begin, match_end, current_position, matches,
						  this_char):
		if not this_char.isspaces():
			self.processRules(text, rule_map['a'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'a')
			pass

	def processWildCard_u(self, text, rule_map, match_begin, match_end, current_position, matches,
						  this_char):
		if this_char > '~' and ord(this_char) != 160:
			self.processRules(text, rule_map['u'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'u')
			pass

	def processWildCard_w(self, text, rule_map, match_begin, match_end, current_position, matches,
						  this_char):
		if this_char > '~' or this_char.isspaces():
			self.processRules(text, rule_map['w'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'w')
			pass
