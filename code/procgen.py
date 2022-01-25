from __future__ import annotations
import random
import tcod
from typing import Tuple, Iterator, List, TYPE_CHECKING

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
	from entity import Entity

class RectangularRoom:
	def __init__( self, x:int, y:int, width:int, height:int ):
		self.x1 = x
		self.y1 = y # top left # 1,1 is most extreme top left
		self.x2 = x + width
		self.y2 = y + height # bottom right

	@property # @property means the function can be called like an attribute
	def centre( self ) -> Tuple[ int, int ]: 
		centre_x = int( ( self.x1 + self.x2 ) / 2 )
		centre_y = int( ( self.y1 + self.y2 ) / 2 )

		return ( centre_x, centre_y )

	@property
	def inner( self ) -> Tuple[ slice, slice ]: # slice( start, end ) -> set of indexes from argument range in a slice object
		"""Returns inner area of room as 2D array indexes"""
		return ( slice( self.x1+1, self.x2 ), slice( self.y1+1, self.y2 ) )
				# width of room 				# height
				# adding 1 ensures adjacent rooms have walls between them

	def intersects( self, other: RectangularRoom ) -> bool:
		"""Return true if overlapping with other room"""
		return( # Series tests evaluate as True or False
			self.x1 <= other.x2
			and self.x2 >= other.x1
			and self.y1 <= other.y2
			and self.y2 >= other.y1
		)

def generate_dungeon(
	max_rooms: int,
	room_min_size: int,
	room_max_size: int,
	map_width: int,
	map_height: int,
	player: Entity
) -> GameMap:
	"""Create an instance of GameMap and modify it to have rooms and corridors before returning it."""
	dungeon = GameMap( map_width, map_height )

	rooms: List[ RectangularRoom ] = [] # extra bit is just annotation saying this will be a list of RectRoom instances

	for room in range( max_rooms ):
		# getting room attributes:
		room_width = random.randint( room_min_size, room_max_size )
		room_height = random.randint( room_min_size, room_max_size )

		x = random.randint( 0, dungeon.width-room_width-1 ) # preventing rooms from being created at edge of screen
		y = random.randint( 0, dungeon.height-room_height-1 )

		new_room = RectangularRoom( x, y, room_width, room_height )

		if any( new_room.intersects( other_room ) for other_room in rooms ): # returns True if any element in interation returns True
			continue # room overlaps too much, discard this one and try again.

		dungeon.tiles[ new_room.inner ] = tile_types.floor

		if len( rooms ) == 0: # if first room created, place player in middle
			( player.x, player.y ) = new_room.centre
		else: # else, draw corridors between new room and one last added to list
			for ( x, y ) in tunnel_between( start=new_room.centre, end=rooms[-1].centre ):
				dungeon.tiles[ x, y ] = tile_types.floor

		rooms.append( new_room ) # adds new element onto end of list

	return dungeon

		


def tunnel_between( start: Tuple[int,int], end: Tuple[int,int] ) -> Iterator[ Tuple[int,int] ]:
	"""Get coordinates of 2 rooms and draw a bresenham lines corridor between them"""
	# bresenham line algorithm draws a raster graphic line between 2 points
	(x1, y1) = start
	(x2, y2) = end # coordinates from the centre function of 2 rooms

	if random.random() > 0.5:
		( corner_x, corner_y ) = ( x2, y1 )
	else:
		( corner_x, corner_y ) = ( x1, y2 )

	if random.random() < 0.9:
		# calling tcod's bresenham line algorithm function to draw raster graphic lines # L shape corridors
		for ( x, y ) in tcod.los.bresenham( start = (x1, y1), end = (corner_x, corner_y) ).tolist():
			yield ( x, y )  # like return, but for generator iterables. It doesn't quit the function and returns something on each loop
		for ( x, y ) in tcod.los.bresenham( start = (corner_x, corner_y), end = (x2, y2) ).tolist():
			yield ( x, y )
	else:
		# diagonal corridors
		for ( x, y ) in tcod.los.bresenham( start = ( x1, y1 ), end = ( x2, y2 ) ).tolist():
			yield (x, y)

	