from base import ModelBase, single_result
from common import db

class CreditCardModel(ModelBase):
	def __init__(self):
		ModelBase.__init__(self, 'credit_card')

	def load_by_card_number(self, card_number):
                ret = db().select(self.className, {'card_number': card_number}, where="card_number=$card_number")
                return single_result(ret)

	def get_by_user_id(self, user_id):
                ret = db().select(self.className, {'user_id': user_id}, where="user_id=$user_id")
                return single_result(ret)

