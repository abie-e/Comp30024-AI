# our evaluation function:
# Eval(s) = w1*f1(s) + w2*f2(s) + . . . + w5*f5(s) + w6*f6(s)

from Hide_on_bush import board as bd
import copy
import math

def evaluation(stack_list, color, w):
    value = 0
    for element in stack_list:
        num_token = element[1]
        if num_token > 5:
            num_token = 5
        if color == element[0]:            
            value += w[num_token - 1]
            value -= w[5] 
        else:            
            value -= w[num_token - 1]
            value += w[5]
     
    return round(value,5)

def single_color_score(stack_list):
    value = 0
    for element_one in stack_list:        
        for element_two in stack_list:
            number = element_one[1] + element_two[1]            
            diffx = element_one[2][0] - element_two[2][0]
            diffy = element_one[2][1] - element_two[2][1]
            diff = min(diffx,diffy)
            if diff > 2:
                value += 3*number
            else:
                value +=diff*number
    return value                  

def density_evaluation(color, stack_list):
    own_side_list = []
    opponent_list = []
    
    for element in stack_list:
        if (element[1] > 2):
            if (element[0] == color):
                own_side_list.append(element)
            else:
                opponent_list.append(element)
    return (single_color_score(own_side_list)-single_color_score(opponent_list))/50
                                      
def filter_move(color, move, board, step_forward):
    
    if (move[0] == 0):
        return 1
    
    surround_position = bd.find_surround(move[1])
    for element in surround_position:       
        if (board[element[0]][element[1]][1] > 0) and (board[element[0]][element[1]][0] != color):
            return 1  
    
    opponent_token = 0
    surround = bd.find_surround(move[2])
    for element in surround:
        number = board[element[0]][element[1]][1]
        if (( number > 0) and (board[element[0]][element[1]][0] != color)):
            opponent_token += number
    if (move[0] <= opponent_token):
        return 1
    elif (move[0]>2):
        if (opponent_token == 0):
            return 1 
        else:
            return 0
                
    if (step_forward == 2):       
        number_after = move[0] + board[move[2][0]][move[2][1]][1]    
        x = move[2][0]
        y = move[2][1]
                       
        for i in range(1,number_after+2):
            search_position = []
            for j in range(-1,2):
                search_position.append([x + i, y + j])
                search_position.append([x - i, y + j])
                search_position.append([x + j, y + i])
                search_position.append([x + j, y - i])
            for element in search_position:
                if (element[0]>=0 and element[0]<=7 and element[1]>=0 and element[1]<=7) :
                    if (board[element[0]][element[1]][1] > 0) and (board[element[0]][element[1]][0] != color):
                        return 1      
    return 0

def max_value(past_state, board, stack_list, color, w, current_depth, target_depth, alpha, beta):
    
    if color == "black":
        opponent_color = "white"
    else:
        opponent_color = "black"
    
    
    end_check = bd.check_end(stack_list)
   
    if ((current_depth == target_depth) or (end_check == 1)):          
        return evaluation(stack_list, color, w)
        
    action_list_before = bd.find_move(color,board,stack_list)         
    action_list = []        
    if ((target_depth - current_depth) == 5):   
        for element in action_list_before:
            if ((element[0] == 0) or (filter_move(color, element, board, 2) == 1)):
                action_list.append(element)
                
    elif ((target_depth - current_depth) == 3):    
        
        for element in action_list_before:
            if ((element[0] == 0) or (filter_move(color, element, board, 1) == 1)):
                action_list.append(element)   
    else:    
        action_list = action_list_before
    
    if not action_list:
        if ((target_depth - current_depth) == 5):      
            return max_value(past_state, board, stack_list, color, w, 0, 1, -math.inf, math.inf)
        else:             
            return evaluation(stack_list, color, w)
           
    
    if ((current_depth == 0) and (action_list)):
       
        final_action = action_list[0]
        original_alpha = alpha
  
    for action in action_list:
          
        next_board = copy.deepcopy(board)
        bd.update_board(next_board,action)     
        next_state = bd.extract(next_board)       
        
        if ((current_depth == 0) and action[0] == 0):
            if (evaluation(next_state, color, w) > evaluation(stack_list, color, w)):
                return [action, evaluation(next_state, color, w)] 
        
        if ((current_depth > 0) or (next_state not in past_state)):
            alpha = max(alpha, min_value(past_state, next_board, next_state, opponent_color, w, (current_depth+1), target_depth, alpha, beta))
        
        if (current_depth == 0):
            if (original_alpha < alpha):
                final_action = action
                original_alpha = alpha
                
        if (alpha >= beta):
           
            return beta
   
    
    if (current_depth == 0):
       
        return [final_action, original_alpha]
    return alpha

def min_value(past_state, board, stack_list, color, w, current_depth, target_depth, alpha, beta):    
    if color == "black":
        opponent_color = "white"
    else:
        opponent_color = "black"
        
   
    end_check = bd.check_end(stack_list)
    
    if ((current_depth == target_depth) or (end_check == 1)):  
      
        return evaluation(stack_list, opponent_color, w)
    
    action_list_before = bd.find_move(color,board,stack_list)         
    action_list = []            
    if ((target_depth - current_depth) == 4):         
        for element in action_list_before:
            if ((element[0] == 0) or (filter_move(color, element, board, 1) == 1)):
                action_list.append(element)          
    else:    
        action_list = action_list_before
    
    if not action_list:              
        action_list.append(max_value(past_state, board, stack_list, color, w, 0, 1, -math.inf, math.inf)[0])
        
        
    for action in action_list:
       
        next_board = copy.deepcopy(board)
        bd.update_board(next_board,action)
        next_state = bd.extract(next_board)
        
        if (action[0] == 0):
            if (evaluation(next_state, color, w) < evaluation(stack_list, color, w)):
                return evaluation(next_state, color, w)
        if ((current_depth > 0) or (next_state not in past_state)):
            beta = min(beta, max_value(past_state, next_board, next_state, opponent_color, w, (current_depth+1), target_depth, alpha, beta))
        if (beta <= alpha):
           
            return alpha
    return beta
        
        
        
        
        
    