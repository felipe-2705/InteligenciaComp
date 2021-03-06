from typing import Sequence
import Graph
import random as rand
from copy import deepcopy, deepcopy
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
    def __init_population(self): 
        for i in range(self.__population_size):
            self.__population.append([]) ### cria um sequencia genetica vazia para a populaçao
            for j in range(self.graph.get_Vertexes_Number()):
                color =  rand.randint(1,self.__minimum_colors) ### gera aleatoriamente um gene entre um e o valor minimo de cores  
                self.__population[i].append(color) ### adiciona essa cor a sequencia genetica
    def reset(self):
        self.__population = []
        self.__generation = 0
    def get_Population(self):
        return self.__population
    def get_generation(self):
        return self.__generation
    def fitness(self,sequence_index):
        f = set(self.__population[sequence_index])
        return len(f)
    def conflict_pairs(self,Sequence):
        conflict =  []
        for i in range(len(Sequence)):
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
        Sequence =  self.__population[sequence_index]
        for i in range(self.graph.get_Vertexes_Number()):
            color_i = Sequence[i] ### cor atribuida ao vertece i na sequencia 
            for edge in self.graph.get_Vertex_Edges(i):
                if color_i == Sequence[edge]: ### se a cor do vertice for igual a de um de seus vertices adjacentes 
                    return False 
        return True 
    def __expected_Observations(self):
        ### calculando probabilidades de cada sequencia 
        f = []
        f_sum = 0
        for sequence_index in range(self.__population_size):
            conflict =  self.conflict_pairs(self.__population[sequence_index])
            f.append(self.fitness_Evaluation(conflict))
            f_sum += f[sequence_index]
        if f_sum == 0:
            f = [0]*self.__population_size
            return f
        for sequence_index in range(self.__population_size):
            f[sequence_index] = f[sequence_index]/f_sum
            f[sequence_index] = f[sequence_index]*self.__population_size
        return f
    ### função de crossover proposta no artigo 
#    def __crossover(self, sequence_1, sequence_2):
#        new = []
#        new.append(deepcopy(sequence_1))
#        new.append(deepcopy(sequence_2))
#        p =  rand.uniform(0,1)
#        if p > self.__probability_Crossover:
#            return 
#        conflicts_1 =  self.conflict_pairs(new[0])
#        conflicts_2 = self.conflict_pairs(new[1])
#        for pair in conflicts_1:
#            if new[0][pair[1]] == new[0][pair[0]]: ### verifica se os pares ainda estão conflitando 
#                new[0][pair[1]] += 1 ### soma 1 na posiçao conflitante da sequencia 
#        for pair in conflicts_2:
#            if new[1][pair[1]] == new[1][pair[0]]: ## verifica se os pares ainda estão conflitando 
#                new[1][pair[1]] += 1 ### soma 1 na posiçao conflitante da sequencia
#        return new 
    def update_Population(self,new_sequence):
        conflicts = self.conflict_pairs(new_sequence)
        new_sequence_FE = self.fitness_Evaluation(conflicts)
        expected_ob = self.__expected_Observations()
        worst = 0     
        for index in range(len(expected_ob)):
            if expected_ob[index] > expected_ob[worst]:
                worst = index
        conflicts_worst = self.conflict_pairs(self.__population[worst])
        worst_FE =  self.fitness_Evaluation(conflicts_worst)
        if  new_sequence_FE < worst_FE:
            self.__population[worst] = new_sequence
            return True
        else: 
            return False
    ### cross over proposta por mim 
    def __crossover(self, sequence_1, sequence_2):
        new = []
        new.append(deepcopy(sequence_1))
        new.append(deepcopy(sequence_2))
        p =  rand.uniform(0,1)
        if p > self.__probability_Crossover:
            return 
        conflicts_1 =  self.conflict_pairs(new[0])
        conflicts_2 = self.conflict_pairs(new[1])
        for pair in conflicts_1:
             if new[0][pair[1]] == new[0][pair[0]]: ## verifica se ainda são conflitantes 
               color = new[0][pair[1]] 
               if color == new[1][pair[1]]:
                   new[0][pair[1]] += 1 ### soma 1 na posiçao conflitante da sequencia 
               else:
                   new[0][pair[1]] =  new[1][pair[1]] ### a posiçao conflitante recebe a mesma cor que esta na sequence parceira
        for pair in conflicts_2:
            if new[1][pair[1]] == new[1][pair[0]]:
                color = new[1][pair[1]] 
                if color == new[0][pair[1]]:
                    new[1][pair[1]] += 1 ### soma 1 na posiçao conflitante da sequencia 
                else:
                    new[1][pair[1]] =  new[0][pair[1]] ### a posiçao conflitante recebe a mesma cor que esta na sequence parceira
        return new 
    def __mutation(self,sequence):
        p = rand.uniform(0,1)
        new = deepcopy(sequence)
        if p > self.__probability_Mutation:
            return
        conflict = self.conflict_pairs(new)
        for pair in conflict:
            if new[pair[0]] == new[pair[1]]:
                if new[pair[0]] > 1:
                    new[pair[0]] = new[pair[0]] - 1
        return new 
    def execute(self): 
        self.__init_population()
#        print("Population[0]")
#        for s in self.__population:
#            print("\t"+ str(s))
        while self.__generation < self.__generation_Max:  
            expected_ob = self.__expected_Observations()
            b1 = 0
            b2 = 1
            for index in range(len(expected_ob)):
                if expected_ob[index] < expected_ob[b1]:
                    b2 = b1
                    b1 = index
                elif (index != 0)and (expected_ob[index] < expected_ob[b2]):
                    b2 = index
#            print("best1 = " + str(self.__population[b1]))
#            print("best2 = " + str(self.__population[b2]))
            new = self.__crossover(self.__population[b1],self.__population[b2]) ### cruza as duas melhores sequencias
            if new is not None:
#                print("New Sequences:")
#                print("\t"+str(new[0]))
#                print("\t"+str(new[1]))
                mutated1 = self.__mutation(new[0])
                if mutated1 is not None:
                    new[0] = mutated1
#                    print("\tMutated new 0:")  
#                    print("\t\t"+str(new[0]))
                mutated2 = self.__mutation(new[1])
                if mutated2 is not None:
                    new[1] = mutated2
#                    print("\tMutated new 1:")  
#                    print("\t\t"+str(new[1]))
            else:
                new = [[],[]]
                mutated1 = self.__mutation(self.__population[b1])
                mutated2 = self.__mutation(self.__population[b2])
#                print("Mutated Population:")
                if mutated1 is not None:
                    new[0] = mutated1
#                    print("\t"+str(new[0]))
                if mutated2 is not None:
                    new[1]= mutated2
#                    print("\t"+str(new[1]))
            if new[0] is not None and (new[0] != []):
                self.update_Population(new[0])
            if new[1] is not None and (new[1] != []):
                self.update_Population(new[1])
            self.__generation += 1
#            print("Population["+str(self.__generation)+"]:")
#            for s in self.__population:
#                print("\t"+ str(s))
            for index in range(self.__population_size):
                if self.is_Objetive(index):
                    return self.__population[index]


