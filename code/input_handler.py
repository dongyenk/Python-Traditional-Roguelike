from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction, MoveOrMeleeAction

class EventHandler( tcod.event.EventDispatch[ Action ] ): # Optional seems to be for annotation? meaning an Action subclass or none
#EventDispatch has special functions such as ev_quit, ev_mousemotion,that get  called automatically when input happens
	def ev_quit( self, event: tcod.event.Quit ) -> Optional[ Action ]:
		raise SystemExit()

	def ev_keydown( self, event: tcod.event.KeyDown ) -> Optional[ Action ]:
	#Going to return None or an instance of an Action subclass, which represents what the game will do next
		action: Optional[Action] = None
		# when ev_event auto called, event.sym holds constant representing key that was pressed
		key = event.sym
		# tcod documentation lists constants assigned to different key presses, such as SDLK_q / tcod.event.K_q
		if key == tcod.event.K_KP_8:
			action = MoveOrMeleeAction( 0, -1 ) # instance of class that represents the next move for the @
		elif key == tcod.event.K_KP_2:
			action = MoveOrMeleeAction( 0, 1 ) # x=1, y=1 is the top left. # -x is left, -y is up
		elif key == tcod.event.K_KP_4:
			action = MoveOrMeleeAction( -1, 0 )
		elif key == tcod.event.K_KP_6:
			action = MoveOrMeleeAction( 1, 0 )
		# diagonals
		elif key == tcod.event.K_KP_7:
			action = MoveOrMeleeAction( -1, -1 )
		elif key == tcod.event.K_KP_9:
			action = MoveOrMeleeAction( +1, -1 )
		elif key == tcod.event.K_KP_1:
			action = MoveOrMeleeAction( -1, +1 )
		elif key == tcod.event.K_KP_3:
			action = MoveOrMeleeAction( +1, +1  )
		# waiting
		elif key == tcod.event.K_KP_5:
			action = MoveOrMeleeAction( 0, 0 )


		elif key == tcod.event.K_ESCAPE or key == tcod.event.K_q:
			action = EscapeAction()

		return action
