from typing import Tuple

class Entity:
	"""Class representing the x, y, colour, char attributes of all game entities"""
	def __init__( self, x: int, y: int, char: str, colour: Tuple[ int, int, int ] ): # special function that assigns attributes to classes
		self.x = x
		self.y = y
		self.char = char
		self.colour = colour # rgb colour code, with each being 0-255

	def move( self, dx: int, dy: int ) -> None:
		self.x += dx
		self.y += dy
