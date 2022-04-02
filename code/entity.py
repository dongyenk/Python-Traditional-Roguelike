from __future__ import annotations

import copy # for copying objects of class that models game characters
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING, Type

if TYPE_CHECKING:
	from ai import BaseAI # classes that model components, instead of objects
	from fighter import Fighter 
	from game_map import GameMap

T = TypeVar( 'T', bound="Entity" ) # Seems like an annotation thing called type variable 
	# seems to just be some annotation thing representing the Entity class

class Entity:
	"""Generic class that can be used to create all objects that exist in the dungeon"""

	game_map: GameMap

	def __init__(  
		self,
		game_map: Optional[ GameMap ] = None,
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
		if game_map:
			# if game_map object provided, set it as value of attribute
			self.game_map = game_map
			game_map.entities.add( self ) # game entities add themselves to the entities eet

	def spawn( self: T, game_map: GameMap, x: int, y: int ):# -> T:
		"""Copy an existing instance of the Entity class and add it to the dungeon."""
		clone = copy.deepcopy( self )
		clone.x = x # going to take arguments from procgen module
		clone.y = y 
		clone.game_map = game_map
		game_map.entities.add(clone)
		return clone # Tutorial has this but it seems useless

	def place( self, x: int, y: int, game_map: Optional[GameMap] = None ) -> None:
		self.x = x
		self.y = y
		if game_map:
			if hasattr( self, "game_map" ): # checking if Entity object has game_map attributes
				self.game_map.entities.remove( self )
			self.game_map = game_map
			game_map.entities.add( self )

	def move( self, dx: int, dy: int ) -> None:
		self.x += dx
		self.y += dy

# Actor is Entity subclass
class Actor( Entity ):
	def __init__(
		self,
		*,
		x: int = 0, # optional parameters
		y: int = 0,
		char: str = "?", # default values
		colour: Tuple[int,int,int] = (255, 255, 255), # white
		name: str = "<Unnamed>",
		ai_cls: Type[BaseAI], # will be subclass of BaseAI
		fighter: Fighter, # I haven't used component OOP before
	):
		super().__init__( # seems like calling constructor from super class
			x=x,
			y=y,
			char=char,
			colour=colour,
			name=name,			
			blocks_movement=True,			
		)

		self.ai: Optional[BaseAI] = ai_cls(self)
		self.fighter = fighter
		self.fighter.entity = self

	@property # a getter function that is called like a variable
	def is_alive(self) -> bool:
		"""Dead actor can't perform actions"""
		return bool(self.ai)

