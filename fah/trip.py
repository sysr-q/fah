#!/usr/bin/env python2
from __future__ import print_function
import crypt
import random
import re
import string

def mktripcode(pw, salt=None):  # We 4chan now, baby!
	pw = pw.decode('utf_8', 'ignore')  \
		.encode('shift_jis', 'ignore') \
		.replace('"', '&quot;')        \
		.replace("'", '')              \
		.replace('<', '&lt;')          \
		.replace('>', '&gt;')          \
		.replace(',', ',')

	if salt is None:
		salt = ""
 
	salt += (pw + '...')[1:3]  # top kek
	salt = re.compile('[^\.-z]').sub('.', salt)
	salt = salt.translate(string.maketrans(':;<=>?@[\\]^_`', 'ABCDEFGabcdef'))
	trip = crypt.crypt(pw, salt)[-10:]
	return trip
