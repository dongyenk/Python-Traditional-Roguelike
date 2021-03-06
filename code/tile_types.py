from typing import Tuple

import numpy as np # .dtype is like a C struct. A container for elements of different types

# code for game tiles before making dungeon. 2 Numpy dtypes. 

graphic_dt = np.dtype( # stores tile symbol, fore-background colours
	[
		( "ch", np.int32 ),
		( "fg", "3B" ), # 3 bytes for r-g-b colour codes
		( "bg", "3B" ),
	]
)

tile_dt = np.dtype( # stores walkable, transparent, & visibility attributes of tiles
	[
		( "walkable", bool ),
		( "transparent", bool ),
		( "dark", graphic_dt ),  # Colours and symbol of that tile when in darkness. Will update to add a light element
		( "light", graphic_dt )
	]
)
																	# e.g. (255,255,255) 
def new_tile( 
	walkable: bool, 
	transparent: bool, 
	dark: Tuple[ int, Tuple[int,int,int], Tuple[int,int,int] ] ,
	light: Tuple[ int, Tuple[int,int,int], Tuple[int,int,int] ]
	) -> np.ndarray:
	"""Helper function for defining tile types""" # <- for inline comments. """""" <- for documentation comments
	return np.array( (walkable, transparent, dark, light), dtype=tile_dt )
	# numpy.array takes a numpy.dtype argument and creates an array or grid of that dtype

# The SHROUD array will represent unexplored dungeon areas
SHROUD = np.array( ( ord(" "), (0,0,0), (0,0,0) ), dtype=graphic_dt )
	# arguments taken by numpy.array depends on arguments required by the numpy.dtype



floor = new_tile( # A special type of array with these attributes is returned and assigned to this variable
	### For colourful minimalist look
	walkable=True, transparent=True, 	
	dark=( ord(" "), (255,255,255), (64,39,35) ),
	light=( ord(" "), (255,255,255), (214,149,43) ),

	### For traditional roguelike look
	#walkable=True, transparent=True, 
	#dark=( ord("."), (200,200,200), (25,25,25) ),
	#light=( ord("."), (255,255,255), (50,50,25) ),
)	
	# ord is standard function that returns integer representing any given character
	# using space makes graphics look tidier and less confusing

wall = new_tile(
	### For colourful minimalist look
	walkable=False, transparent=False, 
	dark=( ord(" "), (255,255,255), (40, 56, 67) ),
	light=( ord(" "), (255,255,255), (80,112,134) ),

	### For traditional roguelike look
	#walkable=False, transparent=False, 
	#dark=( ord("#"), (200,200,200), (25,25,25) ),
	#light=( ord("#"), (255,255,255), (50,50,25) ),
)

