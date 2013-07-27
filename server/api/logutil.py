import logging

def setup_logger():
	logger = logging.getLogger('miniv')
	logger.setLevel(logging.DEBUG)
	fh = logging.FileHandler('miniv.log')
	fh.setLevel(logging.DEBUG)
	# create console handler with a higher log level
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(fh)
	logger.addHandler(ch)

def get_logger(name):
	return logging.getLogger('miniv.' + name)

