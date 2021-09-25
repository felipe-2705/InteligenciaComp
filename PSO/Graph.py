import csv
###### VERTEX DEFINITION SECTION ##################################
class Vertex:
    def __init__(self,value,edge):
        ## value valor atribuido ao Vertex 
        ## Edges uma lista de indexadores para os outros Vertex com quem possui edges
        self.__Value = value
        self.__Edges = edge  
    def get_Value(self):
        return self.__Value
    def get_Edges(self):
        return self.__Edges
    def exist_Edge(self, Vertex_index):
        return Vertex_index in self.__Edges
    def set_Value(self,newvalue):
        self.__Value = newvalue
    def insert_Edge(self, Vertex_index):
        self.__Edges.append(Vertex_index)
    def remove_Edge(self, Vertex_index):
        if Vertex_index in self.__Edges:
            self.__Edges.pop(Vertex_index)


######## DEFINE GRAPH ###################
class Graph:
    def __init__(self):
    ## Vertex é uma lista de vertices inicialmente vazia
        self.__Vertex = []
        self.__Edges_number = 0
    def insert_Vertex(self, vertex):
        self.__Vertex.append(vertex)
        return True
    def get_Vertex_Value(self,vertex_index):
        return self.__Vertex[vertex_index].get_Value()
    def set_Vertex_Value(self,vertex_index,value):
        if not self.exist_Vertex(vertex_index):
            return False
        self.__Vertex[vertex_index].set_Value(value)
        return True
    def get_Vertexes_Number(self):
        return len(self.__Vertex)
    def exist_Vertex(self,vertex_index):
        if len(self.__Vertex) - 1 < vertex_index:
            return False
        return True
    def get_Vertex_Edges(self,vertex_index):
        return self.__Vertex[vertex_index].get_Edges()
    def exist_Edge(self,vertex_index1,vertex_index2):
        return vertex_index1 in self.__Vertex[vertex_index2].get_Edges()
    def insert_Edge(self,vertex_index1,vertex_index2):
        if not(self.exist_Vertex(vertex_index1) and self.exist_Vertex(vertex_index2)):
            print("VERTEX_INDEX " + str(vertex_index1) +"OR "+ str(vertex_index2) + " DOES NOT EXIST")
            return False
        if self.exist_Edge(vertex_index1,vertex_index2):
            return True
        self.__Vertex[vertex_index1].insert_Edge(vertex_index2)
        self.__Vertex[vertex_index2].insert_Edge(vertex_index1)
        self.__Edges_number += 1
        return True
    def remove_Edge(self,vertex_index1,vertex_index2):
        if not self.exist_Edge(vertex_index1,vertex_index2):
            return False
        self.__Vertex[vertex_index1].remove_Edge(vertex_index2)
        self.__Vertex[vertex_index2].remove_Edge(vertex_index1)
        self.__Edges_number -= 1
    def get_Edge_Number(self):
        return self.__Edges_number


#############################################  CREATE GRAPH FROM FILE #########################################
def read_graph_from_file(graph_file_path):
    print("READING FILE AND BUILDING GRAPH ..... ")
    graph = Graph()
    with open(graph_file_path, "r") as file: 
        line = file.readline()
        line = line.split()
        vertex = int(line[2])
        edge = int(line[3])
        ### insere Vertexs no grafo
        i= 0
        for i in range(vertex):
            v =  Vertex(0,[])   #### Todos os vertices vao iniciar com a mesma cor 0
            graph.insert_Vertex(v)
        # insere arestas 
        while 1:
            line = file.readline()
            if line == "":
                break
            line = line.split()
            vertex_index1 = int(line[1])
            vertex_index2 = int(line[2])
            #print(vertex_index1-1, vertex_index2-1) ### debug
            if not graph.insert_Edge(vertex_index1-1,vertex_index2-1):
                print("ERROR INSERTING EDGE " + str(vertex_index1-1) + " " + str(vertex_index2-1))
                return 
    print("GRAPH BUILDING COMPLETED!!!")
    return graph
