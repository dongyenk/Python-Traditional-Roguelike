from __future__ import annotations
import random
import tcod
from typing import Tuple, Iterator, List, TYPE_CHECKING

from game_map import GameMap
import tile_types
import entity_objects

if TYPE_CHECKING:
	from engine import Engine

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
	max_monsters_per_room: int,
	engine: Engine
) -> GameMap:
	"""Create an instance of GameMap and modify it to have rooms and corridors before returning it."""
	player = engine.player
	dungeon = GameMap( engine=engine, width=map_width, height=map_height, entities=[player] )

	rooms: List[ RectangularRoom ] = [] # extra bit is just annotation saying this will be a list of RectRoom instances

	diagonal_corridors: bool = ( random.random() > 0.9 ) # test will evaluate as bool that gets assigned to variable

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
			player_x, player_y = new_room.centre
			player.place( player_x, player_y, dungeon )
		else: # else, draw corridors between new room and one last added to list # also add monsters
			if ( diagonal_corridors ):
				for ( x, y ) in tunnel_between( start=new_room.centre, end=rooms[-1].centre, diag=True ):
					dungeon.tiles[ x, y ] = tile_types.floor
			else:
				for ( x, y ) in tunnel_between( start=new_room.centre, end=rooms[-1].centre, ):
					dungeon.tiles[ x, y ] = tile_types.floor

			place_entities( new_room, dungeon, max_monsters_per_room )

		rooms.append( new_room ) # adds new element onto end of list

	return dungeon

def place_entities( room: RectangularRoom, dungeon: GameMap, max_monsters: int ):
	"""Choose random x, y coordinates that fit inside room, check for overlap with entities stored in dungeon, for loop based on max monsters."""
	for monster in range( max_monsters ):
		x = random.randint( room.x1+1, room.x2-1 ) # -1, or +1 to make monster not inside wall
		y = random.randint( room.y1+1, room.y2-1 ) 

		if any( x==other.x and y==other.y for other in dungeon.entities ):
			continue # go back to top of loop when monsters overlap
		else:
			if random.random() <= 0.8:
				entity_objects.dungeon_ratto.spawn( dungeon, x, y ) # Calling on class function from object, to copy itself and send the copy to the Entity bbjects set, in the GameMap dungeon object
			else:
				#pass # place cyber skeleton youngin
				entity_objects.cyber_skeleton_youngin.spawn( dungeon, x, y )

def tunnel_between( start: Tuple[int,int], end: Tuple[int,int], diag: bool = False ) -> Iterator[ Tuple[int,int] ]:
	"""Get coordinates of 2 rooms and draw a bresenham lines corridor between them"""
	(x1, y1) = start
	(x2, y2) = end # coordinates from the centre function of 2 rooms

	if diag:
		for ( x, y ) in tcod.los.bresenham( start = ( x1, y1 ), end = ( x2, y2 ) ).tolist():
			yield ( x, y )

	else:
		# bresenham line algorithm draws a raster graphic line between 2 points	

		if random.random() > 0.5:
			( corner_x, corner_y ) = ( x2, y1 )
		else:
			( corner_x, corner_y ) = ( x1, y2 )

		# calling tcod's bresenham line algorithm function to draw raster graphic lines # L shape corridors
		for ( x, y ) in tcod.los.bresenham( start = (x1, y1), end = (corner_x, corner_y) ).tolist():
			yield ( x, y )  # like return, but for generator iterables. It doesn't quit the function and returns something on each loop
		for ( x, y ) in tcod.los.bresenham( start = (corner_x, corner_y), end = (x2, y2) ).tolist():
			yield ( x, y )

	