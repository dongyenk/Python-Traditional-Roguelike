from __future__ import annotations

import copy # for copying objects of class that models game characters
from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
	from game_map import GameMap

T = TypeVar( 'T', bound="Entity" ) # Seems like an annotation thing called type variable 
	# seems to just be some annotation thing representing the Entity class

class Entity:
	"""Generic class that can be used to create all objects that exist in the dungeon"""
	def __init__(  
		self,
		x: int = 0,
		y: int = 0,
		char: str = '?',
		colour: Tuple[ int, int, int ] = (255, 255, 255),
		name: str = "Unamed",
		blocks_movement: bool = False,		
	):
		self.x = x
		self.y = y
		self.char = char
		self.colour = colour # assigning arguments to object attributes
		self.name = name
		self.blocks_movement = blocks_movement

	def spawn( self: T, game_map: GameMap, x: int, y: int ):# -> T:
		"""Copy an existing instance of the Entity class and add it to the dungeon."""
		clone = copy.deepcopy( self )
		clone.x = x # going to take arguments from procgen module
		clone.y = y 
		game_map.entities.add(clone)
		#return clone # Tutorial has this but it seems useless 

	def move( self, dx: int, dy: int ) -> None:
		self.x += dx
		self.y += dy
