class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

def test_struct():
	assert 1 == Struct(**{'id':1}).id

