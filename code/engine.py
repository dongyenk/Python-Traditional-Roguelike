from __future__ import annotations
from typing import TYPE_CHECKING

from tcod.context import Context # game windows
from tcod.console import Console # drawing graphics
from tcod.map import compute_fov # for adding tiles to visible and explored numpy arrays

from actions import EscapeAction, MovementAction

from input_handler import EventHandler

if TYPE_CHECKING:
	from entity import Entity
	from game_map import GameMap

class Engine: # class gets arguments for these parameters, which become attributes
	game_map: GameMap # GameMap object made in main.py # engine.game_map = generate_dungeon( ...

	def __init__( self, player: Entity ):
		self.event_handler: EventHandler = EventHandler( self )
		self.player = player

	def handle_enemy_turns(self) -> None:
		#for entity in self.game_map.entities - {self.player}:
		#	pass
		for entity in set(self.game_map.actors) - {self.player}:
			if entity.ai:
				entity.ai.perform()


	def update_fov(self) -> None:
		"""On each turn, completely refresh the visible array with a new set of values while appending values to the explored array"""
		self.game_map.visible[:] = compute_fov( # the visible numpy array is given whole new values after every move
				transparency = self.game_map.tiles[ "transparent" ],
				pov = ( self.player.x, self.player.y ),
				radius = 8
			)
		# whatever is in visible needs to be added to the explored array # Pipe is the set union operator		 
		self.game_map.explored = self.game_map.visible | self.game_map.explored #self.game_map.explored |= self.game_map.visible

	def render( self, console: Console, context: Context ) -> None:
		console.clear() # so previous positions of entities aren't shown

		self.game_map.render( console )		

		context.present( console ) # console.print only creates internal representation. The window managing class actually draws graphics

		