import Graph
import random as rand
from copy import deepcopy, deepcopy
############## Graph file ################################
graph_file =  "queen6_6.col"
graph_path = "./graphs"
graph_file_path = graph_path + "/" + graph_file

############## PARTICLE DEFINITION #######################
class Particle: 
    def __init__(self):
        self.__Position = []
        self.__Best_Position = []
        self.__Best_fitness = float("inf")
        self.__Velocity = []
    def start_position(self,size,best_coloring):
        self.__Size = size
        self.__Best_Coloring = best_coloring 
        for i in range(size):
            self.__Position.append(rand.randint(0,best_coloring-1))
            self.__Velocity.append(0.0)
            self.__Best_Position.append(self.__Position[i])
    def update_velocity(self,v_weight,c1,c2,g_best):
        r1 = rand.uniform(0,1)
        r2 = rand.uniform(0,1)
        g_best_position = g_best.get_position()
        for i in range(self.__Size):
            self.__Velocity[i] = round(v_weight * self.__Velocity[i]) + round(c1 * r1 *(self.__Best_Position[i] - self.__Position[i])) + round(c2*r2*( g_best_position[i] - self.__Position[i] ))
    def __inverse_velocity(self,pos):
        self.__Velocity[pos] = (-1)*self.__Velocity[pos]
    def update_position(self):
        for i in range(self.__Size):
            sum = self.__Position[i] + self.__Velocity[i]
            self.__Position[i] = abs(sum % self.__Best_Coloring)
            if (sum > self.__Best_Coloring) or (sum < 0): 
                self.__inverse_velocity(i)
    def get_position(self):
        return self.__Position
    def get_Best_position(self):
        return self.__Best_Position
    def get_Best_fitness(self):
        return self.__Best_fitness
    def set_position(self,position):
        self.__Position = position
    def set_velocity(self, velocity):
        self.__Velocity = velocity
    def set_Best_fitness(self,fitness):
        self.__Best_fitness = fitness
    def set_Best_position(self,position):
        self.__Best_Position = position

################## PARTICLE SWARM OPTIMIZATION ###############################
class PSO:
    def __init__(self,graph,best_coloring,evaluation_value,v_weight,c1,c2):
        self.__Graph = graph
        self.__Best_Coloring =  best_coloring
        self.__Evaluation_Value = evaluation_value
        self.__V_Weight = v_weight
        self.__c1 = c1
        self.__c2 = c2
        self.__Best_Particle = [] 
        self.__Best_fitness  = float("inf")
        self.__iteration = 0
    def init_particles(self,particles_number):
        self.__Particles = []
        for i in range(particles_number):
            self.__Particles.append(Particle())
            self.__Particles[i].start_position(self.__Graph.get_Vertexes_Number(),self.__Best_Coloring)
    def conflict_pairs(self,Position):
        conflict_vertixes = 0
        conflict_edges    = 0
        for i in range(len(Position)):
            flag = False
            for edge in self.__Graph.get_Vertex_Edges(i):
                if Position[i] == Position[edge]:
                    if edge > i: ## evita a mesma aresta de ser contada duas vezes  
                        conflict_edges +=1
                    flag = True
            if flag == True:
                conflict_vertixes += 1
        return conflict_vertixes, conflict_edges 
    def fitness(self,particle):
        conflict_vertixes, conflict_edges = self.conflict_pairs(particle.get_position())
        value = (self.__Evaluation_Value * conflict_vertixes) + conflict_edges 
        return value
    def get_particles(self):
        return self.__Particles
    def get_Best_particle(self):
        return self.__Best_Particle
    def get_iteration(self):
        return self.__iteration
    def reset (self):
        self.__Particles     = []
        self.__Best_Particle = [] 
        self.__Best_fitness  = float("inf")
        self.__iteration     = 0
    def execute(self,particles_number,iterations):
        self.init_particles(particles_number)
        while self.__iteration < iterations:
            for i in range(particles_number):
                fitness = self.fitness(self.__Particles[i])
                if fitness < self.__Particles[i].get_Best_fitness():
                    self.__Particles[i].set_Best_fitness(fitness)
                    self.__Particles[i].set_Best_position(self.__Particles[i].get_position())
                if fitness < self.__Best_fitness:
                    self.__Best_Particle = self.__Particles[i]
                    self.__Best_fitness = fitness
            if self.__Best_fitness == 0 :
                return self.__Best_Particle
            for particle in self.__Particles:
                particle.update_velocity(self.__V_Weight, self.__c1,self.__c2,self.__Best_Particle)
                particle.update_position()
            self.__iteration +=1
    def mutation(self, Particle,probability_mutation):
        p = rand.uniform(0,1)
        conflict = []
        if p < probability_mutation: 
            pos = Particle.get_position()
            for i in range(len(pos)):
                for edge in self.__Graph.get_Vertex_Edges(i):
                    if pos[i] == pos[edge]:
                        if [edge,i] not in conflict : ## evita colocar a mesma aresta duas vezes  
                            conflict.append([i,edge])             
            conf = conflict.pop(0)
            x = abs(pos[conf[0]] - 1)
            pos[conf[0]] =  x
            c = conf[0]
            while len(conflict) != 0:
                while True:
                    conf = conflict.pop(0)
                    if conf[0] != c or len(conflict) == 0:
                        break
                if len(conflict) == 0:
                    break   
                x = abs(pos[conf[0]] - 1)
                pos[conf[0]] =  x
                c = conf[0]           
            fitness = self.fitness(Particle)
            if fitness < Particle.get_Best_fitness():
                Particle.set_Best_fitness(fitness)
                Particle.set_Best_position(pos)
            if fitness < self.__Best_fitness:
                self.__Best_fitness = fitness
                self.__Best_Particle = Particle
            if self.__Best_fitness == 0 :
                return self.__Best_Particle
            Particle.update_velocity(self.__V_Weight, self.__c1,self.__c2,self.__Best_Particle)
    def execute_hybrid(self,particles_number,iterations,probability_mutation):
        self.init_particles(particles_number)
        while self.__iteration < iterations:
            for i in range(particles_number):
                fitness = self.fitness(self.__Particles[i])
                if fitness < self.__Particles[i].get_Best_fitness():
                    self.__Particles[i].set_Best_fitness(fitness)
                    self.__Particles[i].set_Best_position(self.__Particles[i].get_position())
                if fitness < self.__Best_fitness:
                    self.__Best_Particle = self.__Particles[i]
                    self.__Best_fitness = fitness
            if self.__Best_fitness == 0 :
                return self.__Best_Particle
            for particle in self.__Particles:
                particle.update_velocity(self.__V_Weight, self.__c1,self.__c2,self.__Best_Particle)
                particle.update_position()
                self.mutation(particle,probability_mutation)
            
            self.__iteration +=1
Evaluetion_value = 1
best_coloring = 7
v_weight   = 0.5
coeficient_local = 0.6
coeficient_global= 0.7
iterations = 150
probability_mutation = 0.6
graph = Graph.read_graph_from_file(graph_file_path)

p = PSO(graph,best_coloring,Evaluetion_value,v_weight,coeficient_local,coeficient_global)

b = p.execute_hybrid(200,iterations,probability_mutation)
if b is not None:
    print(b.get_position())
print(p.get_iteration())
print("BEST PARTICLE")
print(p.get_Best_particle().get_position())
print(p.get_Best_particle().get_Best_fitness())
print("Particles")
particles = p.get_particles()
for i in range(200):
    print(particles[i].get_position())