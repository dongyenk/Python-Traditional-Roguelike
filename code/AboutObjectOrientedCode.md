# Engine Class

Class for the important Engine object which contains vital objects. These are mentioned below.

## GameMap object

GameMap object contains all the game's entities, such as dungeon rats, rooms and corridors.

Entity objects are stored in a set inside the GameMap object. This GameMap object is an attribute of the Engine object.

Each room is an object, and the corridors are not. They are just array locations selected by TCOD libray line drawing function.

## EventHandler object

Which contains the Action subclass objects, with code used to make entities act.

A lot of the code vital to the game's main loop is in the EventHandler object, which handles enemy and player actions.

### 👁 The Engine object, and it's GameMap and InputHandler attribute objects draw the game's graphics.
