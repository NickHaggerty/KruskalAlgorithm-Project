#   Nick Haggerty Assignment #1
#   Kruskals Algorythm
#   11/16/2022



import numpy as np

class kruskalClass:
    
    def mergesort(self, a):
        #while the array is bigger then a single digit, continue (thanks to if statement and recursion)
        if len(a)>1:
            #cut the array in half, set left and right pointers
            mid = len(a)//2
            Left = a[:mid]
            Right = a[mid:]

            #recursive call to continue splitting each side until len(a)<1
            self.mergesort(Left)
            self.mergesort(Right)

            #by now each array is size 1, so its time to merge, set base variables
            i=0
            j=0
            aInd = 0;
            #i pointer is beginning of left array, j is pointing to start of left array, go until they are both at the end
            while i < len(Left) and j < len(Right):
                #check if i value or j value is bigger
                if Left[i] <= Right[j]:
                    #if right is bigger, add it
                    a[aInd] = Left[i]
                    i += 1
                else:
                    #else, left is bigger, so add it
                    a[aInd] = Right[j]
                    j += 1
                aInd += 1

            #some values can be missed from either array, so this is a last check to make sure the last values are added
            while i < len(Left):
                a[aInd] = Left[i]
                i += 1
                aInd += 1
                
            #each side needs this last check
            while j < len(Right):
                a[aInd] = Right[j]
                j += 1
                aInd += 1

        #return the sorted array
        return a

    
    def makeUnionFind(self, N):
        #build dict
        unionSet = {}
        #for every vertex, add it to the dictionary, and set it to point to itself
        for i in range(N):
            unionSet[i] = np.array([i, 1])

        #return the filled dict for union
        return unionSet
       

    
    def find(self, u,v):
        #set key to equal beginning
        key = v
        #while the key doesnt equal value in the dictionary, continue down the path. this is finding the root node
        while key != u[key][0]:
            key = u[key][0]

        #return key, which is root node
        return key
        

    
    def union(self, u_in,s1,s2):
        #set variables
        u_out = u_in

        #if each vertex shares a root node, adding it will create a cycle, so continue with no changes
        if self.find(u_out, s1) == self.find(u_out, s2):
            return u_out

        #check to see if s1 is not a root node, if not...
        if u_out[s1][0] != s1:

            #grab its root node, and create variables to iterate from s1 to root...
            #essentially this function reverses the path so that the tail becomes the root, this ensures
            #that no edge will be overwritten when making a union. 
            root = self.find(u_out,s1)
            i = s1
            j = 0
            prev = 0
            #while we are not at the root, step
            while i != root:
                #save current value
                j = u_out[i][0]
                #and change the current value to point to the last
                u_out[i][0] = i
                #save the previous value so that we can make the root once done
                prev = i
                #iterate to next vertex
                i = j

            #once at the end, the last node (tail) will be pointing forward still, this sets it to equal itself, making it a root
            u_out[i][0] = prev
            
        #this is essentially the same exact thing as above, except on s2 instead of s1. 
        elif u_out[s2][0] != s2:
            root = self.find(u_out,s2)
            i = s2
            j = 0
            prev = 0
            while i != root:
                j = u_out[i][0]
                u_out[i][0] = i
                prev = i
                i = j
            u_out[i][0] = prev


        
        #finally, we look to bind the vertices to the root that has the highest number of incoming edges. 
        if u_out[s1][1] <= u_out[s2][1]:
            #connect edges
            u_out[s1][0] = u_out[s2][0]
            #add to incoming edge count
            u_out[s2][1] += 1
        else:
            #connect edges
            u_out[s2][0] = u_out[s1][0]
            #add to incoming edge count
            u_out[s1][1] += 1

        #return our dictionary with the new union
        return u_out


    def buildIndexDict(self, A):
        #Create beginning variables
        posDict = {}
        a = []
        k = 0
        l = 0
        #iterate through A
        for i in A:
            l = 0
            for j in i:
                if j != 0:
                    #add weight to an array
                    a.append(j)
                    #for node of weight KEY, value inside are the coordinates
                    posDict[j] = np.array([k,l])
                l += 1
            k += 1
        #return weight array, and union Dictionary linked to itself
        return a,posDict


    def MSTConverter(self, output, mst):
        #set beginning variables, X and Y being used as coordinates
        out = output
        x=0
        y=0
        #iterate through all coordinates
        for i in out:
            y=0
            for j in i:
                #if the [x,y] is not in MST, set it to 0
                if [x,y] not in mst and [y,x] not in mst:
                    out[x][y] = 0
                y+=1
            x+=1
        #return MST adjacency matrix
        return out


    def findMinimumSpanningTree(self, A):
        #set output matrix to alter
        output = A
        #build an empty dictionary to keep x and y positions of each edge, also build an array of all edges
        a,posDict = self.buildIndexDict(A)

        #call mergesort on array of edges to get weights in order
        b = self.mergesort(a)
        #calculate the number of edges
        N = len(b)
        #create the union dictionary with each node pointing to itself
        u = self.makeUnionFind(N)

        #iterate once for each edge weight
        for i in range(len(posDict)):
            #union nodes at weight i, i being weights in ascending order
            u = self.union(u, posDict[b[i]][0], posDict[b[i]][1])

        #create empty 2d 
        mst = []
        #for every edge in the graph u, if the edge is present in unionDict, it is part of the MST...
        for edge in u:
            if edge != u[edge][0]:
                #so add the coordinates of the edge to the MST array
                mst.append([edge, u[edge][0]])

        #convert the output adjacency matrix to be the MST, then return it
        return self.MSTConverter(output, mst)
        

