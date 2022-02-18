from typing import Tuple
from entity import Entity

bone_white: Tuple = (223,208,183) # RGB codes in Tuple 
dungeon_rat_green: Tuple = (94,113,106) # object colour variable accessed in game_map.py's rendering code
white_white: Tuple = (255,255,255)

player = Entity( char="@", name='Hoooman, weak sad. Play dom-jot.', colour=white_white, blocks_movement=True )

cyber_skeleton_youngin = Entity( char='s', name="Cyber Skelet0n Youngin", colour=bone_white, blocks_movement = True  )
dungeon_ratto = Entity( char='r', name="Dungeon Ratto", colour=dungeon_rat_green, blocks_movement = True )