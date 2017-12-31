import string


class ReplicationFunctions:
	def __init__(self, processRulesFunc, max_repeat=50):
		self.replication_funcs = dict()
		self.processRules = processRulesFunc
		self.max_repeat = max_repeat
		self.initWildCardFuncs(self.replication_funcs)
		pass

	def initWildCardFuncs(self, replication_funcs):
		replication_funcs['s'] = self.processReplication_s
		replication_funcs['n'] = self.processReplication_n
		replication_funcs['('] = self.processReplication_openParan
		replication_funcs[')'] = self.processReplication_closeParan
		replication_funcs['d'] = self.processReplication_d
		replication_funcs['C'] = self.processReplication_C
		replication_funcs['c'] = self.processReplication_c
		replication_funcs['p'] = self.processReplication_p
		replication_funcs['+'] = self.processReplication_plus
		replication_funcs['\\'] = self.processReplication_backSlash
		replication_funcs['a'] = self.processReplication_a
		replication_funcs['u'] = self.processReplication_u
		replication_funcs['w'] = self.processReplication_w
		pass

	def processReplication_s(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		current_repeats = 0
		text_length = len(text)
		while ((this_char == ' ' or this_char == '\t' or ord(this_char) == 160)
			   and current_repeats < self.max_repeat and current_position < text_length):
			current_repeats += 1
			current_position += 1
			if current_position == text_length:
				break
			this_char = text[current_position]
		self.processRules(text, rule_map, match_begin, match_end, current_position, matches, previous_char, False, '+')
		pass

	def processReplication_n(self, text, rule_map, match_begin, match_end, current_position, matches, this_char, previous_char):
		current_repeats = 0
		text_length = len(text)
		while (this_char == '\n' or this_char == '\r') and current_repeats < self.max_repeat and current_position < text_length:
			current_repeats += 1
			current_position += 1
			if current_position == text_length:
				break
			this_char = text[current_position]
		self.processRules(text, rule_map, match_begin, match_end, current_position, matches, previous_char, False, '+')
		pass

	def processReplication_d(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		current_repeats = 0
		text_length = len(text)
		while this_char.isdigit() and current_repeats < self.max_repeat and current_position < text_length:
			current_repeats += 1
			current_position += 1
			if current_position == text_length:
				break
			this_char = text[current_position]
		self.processRules(text, rule_map, match_begin, match_end, current_position, matches, previous_char, False, '+')
		pass

	def processReplication_C(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		current_repeats = 0
		text_length = len(text)
		while this_char.isupper() and current_repeats < self.max_repeat and current_position < text_length:
			current_repeats += 1
			current_position += 1
			if current_position == text_length:
				break
			this_char = text[current_position]
		self.processRules(text, rule_map, match_begin, match_end, current_position, matches, previous_char, False, '+')
		pass

	def processReplication_c(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		current_repeats = 0
		text_length = len(text)
		while this_char.islower() and current_repeats < self.max_repeat and current_position < text_length:
			current_repeats += 1
			current_position += 1
			if current_position == text_length:
				break
			this_char = text[current_position]
		self.processRules(text, rule_map, match_begin, match_end, current_position, matches, previous_char, False, '+')
		pass

	def processReplication_p(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		current_repeats = 0
		text_length = len(text)
		while this_char in string.punctuation and current_repeats < self.max_repeat and current_position < text_length:
			current_repeats += 1
			current_position += 1
			if current_position == text_length:
				break
			this_char = text[current_position]
		self.processRules(text, rule_map, match_begin, match_end, current_position, matches, previous_char, False, '+')
		pass

	def processReplication_a(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		current_repeats = 0
		text_length = len(text)
		while (not this_char.isspaces()) and current_repeats < self.max_repeat and current_position < text_length:
			current_repeats += 1
			current_position += 1
			if current_position == text_length:
				break
			this_char = text[current_position]
		self.processRules(text, rule_map, match_begin, match_end, current_position, matches, previous_char, False, '+')
		pass

	def processReplication_u(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		current_repeats = 0
		text_length = len(text)
		while (this_char > '~' and ord(this_char) != 160) and current_repeats < self.max_repeat and current_position < text_length:
			current_repeats += 1
			current_position += 1
			if current_position == text_length:
				break
			this_char = text[current_position]
		self.processRules(text, rule_map, match_begin, match_end, current_position, matches, previous_char, False, '+')
		pass

	def processReplication_w(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		current_repeats = 0
		text_length = len(text)
		while (this_char > '~' or this_char.isspaces()) and current_repeats < self.max_repeat and current_position < text_length:
			current_repeats += 1
			current_position += 1
			if current_position == text_length:
				break
			this_char = text[current_position]
		self.processRules(text, rule_map, match_begin, match_end, current_position, matches, previous_char, False, '+')
		pass

