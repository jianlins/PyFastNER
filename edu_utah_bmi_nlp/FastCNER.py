import string

from edu_utah_bmi_nlp.IOUtils import IOUtils, Rule


class FastCNER:
	END = ('<END>')

	def __init__(self, rule_str):
		self.wildcard_funcs = dict()
		self.replication_funcs = dict()
		self.rule_str = rule_str
		io_utils = IOUtils(rule_str)
		self.rule_store = io_utils.rule_cells
		self.constructRuleMap(self.rule_store)
		self.rule_map = dict()
		self.sores = dict()
		self.initWildCardFuncs(self.wildcard_funcs)
		self.initReplicationFuncs(self.replication_funcs)

	def constructRuleMap(self, rule_store):
		for id, rule in rule_store.items():
			if '[' in rule.rule:
				rules = self.expand_square_bracket(rule)
				for subrule in rules:
					self.addRule(subrule)
			else:
				self.addRule(rule)
		pass

	# expand rules with square brackets
	def expandSquareBracket(self, rule):
		expanded_rules = []
		rule_builder = []
		rule_str = rule.rule
		# status: 0 for OUT, 1 for in
		status = 0
		pre_char = ' '
		next_ch = ' '
		branches = []
		for i in range(0, len(rule_str)):
			ch = rule_str[i]
			if i > 0:
				pre_char = rule_str[i - 1]
			if i < len(rule_str) - 1:
				next_ch = rule_str[i + 1]
			else:
				next_ch = ' '
			if status == 0 and (ch != '[' or pre_char == '\\'):
				if ch == '\\' and (next_ch == '[' or next_ch == ']'):
					pre_char = ch
					continue
				for j in range(0, len(rule_builder)):
					rule_builder[j].append(ch)
			elif status == 0 and ch == '[' and pre_char != '\\':
				status = 1
				branches = [[]]
				continue
			elif status == 1 and (ch != '[' and pre_char != '\\'):
				if ch == '|':
					branches.append([])
				elif ch == '\\' and (next_ch == '[' or next_ch == ']'):
					pre_char = ch
					continue
				else:
					branches[-1].append(ch)
			elif status == 1 and ch == ']' and pre_char != '\\':
				status == 0
				previous_size = len(rule_builder)
				if ch == '\\' and (next_ch == '[' or next_ch == ']'):
					pre_char = ch
					continue
				for j in range(0, previous_size):
					sb = rule_builder[j]
					rule_builder[j].append(branches[0])
					for k in range(1, len(branches)):
						rule_builder.append(list(sb))
						rule_builder[-1].append(branches[k])
		cleanSet = set()
		for sub_rule in rule_builder:
			rule_str = ''.join(sub_rule)
			if rule_str not in cleanSet:
				new_rule = Rule(rule.id, sub_rule, rule.score, rule.rule_name, rule.type)
				expanded_rules.append(new_rule)
				cleanSet.add(rule_str)

	def addRule(self, rule):
		determinant = rule.rule_name
		rule_map1 = self.rule_map
		rule_map2 = dict()
		length = len(rule)
		i = 0
		while i < length and rule_map1 != None and rule[i] in rule_map1:
			rule_map1 = rule_map1.get(rule[i])
			i += 1
		# if the rule has been included
		if i == length and FastCNER.END in rule_map1 and rule_map1[FastCNER.END] == determinant:
			return False
		# 		start with the determinant, construct the last descendant dict
		if i == length:
			if FastCNER.END in rule_map1:
				rule_map1[FastCNER.END][determinant] = rule.id
			else:
				rule_map2[determinant] = rule.id
				rule_map1[FastCNER.END] = rule_map2.copy()
			self.scores[rule.id] = rule.score
			return True
		else:
			rule_map2[determinant] = rule.id
			rule_map2[FastCNER.END] = rule_map2.copy()
			rule_map2.pop(determinant, None)

			for j in range(length - 1, i, -1):
				rule_mapt = rule_map2.copy()
				rule_map2.clear()
				rule_map2[rule[j]] = rule_mapt

		self.scores[rule.id] = rule.score
		rule_map1[rule[i]] = rule_map2.copy()
		return True

	def processString(self, text):
		self.processStringOffset(text, 0)

	def processStringOffset(self, text, offset):
		matches = dict()
		for i in range(0, len(text)):
			pre_char = text[i - 1] if i > 0 else ' '
			self.processRules(text, self.rule_map, i, 0, i, matches, pre_char, False, ' ')
		self.removePseudo(matches)
		return matches

	def processRules(self, text, rule_map, match_begin, match_end, current_position,
					 matches, pre_char, wildcard_support, pre_key):
		length = len(text)
		if current_position < length:
			this_char = text[current_position]

			if '\\' in rule_map:
				self.processWildCards(text, rule_map['\\'], match_begin, match_end, current_position,
									  matches, pre_char, True, '\\')
			if '(' in rule_map:
				self.processRules(text, rule_map['('], current_position, match_end, current_position,
								  matches, pre_char, False, '(')
			if ')' in rule_map:
				self.processRules(text, rule_map[')'], match_begin, current_position, current_position,
								  matches, pre_char, False, ')')

			if FastCNER.END in rule_map:
				self.addDeterminants(text, rule_map, match_begin, match_end, current_position, matches)
			if this_char in rule_map and this_char != ')' and this_char != '(':
				self.processRules(text, rule_map[this_char], match_begin, match_end, current_position + 1,
								  matches, this_char, False, this_char)

			if self.support_replication and '+' in rule_map:
				self.processRules(text, rule_map['+'], match_begin, match_end, current_position, matches, this_char,
								  False, '+')
				self.processReplication(text, rule_map['+'], match_begin, match_end, current_position, matches,
										this_char, wildcard_support, pre_key)
		elif current_position == length and FastCNER.END in rule_map:
			if match_end == 0:
				self.addDeterminants(text, rule_map, matches, match_begin, current_position, current_position)
			else:
				self.addDeterminants(text, rule_map, matches, match_begin, match_end, current_position)
		elif current_position == length and '\\' in rule_map and 'e' in rule_map['\\']:
			deter_rule = rule_map['\\']['e']
			if match_end == 0:
				self.addDeterminants(text, deter_rule, matches, match_begin, current_position, current_position)
			else:
				self.addDeterminants(text, deter_rule, matches, match_begin, match_end, current_position)
		elif current_position == length and ')' in rule_map:
			deter_rule = rule_map[')']
			if FastCNER.END in deter_rule:
				self.addDeterminants(text, deter_rule, matches, match_begin, current_position, current_position)
			else:
				self.processRules(text, deter_rule['\\'], match_begin, current_position, current_position,
								  matches, pre_char, False, ' ')
		elif current_position == length and '+' in rule_map:
			self.processRules(text, rule_map['+'], match_begin, match_end, current_position,
							  matches, pre_char, wildcard_support, pre_key)

	def processReplication(self):

		pass

	def processWildCards(self, text, rule_map, match_begin, match_end, current_position, matches,
						 pre_char, wildcard_support, pre_key):
		this_char = text[current_position]
		for rule_char in rule_map.keys():
			self.wildcard_funcs[rule_char](text, rule_map, match_begin, match_end, current_position, matches, this_char)
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
		if not this_char > '~' and ord(this_char) != 160:
			self.processRules(text, rule_map['u'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'u')
			pass

	def processWildCard_w(self, text, rule_map, match_begin, match_end, current_position, matches,
						  this_char):
		if not this_char > '~' and ord(this_char) != 160:
			self.processRules(text, rule_map['w'], match_begin, match_end, current_position + 1, matches,
							  this_char, True, 'w')
			pass

	def initReplicationFuncs(self, replication_funcs):
		replication_funcs['s'] = self.processReplicant_s
		replication_funcs['n'] = self.processReplicant_n
		replication_funcs['d'] = self.processReplicant_d
		replication_funcs['C'] = self.processReplicant_C
		replication_funcs['c'] = self.processReplicant_c
		replication_funcs['p'] = self.processReplicant_p
		replication_funcs['a'] = self.processReplicant_a
		replication_funcs['u'] = self.processReplicant_u
		replication_funcs['w'] = self.processReplicant_w
		pass

	def processReplicant_s(self, text, rule_map, match_begin, match_end, current_position, matches, pre_char,
						   wildcard_support, pre_key):
		this_char=text[current_position]
		current_repeats=0


		pass
