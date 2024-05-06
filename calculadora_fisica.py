import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.integrate import quad as integral_definida


# na interface, colocar valores de n para as series
"""
Entradas do programa -> unidade: 

L (largura caixa) -> m
n inicial 
n final
a e b (posição no poço) -> m
tipo (proton ou eletron)

"""

c = 3e8
planck_em_joule = 6.62607e-34
planck_em_ev = 4.13566e-15
planck_reduzida = planck_em_joule / (2 * np.pi)

v = 2.187e6

massa_eletron = 9.109e-31
massa_proton = 1.672e-27

def ev_para_joules(energia_ev):
    joules_por_ev = 1.60218e-19
    return energia_ev * joules_por_ev

def joules_para_ev(energia_joules):
    joules_por_ev = 1.60218e-19
    return energia_joules / joules_por_ev

def string_funcao_de_onda_quantica(numero_n, L):
  return f"psi = {np.sqrt(2/L):.2e} sen({numero_n * np.pi/L:.2e}x)"

def calcula_energia_para_estado_n(n, L, massa):
   return (n ** 2 * np.pi ** 2 * planck_reduzida**2)/(2 * massa * L**2)

def calcula_energia_foton(n):
  e_foton = (13.6 / (n**2))
  return e_foton


def velocidade_particula_nivel_quantico(n_inicial, n_final):
  velocidade_nivel_inicial = v / n_inicial
  velocidade_nivel_final = v / n_final

  print(
      f"Velocidade da particula no nível quântico inicial: {velocidade_nivel_inicial:.2e} m/s"
  )
  print(
      f"Velocidade da particula no nível quântico final: {velocidade_nivel_final:.2e} m/s"
  )

  return velocidade_nivel_inicial, velocidade_nivel_final

def calcula_velocidade(n, L, massa):
   return (n * np.pi * planck_reduzida)/(massa*L)

def calcula_comprimento_de_onda_de_broglie(n, L):
  """
  Calcula o comprimento de onda de De Broglie para um dado nível quântico n
  em um poço de potencial de largura L.
  """
  comprimento = (2 * L) / n
  return comprimento

def calcula_diferenca_de_energia_para_transicao(n_inicial, n_final, L, massa):
  delta_energia = (n_final ** 2 - n_inicial**2) * ((np.pi**2 * planck_reduzida**2)/(2 * massa * L**2))
  return np.absolute(delta_energia)

# energia deve estar em joules
def calcula_frequencia_com_energia(energia):
  return (energia) / planck_em_joule

def calcula_comprimento_com_frequencia(frequencia):
  return (c / frequencia)

def calcula_probabilidade(a, b, n, L):
  """
  Calcula a probabilidade de encontrar a partícula entre a posição a e b
  para o nível quântico n em um poço de potencial de largura L.
  """

  # Define a função de onda para ser integrada
  def funcao_de_onda_ao_quadrado(x):
    return (2 / L) * (np.sin(n * np.pi * x / L))**2

  # Calcula a integral do quadrado da função de onda entre a e b
  prob, _ = integral_definida(funcao_de_onda_ao_quadrado, a, b)
  return prob * 100  # Retorna a probabilidade em percentual %

def calcula_largura_caixa(A):
  L = 2/A**2
  return L

def calcula_n_com_k(k, L):
  return (k * L)/(np.pi)

def calcula_probabilidade_de_posicao_x(A, k, x, L):
   return A ** 2 * (np.sin(k * x))**2

def abrir_janela_com_graficos(n_inicial, n_final, L):
    # Nova janela
    new_window = tk.Toplevel(root)
    new_window.title("Gráficos")
    
    # Criação de uma figura com subplots
    fig, axs = plt.subplots(2, 2)  # Grid de 2x2 para os gráficos

    def funcao_de_onda(x, n, L):
      return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)
    
    def funcao_de_onda_ao_quadrado(x, n, L):
      return (2 / L) * (np.sin(n * np.pi * x / L))**2
    
    
    x1 = np.linspace(0, L, 500)
    y1 = funcao_de_onda(x1, n_inicial, L)

    x2 = np.linspace(0, L, 500)
    y2 = funcao_de_onda(x2, n_final, L)

    x3 = np.linspace(0, L, 500)
    y3 = funcao_de_onda_ao_quadrado(x3, n_inicial, L)

    x4 = np.linspace(0, L, 500)
    y4 = funcao_de_onda_ao_quadrado(x4, n_final, L)

    
    axs[0, 0].plot(x1, y1, 'tab:red')
    axs[0, 0].set_title('Função de onda para n inicial')
    axs[0, 0].set_ylabel('Ψ')
    axs[0, 0].set_xlabel('x')

    
    axs[0, 1].plot(x2, y2, 'tab:blue')
    axs[0, 1].set_title('Função de onda para n final')
    axs[0, 1].set_ylabel('Ψ')
    axs[0, 1].set_xlabel('x')
    
    axs[1, 0].plot(x3, y3, 'tab:green')
    axs[1, 0].set_title('Probabilidade para n inicial')
    axs[1, 0].set_label('teste')

    axs[1, 0].set_ylabel('|Ψ|²')
    axs[1, 0].set_xlabel('x')
    
    axs[1, 1].plot(x4, y4, 'tab:orange')
    axs[1, 1].set_title('Probabilidade para n final')
    axs[1, 1].set_ylabel('|Ψ|²')
    axs[1, 1].set_xlabel('x')
    
    fig.tight_layout(pad=3.0)
    
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def executar_calculos():
    L = float(entry_L.get())
    n_inicial = int(entry_n_inicial.get())
    n_final = int(entry_n_final.get())
    a = float(entry_a.get())
    b = float(entry_b.get())
    massa = massa_eletron if tipo_massa.get() == 0 else massa_proton

    #sem o lambda no command a funcao é executada assim que o executar_calculos() é chamado
    button_graficos = ttk.Button(root, text="Ver graficos", command=lambda: abrir_janela_com_graficos(n_inicial, n_final, L))
    button_graficos.grid(column=0, row=6, columnspan=2, pady=5)

    diferenca_energia = calcula_diferenca_de_energia_para_transicao(n_inicial, n_final, L, massa)
    frequencia = calcula_frequencia_com_energia(diferenca_energia)
    comprimento = calcula_comprimento_com_frequencia(frequencia)

    resultados = []
    resultados.append(string_funcao_de_onda_quantica(n_inicial, L))
    resultados.append(f"Energia do foton absorvido ou emitido: {diferenca_energia:.3e} J")
    resultados.append(f"Energia do foton absorvido ou emitido: {joules_para_ev(diferenca_energia):.3e} eV")
    resultados.append(f"Energia do eletron/proton no nível n = {n_inicial}: {calcula_energia_para_estado_n(n_inicial, L, massa):.3e} J")
    resultados.append(f"Energia do eletron/proton no nível n = {n_inicial}: {joules_para_ev(calcula_energia_para_estado_n(n_inicial, L, massa)):.3e} eV")
    resultados.append(f"Energia do eletron/proton no nível n = {n_final}: {calcula_energia_para_estado_n(n_final, L, massa):.3e} J")
    resultados.append(f"Energia do eletron/proton no nível n = {n_final}: {joules_para_ev(calcula_energia_para_estado_n(n_final, L, massa)):.3e} eV")
    resultados.append(f"Comprimento de onda do fóton emitido ou absorvido: {comprimento:.3e} m")
    resultados.append(f"Comprimento de onda de broglie no nível n = {n_inicial}: {calcula_comprimento_de_onda_de_broglie(n_inicial, L):.3e} m")
    resultados.append(f"Comprimento de onda de broglie no nível n = {n_final}: {calcula_comprimento_de_onda_de_broglie(n_final, L):.3e} m")
    resultados.append(f"Frequencia do fóton emitido ou absorvido: {frequencia:.3e} m")
    resultados.append(f"Velocidade do elétron/proton no nível n = {n_inicial}: {calcula_velocidade(n_inicial, L, massa):.3e} m/s")
    resultados.append(f"Velocidade do elétron/proton no nível n = {n_final}: {calcula_velocidade(n_final, L, massa):.3e} m/s")
    resultados.append(f"Probabilidade entre a e b no nível n = {n_inicial}: {calcula_probabilidade(a, b, n_inicial, L):.2f}%")
    resultados.append(f"Probabilidade entre a e b no nível n = {n_final}: {calcula_probabilidade(a, b, n_final, L):.2f}%")
    
    resultados_texto.set("\n".join(resultados))
    
def executar_calculos2():
    A = float(entry_A.get())
    k = float(entry_k.get())
    xp = float(entry_xp.get())

    L = calcula_largura_caixa(A)
    n = calcula_n_com_k(k, L)
    prob_xp = calcula_probabilidade_de_posicao_x(A, k, xp, L)

    resultados = []
    resultados.append(f"Largura da caixa L: {L:.2e} m")
    resultados.append(f"Nivel quantico da particula: {n:.2e}")
    resultados.append(f"P(x): {prob_xp:.3e} dx")

    
    resultados_texto.set("\n".join(resultados))


# GUI
root = tk.Tk()
root.title("Calculadora Quântica")

# Entradas

tipo_massa = tk.IntVar()
radio_button_a = ttk.Radiobutton(root, text="Eletron", variable=tipo_massa, value=0).grid(column=0, row=0, pady=10, padx = 5)
radio_button_b = ttk.Radiobutton(root, text="Proton", variable=tipo_massa, value=1).grid(column=1, row=0, pady=10, padx=5)


ttk.Label(root, text="L (m):").grid(column=0, row=1)
entry_L = ttk.Entry(root)
entry_L.grid(column=1, row=1)

ttk.Label(root, text="n inicial:").grid(column=0, row=2)
entry_n_inicial = ttk.Entry(root)
entry_n_inicial.grid(column=1, row=2)

ttk.Label(root, text="n final:").grid(column=0, row=3)
entry_n_final = ttk.Entry(root)
entry_n_final.grid(column=1, row=3)

ttk.Label(root, text="a (m):").grid(column=0, row=4)
entry_a = ttk.Entry(root)
entry_a.grid(column=1, row=4)

ttk.Label(root, text="b (m):").grid(column=0, row=5)
entry_b = ttk.Entry(root)
entry_b.grid(column=1, row=5)

button_calcular = ttk.Button(root, text="Calcular", command=executar_calculos)
button_calcular.grid(column=0, row=7, columnspan=2, pady=5)

ttk.Label(root, text="A:").grid(column=0, row=8)
entry_A = ttk.Entry(root)
entry_A.grid(column=1, row=8)

ttk.Label(root, text="k:").grid(column=0, row=9)
entry_k = ttk.Entry(root)
entry_k.grid(column=1, row=9)

ttk.Label(root, text="xp:").grid(column=0, row=10)
entry_xp = ttk.Entry(root)
entry_xp.grid(column=1, row=10)

button_calcular2 = ttk.Button(root, text="Calcular", command=executar_calculos2)
button_calcular2.grid(column=0, row=11, columnspan=2, pady=5)

resultados_texto = tk.StringVar()
ttk.Label(root, textvariable=resultados_texto, background="white", anchor="center").grid(column=0, row=12, columnspan=2, sticky="ew", ipadx=10, ipady=10)

root.mainloop()

