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

class ActionWithDirection( Action ):
	def __init__( self, dx: int, dy: int ):
		super().__init__()
		self.dx = dx
		self.dy = dy

	def perform( self, engine: Engine, entity: Entity ) -> None:
		raise NotImplementedError

class MoveOrMeleeAction( ActionWithDirection ):
	"""Determines if player moves or attacks."""
	def perform(self, engine: Engine, entity: Entity) -> ActionWithDirection: # subclass of it
		"""Decide to call Melee or Movement Action class"""
		dest_x = entity.x + self.dx
		dest_y = entity.y + self.dy

		if engine.game_map.get_blocking_entity( dest_x, dest_y ):
			return MeleeAction( self.dx, self.dy ).perform( engine, entity )

		if not engine.game_map.get_blocking_entity( dest_x, dest_y ):
			return MovementAction( self.dx, self.dy ).perform( engine, entity )

		else:
			print(f"What did you do {entity.name}?")

class MeleeAction( ActionWithDirection ):
	"""To handle glorious bad graphics combat"""
	def perform( self, engine: Engine, entity: Entity ) -> None:
		dest_x = entity.x + self.dx
		dest_y = entity.y + self.dy
		target = engine.game_map.get_blocking_entity( dest_x, dest_y )
		if not target:
			return # early exits function

		print(f"You effortfully nudge {target.name} :O !!! Rude!")


class MovementAction( ActionWithDirection ): # def __init__( self, maybe other parameters ): is a function to create class attributes
	
	def perform( self, engine: Engine, entity: Entity ):
		"""Using guarding / early exits that can quit function before it does something not good"""
		# return on its own == return None
		dest_x = entity.x + self.dx
		dest_y = entity.y + self.dy

		if not engine.game_map.in_bounds( dest_x, dest_y ):
			return
		if not engine.game_map.tiles["walkable"][ dest_x, dest_y ]:
			return
		## MY SOLUTION TO BLOCKING MOVEMENT # Tutorial has another, that returns Entity object so it can be killed.
		# first check if there is an entity at the destination, then check if the entity is supposed to block movement, before early exit
		#if any( entity.x == dest_x and entity.y == dest_y for entity in engine.game_map.entities ):
		#	if entity.blocks_movement:
		#		return
		if engine.game_map.get_blocking_entity( x=dest_x, y=dest_y ):
			return

		entity.move( self.dx, self.dy ) # function only called if early exit/guarding didn't happen