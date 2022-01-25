from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity

class Action: 
	def perform(self, engine: Engine, entity: Entity):
		"""Functionality moved from engine module to these perform functions"""
		raise NotImplementedError()
	# seems like subclasses automatically inherit functions, but super().__init__() needed to inherit attributes

class EscapeAction( Action ):
	def perform( self, engine: Engine, entity: Entity ):
		raise SystemExit()

class MovementAction( Action ): # def __init__( self, maybe other parameters ): is a function to create class attributes
	def __init__( self, dx: int, dy: int ):
		super().__init__(  ) # calls __init__ function from super class, causing attributes to be inherited

		self.dx = dx
		self.dy = dy	

	def perform( self, engine: Engine, entity: Entity ):
		"""Using guarding / early exits that can quit function before it does something not good"""
		# return on its own == return None
		dest_x = entity.x + self.dx
		dest_y = entity.y + self.dy

		if not engine.game_map.in_bounds( dest_x, dest_y ):
			return
		if not engine.game_map.tiles["walkable"][ dest_x, dest_y ]:
			return

		entity.move( self.dx, self.dy ) # function only called if early exit/guarding didn't happen