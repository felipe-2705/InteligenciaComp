import Graph
import statistics as st
import matplotlib.pyplot as plt
import random as rand

############## Graph file ##########################
graph_file =  "queen5_5.col"
graph_path = "./graphs"
graph_file_path = graph_path + "/" + graph_file

################################## AG CLASS DEFINITION ###################################
class AG_Coloring_Graph:
    def __init__(self,graph,probability_crossover, probability_mutation,generation_max,population_size,colors):
        self.graph = graph
        self.__population = [] ### é uma lista de sequencias geneticas 
        self.__probability_Crossover = probability_crossover ### probabilidade de cruzamento dos dois melhores membros de uma população
        self.__probability_Mutation = probability_mutation ### probabilidade de os dois inviduos resultantes do cruzamento terem uma mutação 
        self.__generation = 0 ### a geração atual da população
        self.__generation_Max = generation_max  ## para o caso de querer terminar com um numero maximo de geraçoes 
        self.__population_size = population_size #### tamanho da população
        self.__minimum_colors =  colors ## quantidade minima de cores necessaria para colorir o grafo em questão 
        self.__init_population()
    def __init_population(self): 
        for i in range(self.__population_size):
            self.__population.append([]) ### cria um sequencia genetica vazia para a populaçao
            for j in range(self.graph.get_Vertexes_Number()):
                color =  rand.randint(1,self.__minimum_colors) ### gera aleatoriamente um gene entre um e o valor minimo de cores  
                self.__population[i].append(color) ### adiciona essa cor a sequencia genetica
    def fitness(self,sequence_index):
        return max(self.__population[sequence_index])
    def __conflict_pairs(self,Sequence):
        conflict =  []
        for i in range(Sequence):
            for edge in self.graph.get_Vertex_Edges(i):
                if Sequence[i] == Sequence[edge]:
                    if not [edge,i] in conflict: #### evita que o mesmo par seja inserido duas vezes 
                        conflict.append([i,edge])
        return conflict ### retorna uma lista de pares conflitantes de vertices 
    def fitness_Evaluation(self,conflict):
        return len(conflict)
    def is_Objetive(self,sequence_index):
        if (self.fitness(sequence_index) - self.__minimum_colors == 0) and self.is_Sequence_Valid(sequence_index):
            return True
        return False
    def is_Sequence_Valid(self,sequence_index):
        Sequence =  self._population[sequence_index]
        for i in range(self.graph.get_Vertexes_Number()):
            color_i = Sequence[i] ### cor atribuida ao vertece i na sequencia 
            for edge in self.graph.get_Vertex_Edges(i):
                if color_i == Sequence[edge]: ### se a cor do vertice for igual a de um de seus vertices adjacentes 
                    return False 
        return True 
    def expected_Observations(self):
        ### calculando probabilidades de cada sequencia 
        f = []
        f_sum = 0
        for sequence_index in range(self.__population):
            conflict =  self.__conflict_pairs(sequence_index)
            f.append(self.fitness_Evaluation(conflict))
            f_sum += f[sequence_index]
        for sequence_index in range(self.__population):
            f[sequence_index] = f[sequence_index]/f_sum
            f[sequence_index] = f[sequence_index]*self.__population_size
    ### função de crossover proposta no artigo 
    def crossover(self, sequence_1, sequence_2):
        new = []
        new.append(sequence_1[:])
        new.append(sequence_2[:])
        p =  rand.uniform(0,1)
        if p > self.__probability_Crossover:
            return 
        conflicts_1 =  self.__conflict_pairs(new[0])
        conflicts_2 = self.__conflict_pairs(new[1])
        for pair in conflicts_1:
            new[0][pair[1]] += 1 ### soma 1 na posiçao conflitante da sequencia 
        for pair in conflicts_2:
            new[1][pair[1]] += 1 ### soma 1 na posiçao conflitante da sequencia
        return new 
    ### cross over proposta por mim 
    def crossover(self, sequence_1, sequence_2):
        new = []
        new.append(sequence_1[:])
        new.append(sequence_2[:])
        p =  rand.uniform(0,1)
        if p > self.__probability_Crossover:
            return 
        conflicts_1 =  self.__conflict_pairs(new[0])
        conflicts_2 = self.__conflict_pairs(new[1])
        for pair in conflicts_1:
            color = new[0][pair[1]] 
            if color == new[1][pair[1]]:
                new[0][pair[1]] += 1 ### soma 1 na posiçao conflitante da sequencia 
            else:
                new[0][pair[1]] =  new[1][pair[1]] ### a posiçao conflitante recebe a mesma cor que esta na sequence parceira
        for pair in conflicts_2:
            color = new[1][pair[1]] 
            if color == new[0][pair[1]]:
                new[1][pair[1]] += 1 ### soma 1 na posiçao conflitante da sequencia 
            else:
                new[1][pair[1]] =  new[0][pair[1]] ### a posiçao conflitante recebe a mesma cor que esta na sequence parceira
        return new 
graph = Graph.read_graph_from_file(graph_file_path)
ag = AG_Coloring_Graph(graph,0.5, 0.1,1000,20,10)
