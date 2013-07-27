import sys
from cmd import Cmd
USING_READLINE = True
try:
	import readline
except:
	try:
		# For Windows readline support go visit ...
		# https://launchpad.net/pyreadline
		import pyreadline
	except:
		USING_READLINE = False
import json
import requests

BASEURL='http://localhost:8080'
JSON_HEADERS={'content-type': 'application/json'}

def do_post(path, payload):
	"""
	Does an HTTP POST request, pushes data and returns result as JSON
	"""
	return do_http(lambda : requests.post(BASEURL + path, data=json.dumps(payload), headers=JSON_HEADERS))

def do_get(path):
	"""
	Does an HTTP GET request and returns result as JSON
	"""
	return do_http(lambda : requests.get(BASEURL + path))

def do_http(func):
	"""
	Executes given function in a simply managed environment
	"""
	try:
		try:
			r = func()
		except Exception as e2:
			print_error_raw(str(e2))
			return 'error.communication'
		return json.loads(r.content)
	except Exception as e:
		print_error_raw(str(e))
		return 'error.cannot_parse_json'
	
MESSAGEDICT={
	'unknown_error': 'Unknown error occurred',
	'error.cannot_parse_json': 'Cannot parse JSON',
	'error.communication': 'Communication error occurred.',
	'error.actor_user.no_credit_card': 'This user does not have a credit card.',
	'error.cc.credit_card_number.required': 'Credit card number is required',
	'error.cc.credit_card_number.cc.validate.length.between_13_and_19': 'Credit card number should be should be no shorter than 13 characters but no longer than 19',
	'error.cc.credit_card_number.should_be_numeric': 'Credit card number should be numeric',
	'error.cc.credit_card_number.failed_luhn10': 'This card is invalid.',
	'error.cc.belongs_to_another_user': 'That card has already been added by another user, reported for fraud!',
	'error.cc.already_added': 'This user already added this credit card.',
	'error.actor_user.cannot_pay_self': 'User cannot pay to himself/herself.',
	'error.server.cannot_parse_json': 'Server cannot parse JSON.',
	'error.server.cannot_generate_json': 'Server cannot generate JSON.',
	'error.actor_user.does_not_exist': 'Actor user does not exists.',
	'error.target_user.does_not_exist': 'Target user does not exists.',
	'error.credit_card.payment.error': 'Couldn\'t pay with this user\'s credit card.',
	'error.credit_card.communication.error': 'Cannot communicate with payment processor.',
	'error.user.new.user_exists': 'A user with this username already exists.',
	'error.user.does_not_exists': 'User does not exists',
	'error.user.feed.internal': 'Internal server error occurred when generating user feed.',
	'error.user.balance.internal': 'Internal server error occurred when fetching user balance.',
	'error.no_json_data': 'There is no JSON data to process.',
	'error.decimal.amount.required': 'A decimal value for amount is required.',
	'error.decimal.amount.invalid': 'Amount should be a decimal value.',
	'error.str.username.required': 'Username is required',
	'error.str.username.validate.length.between_4_and_15': 'Username should be no shorter than 4 characters but no longer than 15.',
	'error.str.username.validate.pattern.^[\w_-]+$': 'Username should be alphanumeric but also allow underscores and dashes.',
	'error.str.target_user.required': 'Username for target user is required',
	'error.str.target_user.validate.length.between_4_and_15': 'Username for target user should be should be no shorter than 4 characters but no longer than 15.',
	'error.str.target_user.validate.pattern.^[\w9_-]+$': 'Username for target user should be alphanumeric but also allow underscores and dashes.',
	'user.ok' : 'Created user successfully',
	'user.pay.ok' : 'Completed payment successfully',
	'user.card.ok' : 'Added credit card to user successfully'
}

def get_message(key):
	"""
	Gets message string from MESSAGEDICT. If not found returns the key itself
	"""
	if key in MESSAGEDICT:
		return MESSAGEDICT[key]
	else:
		return key

def print_raw(raw):
	"""
	Prints string directly.
	"""
	sys.stdout.write('-- ' + raw + '\n')

def print_message(key):
	"""
	Gets associated message for key and prints it.
	"""
	print_raw(get_message(key))

def print_error(result):
	"""
	Gets associated message for key and prints it as an error.
	"""
	key = 'unknown_error'
	if type(result) in [str, unicode]:
		key = result
	print_error_raw(get_message(key))

def print_error_raw(raw):
	"""
	Prints string directly as an error.
	"""
	sys.stdout.write('ERROR: ' + raw + '\n')

 
class CmdLine(Cmd):
	def __init__(self):
		Cmd.__init__(self)
		if not USING_READLINE:
			self.completekey = None
		self.prompt = "> "
		self.intro  = "Mini-V Application Interactive CLI Terminal"
        
	def default(self, line):
		cmd, arg, line = self.parseline(line)
		cmds = self.completenames(cmd)
		num_cmds = len(cmds)
		if num_cmds == 1:
			getattr(self, 'do_'+cmds[0])(arg)
		elif num_cmds > 1:
			sys.stdout.write('\nERROR: Ambiguous command:\t"%s"\n' % cmd)
		else:
			sys.stdout.write('\nERROR: Unrecognized command\n')
 
	def emptyline(self):
		pass
    
	def do_help(self, args):
		doc_strings = [ (i[3:], getattr(self, i).__doc__) for i in dir(self) if i.startswith('do_') ]
		doc_strings = [ ( '  %s\t%s\n' if len(i) > 5  else '  %s\t\t%s\n' ) % (i, j) for i, j in doc_strings if j is not None ]
		sys.stdout.write('Commands:\n%s\n' % ''.join(doc_strings))

	def do_exit(self, args):
		" Exit from this terminal:\t\t\t exit "
		sys.exit(0)
 
	def do_user(self, args):
		" Add new user:\t\t\t\t\t user Username "
		args = args.strip().split(' ')
		if len(args) != 1:
			self.do_help(args)
			return
			
		result = do_post('/user', {'username': args[0]})
		if result == 'ok':
			print_message('user.ok')
		else:
			print_error(result)
        
	def do_add(self, args):
		" Add new credit card to user:\t\t\t add Username CreditCardNumber "
		args = args.strip().split(' ')
		if len(args) != 2:
			self.do_help(args)
			return
		
		result = do_post('/user/' + args[0] + '/card', {'credit_card_number': args[1]})
		if result == 'ok':
			print_message('user.card.ok')
		else:
			print_error(result)

	def do_pay(self, args):
		" Make payment from a user to another user:\t pay ActorUsername TargetUsername Amount Note "
		args = args.strip().split(' ')
		if len(args) < 3:
			self.do_help(args)
			return
		
		result = do_post('/user/' + args[0] + '/pay', {
				'target_user': args[1], 
				'amount': args[2][1:] if args[2][0] == '$' else args[2], 
				'note': ' '.join(args[3:])})
		if result == 'ok':
			print_message('user.pay.ok')
		else:
			print_error(result)

	def do_feed(self, args):
		" Show user feed:\t\t\t\t feed Username "
		args = args.strip().split(' ')
		if len(args) != 1:
			self.do_help(args)
			return

		user = args[0]
		result = do_get('/user/' + user + '/feed')
		if type(result) is list:
			for entry in result:
				actor = entry['actor']
				actor = 'You' if user == actor else actor
				target = entry['target']
				target = 'you' if user == target else target
				print_raw('%s paid %s $%s for %s' % (actor, target, entry['amount'], entry['note']) )
		else:
			print_error(result)

	def do_balance(self, args):
		" Show balance of user:\t\t\t\t balance Username "
		args = args.strip().split(' ')
		if len(args) != 1:
			self.do_help(args)
			return
		
		result = do_get('/user/' + args[0] + '/balance')
		if type(result) is dict:
			print_raw('$' + result['balance'])
		else:
			print_error(result)
 
	def precmd(self, line):
		if line.strip() == 'help':
			self.do_help(line)
			return ''
		cmd, arg, line = self.parseline(line)
		if arg == '?':
			cmds = self.completenames(cmd)
			if cmds:
				self.columnize(cmds)
				sys.stdout.write('\n')
			return ''
		return line           

	def cmdloop(self):
		"""
		Overriding this method to handle Ctrl+C
		"""
		try:
			Cmd.cmdloop(self)
		except KeyboardInterrupt as e:
			sys.stdout.write('\n^C\n')
			sys.exit(0)
    
# *** MAIN LOOP ***
if __name__ == '__main__':
	cmdLine = CmdLine()
	cmdLine.cmdloop()
