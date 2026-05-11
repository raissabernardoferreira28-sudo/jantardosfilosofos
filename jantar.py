from random import uniform
from time import sleep
from threading import Thread, Lock

# Configurações
LIMITE_REFEICOES = 3  # Quantas vezes cada um deve comer
pratos = [0, 0, 0, 0, 0] 
nomes = ['Aristóteles', 'Platão', 'Sócrates', 'Pitágoras', 'Demócrito']

class Filosofo(Thread):
    def __init__(self, id, nome, garfo_esquerda, garfo_direita):
        Thread.__init__(self)
        self.id = id
        self.nome = nome
        self.garfo_esquerda = garfo_esquerda
        self.garfo_direita = garfo_direita

    def run(self):
        # O filósofo tentará comer até atingir o limite definido
        while pratos[self.id] < LIMITE_REFEICOES:
            print(f"\n[Pensando] {self.nome} está refletindo sobre o universo...")
            sleep(uniform(1, 3)) # Reduzi o tempo para o teste ser mais rápido
            self.tentar_comer()
        
        print(f"\n--- {self.nome} está satisfeito e saiu da mesa. ---")

    def tentar_comer(self):
        g1, g2 = self.garfo_esquerda, self.garfo_direita

        # Tenta pegar os garfos
        g1.acquire()
        locked = g2.acquire(False) # False para não travar se o garfo estiver ocupado

        if locked:
            # Conseguiu os dois garfos
            print(f"\n  [Comendo] {self.nome} pegou os dois garfos.")
            sleep(uniform(1, 2))
            
            pratos[self.id] += 1
            print(f"  [Status] Pratos consumidos: {pratos}")
            
            g2.release()
            g1.release()
            print(f"\n[Terminou] {self.nome} soltou os garfos.")
        else:
            # Não conseguiu o segundo, solta o primeiro para evitar Deadlock
            g1.release()
            print(f"\n  [Desistência] {self.nome} não conseguiu o segundo garfo e voltou a pensar.")

# Inicialização
garfos = [Lock() for _ in range(5)]
mesa = [Filosofo(i, nomes[i], garfos[i], garfos[(i + 1) % 5]) for i in range(5)]

# Inicia todos os filósofos uma única vez
for filosofo in mesa:
    filosofo.start()

# Aguarda todos terminarem para encerrar o programa principal
for filosofo in mesa:
    filosofo.join()

print("\n" + "="*30)
print("A refeição acabou! Todos estão satisfeitos.")
print(f"Resultado final: {pratos}")
print("="*30)
