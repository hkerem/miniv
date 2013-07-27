from base import ModelBase, single_result
from common import db

class UserModel(ModelBase):
	def __init__(self):
		ModelBase.__init__(self, 'user')

        def load_by_username(self, username):
		ret = db().select(self.className, {'username': username}, where="username=$username")
		return single_result(ret)

