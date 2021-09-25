import Genetic_algorithm as AG 
import Graph 

graph_file            = "./graphs/queen6_6.col"
probability_crossover = 0.5
probability_mutation  = 0.7
population_size       = 70
generation_max        = 2000
min_colors            = 7
iterations            = 100

g = Graph.read_graph_from_file(graph_file)
ag =  AG.AG_Coloring_Graph(g,probability_crossover,probability_mutation,generation_max,population_size,min_colors)

solutions = []
optimum = []
f1      = []
f2      = []
i = 0 
generations = 0
while i < iterations:
    print(i)
    pr = ag.execute()

    print("best sequence:" + str(pr))
    print("final population")
    population =  ag.get_Population()
    for s in range(population_size):
        print("\t"+str(population[s]))
    for sequence in range(population_size):
        if ag.is_Sequence_Valid(sequence):
            f = ag.fitness(sequence)
            if f == min_colors:
                optimum.append(sequence)
            elif f == min_colors +1:
                f1.append(sequence)
            elif f == min_colors + 2:
                f2.append(sequence)
            solutions.append(sequence)
    generations += ag.get_generation()
    ag.reset()
    i += 1

string = str(generations/iterations)+ " | " + str(min_colors) +" | "+str(len(optimum)) +" | " +str(len(f1)) + " | " + str(len(f2))  + " | " + str(len(solutions))
print(string)   
print(str(len(set(optimum))))