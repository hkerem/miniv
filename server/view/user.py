from view.base import *
from view.validator.common import *
from model.user import UserModel
from model.user_payment import UserPaymentModel
from model.common import transaction

class UserView(ViewBase):
        def __init__(self):
                ViewBase.__init__(self, 'user')

	@json
	@validate_username('username')
	def POST(self, data={}):
		"""
		Function to handle new user creations.
		"""
		origname = data['username'];
		with transaction() as t:
			if UserModel().load_by_username(origname.lower()):
				self.logger.debug('User tried to create a new account with a chosen username [%s]', origname)
				t.rollback()
				return 'error.user.new.user_exists'
			self.logger.debug('User created new account with username [%s]', origname)
			UserModel().new(is_active=True, username=origname.lower(), name=origname)
		return 'ok'
		
class UserBalanceView(ViewBase):
        def __init__(self):
                ViewBase.__init__(self, 'user.balance')

	@json
	def GET(self, origname, data={}):
		"""
		Function handle request to get user balance.
		"""
		with transaction() as t:
			user = UserModel().load_by_username(origname.lower())
			if user is None:
				self.logger.error('User [%s] does not exists', origname)
				t.rollback()
				return 'error.user.does_not_exists'
			return {'balance': str(user.balance)}
		self.logger.error('Unexpected error')
		return 'error.user.balance.internal'

class UserFeedView(ViewBase):
        def __init__(self):
                ViewBase.__init__(self, 'user.feed')

	@json
	def GET(self, origname, data={}):
		"""
		Function handle request to get user feed.
		"""
		with transaction() as t:
			user = UserModel().load_by_username(origname.lower())
			if user is None:
				self.logger.error('User [%s] does not exists', origname)
				t.rollback()
				return 'error.user.does_not_exists'
			logger.debug('Generating feed for user [%s]', origname)
			return UserPaymentModel().get_user_feed(user.id).list()
		self.logger.error('Unexpected error')
		return 'error.user.feed.internal'

