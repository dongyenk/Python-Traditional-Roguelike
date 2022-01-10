import tcod # uses NumPy
# I studied https://python-tcod.readthedocs.io/en/latest/ to better understand what these things do

def main() -> None: # function return annotation. Not needed.
	screen_width = 80
	screen_height = 50

	player_x = 1
	player_y = 1

	# Using tcod.tileset.load_tilesheet(path: Union[str, PathLike[str]], columns: int, rows: int, charmap: Optional[Iterable[int]]) -> Tileset
	tileset = tcod.tileset.load_tilesheet( 
		"characters.png", columns = 32, rows = 8, charmap = tcod.tileset.CHARMAP_TCOD # columns and rows refer to how many exist in tilesheet
	) # CHARMAP_TCOD is a list of unicode numbers, used to map characters
     	

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
		root_console.print( x = player_x, y = player_y, string = "@" ) # 1,1 = top left
		context.present( root_console ) # root_console is like internal representation, that needs context.present() to actually draw the graphics

		for event in tcod.event.wait(): # returns event iterator, an object with countable number of values, Like a list?
			if event.type == "QUIT":
				raise SystemExit()	# a built in Python exception
				#break # doesn't work

if __name__ == "__main__":  # works regardless of function's name
	main() # Python interpreter creates special variables and values. __name__ contains "__main__" if python file being run is main program
	# function only called if the module where it's defined is built