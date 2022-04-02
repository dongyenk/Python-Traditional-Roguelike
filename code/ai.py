from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import numpy as np
import tcod

from actions import Action, MeleeAction, MovementAction, WaitAction
from base_component import BaseComponent

if TYPE_CHECKING:
	from entity import Actor	

# super class
class BaseAI(Action, BaseComponent ): # inherits entity attribute and engine property function
	entity: Actor

	def perform( self ) -> None:
		raise NotImplementedError()

	def get_path_to( self, dest_x: int, dest_y: int ) -> List[ Tuple[int,int] ]:
		"""
		Takes destination coordinate arguments, 
		and if valid path, return list of coordinates that make up the path to destination,
		else return empty list.
		"""	
		cost = np.array( self.entity.game_map.tiles["walkable"], dtype=np.int8 ) # non walkable tiles have the value 0, in this array
		# Each node in the numpy array has a value representing the "cost" of moving to that location.

		for entity in self.entity.game_map.entities:
	 		# if blocks_mov attribute true, and tile beneath entity is walkable (doesnt have value 0)
	 		if entity.blocks_movement and cost[entity.x, entity.y]:
	 			cost[ entity.x, entity.y ] += 10
 				# Increase the 'cost', for a walkable tile(numpy array cell), if there is a movement-blocking entity there
 			# Each cell's cost value is accounted for in tcod pathfinding, which prefers low cost routes 			
 			# this causes monsters to go around, instead of being stuck in a line
	 	
		graph = tcod.path.SimpleGraph( cost=cost, cardinal=2, diagonal=3 )	# moving diagonally 'costs' more than cardinal

		pathfinder = tcod.path.Pathfinder( graph ) # graph object determines how tcod pathfinding works
		# PathFinder object needs to have it's root attribute set to the coordinate of the Entity object it's attached to, as the starting position
		pathfinder.add_root( (self.entity.x, self.entity.y) )
													    # Tuple[int,int]
		path: List[ List[int] ] = pathfinder.path_to( ( dest_x, dest_y ) )[1:].tolist()
									# getting path to a matrix/2d array address, then making a list of values, starting from the 2nd element in the path
		return [ ( index[0], index[1] ) for index in path ]
				# This Tuple[int,int] used to access 2d array/matrix coordinate values from PathFinder's path_to function

		# created 2d array/matrix 'cost'. Array cells with value 0 are unwalkable # Each cell has a value, 'cost' to move onto that cell
		# cost array used to make SimpleGraph, used to make PathFinder object, which draws path lines, and returns its array coordinates
		# THE PATHFINDER FAVOURS LOWER 'cost' VALUES. Meaning, tiles (represented by array cells), with a higher cost value, may be avoided by path finder.

class HostileEnemy( BaseAI ):
	def __init__(self, entity: Actor):
		super().__init__(entity)
		self.path: List[Tuple[int,int]] = [] # a list of coordinates that make up the path the Entity object will take

	def perform(self) -> None:
		target = self.engine.player
		dx = target.x - self.entity.x
		dy = target.y - self.entity.y
		distance = max( abs(dx), abs(dy) ) # absolute number means distance from 0

		# Monsters can only start to act, if the player's visible tiles array contains the monster
		if self.engine.game_map.visible[ self.entity.x, self.entity.y ]:
			if distance <= 1: # right next to enemy
				MeleeAction( self.entity, dx, dy ).perform()

			self.path = self.get_path_to( target.x, target.y ) # target.x is the player Entity object
		# if the path has values
		if self.path:
			(dest_x, dest_y) = self.path.pop(0) # get and remove the first coordinate on the path
			return MovementAction(  # will early exit the function if called
				self.entity, dest_x-self.entity.x, dest_y-self.entity.y,
			).perform()
		# if player can't see monster, if monster has no path, just pass the turn
		return WaitAction(self.entity).perform()	


