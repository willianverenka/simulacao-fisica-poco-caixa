from vpython import curve, vector, rate, color, label, scene
import numpy as np
import time


def funcao_de_onda(x, n, L):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)

#essas variaveis de n não podem ser alteradas, não são flexiveis por conta dos caminhos de decaimento.
n_inicial = 1
n_final = 5

"""
O vpython lida muito mal com escalas, essa limitação faz com que seja inviável setar o valor real pra L,
que geralmente está nas casas de nanômetro por exemplo.
Como o intuito é fazer uma simulação visual, um valor arbitrário como 3 funciona perfeitamente já que a visualização 
das ondas não será muito diferente.
"""

L = 3
"""
dx é como um step pro intervalo de x da função, determina a quantidade de pontos calculados no eixo x.
seria L/dx, no padrão 30.
"""
dx = 0.1
y_offset = 2  # espacamento vertical pra cada onda em um uma visualizao de decaimento
x_offset = 10  # espacamento horizontal pra cada visualizacao de decaimento

# todas possibilidades de decaimento de n = 5 para o nivel fundamental.
# seria melhor fazer um algoritmo pra isso, mas como diz que é pra fazer até o nível 5 é melhor chumbar no código mesmo
# se alterar algo aqui não vai quebrar, mas não vai demonstrar as 8 possibilidades corretas

caminhos_decaimento = [
    (5, 4, 3, 2, 1),
    (5, 4, 3, 1),
    (5, 4, 2, 1),
    (5, 3, 2, 1),
    (5, 3, 1),
    (5, 2, 1),
    (5, 1)
]

# resolucao da cena, se seu monitor não tiver 1400px horizontais pode diminuir
scene.width = 1400
scene.height = 600

# zoom da cena
scene.range = 40

"""
gambiarra pra centralizar a tela nas 8 possibilidades, tem que ir ajustando os valores e testando.
se sentir que existem visualizações pra esquerda da tela que não estão aparecendo, 
aumenta o primeiro parâmetro que é o X.
Se for o lado direito da tela, diminui o X. Mesma lógica é aplicada se estiver descentralizado verticalmente, ajusta o segundo parametro.
se o codigo rodou sem nenhum erro ou warning e a tela ficou preta, provavelmente é essa opcao. 
coloca pra vector(40, 5, 33) que deve ser possivel enxergar algo, é um ponto de partida ao menos
não recomendo alterar o valor de Z, usa o scene.range se quiser aumentar ou diminuir o zoom
"""
scene.camera.pos = vector(40, 5, 33)


curvas = []
labels = []

"""
esse loop prepara o terreno pra animação. além de definir as posições nos eixos considerando os espaçamentos declarados, também define
as curvas iniciais e posiciona as labels pra identificar os níveis.
"""

for index_decaimento, caminho in enumerate(caminhos_decaimento):
    caminho_curvas = []
    caminho_labels = []
    valores_x = np.arange(0, L, dx)
    caminho_ordenado = sorted(caminho, reverse=True) # sem o reverse o n = 5 fica em baixo, n = 1 no topo.
    for index, n in enumerate(caminho_ordenado):
        # prepara a posicao y da curva pra "empilhar" elas e evitar sobreposicao
        posicao_y = y_offset * (len(caminho_ordenado) - 1 - index)
        curva_onda = curve(color=color.hsv_to_rgb(vector(n / 6, 1, 1)))
        #pega os valor de x e calcula o y
        for x in valores_x:
            y = funcao_de_onda(x, n, L)
            curva_onda.append(vector(x + index_decaimento * x_offset, y + posicao_y, 0))
        
        #label pra indicar o nivel de n
        curva_label = label(pos=vector(L + 0.5 + index_decaimento * x_offset, posicao_y, 0), text=f'n = {n}', height=10, color=color.white, box=False, opacity=0)
        caminho_labels.append(curva_label)
        caminho_curvas.append(curva_onda)
    
    curvas.append(caminho_curvas)
    labels.append(caminho_labels)

"""
esse é o loop infinito pra modificar as curvas e fazer as animações.
essa parte do código respira com a ajuda de aparelhos e se algum valor for modificado provavelmente vai quebrar todas as ondas.
exceto o rate, esse da pra mudar e tem um intervalo de valores que funciona bem
"""

while True:
    rate(30) # taxa de atualizacao da animacao, nao da onda. entre 20 e 30 funciona bem
    tempo = time.time()
    for caminho_index, caminho_curvas in enumerate(curvas):
        for index, curva_onda in enumerate(caminho_curvas):
            n = int(labels[caminho_index][index].text.split('=')[1].strip())
            posicao_y = y_offset * (len(caminhos_decaimento[caminho_index]) - 1 - index)
            for i, x in enumerate(valores_x):
                y = funcao_de_onda(x, n, L) * np.cos(np.pi * tempo)
                curva_onda.modify(i, vector(x + caminho_index * x_offset, y + posicao_y, 0))
