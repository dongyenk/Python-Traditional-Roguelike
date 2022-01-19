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
	]
)
																	# e.g. (255,255,255) 
def new_tile( walkable: bool, transparent: bool, dark: Tuple[ int, Tuple[int,int,int], Tuple[int,int,int] ] ) -> np.ndarray:
	"""Helper function for defining tile types""" # <- for inline comments. """""" <- for documentation comments
	return np.array( (walkable, transparent, dark), dtype=tile_dt )

floor = new_tile( # A special type of array with these attributes is returned and assigned to this variable
	walkable=True, transparent=True, dark=( ord(" "), (255,255,255), (150,75,0) )
)	# ord is standard function that returns unicode of any given character

wall = new_tile(
	walkable=False, transparent=False, dark=( ord("#"), (255,255,255), (155,155,255) )
)

