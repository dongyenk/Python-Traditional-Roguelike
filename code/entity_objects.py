from typing import Tuple
from entity import Actor
from ai import HostileEnemy
from fighter import Fighter

bone_white: Tuple = (223,208,183) # RGB codes in Tuple 
dungeon_rat_green: Tuple = (94,113,106) # object colour variable accessed in game_map.py's rendering code
white_white: Tuple = (255,255,255)

#player = Entity( char="@", name='humie', colour=white_white, blocks_movement=True )
#cyber_skeleton_youngin = Entity( char='s', name="Cyber Skelet0n Youngin", colour=bone_white, blocks_movement = True  )
#dungeon_ratto = Entity( char='r', name="Dungeon Ratto", colour=dungeon_rat_green, blocks_movement = True )

# Using the Actor subclass instead, which blocks movement by default 
# now needs additional parameters for the AI and Fighter components. Also don't need to state blocks_movement
player = Actor(
	char="@",
	name="Tortoise",
	colour=white_white,
	ai_cls=HostileEnemy, # Just for fulfilling a parameter of Actor
	fighter=Fighter(hp=50, attack=10, defence=10),
)

cyber_skeleton_youngin = Actor(
	char="S",
	name="Skull Sword",
	colour=bone_white,
	ai_cls=HostileEnemy,
	fighter=Fighter(hp=15, attack=5, defence=0),
)

dungeon_ratto = Actor(
	char="r",
	name="Jeffery",
	colour=dungeon_rat_green,
	ai_cls=HostileEnemy, # Component OOP
	fighter=Fighter(hp=1, attack=3, defence=0),
)
