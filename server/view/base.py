from common import *
from api import logutil

logger = logutil.get_logger('view.base')

class ViewBase():
	"""
	Abstact class implementation for View objects
	"""
        viewName=''
        logger=None

        def __init__(self, name):
                self.viewName = name;
                self.logger = logutil.get_logger('view.' + self.viewName)

def json(f):
	"""
	Decorator to handle arguemnts and return types will be converted from/to JSON.
	This JSON decorator will parse data in web context, decodes as JSON and add resulting value to function arguments. 
	Also, decorator will encode result to JSON string.
	"""
	def new_f(*args, **kwds):
		if f.func_name in ['POST', 'PUT']:
			data = {}
			try:
				data = read_json()
			except Exception as e:
				logger.exception('Cannot parse JSON')
				return to_json('error.server.cannot_parse_json')
			kwds['data']=data
		ret = f(*args, **kwds)
		try:
			return to_json(ret)
		except Exception as e2:
			logger.exception('Cannot generate JSON')
			return to_json('error.server.cannot_generate_json')
	new_f.func_name = f.func_name
	return new_f

