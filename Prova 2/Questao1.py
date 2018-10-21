import numpy as np, random, time, operator, pandas as pd

# Gene
class Ponto:
	# Ligacoes eh um array de arrays de tamanho 2, onde o primeiro elemento do array
	# eh o numero do ponto em que ele esta se ligando, e o segundo eh
	# a distancia entre os dois, por exemplo.
	# para o ponto 1: [[2,2], [3,9], [4,3], [5,6]]
	def __init__(self, numero, ligacoes):
		self.numero = numero
		self.ligacoes = ligacoes
	
	def distance(self, ponto):
		distance = 0
		for i in self.ligacoes:
			if(ponto.numero == i[0]):
				distance = i[1]
				break

		return distance

	def __repr__(self):
		return "(" + str(self.numero) + ")"

class Fitness:
	# route eh um array de caminho, representado por os pontos (objetos)
	def __init__(self, route):
		self.route = route
		self.distance = 0
		self.fitness= 0.0
	
	def routeDistance(self):
		if self.distance == 0:
			pathDistance = 0
			for i in range(0, len(self.route)):
				fromPoint = self.route[i]
				toPoint = None
				if i + 1 < len(self.route):
					toPoint = self.route[i + 1]
				else:
					toPoint = self.route[0]
				pathDistance += fromPoint.distance(toPoint)
			self.distance = pathDistance
		return self.distance
	
	def routeFitness(self):
		if self.fitness == 0:
			self.fitness = 1 / float(self.routeDistance())
		return self.fitness


# ===================== Declaracao de funcoes ==================

# Cria rota aleatoria entre os pontos
def createRoute(pontoList):
	route = random.sample(pontoList, len(pontoList))
	return route

# gera geracao
def initialPopulation(popSize, pontoList):
	population = []

	for i in range(0, popSize):
		population.append(createRoute(pontoList))
	return population

# Retorna a distancia total entre a populacao de cidades
def rankRoutes(population):
	fitnessResults = {}
	for i in range(0,len(population)):
		fitnessResults[i] = Fitness(population[i]).routeFitness()
	return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

# Retorna melhores resultados de uma populacao (cromossomo)
def selection(popRanked, eliteSize):
	selectionResults = []
	df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
	df['cum_sum'] = df.Fitness.cumsum()
	df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
	
	for i in range(0, eliteSize):
		selectionResults.append(popRanked[i][0])
	for i in range(0, len(popRanked) - eliteSize):
		pick = 100*random.random()
		for i in range(0, len(popRanked)):
			if pick <= df.iat[i,3]:
				selectionResults.append(popRanked[i][0])
				break
	return selectionResults

# selecao de pais com tamanho o eliteSize para proxima geracao de filhos
def matingPool(population, selectionResults):
	matingpool = []

	for i in range(0, len(selectionResults)):
		index = selectionResults[i]
		matingpool.append(population[index])
	return matingpool

# Criando filhos a partir dos pais
def breed(parent1, parent2):
	child = []
	childP1 = []
	childP2 = []
	
	geneA = int(random.random() * len(parent1))
	geneB = int(random.random() * len(parent1))
	
	startGene = min(geneA, geneB)
	endGene = max(geneA, geneB)

	for i in range(startGene, endGene):
		childP1.append(parent1[i])
		
	childP2 = [item for item in parent2 if item not in childP1]

	child = childP1 + childP2
	return child


def breedPopulation(matingpool, eliteSize):
	children = []
	length = len(matingpool) - eliteSize
	pool = random.sample(matingpool, len(matingpool))

	for i in range(0,eliteSize):
		children.append(matingpool[i])
	
	for i in range(0, length):
		child = breed(pool[i], pool[len(matingpool)-i-1])
		children.append(child)
	return children

# mutacao de um cromossomo
def mutate(individual, mutationRate):
	for swapped in range(len(individual)):
		if(random.random() < mutationRate):
			swapWith = int(random.random() * len(individual))
			
			point1 = individual[swapped]
			point2 = individual[swapWith]
			
			individual[swapped] = point2
			individual[swapWith] = point1
	return individual


# mutacoes em uma populacao
def mutatePopulation(population, mutationRate):
	mutatedPop = []
	
	for ind in range(0, len(population)):
		mutatedInd = mutate(population[ind], mutationRate)
		mutatedPop.append(mutatedInd)
	return mutatedPop


# Gerar proxima geracao de cromossomos
def nextGeneration(currentGen, eliteSize, mutationRate):

	# Gera distancia da populacao atual
	popRanked = rankRoutes(currentGen)
	# Captura os melhores resultados
	selectionResults = selection(popRanked, eliteSize)
	# gerando pais
	matingpool = matingPool(currentGen, selectionResults)
	# gerando filhos
	children = breedPopulation(matingpool, eliteSize)
	nextGeneration = mutatePopulation(children, mutationRate)
	
	return nextGeneration


def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
	pop = initialPopulation(popSize, population)
	indexRandom = random.randint(0, len(pop))

	# Primeira rota gerada aleatoriamente
	print("Initial distance: " + str( 1 / Fitness(pop[indexRandom]).routeFitness()))
	print("Rota inicial")
	print(pop[indexRandom])

	for i in range(0, generations):
		pop = nextGeneration(pop, eliteSize, mutationRate)

	print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
	bestRouteIndex = rankRoutes(pop)[0][0]
	bestRoute = pop[bestRouteIndex]
	return bestRoute

# ===================== FIM DAS FUNCOES ===============================

pontos = [
	Ponto(numero=1, ligacoes=[[2,2], [3,9], [4,3], [5,6]]),
	Ponto(numero=2, ligacoes=[[1,2], [3,4], [4,3], [5,8]]),
	Ponto(numero=3, ligacoes=[[1,9], [2,4], [4,7], [5,3]]),
	Ponto(numero=4, ligacoes=[[1,3], [2,3], [3,7], [5,3]]),
	Ponto(numero=5, ligacoes=[[1,6], [2,8], [3,3], [4,3]])
]

# PARA LEMBRAR: MENOR DISTANCIA EH 15
best = geneticAlgorithm(population=pontos, popSize=50, eliteSize=10, mutationRate=0.01, generations=50)

print("Melhor rota final")
print(best)


