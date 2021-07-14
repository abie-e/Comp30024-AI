def create_board():
    gameboard=[[["black",0] for j in range(8)] for i in range(8)]
    
    for s in range(8):
        for t in range(8):
            if t==0 or t==1:
                if s!=2 and s!=5:
                    gameboard[s][t]=["white",1]
            if t==6 or t==7:       
                if s!=2 and s!=5:
                    gameboard[s][t]=["black",1]   
    return gameboard
            
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
        
def update_board(board,action):
    location=position(board)
    if action[0]==0:
        boom=[]
        boom.append(action[1])
        board[action[1][0]][action[1][1]][1]=0
        while boom:
            explosion = boom.pop()
            surround = find_surround(explosion)
            contact_point=find_overlap(surround,location)
            location=[i for i in location if i not in contact_point]
            boom+=[i for i in contact_point]
            for i in range(len(contact_point)):
                board[contact_point[i][0]][contact_point[i][1]][1]=0
    else:
        board[action[2][0]][action[2][1]]=[board[action[1][0]][action[1][1]][0],action[0]+board[action[2][0]][action[2][1]][1]]
        board[action[1][0]][action[1][1]][1]-=action[0]

def position(gameboard):
    location=[]
    for i in range(8):
        for j in range(8):
            if gameboard[i][j][1]!=0:
                location.append([i,j])
    return location

def extract(board):
    existing_token=[]
    for i in range(8):
        for j in range(8):
            if board[i][j][1]!=0:
                 existing_token.append(board[i][j]+[[i,j]])
    return existing_token

def find_move(color, board, extract_list):
    result = []
    boom = []
    move = []
    for element in extract_list:
        if (element[0] == color):
            surround = find_surround(element[2])
            own_num = element[1]
            opponent_num = 0
            valid = 1
            for position in surround:
                token = board[position[0]][position[1]]
                if token[1] > 0:
                    if token[0] == color:
                        valid = 0
                        break
                    else:
                        opponent_num += token[1]
            if ((valid == 1) and (opponent_num >= own_num)):
                boom.append([0, element[2], element[2]])
            move += single_token_move(element,board)
    result = boom + move
    return result
    
def single_token_move(token, board):
    all_case=[]
    valid_case=[]
    k = 1
    if (token[1] > 1):
        k = token[1]-1
    for i in range(1,token[1]+1):
        for j in {1,token[1],k}:
            all_case.append([j]+[token[2]]+[[token[2][0]+i,token[2][1]]])
            all_case.append([j]+[token[2]]+[[token[2][0],token[2][1]+i]])
            all_case.append([j]+[token[2]]+[[token[2][0]-i,token[2][1]]])
            all_case.append([j]+[token[2]]+[[token[2][0],token[2][1]-i]])
    for element in all_case:
        if 0<=element[2][0]<8 and 0<=element[2][1]<8:
            if board[element[2][0]][element[2][1]][1]==0:                
                valid_case.append(element)
                continue
            if board[element[2][0]][element[2][1]][0]==token[0]:
                if (board[element[2][0]][element[2][1]][1] + token[1]) <= 5:                   
                    valid_case.append(element)                  
    return valid_case

def check_end(stack_list):
    if (len(stack_list) <= 1):
        return 1
    color = stack_list[0][0]
    for i in range(1,len(stack_list)):
        if (stack_list[i][0] != color):
            return 0
    return 1

def check_result(stack_list):
    if len(stack_list) == 0:
        return "draw"
    if stack_list[0][0] == "black":
        return "black win"
    return "white win"

def num_token(stack_list):
    if len(stack_list) == 0:
        return 0
    number = 0
    for element in stack_list:
        number += element[1]
    return number

def reformat(action):    
    if len(action)>2:
        reformatted_action=list(action)
        reformatted_action[2]=list(reformatted_action[2])
        reformatted_action[3]=list(reformatted_action[3])
        reformatted_action=reformatted_action[1:]       
    else:
        reformatted_action=[[] for i in range(3)]
        reformatted_action[0]=0
        reformatted_action[1]=list(action[1])
        reformatted_action[2]=list(action[1])
    return reformatted_action
                                           