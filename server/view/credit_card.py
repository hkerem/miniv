from view.base import *
from view.validator.credit_card import *
from model.user import UserModel
from model.credit_card import CreditCardModel
from model.common import transaction

class CreditCardView(ViewBase):
        def __init__(self):
                ViewBase.__init__(self, 'credit_card')

	@json
	@validate_cc_number('credit_card_number')
	def POST(self, origname, data={}):
		"""
		Function to handle new credit card additions.
		"""
		ccnumber = data['credit_card_number'];
		with transaction() as t:
			user = UserModel().load_by_username(origname.lower())
			if user is None:
				self.logger.error('User [%s] does not exists', origname)
				t.rollback()
				return 'error.user.does_not_exists'
			cc = CreditCardModel().load_by_card_number(ccnumber)
			if cc is not None:
				if cc.user_id == user.id:
					self.logger.debug('User [%s] tried to add same card.', origname)
					t.rollback()
					return 'error.cc.already_added'
				else:
					self.logger.critical('User [%s] tried to add a card [id:%d] belongs to other user [id:%d].', origname, cc.id, cc.user_id)
					t.rollback()
					return 'error.cc.belongs_to_another_user'
			self.logger.debug('User [%s] added new card.', origname)
			CreditCardModel().new(user_id=user.id, card_number=ccnumber, is_validated=True, is_active=True)
		return 'ok'
		
