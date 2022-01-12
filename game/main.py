from actions import EscapeAction, MovementAction
from input_handler import EventHandler # Can't use classes until instances of them have been created

import tcod # uses NumPy
# I studied https://python-tcod.readthedocs.io/en/latest/ to better understand what these things do

def main() -> None: # function return annotation. Not needed.
	screen_width = 80
	screen_height = 50

	player_x = int((screen_width/2)) # values in python more fluid than in c++. Can easily change from int to float, so need to use int() to ensure it stays integer
	player_y = int((screen_height/2))

	# Using tcod.tileset.load_tilesheet(path: Union[str, PathLike[str]], columns: int, rows: int, charmap: Optional[Iterable[int]]) -> Tileset
	tileset = tcod.tileset.load_tilesheet( 
		"characters.png", columns = 32, rows = 8, charmap = tcod.tileset.CHARMAP_TCOD # columns and rows refer to how many exist in tilesheet
	) # CHARMAP_TCOD is a list of unicode numbers, used to map characters
     	
 	# creating instance of EventHandler
	event_handler = EventHandler() # a subclass of tcod.event.EventDispatch, which auto calls ev_keydown etc

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
	while True:
	#Console.print(x: int, y: int, string: str, fg: Optional[Tuple[int, int, int]] = None, bg: Optional[Tuple[int, int, int]] = None, bg_blend: int = 1, alignment: int = 0) → None		
		root_console.clear() # clears previous graphics. Prevents past positions of the @ being shown
		root_console.print( x = player_x, y = player_y, string = "@" ) # 1,1 = top left
		context.present( root_console ) # root_console is like internal representation, that needs context.present() to actually draw the graphics

		for event in tcod.event.wait(): # returns event iterator, an object with countable number of values, Like a list?
			# documentation says .wait() halts the loop, then returns an iterator for an event
			action = event_handler.dispatch( event ) # causes an ev_event function to be called
				#  will return None or an Action subclass to be assigned
			if action is None:
				continue # back to top of loop

			elif isinstance( action, MovementAction ):
			# event_handler class functions create MovementAction instance, that has attributes representing movements to be made
			# Use these to update player coordinate variables
				player_x += action.dx
				player_y += action.dy # At top of while loop, the @'s new position will be redrawn

			elif isinstance( action, EscapeAction ):
				raise SystemExit() # raising a Python exception
			

if __name__ == "__main__":  # works regardless of function's name
	main() # Python interpreter creates special variables and values. __name__ contains "__main__" if python file being run is main program
	# function only called if the module where it's defined is built
