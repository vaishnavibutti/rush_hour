import numpy as np
import sys
from z3 import * # load z3 library

ans=[]
def move_right(table,i,j,n):
	
    if not(j < n-1):
        return False
    if (table[i][j-1]!=table[i][j]):
    	return False
    sr=Solver()
    v=table[i][j+1]
    if v==0:
        table[i][j-1]=0
        table[i][j+1]=table[i][j]
        ans.append(f"{i},{j}")
        return True
    elif v==-1 or v==3:
        return False
    elif v==2 :
        sr.add(Or(move_up(table,i-1,j+1,n),move_down(table,i+1,j+1,n)))
    elif v==1 :
        sr.add(move_right(table,i,j+2,n))

    if sr.check()==sat:
        table[i][j-1]=0
        table[i][j+1]=table[i][j]
        ans.append(f"{i},{j}")
        return True
    else:
        return False  



def move_left(table,i,j,n):
    if not(j > 0):
        return False
    if (table[i][j+1]!=table[i][j]):
    	return False
    sl=Solver()
    v=table[i][j-1]
    if v==0:
        table[i][j+1]=0
        table[i][j-1]=table[i][j]
        ans.append(f"{i},{j}")
        return True
    elif v==-1 or v==3:
        return False
    elif v==2:
        sl.add(Or(move_up(table,i-1,j-1,n),move_down(table,i+1,j-1,n)))
    elif v==1 :
        sl.add(Implies((table[i][j-1] == 1),move_left(table,i,j-2,n)))

    if sl.check()==sat:
        table[i][j+1]=0
        table[i][j-1]=table[i][j]
        ans.append(f"{i},{j}")
        return True
    else:
        return False 

def move_up(table,i,j,n):
    if not(i > 0):
        return False
    if (table[i+1][j]!=table[i][j]): #or table[i-1][j] == table[i][j] is true then move up(table,i-1,j,n)
    	return False
    su=Solver()
    v=table[i-1][j]
    if v==0:
        table[i+1][j]=0
        table[i-1][j]=table[i][j]
        ans.append(f"{i},{j}")
        return True
    elif v==-1 or v==3:
        return False
    elif v==1 :
        su.add(Or(move_right(table,i-1,j+1,n),move_left(table,i-1,j-1,n)))
    elif v==2:
        su.add(move_up(table,i-2,j,n))

    if su.check()==sat:
        table[i+1][j]=0
        table[i-1][j]=table[i][j]
        ans.append(f"{i},{j}")
        return True
    else:
        return False 

def move_down(table,i,j,n):
    if not(i < n-1):
        return False
    if (table[i-1][j]!=table[i][j]):
    	return False
    sd=Solver()
    v=table[i+1][j]
    if v==0:
        table[i-1][j]=0
        table[i+1][j]=table[i][j]
        ans.append(f"{i},{j}")
        return True
    elif v==-1 or v==3:
        return False
    elif v==1 :
        sd.add(Or(move_right(table,i+1,j+1,n),move_left(table,i+1,j-1,n)))
    elif v==2:
        sd.add(move_down(table,i+2,j,n))

    if sd.check()==sat:
        table[i-1][j]=0
        table[i+1][j]=table[i][j]
        ans.append(f"{i},{j}")
        return True
    else:
        return False 
   

file = open(sys.argv[1],'r')
count=0
vertical_pos=[]
horizontal_pos=[]
mine_pos=[]
for l in file:
    l=l.strip("\n")
    num=l.split(",")
    num=np.array(num,dtype=int)
    count=count+1
    if(count==1):
        n=num[0]
        table= np.zeros((n,n),dtype=int)
        moves=num[1]
    elif(count==2):
        red_pos=np.array([num[0],num[1]],dtype=int)
        table[num[0]][num[1]]=3 # 3 for red
        table[num[0]][num[1]+1]=3
    else:
        o=num[0]
        if(o==0):
            vertical_pos.append(np.array([num[1],num[2]],dtype=int))
            table[num[1]][num[2]]=2 # 2 for vertical
            table[num[1]+1][num[2]]=2
        elif(o==1):
            horizontal_pos.append(np.array([num[1],num[2]],dtype=int))
            table[num[1]][num[2]]=1 # 1 for horizontal
            table[num[1]][num[2]+1]=1
        else:
            mine_pos.append(np.array([num[1],num[2]],dtype=int))
            table[num[1]][num[2]]=-1 # -1 for mines

vertical_pos=np.array(vertical_pos)
horizontal_pos=np.array(horizontal_pos)
mine_pos=np.array(mine_pos)


#print(table,'\n\n')


for k in range(red_pos[1]+1,n-1):
	
    if(move_right(table,red_pos[0],k,n)):
    	#print(table,'\n') 
    	continue
    else:
    	print("unsat")
    	sys.exit()
    	
if(len(ans)<= moves):   
    for a in ans:
        print(a)
else:
    print("unsat")
    sys.exit()