import web
from common import db
from api import logutil

class ModelBase():
	"""
	Abstract class implementation for DAOs
	"""
	className=''
	logger=None

	def __init__(self, table):
		__metaclass__ = SingletonModel
		self.className = table;
		self.logger = logutil.get_logger('model.' + self.className)

	def list(self):
		return db().select(self.className, order='id DESC')

	def load(self, __id):
		ret = db().select(self.className, where="id=$id", vars={'id': __id})
		return single_result(ret)

	def new(self, **kwargs):
		if 'id' in kwargs:
			del kwargs['id']
		return db().insert(self.className, **kwargs)

	def update(self, __id, **kwargs):
		if 'id' in kwargs:
			del kwargs['id']
		db().update(self.className, where="id=$id", vars={'id': __id}, **kwargs)

	def delete(self, __id):
		db().delete(self.className, where="id=$id", vars={'id': __id})

			
def single_result(result):
	if result is None:
		return None
	for row in result:
		return row
	return None

class SingletonModel(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

