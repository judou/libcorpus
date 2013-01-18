# -*- coding: utf8
import re

class Word(object):
	def __init__(self, term, pos, encoding="utf-8"):
		if encoding is None:
			self.term = term
			self.pos = pos
		else:
			self.term = term.decode(encoding)
			self.pos = pos.decode(encoding)

	def __unicode__(self):
		return u'%s/%s' % (self.term, self.pos)

	def __str__(self):
		return self.__unicode__().encode("utf-8")

class CorpusPeopleDaily(object):
	def __init__(self, filename, encoding="utf-8"):
		self.f = open(filename)
		self.encoding = encoding

	@classmethod
	def _split_word(self, pair):
		'''
		>>> CorpusPeopleDaily._split_word(u"a/b")
		(u'a', u'b')
		>>> CorpusPeopleDaily._split_word(u"a\//b")
		(u'a\\\\/', u'b')
		'''
		assert type(pair) is unicode
		split_pos = pair.find(u"/")
		prev_c = pair[split_pos-1]
		while prev_c == u"\\":
			split_pos = pair.find(u"/", split_pos+1)
			if split_pos == -1:
				break
			prev_c = pair[split_pos-1]
			if prev_c != u"\\":
				break
		term = pair[:split_pos].strip()
		pos = pair[split_pos+1:].strip()
		return term, pos

	def __iter__(self):
		lines = self.f.readlines() # into memory
		for _line in lines:
			line = _line.strip().decode(self.encoding)
			if line:
				pairs = re.split(ur" +", line)
				for pair in pairs:
					term, pos = self._split_word(pair)
					if term and pos:
						yield Word(term, pos, encoding=None)

	def close(self):
		self.f.close()

def test():
	c = CorpusPeopleDaily("/home/ant/hobbies/people-daily-98-1/people-daily.txt")
	for word in c:
	    print word.term, word.pos

def main():
	'''
	People Daily corpus sample:

	19980101-01-001-001/m  迈向/v  充满/v  希望/n  的/u  ... <CR>
	<CR>
	...

	fileencoding=utf-8 etc.
	'''
	import doctest
	doctest.testmod()

if __name__ == '__main__':
	main()