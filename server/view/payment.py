from view.base import *
from view.validator.common import *
from model.user import UserModel
from model.user_payment import UserPaymentModel
from model.credit_card import CreditCardModel
from model.credit_card_transaction import CreditCardTransactionModel
from model.common import transaction
from api.struct import Struct

import random
from decimal import Decimal

class PaymentView(ViewBase):
        def __init__(self):
                ViewBase.__init__(self, 'payment')

	@json
	@validate_username('target_user')
	@validate_decimal('amount')
	def POST(self, actor_origname, data={}):
		"""
		Function to handle credit card payments.
		"""
		amount = data['amount']
		target_origname=data['target_user']
		with transaction() as t:
			actor_user = UserModel().load_by_username(actor_origname.lower())
			if actor_user is None:
				self.logger.error('Actor user [%s] does not exist', actor_origname)
				t.rollback()
				return 'error.actor_user.does_not_exist'
			target_user = UserModel().load_by_username(target_origname.lower())
			if target_user is None:
				self.logger.error('Target user [%s] does not exist', target_origname)
				t.rollback()
				return 'error.target_user.does_not_exist'
			if actor_user.id == target_user.id:
				self.logger.error('Tried to pay self [%s]', actor_origname)
				t.rollback()
				return 'error.actor_user.cannot_pay_self'
				
			actor_cc = CreditCardModel().get_by_user_id(actor_user.id)
			if actor_cc is None:
				self.logger.debug('Actor user [%s] does not have a credit card.', actor_origname)
				t.rollback()
				return 'error.actor_user.no_credit_card'

			# Try to verify payment
			# result = braintree.Transaction.sale({
			# 	"amount": "1000.00",
			#	"credit_card": {
			#		"number": "4111111111111111",
			#		"expiration_month": "05",
			#		"expiration_year": "2012"
			#		}})
			result = Struct(**{	
					'is_success': True,
					'transaction': Struct(**{
							'id': str(random.randint(10,10000)) + '-' + str(random.randint(10,10000))
							})
					}) # mock object

			if result.is_success:
				self.logger.debug("Succeeded transaction from credit card [id:%d]", actor_cc.id)
				# also it is possible to log transaction id from result.transaction.id
			elif result.transaction:
				self.logger.debug("Payment error occurred when processing transaction from credit card [id:%d]", actor_cc.id)
				# also it is possible to log other details
				#   result.message
				#   result.transaction.processor_response_code
				#   result.transaction.processor_response_text
				t.rollback()
				return 'error.credit_card.payment.error' # + result.transaction.processor_response_code 
			else:
				self.logger.error("Error occurred when processing transaction from credit card [id:%d]", actor_cc.id)
				# also it is possible to log other details
				#   result.errors.deep_errors:
				#     error.attribute
				#     error.code
				#     error.message
				t.rollback()
				return 'error.credit_card.communication.error'

			db_transaction_pkey = CreditCardTransactionModel().new(**{
					'user_id': actor_user.id,
					'credit_card_id': actor_cc.id,
					'amount': str(amount),
					'is_success': True,
					'transaction_id': result.transaction.id})
			self.logger.debug("Stored details of transaction [id:%d]", db_transaction_pkey)

			db_payment_pkey = UserPaymentModel().new(**{
					'actor_user_id': actor_user.id,
					'target_user_id': target_user.id,
					'amount': str(amount),
					'note': data['note'] })
			self.logger.debug("Stored details of payment [id:%d]", db_payment_pkey)

			new_balance = str(Decimal(target_user.balance) + amount)
			UserModel().update(target_user.id, balance=new_balance)
			self.logger.debug("Increment balance of user [id:%d]", target_user.id)
			self.logger.debug("Successfully completed payment [id:%d]", db_payment_pkey)

		return 'ok'
		
