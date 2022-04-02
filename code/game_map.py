from __future__ import annotations # allows more flexible annotations that might cause errors otherwise

from typing import Iterable, Optional, TYPE_CHECKING, Iterator

import numpy as np
from tcod.console import Console # for drawing graphics in internal representation

import tile_types

from entity import Actor

if TYPE_CHECKING:
	from entity import Entity
	from engine import Engine

class GameMap:
	def __init__(
		self, engine: Engine, width: int, height: int, entities: Iterable[Any]
	):
		self.engine = engine
		self.width = width
		self.height = height
		# numpy.full(shape,fill_value,dtype,order,like) returns an array in some shape filled with something
		self.tiles = np.full( shape=(width,height), fill_value=tile_types.wall, order="F" )
			# filling dungeon with floor tiles	# F makes coordinates x,y instead of C which makes them y,x

		self.entities: set = set(entities)

		#2 Other numpy arrays for currently and previously visible tiles
		self.visible = np.full(
			shape=(width, height), fill_value=False, order="F"
		)		
		self.explored = np.full( 
			shape=(width,height), fill_value=False, order="F" 
		)

		#self.tiles[ 30:33, 22 ] = tile_types.wall

	@property
	def actors(self) -> Iterator[Actor]:
		yield from{
			entity
			for entity in self.entities
			if isinstance(entity, Actor) and entity.is_alive
		}

	def get_blocking_entity(
		self, x:int, y:int
	) -> Optional[Entity]:
		"""If requested player direction contains a blocking Entity, return it."""
		self.x = x
		self.y = y # gets arguments to make into attributes

		for entity in self.entities:
			if (
				entity.x == self.x 
				and entity.y == self.y 
				and entity.blocks_movement
			):
				return entity

		return # only called if match not found in for loop

	def get_actor_at_location( self, x:int, y:int ) -> Optional[Actor]:
		for actor in self.actors: # actors is a function that gets called like a collection attribute
			if actor.x == x and actor.y == y:
				return actor # early exits if executes
		return None


	def in_bounds( self, x: int, y: int ) -> bool:
		"""Return True of the entity is not headed off the screen"""
		# if x not less than 0 and x not greater than width. if y not less than 0 and y not greater than height
		return 0 <= x < self.width and 0 <= y < self.height
			# above is just a fancy way to check x is not off screen. return {expression} == return True if expression evaluates as True
	def render( self, console: Console ):				
		# console.tiles_rgb / rgb used to draw tile graphics 
		console.tiles_rgb[ 0 : self.width, 0 : self.height ] = np.select( # originally was just = self.tiles["dark"]
			condlist = [ self.visible, self.explored ],
			# listed visible array first, because there will be tiles in the visible and explored arrays. This way, being in visible array is prioritised
			choicelist = [ self.tiles["light"], self.tiles["dark"] ], # if tile in visible array, use light graphics ....
			default = tile_types.SHROUD,
		) # combining Console.tiles_rgb and numpy.select to conditionally draw dungeon

		for entity in self.entities:
			if self.visible[ entity.x, entity.y ]:
				console.print( x=entity.x, y=entity.y, string=entity.char, fg=entity.colour )
