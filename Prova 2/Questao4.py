import math
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

#Calculo da probabilidade de aceitacao
def acceptanceProbability(energy, newEnergy, temperature):
    if (newEnergy < energy):
        return 1.0
    
    return math.exp((energy - newEnergy) / temperature)

# Funcao determinada pela questao
def f(x):
	return 50 + ((x*x) - 10*np.cos(2*np.pi*x))

# Calculo da energia (valor da funcao para um determinado x)
def calculateEnergy(xAtual):
	return f(xAtual)

# ========================  Fim das funcoes ====================

# Gerando 100 numeros aleatorios de -2pi a +2pi
x = [random.uniform(-(2*np.pi),(2*np.pi)) for i in range(0,1000)]

# Iniciando o x de teste e o melhor resultado
xAtual = x[0]
xBest = xAtual

# set initial temp
temp = 10000

# Cooling rate
coolingRate = 0.003;

print("Primeiro valor de xAtual: " + str(xAtual))
print("Energia do chute inicial: " + str(calculateEnergy(xAtual)))

while temp > 1:

	# numero aleatorio entre 0 e 100 para gerar uma perturbacao do meio
	randomPosition = random.randint(0, len(x)-1)
	# Iniciando novo x com perturbacao ou mutacao
	newX = x[randomPosition]

	# Capturando energia do sistema, ou seja, valores da funcao para tres x's diferentes
	energiaDoMelhor = calculateEnergy(xBest)
	energiaAtual = calculateEnergy(xAtual)
	energiaDoVizinho = calculateEnergy(newX)

	# Teste de probabilidade randomica 
	if(acceptanceProbability(energiaAtual, energiaDoVizinho, temp) > random.random()):
		xAtual = newX

	# Teste de melhor solucao
	if(energiaAtual < energiaDoMelhor):
		xBest = xAtual

	temp = temp * (1 - coolingRate)

print("Melhor resultado para x = " + str(xBest))
print("Com energia de " + str(calculateEnergy(xBest)))

plt.plot([x[i] for i in range(len(x))], [f(x[i]) for i in range(len(x))], 'x');
plt.show()