from typing import Set, Iterable, Any # just used for annotation

from tcod.context import Context # game windows
from tcod.console import Console # drawing graphics

from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import GameMap
from input_handler import EventHandler

class Engine: # class gets arguments for these parameters, which become attributes
	def __init__( self, entities: Set[ Entity ], event_handler: EventHandler, game_map: GameMap, player: Entity ):
		self.entities = entities
		self.event_handler = event_handler
		self.game_map = game_map
		self.player = player

	def handle_events(self, events: Iterable[Any] ) -> None:
		for event in events: # tcod.event.wait()
			action = self.event_handler.dispatch( event ) # becomes an instance of an Action subclass

			if action is None: # None by default
				continue

			#elif isinstance( action, MovementAction ): # <- No longer need as action module redesigned
			action.perform( self, self.player )
				

	def render( self, console: Console, context: Context ) -> None:
		console.clear() # so previous positions of entities aren't shown

		self.game_map.render( console )
		
		for entity in self.entities:
			console.print( x=entity.x, y=entity.y, string=entity.char, fg=entity.colour )

		context.present( console ) # console.print only creates internal representation. The window managing class actually draws graphics

		