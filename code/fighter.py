# Instead of totally modeling dungeon monsters, as Entity objects with hp, attck, ac attributes
# Going to make a Fighter object a component of the Entity monsters.

from base_component import BaseComponent

class Fighter( BaseComponent ): # being a subclass of BaseComponent gives it access to the parent Entity object, and Engine object
	def __init__( self, hp: int, attack: int,  defence: int ):
		self.max_hp = hp
		self._hp = hp # creating a special function called hp instead
		self.attack = attack
		self.defence = defence

	@property
	def hp(self) -> int: # getter and setter functions like what you get in java for private variables
		return self._hp

	@hp.setter
	def hp(self, value: int) -> None:
		self.hp = max( 0, min(value,self.max_hp) ) # if argument int exceeds max_hp or is < 0, it won't be used. 