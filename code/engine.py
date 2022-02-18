from typing import Iterable, Any # just used for annotation

from tcod.context import Context # game windows
from tcod.console import Console # drawing graphics
from tcod.map import compute_fov # for adding tiles to visible and explored numpy arrays

from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import GameMap
from input_handler import EventHandler

class Engine: # class gets arguments for these parameters, which become attributes
	def __init__( self, event_handler: EventHandler, game_map: GameMap, player: Entity ):		
		self.event_handler = event_handler
		self.game_map = game_map
		self.player = player
		self.update_fov()

	def handle_enemy_turns(self) -> None:
		for entity in self.game_map.entities - {self.player}:
			print( f"The {entity.name} makes an awfully cunning move.\n" )

	def handle_events(self, events: Iterable[Any] ) -> None:
		for event in events: # tcod.event.wait()
			action = self.event_handler.dispatch( event ) # becomes an instance of an Action subclass

			if action is None: # None by default
				continue

			#elif isinstance( action, MovementAction ): # <- No longer need as action module redesigned
			action.perform( self, self.player )
			self.handle_enemy_turns( )
			# visibility graphics must be updated after each player move
			self.update_fov() 

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

		