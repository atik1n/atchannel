def mktripcode(pw):
	import hashlib
	pw = pw[:8]
	salt = (pw + "H.")[1:3]
	m = hashlib.sha512()
	m.update(salt.encode())
	m.update(pw.encode())
	trip = m.hexdigest()
	return trip[-10:]

def mkID(sKey, threadID):
	parts = []
	k, l = threadID%9, threadID%4
	tmp = mktripcode(sKey[l*8:l*8+8])
	return '%s%s' % (tmp[k:], tmp[:k-9])
