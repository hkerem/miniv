import web
from api import logutil
from api import dbutil
from view.user import *
from view.credit_card import CreditCardView
from view.payment import PaymentView
import os.path
from model.common import db

urls = (
	'/user', 'UserView',
	'/user/(.+)/balance', 'UserBalanceView',
	'/user/(.+)/feed', 'UserFeedView',
	'/user/(.+)/pay', 'PaymentView',
	'/user/(.+)/card', 'CreditCardView'
)
app = web.application(urls, globals())


if __name__ == '__main__':
	logutil.setup_logger()
	logutil.get_logger('main').info('Starting application')
	dbutil.load_db()
	app.run()
