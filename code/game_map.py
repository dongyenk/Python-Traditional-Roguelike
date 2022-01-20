import numpy as np
from tcod.console import Console # for drawing graphics in internal representation

import tile_types

class GameMap:
	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height
		# numpy.full(shape,fill_value,dtype,order,like) returns an array in some shape filled with something
		self.tiles = np.full( shape=(width,height), fill_value=tile_types.floor, order="F" )
			# filling dungeon with floor tiles	# F makes coordinates x,y instead of C which makes them y,x

		self.tiles[ 30:33, 22 ] = tile_types.wall

	def in_bounds( self, x: int, y: int ) -> bool:
		"""Return True of the entity is not headed off the screen"""
		# if x not less than 0 and x not greater than width. if y not less than 0 and y not greater than height
		return 0 <= x < self.width and 0 <= y < self.height
			# above is just a fancy way to check x is not off screen. return {expression} == return True if expression evaluates as True
	def render( self, console: Console ):
		console.tiles_rgb[ 0:self.width, 0:self.height ] = self.tiles["dark"] # accessing values for dark element in array
		# console.tiles_rgb / rgb used to draw tile graphics