import os.path
import os
from model.common import db
from api import logutil

def load_db():
	if os.path.isfile('minivdb') and os.stat('minivdb').st_size > 0:
		logutil.get_logger('main').info('SQLite DB exists. Using existing database.')
	else:
		logutil.get_logger('main').info('SQLite DB cannot be found. Creating new database.')
		with open('sql/schema.sql') as f:
			for q in f.read().split(';'):
				db().query(q)
		logutil.get_logger('main').info('Created new databases. Imported default schema to database.')

