import web
import json

def read_json():
	"""
	Decodes text data in web context as JSON converts to native types and returns it.
	"""
        return json.loads(web.data())

def to_json(data):
	"""
	Encodes native types to JSON string and returns it
	"""
        web.header('Content-Type', 'application/json')
        return json.dumps(data)
