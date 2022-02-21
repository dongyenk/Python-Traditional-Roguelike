from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity

class Action: 
	def __init__( self, entity: Entity ):
			super().__init__()
			self.entity = entity

	@property # just a function accessed like a variable attribute
	def engine( self ) -> Engine:
		"""Return Engine object the acting entity belongs to"""
		return self.entity.game_map.engine

	def perform(self ) -> None:
		"""self.entity performs actions in the scope of self.engine"""
		raise NotImplementedError()
	# seems like subclasses automatically inherit functions, but super().__init__() needed to inherit attributes

class EscapeAction( Action ):
	def perform( self ) -> None:
		raise SystemExit()

class ActionWithDirection( Action ):
	def __init__( self, entity: Entity, dx: int, dy: int ):
		super().__init__( entity )
		self.dx = dx
		self.dy = dy

	@property
	def dest_xy( self ) -> Tuple[ int, int ]:
		"""Coordinates returning function that is accessed like simple attribute"""
		return( ( self.entity.x + self.dx ), ( self.entity.y + self.dy ) )

	@property
	def blocking_entity( self ) -> Optional[ Entity ]:
		"""Return blocking entity object at destination coordinates"""
		x, y = self.dest_xy # unpacking 2 element large tuple

		return self.engine.game_map.get_blocking_entity( x, y )

	def perform( self ) -> None:
		raise NotImplementedError

class MoveOrMeleeAction( ActionWithDirection ):
	"""Determines if player moves or attacks."""
	def perform(self ) -> None: # subclass of it
		"""Decide to call Melee or Movement Action class"""
		if self.blocking_entity:
			return MeleeAction( self.entity, self.dx, self.dy ).perform()

		else:
			return MovementAction( self.entity, self.dx, self.dy ).perform()

class MeleeAction( ActionWithDirection ):
	"""To handle glorious bad graphics combat"""
	def perform( self ) -> None:
		target = self.blocking_entity
		
		if not target:
			return # early exits function

		print(f"You effortfully nudge {target.name} :O !!! Rude!")


class MovementAction( ActionWithDirection ): # def __init__( self, maybe other parameters ): is a function to create class attributes
	
	def perform( self ) -> None:
		"""Using guarding / early exits that can quit function before it does something not good"""
		dest_x, dest_y = self.dest_xy

		if not self.engine.game_map.in_bounds( dest_x, dest_y ):
			return
		if not self.engine.game_map.tiles["walkable"][ dest_x, dest_y ]:
			return
		## MY SOLUTION TO BLOCKING MOVEMENT # Tutorial has another, that returns Entity object so it can be killed.
		# first check if there is an entity at the destination, then check if the entity is supposed to block movement, before early exit
		#if any( entity.x == dest_x and entity.y == dest_y for entity in engine.game_map.entities ):
		#	if entity.blocks_movement:
		#		return
		if self.engine.game_map.get_blocking_entity( x=dest_x, y=dest_y ):
			return

		self.entity.move( self.dx, self.dy ) # function only called if early exit/guarding didn't happen