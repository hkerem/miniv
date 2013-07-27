from api import logutil
from decimal import Decimal

import re

logger =  logutil.get_logger('validator.common')

def validate_string(field_name, pattern=None, minlength=0, maxlength=0):
	"""
	Decorator to ensure that value of JSON entry mets requirements.
	"""
        def validate(f):
                def new_f(*args, **kwds):
                        if kwds['data'] is None:
                                return 'error.no_json_data'
                        data = kwds['data']
                        if data[field_name] is None:
                                return 'error.str.' + str(field_name) + '.required'
                        value = data[field_name]
                        if maxlength > 0:
                                if not (maxlength >= len(value) >= minlength):
                                        return 'error.str.' + str(field_name) + '.validate.length.between_' + str(minlength) + '_and_' + str(maxlength)
                        else:
                                if not (len(value) >= minlength):
                                        return 'error.str.' + str(field_name) + '.validate.length.higher_than_' + str(minlength)
                        if pattern is not None:
                                if not re.match(pattern, value):
                                        return 'error.str.' + str(field_name) + '.validate.pattern.' + str(pattern)

                        return f(*args, **kwds)
                new_f.func_name = f.func_name
                return new_f
        return validate

def validate_username(field_name):
	"""
	Decorator to ensure that value of JSON entry is a username.
	"""
	return validate_string(field_name, pattern='^[\w_-]+$', minlength=4, maxlength=15)

def validate_decimal(field_name):
	"""
	Decorator to ensure that value of JSON entry is a decimal.
	"""
        def validate(f):
                def new_f(*args, **kwds):
                        if kwds['data'] is None:
                                return 'error.no_json_data'
                        data = kwds['data']
                        if data[field_name] is None:
                                return 'error.decimal.' + str(field_name) + '.required'
                        value = data[field_name]
			try:
				value = Decimal(value)
			except Exception as e:
				logger.exception('Cannot convert to decimal')
				return 'error.decimal.'	 + str(field_name) + '.invalid'
                        data[field_name] = value
                        kwds['data'] = data
                        return f(*args, **kwds)
                new_f.func_name = f.func_name
                return new_f
        return validate
