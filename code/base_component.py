# The folder this belongs to is a python package, which is just a folder with an empty __init__.py file 

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from engine import Engine
	from entity import Entity

class BaseComponent:
	entity: Entity

	@property
	def engine( self ):
		return self.entity.game_map.engine