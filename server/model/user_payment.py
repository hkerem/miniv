from base import ModelBase, single_result
from common import db

class UserPaymentModel(ModelBase):
	def __init__(self):
		ModelBase.__init__(self, 'user_payment')

	def get_user_feed(self, user_id):
		return db().query(	'select '
					'(select name from user where id=actor_user_id) as actor, '
					'(select name from user where id=target_user_id) as target, '
					'amount, note '
					'from user_payment p '
					'where actor_user_id=$user_id or target_user_id=$user_id', 
				{'user_id': user_id}) 

