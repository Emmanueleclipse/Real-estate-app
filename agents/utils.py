import unicodedata,string,re,datetime

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def to_ascii(input_str):
	input_str = input_str.replace(u"\xc2",'2')
	return remove_accents(input_str).encode('ascii', 'ignore')
