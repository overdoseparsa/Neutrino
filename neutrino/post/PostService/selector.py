from abc import ABC , abstractmethod 

class baseSelectorQueryInterFace(ABC):
	def __init__(self , user_id):
		pass


	@abstractmethod
	def get_the_query(self):
		pass 


class OrmSelectorInerFace(baseSelectorQueryInterFace):
	def __init__(self , user):
		pass 



class Selector:
	def __init__(self , request , *args):
		self._request = request 
		self.args = args
		assert len(args) == 1 , f'input from urls must be One paramets , {args}'


	def authentication(self):
		pass