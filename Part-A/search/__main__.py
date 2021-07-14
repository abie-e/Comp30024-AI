import sys
import json
from collections import defaultdict

from search.util import print_move, print_boom, print_board

def extract_position(token):
    position = []
    for element in token:
        position.append([element[1],element[2]])
    return position
def remove_duplicate(array):
    result = []
    for i in array:
        if i not in result:
            result.append(i)
    return result

#find given a coordinate, find up, down, left, right coordinate
def find_move(coordinate,distance):
    possible_move = []
    valid_move = []
    neg_distance = distance*(-1)    
    for i in range(1,(distance+1)):                           
        possible_move.append([coordinate[0]+i,coordinate[1]])
        possible_move.append([coordinate[0],coordinate[1]+i])
        possible_move.append([coordinate[0]-i,coordinate[1]])
        possible_move.append([coordinate[0],coordinate[1]-i])
    for element in possible_move:
        if (element[0]>=0 and element[0]<=7 and element[1]>=0 and element[1]<=7):
            valid_move.append([element[0],element[1]])    
    return valid_move

def find_surround(coordinate):
    surround = []
    for i in range(-1,2):
        for j in range(-1,2):
            x = coordinate[0]+i
            y = coordinate[1]+j
            if ((not(i==0 and j==0)) and x>=0 and x<=7 and y>=0 and y<=7):
                surround.append([x,y])
    return surround

def find_overlap(token_a,token_b):
    overlap = []
    for element_a in token_a:
        for element_b in token_b:
            if ((element_a[0] == element_b[0]) and (element_a[1] == element_b[1])):
                overlap.append([element_a[0],element_a[1]])
    return overlap

def explosion_radius_overlap(explosion_point):
    all_point = []
    for i in explosion_point:
        all_point += i[1]    
    point_count = defaultdict(int)
    for i in all_point:
        point_count[tuple(i)] += 1
    overlap_point_count = {key:val for key, val in point_count.items() if val >1}
    all_point = [[value, list(key)] for key,value in overlap_point_count.items()]
    for i in range(len(all_point)):
        explosion_token=[]
        for j in explosion_point:
            if all_point[i][1] in j[1]:
                explosion_token +=j[1]
        all_point[i].append(explosion_token)
        all_point[i][2] = remove_duplicate(all_point[i][2])
    return sorted(all_point, key=lambda x: x[0], reverse=True)

def explosion_group(black_queue):
    black_queue_copy = black_queue.copy()
    explosion_point = []
    index = 0
    while black_queue_copy:
        i = black_queue_copy.pop()
        surround = find_surround(i)
        explosion_point.append([[i],find_surround(i)])
        contact_point = find_overlap(surround,black_queue_copy)
        while contact_point!= []:
            black_queue_copy=[j for j in black_queue_copy if j not in contact_point]
            explosion_point[index][0]=explosion_point[index][0]+[k for k in contact_point]                   
            surround = []
            for w in contact_point:
                explosion_point[index][1]=explosion_point[index][1]+find_surround(w) 
                surround += find_surround(w)
            contact_point = find_overlap(surround,black_queue_copy)
        explosion_point[index][1][:] = remove_duplicate(explosion_point[index][1])
        explosion_point[index][0][:] = remove_duplicate(explosion_point[index][0])
        explosion_point[index][1][:] = [i for i in explosion_point[index][1] if i not in black_queue]
        index+=1
    return explosion_point

def explosion_small_group(explosion_point_sec,black):
    explosion_point=explosion_point_sec.copy()
    for i in range(len(explosion_point)):
        group=[]
        queue = explosion_point[i][1].copy()
        point = queue.pop()
        group.append([point])
        while queue:
            point = queue.pop()
            for j in range(len(group)):
                check_point = True
                #change
                if len(simple_BFS(point,group[j][0],black,1)[0]) > 0:
                    group[j]+=[point]
                    check_point = False
                    break
            if check_point:
                group +=[[point]] 
        explosion_point[i]+=group
        explosion_point[i][0] = remove_duplicate(explosion_point[i][0])
        explosion_point[i][1] = remove_duplicate(explosion_point[i][1])
    return explosion_point

def sperate_black(explosion_point):
    group=[]
    explosion_point_copy=explosion_point.copy()
    for i in range(explosion_point_copy):
        for j in explosion_point_copy[i][1]:
            for k in explosion_point_copy[i:]:
                if j in k[1]:
                    group.append([explosion_point_copy[i][0]+k[0]])
    return group

#parameter black and white is the position list of black and white token, black and white should already be extracted
def simple_BFS(start,end,black,distance):
    success = 0
    visited = []
    queue = []
    mother_node = [[[-1,-1] for x in range(8)] for y in range(8)]    
    
    queue.append(start)
    
    while(len(queue) != 0):
        current = queue.pop(0)
        visited.append(current)
        
        if ((current[0] == end[0]) and (current[1] == end[1])):
            success = 1            
            break
        surround = find_move(current,distance)
        
        for element in surround:             
            if ((element not in black) and (element not in visited) and (element not in queue)):               
                queue.append(element)
                mother_node[element[0]][element[1]] = current
                                               
    route = []
    if (success == 1):
        route.append(end)
        current = end
        while(not ((current[0]==start[0]) and (current[1]==start[1]))):              
            current = mother_node[current[0]][current[1]]
            route.append(current)        
    route.reverse()
    
    max_jump = -1
    if len(route)>1:        
        for i in range(len(route)-1):
            jump = abs(sum(route[i])-sum(route[i+1]))
            if (jump>max_jump):
                max_jump = jump
        route.pop(0)
    elif (len(route)==1):        
        max_jump = 0
        route.pop(0)
    return [route,max_jump]

#white and black are not extracted form
def make_stack(white,black):
    move_point = []
    for elements in white:
        return move_point


def one_to_one(explosion_small_group1,black,white):
    
    num_white = len(white)
    num_black_group = len(explosion_small_group1)    
    could_move = 1
    check_matrix =[[[]for x in range(num_black_group)] for y in range(num_white)] 
      
    for i in range(num_white):
        for j in range(num_black_group):
            find_route = 0
            k = 2            
            while ((k < len(explosion_small_group1[j])) and (find_route == 0)):                
                random_route = explosion_small_group1[j][k][0]              
                possible_route = simple_BFS(white[i],random_route,black,1) 
               
                if (possible_route[1]>=0):
                    find_route = 1
                    check_matrix[i][j] = possible_route                   
                k+=1
             
    no_route_group = [i for i in range(num_black_group)] 
    no_route_token = [i for i in range(num_white)]
    final_route = [[] for j in range(num_white)]     
    route_with_position = [[] for j in range(num_white)] 
    
    k = 0
       
    while(k < num_black_group):        
        for j in range(num_black_group):
            if (len(no_route_group) == 0):
                break
            group_has_route = [] 
            for i in range(num_white):
                if ((i in no_route_token) and len(check_matrix[i][j])>0 and (check_matrix[i][j][1]>=0)):
                    group_has_route.append(i)
                    
            if (len(group_has_route) == 0):                 
                return []
            elif (len(group_has_route) == 1):               
                final_route[group_has_route[0]] = check_matrix[group_has_route[0]][j][0]                             
                no_route_token.remove(group_has_route[0])
                no_route_group.remove(j)
                      
            elif( (k>0) and (len(group_has_route) > 1)):               
                final_route[group_has_route[0]] = check_matrix[group_has_route[0]][j][0]
                no_route_token.remove(i)
                no_route_group.remove(j)
        k += 1        
                    
    for i in range(num_white):             
        route_with_position[i] = [white[i],final_route[i]]
           
    return route_with_position

#this function should not be used if there is already a stack consists of more than one token,white and black are positions already extracted
def single_token_move(white,black,explosion_group1,explosion_small_group1,raw_white):
           
    num_white = len(white)
    num_black_group = len(explosion_group1)   
    raw_white_copy = raw_white.copy()
    
    
    if (num_white >= num_black_group):
        
        result = []
        result = one_to_one(explosion_small_group1,black,white)  
        
        if len(result)>0:
            for route in result:          
                for element in raw_white_copy:
                    extract_form = [element[1],element[2]]
                    if (route[0] == extract_form):
                        raw_white.remove(element)           
            return result
            
        else:
            return []
    else:
        white_copy = white.copy()     
        result = []
        single_move_result = []
        multi_overlap = []
        used_explosion = []
        explosion_group2 = []
        explosion_small_group2 = []
        num_muti_token = 0
        multi_overlap = explosion_radius_overlap(explosion_group1)
        
        i = 0
        while (i < len(multi_overlap)):
            element = multi_overlap[i] 
            found_route = 0
            j = 0
            white_copy2 = white_copy.copy()
            while((element[1] not in used_explosion) and j < len(white_copy2) and found_route == 0):            
                token = white_copy2[j]               
                possible_route = simple_BFS(token,element[1],black,1)
                
                if(possible_route[1]>=0):
                    found_route = 1                   
                    result.append([token,possible_route[0]])
                    for position in element[2]:
                        used_explosion.append(position)
                    white_copy.remove(token)
                j += 1
            i += 1
            
        for element in explosion_group1:            
            if not(element[1][0] in used_explosion):                
                explosion_group2.append(element)
               
        explosion_group1[:] = explosion_group2
        explosion_small_group1[:] = explosion_small_group(explosion_group1,black)
       
        single_move_result = one_to_one(explosion_small_group1,black,white_copy) 
        result += single_move_result
        for route in result:          
                for element in raw_white_copy:
                    extract_form = [element[1],element[2]]
                    if (route[0] == extract_form):
                        raw_white.remove(element)
        return result
    

def form_stack(black,raw_white):
    queue = raw_white.copy()
    result = []
    modified_result = []
    index = 0
    while queue:
        moving_token = queue.pop()
        result.append([moving_token[0]]+[[moving_token[1:]]]+[[]])
        while queue:
            check = len(queue)
            check_back = len(result)
            for i in queue:
                BFS_result = simple_BFS(moving_token[1:],i[1:],black,moving_token[0])[0]
                if BFS_result:
                    modified_result.append([moving_token[0]]+[moving_token[1:]]+[BFS_result])
                    moving_token[0] += i[0]
                    moving_token[1:] = i[1:]
                    result[index][0] += i[0]
                    result[index][1] += [i[1:]]
                    result[index][2] += BFS_result
                    queue.remove(i)
            for j in result:
                if j[2]:
                    position=j[2][-1]
                    BFS_result_back = simple_BFS(moving_token[1:],position,black,moving_token[0])[0]
                else:
                    position = j[1][0]
                    BFS_result_back = simple_BFS(moving_token[1:],position,black,moving_token[0])[0]
                if BFS_result_back:
                    modified_result.append([moving_token[0]]+[moving_token[1:]]+[BFS_result_back])
                    moving_token[0] += j[0]
                    moving_token[1:] = position
                    result[index][0] += j[0]
                    result[index][1] += j[1]
                    result[index][2] += BFS_result_back
                    result.remove(j)
                    index -= 1
            if check == len(queue) and check_back == len(result):
                break
        index += 1  
        
    raw_white[:] = sorted([[w[0]]+w[2][-1] if w[2] else [w[0]]+w[1][0] for w in result], key=lambda x: x[0], reverse=True)
    return modified_result 

   
def multi_move(black, raw_white, explosion_group1,explosion_small_group1):
    
    white = extract_position(raw_white)
    num_white = len(raw_white)
    num_black_group = len(explosion_small_group1) 
    start_position_raw = raw_white[0]
    end_position = []
    route = []
    group_route = []
            
    for j in range(num_black_group):
        small_group_route = []       
        k = 2
        route_found = 0
        
        while (k < len(explosion_small_group1[j])) :                
            random_route = explosion_small_group1[j][k][0]           
            route_set = simple_BFS(white[0],random_route,black,raw_white[0][0])            
            jump = route_set[1]
            possible_route = route_set[0]
            if (len(possible_route)>0 ):               
                small_group_route.append(route_set)
                route_found += 1                
            k+=1
              
        if (route_found == 0):            
            return []
                
        sorted(small_group_route, key=lambda x: x[1], reverse=True) 
        if (len(small_group_route)>0):
            group_route.append(small_group_route[0])
            
    sorted(group_route, key=lambda x: x[1], reverse=True)  
    multi_overlap = explosion_radius_overlap(explosion_group1)
   
    for element in group_route:        
        for overlap in multi_overlap:
            if (element[0][-1] == overlap[1]):                              
                route = element[0]                
                break
        if (len(route) > 0):
            break
    if (len(route) == 0):
        route = group_route[0][0]
   
    explosion_group2 = explosion_group1.copy()
    
    if(len(route) > 0):
        end_position = route[-1]
        delete_explosion_group = []
        #update explosion group
        for element in explosion_group1:
            if end_position in element[1]:
                explosion_group2.remove(element)
    
    explosion_group1[:] = explosion_group2   
    explosion_small_group1[:] = explosion_small_group(explosion_group1,black)
           
    result_route = [[raw_white[0][0],[start_position_raw[1],start_position_raw[2]],route]]
    
    if (len(route)== 1):           
        raw_white.append([(raw_white[0][0]-1),start_position_raw[1],start_position_raw[2]])
        result_route.append( [(raw_white[0][0]-1),end_position,[[start_position_raw[1],start_position_raw[2]]]])
    elif(len(route) > 1):        
        raw_white.append([(raw_white[0][0]-1),route[-2][0],route[-2][1]])
        result_route.append([(raw_white[0][0]-1),end_position,[route[-2]]])
    raw_white.pop(0)
    raw_white[:] = sorted([w[:] for w in raw_white], key=lambda x: x[0], reverse=True)
    
    return result_route
    
def strategy_one(white,black,raw_white,explosion_group1,explosion_small_group1):
    explosion_coordinate = []
    single_move_result = []
    form_stack_result = []
    multi_move_result = []
        
    single_move_result += single_token_move(white,black,explosion_group1,explosion_small_group1,raw_white)
    
    if (len(explosion_group1)>0):           
        has_move = 1        
        form_stack_result += form_stack(black, raw_white) 
        
        #if (len(form_stack_result) > 0):          
        if (len(raw_white) > 0 and raw_white[0][0] > 1):            
            while (raw_white[0][0] > 1):               
                result = multi_move(black, raw_white, explosion_group1,explosion_small_group1)
                if (len(result) == 0):                   
                    break;
                multi_move_result += result
            
            if(len(raw_white) > 0):        
                
                single_move_result += single_token_move(extract_position(raw_white),black,explosion_group1,explosion_small_group1,raw_white)
                
    return[single_move_result, form_stack_result, multi_move_result]

def all_position_on_board():
    board=[]
    for i in range(8):
        for j in range(8):
            board.append([i,j])
    return board 

def blasting(black,raw_white,explosion_group1,explosion_small_group1):
    route=[]
    black_explosion = sorted(explosion_group1, key=lambda x: len(x[0]), reverse=True)[0][0]
    for j in raw_white:
        if j[0] == 2:
            raw_white.remove(j)
            raw_white.append([1]+j[1:])
            raw_white.append([1]+j[1:]) 
    for i in sorted(explosion_group1, key=lambda x: len(x[0]), reverse=True)[0][1]:
        for j in raw_white:
            result = simple_BFS(j[1:],i,black,j[0])[0]
            if result or j[1:]==[i]:
                state = True
                raw_white.remove(j)
                black.append(i)
                explosion_range = [w[1] for w in explosion_group(black)]
                board = all_position_on_board()
                protection_route=[]
                for k in raw_white:
                    #  white token is in the explosion area
                    if k[1:] not in [w for w in board if w not in explosion_range[0]+black]:
                        check = 0
                        for position in [w for w in board if w not in explosion_range[0]+black]:
                            BFS_result = simple_BFS(k[1:],position,black,k[0])[0]
                            if BFS_result:
                                check += 1
                                protection_route.append([k[1:]]+[BFS_result])
                                raw_white.remove(k)
                                raw_white.append([1]+position)
                                break
                        if check == 0:
                            state = False
                            break                            
                if state:
                    route.append([j[1:]]+[result])
                    black.remove(i)
                    black[:] = [w for w in black if w not in black_explosion]
                    explosion_group1[:] = explosion_group(black)
                    return route+protection_route
                else:
                    raw_white.append(j)
                    black.remove(i)
    return route 
def to_tuple(a_list):
    return (a_list[0],a_list[1])

def transform_stack_move(stack_result,final_boom_output):
    result = []    
    last_position = []
    for i in range(len(stack_result)):       
        element = stack_result[i]
        num_stack = element[0]  
        result.append(["MOVE ", num_stack, " from ", to_tuple(element[1]), " to ", to_tuple(element[2][0]),"."])            
        if (len(element[2])>1):           
            for i in range(len(element[2])-1):
                result.append(["MOVE ", num_stack, " from ", to_tuple(element[2][i]), " to ", to_tuple(element[2][i+1]),"."])
        if (i < len(stack_result)):
            if ((len(last_position)> 0) and (last_position[0] > num_stack)):
                final_boom_output.append(["BOOM at ",to_tuple(last_position[1]),"."])
        last_position = [element[0],element[2][-1]]
    return result

def transform_boom_first(explosion_first):
    result = []   
    
    for element in explosion_first:
        result.append(["MOVE ",1," from ",to_tuple(element[0])," to ",to_tuple(element[1][0]),"."])
        if (len(element[1]) > 1):
            for i in range(len(element[1])-1):
                result.append(["MOVE ",1," from ",to_tuple(element[1][i])," to ",to_tuple(element[1][i+1]),"."])
    if (len(explosion_first)>0):
        result.append(["BOOM at ",to_tuple(explosion_first[0][1][-1]),"."])
    return result

def transform_single_move(single_move_result,final_boom_output):
    result = []
    
    for element in single_move_result:       
        if (len(element[1]) == 0):
            final_boom_output.append(["BOOM at ",to_tuple(element[0])])
        else:
            result.append(["MOVE ",1," from ",to_tuple(element[0])," to ",to_tuple(element[1][0]),"."])  
            final_boom_output.append(["BOOM at ",to_tuple(element[1][-1]),"."])
        for i in range(len(element[1])-1):
            result.append(["MOVE ",1," from ",to_tuple(element[1][i])," to ",to_tuple(element[1][i+1]),"."])           
        
    return result  

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)  
    
    raw_black = data["black"]
    raw_white = data["white"]
    
    black = extract_position(raw_black)
    white = extract_position(raw_white) 
    
    explosion_group1 = explosion_group(black)
    explosion_small_group1 = explosion_small_group(explosion_group1,black)
    explosion_first = []
    final_boom_output = []
    output = []
    explosion_position = []
    result = strategy_one(white,black,raw_white,explosion_group1,explosion_small_group1)
    single_move_result = result[0]
    form_stack_result = result[1]
    multi_move_result = result[2]
      
    if (len(single_move_result) == 0 and len(multi_move_result)==0): 
        explosion_first = blasting(black,raw_white,explosion_group1,explosion_small_group1)
        explosion_small_group1 = explosion_small_group(explosion_group1,black)        
        single_move_result = single_token_move(extract_position(raw_white),black,explosion_group1,explosion_small_group1,raw_white)
           
    transform_stack_output = transform_stack_move(form_stack_result,final_boom_output)    
    explosion_first_output = transform_boom_first(explosion_first)   
    multi_move_output = transform_stack_move(multi_move_result,final_boom_output)       
    single_move_output = transform_single_move(single_move_result,final_boom_output)    
    output = transform_stack_output + explosion_first_output + multi_move_output + single_move_output + final_boom_output
    
    for element in output:
        print(*element, sep="")
   
    
    # TODO: find and print winning action sequence


if __name__ == '__main__':
    main()


    