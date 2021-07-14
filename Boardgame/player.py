from Hide_on_bush import board as bd
from Hide_on_bush import utility as ut
import math

def format_change(action_input):
        action=action_input.copy()
        if action[0]==0:
            action[0]="BOOM"
            action[1]=tuple(action[1])
            del action[2]
            return tuple(action)
        else:
            action[1]=tuple(action[1])
            action[2]=tuple(action[2])
            action.insert(0,"MOVE")
            return tuple(action)
        
class ExamplePlayer:
             
    def __init__(self, colour):        
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.        
        self.gameboard = bd.create_board()
        self.past_state = []
        self.past_state.append(bd.extract(self.gameboard))        
        self.color = colour
                
    def action(self):
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        w = [0.25, 0.54, 0.9, 1.08, 1.25, 0.1]
        # machine learning w = [0.25, 6.487810237600579, -0.8834938274172996, -9.299245537507764, 1.4430459914932943, -21.30825512392702]
        
        num_token = bd.num_token(bd.extract(self.gameboard))
        if num_token <= 8:
            step_forward = 5
        elif num_token <=12:
            step_forward = 4
        else:
            step_forward = 3
        
        if (self.color == "black"):
            action = ut.max_value(self.past_state, self.gameboard, bd.extract(self.gameboard), self.color, w, 0, 5, -math.inf, math.inf)[0]
            
        else:
            action = ut.max_value(self.past_state, self.gameboard, bd.extract(self.gameboard), self.color, w, 0, 5, -math.inf, math.inf)[0]
        
        return format_change(action)


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        for the player colour (your method does not need to validate the action
        against the game rules).
        """      
        # TODO: Update state representation in response to action.      
        reformatted_action = bd.reformat(action)     
        
        bd.update_board(self.gameboard,reformatted_action)
        new_state = bd.extract(self.gameboard)
        self.past_state.append(new_state)
      


        
        
        