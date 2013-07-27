import re
from api.ccutil import *

def validate_cc_number(field_name):
	"""
	Decorator to ensure that value of JSON entry is a valid Credit Card Number
	"""
        def validate(f):
                def new_f(*args, **kwds):
                        if kwds['data'] is None:
                                return 'error.no_json_data'
                        data = kwds['data']
                        if data[field_name] is None:
                                return 'error.cc.' + str(field_name) + '.required'
                        value = data[field_name]
                        if not (19 >= len(value) >= 13):
                                return 'error.cc.' + str(field_name) + '.cc.validate.length.between_13_and_19'
                        if not re.match('\d+', value):
                                return 'error.cc.' + str(field_name) + '.should_be_numeric'
                        if not check_luhn10(value):
                                return 'error.cc.' + str(field_name) + '.failed_luhn10'

                        return f(*args, **kwds)
                new_f.func_name = f.func_name
                return new_f
        return validate

