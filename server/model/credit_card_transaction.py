from base import ModelBase, single_result
from common import db

class CreditCardTransactionModel(ModelBase):
	def __init__(self):
		ModelBase.__init__(self, 'credit_card_transaction')

