class Action:
	pass

class EscapeAction( Action ):
	pass

class MovementAction( Action ): # def __init__( self, maybe other parameters ): is a function to create class attributes
	def __init__( self, dx: int, dy: int ):
		super().__init__(  ) # calls __init__ function from super class, causing attributes to be inherited

		self.dx = dx
		self.dy = dy	
