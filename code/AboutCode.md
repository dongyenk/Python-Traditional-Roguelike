# GameMap class in game_map module

It represents the dungeon. It's rooms, corridors and entities. (Characters and items.)

game_map object is in the engine object.
---------------------------------------------------------------------------------------------------------

# Engine class

Has code which handles enemy turns, visibility, and calling game_map object's render function which draws the game's graphics.
---------------------------------------------------------------------------------------------------------

# Entity class

To represent all dungeon entities. Their location, colour, graphics, attributes.

Entity objects created in the entity_objects module. From there, they are copied and put into the game_map dungeon object.

