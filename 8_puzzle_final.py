#8 Puzzle BFS

import numpy as np
import os
    
def moveLeft(data):
    #print("in moveleft")
    i,j = np.where(data==0)
    if (j==0):
        return None
       
    else:
      temp_arr = np.copy(data)
      temp = temp_arr[i,j-1] 
      temp_arr[i,j] = temp
      temp_arr[i,j-1] = 0
      return temp_arr
def moveRight(data):
    #print("in moveright")
    i,j = np.where(data==0)
    if (j==2):
        return None
        
    else:
      temp_arr = np.copy(data)
      temp = temp_arr[i,j+1] 
      temp_arr[i,j] = temp
      temp_arr[i,j+1] = 0
      return temp_arr
    
def moveUp(data):
    #print("in moveup")
    i,j = np.where(data==0)
    if (i==0):
        return None
        
    else:
      temp_arr = np.copy(data)
      temp = temp_arr[i-1,j] 
      temp_arr[i,j] = temp
      temp_arr[i-1,j] = 0
      return temp_arr
    
def moveDown(data):
    #print("in movedown")
    i,j = np.where(data==0)
    if (i==2):
        return None
        
    else:
      temp_arr = np.copy(data)
      temp = temp_arr[i+1,j] 
      temp_arr[i,j] = temp
      temp_arr[i+1,j] = 0
      return temp_arr
      
def moveTile(action, data):
    #print("in moveTile")
    if (action=='up'):
        return moveUp(data)
    if (action=='down'):
        return moveDown(data)
    if (action=='left'):
        return moveLeft(data)
    if (action=='right'):
        return moveRight(data)
    else:
        return None

    
class Node:
    def __init__(self,node_no, data, parent, id, cost):
        #print("node created")
        self.data = data
        self.parent = parent
        self.id = id
        self.node_no = node_no
        self.cost = cost
        
#
    
def printStates(list):
    print("printing")
    for l in list:
        print("Move : "+ str(l.id) + "\t" + "Result : "+ str(l.data) + "\t"+ "node number:" + str(l.node_no))
        
def writeToFile(path,seen,visited):
    #path
    if os.path.exists("Nodepath.txt"):
       os.remove("Nodepath.txt")
    
    f = open("Nodepath.txt", "a")
    for element in path:
        f.write("[")
        for i in range(len(element.data)):
            for j in range(len(element.data)):
                f.write(str(element.data[j][i])+" ")
        f.write("]")
        f.write("\n")
    f.close()
    
    #visited
    if os.path.exists("Nodes.txt"):
       os.remove("Nodes.txt")
    
    f = open("Nodes.txt", "a")
    for element in seen:
        f.write("[")
        for i in range(len(element)):
            for j in range(len(element)):
                f.write(str(element[j][i])+" ")
        f.write("]")
        f.write("\n")
    f.close()
    
    #path
    if os.path.exists("nodeinfo.txt"):
       os.remove("nodeinfo.txt")
    
    f = open("nodeinfo.txt", "a")
    for n in path:
        if n.parent is not None:
            f.write(str(n.node_no) + "\t" + str(n.parent.node_no) + "\t" + str(n.cost)+"\n")
        else:
            f.write(str(n.node_no) + "\t" + "None" + "\t" + str(n.cost)+"\n")
    f.close()    
    

def trackback(node):
    p = list()
    p.append(node)
    parent = node.parent
    if parent == None:
        return p
    
    while parent is not None:
        #print (parent.id)
        p.append(parent)
        parent = parent.parent
    p_rev = list(reversed(p))
    return p_rev
   

def node_creation(node):
    print("node_creation running")
    actions = [ "down","up", "left", "right"]
    goal_node = np.array([[1,2,3],[4,5,6],[7,8,0]])
    node_q = [node]
    seen = list()
    visited = list()
    seen.append(node_q[0].data.tolist())
    #print(seen)
    node_counter = 0
    while  node_q:
        current_root = node_q.pop(0)
        if(current_root.data.tolist() == goal_node.tolist()):
            print("Goal reached: ",current_root.data)
            visited.append(current_root)
            return current_root,seen,visited
    
    #print("Current Root node is :", current_root.data)
            
        for action in actions:
            temp_data = moveTile(action,current_root.data)
            if not temp_data is None:
                node_counter +=1
                child_node = Node(node_counter,np.array(temp_data),current_root,action,0)
            #print(child_node.node_no)
            
                if child_node.data.tolist() not in seen:
                    node_q.append(child_node)
                    #print("child node appended")
                    seen.append(child_node.data.tolist())
                    visited.append(child_node)
                    #print("child appended to seen")
                    if (child_node.data.tolist() == goal_node.tolist()):
                        #print("Goal reached: ",child_node.data)
                        return child_node, seen, visited
    return (None, None, None)

    
    
def get_initial():
    initial_state = list()
    i = 0
    while i <9:
        a = int(input("Enter the "+str(i+1) + " number: "))
        if (a<0 or a>8):
            print("Number must be between 0 and 8")
            continue
        if a not in initial_state:
            initial_state.append(a)
            i+=1
        else:
            print("input repeated, please enter another number")
    counter =0
    for elem in initial_state:
        if not initial_state[elem] == 0:
            check = initial_state[elem]
            for x in range(elem+1,9):
                if check < initial_state[x] or initial_state[x] == 0:
                    continue
                else:
                    counter +=1
    if not counter%2 == 0:
        print("Unsolvable Input")
        print("The program will now exit")
        exit(0)
    else:
        print("Input is valid")
        a = np.reshape(np.array(initial_state),(3,3))
        return a
    
def main():
    root = Node(0,get_initial(),None,None,0)
    goal, s, v = node_creation(root)
   
        
    if s==None:
        print("Invalid Input, node traversal stopped")
    else:
        printStates(trackback(goal))
        writeToFile(trackback(goal),s,v)
         
if __name__ == "__main__":
    main()