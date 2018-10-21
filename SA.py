import math
import random
import numpy
import time
import matplotlib.pyplot as plt

#Calculate the acceptance probability
def acceptanceProbability(energy, newEnergy, temperature):
    if (newEnergy < energy):
        return 1.0
    
    return math.exp((energy - newEnergy) / temperature)

def calculateEnergy(tour, cities):
	energy = 0

	for i in range(0, len(tour)):
		cidadeAtual = cities[tour[i]]

		if i+1 < len(tour):
			cidadeProx = cities[tour[i+1]]
		else:
			cidadeProx = cities[0]

		PosAtualX = cidadeAtual[0]
		PosAtualY = cidadeAtual[1]
		PosProxX = cidadeProx[0]
		PosProxY = cidadeProx[1]

		distanciaX = abs(PosAtualX - PosProxX)
		distanciaY = abs(PosAtualY - PosProxY)

		energy = energy + math.sqrt((distanciaX**2) + (distanciaY**2))

	return energy
# ========================  Fim das funcoes

# iniciando tempo de codigo
start_time = time.time()

# 15 cidades com pares de numeros aleatorios
# cities = [random.sample(range(100), 2) for x in range(15)];
cities = [[60, 200], [180, 200], [80, 180], [140, 180], [20, 60], [100, 160], [200, 160], [140,140],
[40, 120], [100, 120], [180, 100], [60, 80], [120, 80], [180, 60], [20, 40]]

# 15 numeros que representam 15 ordens de caminhos diferentes
tour = random.sample(range(15),15);

# Teste de distancia inicial para comparacao com GA
# tour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

best = tour

# set initial temp
temp = 10000

# Cooling rate
coolingRate = 0.003;

print("Initial solution distance")
print(str(calculateEnergy(best, cities)))

while temp > 1:
	# Iniciando novo tour
	novoTour = list(tour)

	# Dois numeros aleatorios de 0 a 15
	[tourPos1, tourPos2] = sorted(random.sample(range(15), 2))

	# Dando swap entre as cidades sorteadas (perturbacao da entrada)
	aux = novoTour[tourPos1]
	novoTour[tourPos1] = novoTour[tourPos2]
	novoTour[tourPos2] = aux

	# Capturando energia do sistema, ou seja, distancia entre os pontos
	energiaDoMelhor = calculateEnergy(best, cities)
	energiaAtual = calculateEnergy(tour, cities)
	energiaDoVizinho = calculateEnergy(novoTour, cities)

	# Teste de probabilidade randomica 
	if(acceptanceProbability(energiaAtual, energiaDoVizinho, temp) > random.random()):
		tour = novoTour

	# Teste de melhor solucao
	if(energiaAtual < energiaDoMelhor):
		best = tour

	temp = temp * (1 - coolingRate)

# finalizando tempo de codigo
ending_time = time.time()

print("Final solution distance")
print(str(calculateEnergy(best, cities)))
print("Tempo de algoritmo")
print(ending_time - start_time)
print("Melhor rota final")
for i in range(0, len(best)):
	print("(" + str(cities[best[i]][0]) + "|" + str(cities[best[i]][1]) + ") ")

plt.plot([cities[best[i % 15]][0] for i in range(16)], [cities[best[i % 15]][1] for i in range(16)], 'xb-');
plt.show()