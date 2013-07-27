import web

_db = web.database(dbn='sqlite', db='minivdb')

def db():
	"""
	Returns web.py db object.
	"""
	return _db;

def transaction():
	"""
	Returns a new transaction for db()
	"""
	return db().transaction()

