import re

def drop_whitespaces(phrase):
	if phrase is None:
		return '';
	return re.sub('\s+', '', phrase)

luhnify = lambda digit: sum(divmod( digit*2, 10 ))

def check_luhn10(ccnumber):
	"""Return the Luhn checksum of a sequence of digits.
	"""
	if ccnumber is None:
		return False
	digits = map( int, ccnumber)
	odds, evens = digits[-2::-2], digits[-1::-2]
	checksum = sum( map(luhnify,odds) + evens ) % 10
	return ( checksum == 0 )
	
def test_luhn():
	assert check_luhn10("4111111111111111") is True
	assert check_luhn10("411111111111111") is not True
	assert check_luhn10("1234567890123456") is not True

def test_drop_ws():
	assert "" == drop_whitespaces("       ")
	assert "a" == drop_whitespaces("  a     ")
	assert "aa" == drop_whitespaces("  a   a  ")
