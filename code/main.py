#from actions import EscapeAction, MovementAction # Redesigning main.py, by moving code here out to another module's class
from engine import Engine
from input_handler import EventHandler # Can't use classes until instances of them have been created
from game_map import GameMap
from entity import Entity

import tcod # uses NumPy
# I studied https://python-tcod.readthedocs.io/en/latest/ to better understand what these things do

def main() -> None: # function return annotation. Not needed.
	screen_width = 80
	screen_height = 50

	map_width = 80
	map_height = 50

	# Using tcod.tileset.load_tilesheet(path: Union[str, PathLike[str]], columns: int, rows: int, charmap: Optional[Iterable[int]]) -> Tileset
	tileset = tcod.tileset.load_tilesheet( 
		"characters.png", columns = 32, rows = 8, charmap = tcod.tileset.CHARMAP_TCOD # columns and rows refer to how many exist in tilesheet
	) # CHARMAP_TCOD is a list of unicode numbers, used to map characters
     	
 	# creating instance of EventHandler
	event_handler = EventHandler() # a subclass of tcod.event.EventDispatch, which auto calls ev_keydown etc

	player = Entity( x=0, y=0, char='@', colour=(255,255,255) )
	skeleton_warrior = Entity( x=int(screen_width/2), y=int(screen_height/2), char='S', colour=(250,250,150)  )
	# set of entities, that will be used to print the elements in a for loop
	entities = { player, skeleton_warrior } # each game entity has to be individually printed

	game_map = GameMap( map_width, map_height )

	engine = Engine( entities, event_handler, game_map, player )

 	# tcod.context is for window management 
 	# tcod.context.new_terminal(columns: int, rows: int, *, renderer: Optional[int] = None, tileset: Optional[tcod.tileset.Tileset] = None, vsync: bool = True, sdl_window_flags: Optional[int] = None, title: Optional[str] = None) → tcod.context.Context
	context = tcod.context.new_terminal( # returns an instance of tcod.context.Context with some custom attributes
		screen_width,		
		screen_height,
		tileset = tileset,
		title = "Python Roguelike (@+",
		vsync = True,	
	) # Creates an instance of tcod.context.Context		
	
	root_console = tcod.console.Console(width = screen_width, height = screen_height, order="F")
						# order determines how NumPy attributes arranged. "F"= x,y
	while True:	# main.py is a lot cleaner now, that functionality has been moved to another file
		engine.render( root_console, context )
		# simply calling code from new Engine class, instead of having it all typed out in here
		events = tcod.event.wait()

		engine.handle_events( events )

if __name__ == "__main__":  # works regardless of function's name
	main() # Python interpreter creates special variables and values. __name__ contains "__main__" if python file being run is main program
	# function only called if the module where it's defined is built