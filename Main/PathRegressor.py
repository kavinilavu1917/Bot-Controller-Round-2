from collections import defaultdict
from datetime import datetime
import numpy as np 

'''
This Class is used to find a non-correlated path between bot place and destination place
This is functioning with 
        "Directed graph shortest path algorithms"

Functioning Machanism:

    => Design path direction:

        $ In delivery time dest place will be 4 index position , then Returning time, 
          dest place have 1 index position.

          so , we used "Manhattan Distance" formula to predict shortest dest place

        $ we use a algorithm thats gives any start postion and any destination postion
          that leads to organize a submatrix with
            (x1, y1)  and (x2,y2)

            row = | x1-x2 |
            col = | y1-y2 |

        $ That submatrix predict direction of submatrix like a directed graph
          That Directions are predicted with "PathStructure" common value
          Thats shown in a GUI.
          Thats holds all destination place and bot place belongs to 1
          empty places are 0

        $ So, its predict a directed graph using 1, 0 values

    => predict path
        $ This Design path graph is sends to path prediction algorithm to get a
          path

        $ In some case,
              more than one bot holds a next position of a bot are same

              So, we are initialize a temp path structure of next postion with value 1
              to predict random checking with a path

            Its leads to give a non-correlated path  

'''

class PathRegressor():
    class Graph:  
        def __init__(self, vertices):
            self.V = vertices   
            self.path=[]      
            self.graph = defaultdict(list)
        def addEdge(self, u, v,rev=False):
            if rev:
                for i in sorted(v,reverse=True):
                    self.graph[u].append(i)  
            else:
                for i in v:
                    self.graph[u].append(i)
        def printAllPathsUtil(self, u, d, visited, path):
            visited[u]= True
            path.append(u)
            if u == d:
                self.path=path
                return 1
            else:
                for i in self.graph[u]:
                    if visited[i]== False:
                        if self.printAllPathsUtil(i, d, visited, path)==1:
                            return 1
            path.pop()
            visited[u]= False 
        def printAllPaths(self, s, d):
            visited =[False]*(self.V)
            path = []
            self.printAllPathsUtil(s, d, visited, path)


    def Design_path(self,path_structure, bot_point, dest_point,m=0,rev=False):
        g=self.Graph(14*14)
        start=14*bot_point[0] + bot_point[1]
        end  =14*dest_point[0] + dest_point[1]
        path_structure = np.array(path_structure)
        path_structure[bot_point[0],bot_point[1]]=0
        path_structure[dest_point[0],dest_point[1]]=0
        path_numbers   = np.arange(14*14).reshape(14,14)
        index_position = np.array([[[i,j] for j in range(14)] for i in range(14)]).reshape(14*14,2)
        x=min(dest_point[0],bot_point[0])
        y=min(dest_point[1],bot_point[1])
        x1=max(dest_point[0],bot_point[0])
        y1=max(dest_point[1],bot_point[1])
        bot_point=[x,y]
        dest_point=[x1,y1]
        if bot_point[0]>m-1 and bot_point[1]>m-1:
            test_struct = path_structure[bot_point[0]-m:dest_point[0]+m+1, bot_point[1]-m:dest_point[1]+m+1]
            test_number = path_numbers[bot_point[0]-m:dest_point[0]+m+1, bot_point[1]-m:dest_point[1]+m+1]
        elif bot_point[0]>m-1:
            test_struct = path_structure[bot_point[0]-m:dest_point[0]+m+1, :dest_point[1]+m+1]
            test_number = path_numbers[bot_point[0]-m:dest_point[0]+m+1, :dest_point[1]+m+1]
        elif bot_point[1]>m-1:
            test_struct = path_structure[:dest_point[0]+m+1, bot_point[1]-m:dest_point[1]+m+1]
            test_number = path_numbers[:dest_point[0]+m+1, bot_point[1]-m:dest_point[1]+m+1]
        else:
            test_struct = path_structure[:dest_point[0]+m+1, :dest_point[1]+m+1]
            test_number = path_numbers[:dest_point[0]+m+1, :dest_point[1]+m+1]
        row,col = test_number.shape

        path_structure=path_structure.reshape(14*14)

        g.addEdge(test_number[0,0],[i for i in [test_number[0,0]+1,test_number[0,0]+14] if path_structure[i]!=1],rev)
        g.addEdge(test_number[row-1,0], [i for i in [test_number[row-1,0]-14, test_number[row-1,0]+1] if path_structure[i]!=1],rev)
        g.addEdge(test_number[0,col-1], [i for i in [test_number[0,col-1]-1, test_number[0,col-1]+14] if path_structure[i]!=1],rev)
        g.addEdge(test_number[row-1,col-1], [i for i in [test_number[row-1,col-1]-1, test_number[row-1,col-1]-14] if path_structure[i]!=1],rev)

        for e in test_number[1:-1,0]:
            g.addEdge(e, [j for j in [e+1,e-14,e+14]if path_structure[j]!=1],rev)
        for e in test_number[1:-1,-1]:
            g.addEdge(e, [j for j in [e-1,e-14,e+14] if path_structure[j]!=1],rev)
        for e in test_number[0,1:-1]:
            g.addEdge(e,[j for j in [e-1,e+1,e+14] if path_structure[j]!=1],rev)
        for e in test_number[-1,1:-1]:
            g.addEdge(e,[j for j in [e-1,e+1,e-14] if path_structure[j]!=1],rev)

        try:
            for e in test_number[1:-1, 1:-1].reshape((row-2)*(col-2)):
                g.addEdge(e,[j for j in [e-1,e+1,e-14,e+14] if path_structure[j]!=1],rev)
        except:
            pass

        g.printAllPaths(start,end)
        return [index_position[i] for i in g.path]

    def manhatten_distance(self,a,b):
        d=10000
        best=[]
        for i in b:
            distance = abs(a[0]-i[0])+abs(a[1]-i[1])
            if distance<d:
                d=distance
                best=i
        return best

    def Predict(self,path_structure, bot_point, dest_point_array,second_check=True):
        self.path_structure = path_structure
        a=[]
        b=[]
        m=10000
        m_val=0
        while m==10000:
            i=self.manhatten_distance(bot_point,dest_point_array)
            a.append(self.Design_path(self.path_structure ,bot_point,i,m_val,0))
            if m>len(a[-1]) and len(a[-1])!=0:
                b=a[-1]
                m=len(b)
            a.append(self.Design_path(self.path_structure,bot_point,i,m_val,1))
            if m>len(a[-1]) and len(a[-1])!=0:
                b=a[-1]
                m=len(b)
            m_val+=1
        if len(b)>2 and second_check:
            old    = list(b[0])
            start  = list(b[1])
            self.path_structure[old[0]][old[1]]=0
            second = self.Predict(self.path_structure,start,dest_point_array,False)[1]
            if list(old)==list(second):
                self.path_structure[old[0]][old[1]]=1
                self.path_structure[start[0]][start[1]]=1
                return self.Predict(self.path_structure,old,dest_point_array,True)
        return b
        

'''

pattern =[
    [0]*14,
    [0]*14,
    [0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
    [0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
    [0]*14,
    [0]*14,
    [0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
    [0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
    [0]*14,
    [0]*14,
    [0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
    [0]*2 + [1]*2 + [0]*2 +[1]*2 +[0]*2 + [1]*2 +[0]*2,
    [0]*14,
    [0]*14
]

pattern[9][0]=1
for i in PathRegressor().Predict(pattern,(9,0),[(2,2),(2,3),(3,2),(3,3)]):
    print (i,end='->')



###############################################################################################
# [9 0]->[8 0]->[8 1]->[7 1]->[7 0]->[6 0]->[6 1]->[5 1]->[5 0]->[4 0]->[4 1]->[4 2]->[3 2]-> #
###############################################################################################

'''