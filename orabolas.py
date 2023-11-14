import tkinter as tk
from tkinter import messagebox as msgbox
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import sqrt
from sympy import sin, cos, atan
from tkinter import *

# ---- DEFINIÇÃO DOS OBJETOS ----

class Robo:
    def __init__(self, posicao_x=0, posicao_y=0):
        self.velocidade = 0
        self.aceleracao = 2.8 # Ref.: IC-Tavares-2007 (moodle)
        self.pos_x0 = posicao_x
        self.pos_y0 = posicao_y
        self.raio = 0.09
        self.coefAngular = 0
        self.grfX = 0 # deslocamento do robo no eixo x em funçao do tempo
        self.grfY = 0 # deslocamento do robô no eixo Y em função do tempo
        self.alcance = 0.09
        self.pos_x = posicao_x
        self.pos_y = posicao_y
        

    def atualizaVelocidade(self, t):
        self.velocidade = t/100 * self.aceleracao
        if self.velocidade > 2.8: self.velocidade = 2.8

    def retornaVelocidade(self, t):
        vel = t/100 * self.aceleracao
        if vel > 2.8: vel = 2.8
        return vel

    def atualizaAlcance(self, t_final):
        if t_final <= 100:
            velMedia = (self.retornaVelocidade(0) + self.retornaVelocidade(t_final)) / 2
            self.alcance = velMedia * t_final/100 + self.raio
        elif t_final > 100:
            self.alcance = self.retornaAlcance(100) + (self.retornaVelocidade(t_final) * (t_final-100)/100)
        else:
            print(f"ERRO: valor inválido para variável 't_final'")

    def retornaAlcance(self, t_final):
        alc = 0
        if t_final <= 100:
            velMedia = self.retornaVelocidade(0) + self.retornaVelocidade(t_final) / 2
            alc = velMedia * t_final/100 + self.raio
        elif t_final > 100:
            alc = self.retornaAlcance(100) + self.raio + (2.8 * (t_final-100)/100)
        else:
            print(f"ERRO: valor inválido para variável 't_final'")
        return alc

class Bola:
    def __init__(self):
        self.pos_x = self.retornaPosX
        self.vel_x = self.retornaVelX
        self.acel_x = self.retornaAclX
        self.pos_y = self.retornaPosY
        self.vel_y = self.retornaVelY
        self.acel_y = -0.04
        self.raio = 0.021 #Ref.: IC-Rodrigues-2015 https://fei.edu.br/robofei/ics/IC-Rodrigues-2015.pdf
        self.incpos_x = 0
        self.incpos_y = 0
        self.inct = 0

    def atualizaPosX(self, t): self.pos_x = (0.005*((t/100)**3))-(7 * ((t/100)**2) * (10**(-14))) + (0.5*(t/100)) +1
    def atualizaVelX(self, t): self.vel_x = (0.015*((t/100)**2)) - (0.0003*(t/100)) + 0.5
    def atualizaAclX(self, t): self.acel_x = (6*(10**(-16)*((t/100)**2))) + (0.03*(t/100)) - 0.0006
    def atualizaPosY(self, t): self.pos_y = (9*(10**-16*((t/100)**3))) - (0.02*(t/100)**2) + (0.9*(t/100)) + 0.5
    def atualizaVelY(self, t): self.vel_y = (9*(10**(-18))*((t/100)**2)) - (0.04*(t/100)) + 0.9004
    def retornaPosX(self, t=0): return (0.005*((t/100)**3))-(7 * ((t/100)**2) * (10**(-14))) + (0.5*(t/100)) +1
    def retornaVelX(self, t=0): return (0.015*((t/100)**2)) - (0.0003*(t/100)) + 0.5
    def retornaAclX(self, t=0): return (6*(10**(-16)*((t/100)**2))) + (0.03*(t/100)) - 0.0006
    def retornaPosY(self, t=0): return (9*(10**-16*((t/100)**3))) - (0.02*(t/100)**2) + (0.9*(t/100)) + 0.5
    def retornaVelY(self, t=0): return (9*(10**(-18))*((t/100)**2)) - (0.04*(t/100)) + 0.9004
    def listaTodasPosicoes(self):
        t = 0 # tempo (em centésimos de segundo)
        while (0 <= self.retornaPosX(t) and self.retornaPosX(t)<= 9 and 0<= self.retornaPosY(t) and self.retornaPosY(t)<=6):
            print(f"""
                Tempo (seg): {t/100}
                Posição em X: {self.retornaPosX(t):.2f}
                Posição em Y: {self.retornaPosY(t):.2f}
                """)
            t += 2
    def listaTodasVelocidades(self):
        t = 0
        while (0 <= self.retornaPosX(t) and self.retornaPosX(t)<= 9 and 0<= self.retornaPosY(t) and self.retornaPosY(t)<=6):
            print(f"""
                Tempo (seg): {t/100}
                Vx: {self.retornaVelX(t):.2f}
                Vy: {self.retornaVelY(t):.2f}
                  """)
            t += 2
    def exibePosicaoEspecifica(self, t):
        print(f"""
        Tempo (seg): {t/100}
        Posição em X: {self.retornaPosX(t):.2f}
        Posição em Y: {self.retornaPosY(t):.2f}
        """)

class Pag:
    def __init__(self, num=0):
        ind = num

# -------------------------------

def calcular_intercept(robo, bola):
    dT = 0.5
    t = 0

    while True:

        robo.atualizaAlcance(t)

        dist = sqrt((robo.pos_x0 - bola.retornaPosX(t))**2 + (robo.pos_y0 - bola.retornaPosY(t))**2)

        if dist < robo.alcance + bola.raio:
            bola.incpos_x = bola.retornaPosX(t) + (bola.raio*(robo.pos_x0))/dist
            bola.incpos_y = bola.retornaPosY(t) + (bola.raio*(robo.pos_y0))/dist
            bola.inct = t
            break
        
        t += dT

def equacaoDeslocamentoRetaRobo(robo, bola):
    # y = ax + b
    robo.coefAngular = (robo.pos_y0 - bola.retornaPosY(bola.inct))/(robo.pos_x0 - bola.retornaPosX(bola.inct))
    b = (bola.retornaPosY(bola.inct) - (robo.coefAngular * bola.retornaPosX(bola.inct)))
    
    print(f"Equação da reta do deslocamento do robô: y = {robo.coefAngular:.2f}x + {b:.2f}")

def decompoeDeslocamentoRobo(robo, bola):
    theta = atan(robo.coefAngular)
    dist = sqrt((robo.pos_x0 - bola.retornaPosX(bola.inct))**2 + (robo.pos_y0 - bola.retornaPosY(bola.inct))**2)
    if robo.coefAngular < 0:
        robo.grfY = dist * sin(theta) # deslocamento do robô no eixo Y
        robo.grfX = dist * cos(theta) # desloamento do robô no eixo X
    elif robo.coefAngular >= 0:
        robo.grfY = dist * sin(theta)
        robo.grfX = dist * cos(theta)
    robo.pos_x = robo.pos_x0 + robo.grfX
    robo.pos_y = robo.pos_y0 + robo.grfY

# ---- DEFINIÇÃO DAS INTERFACES GRÁFICAS ----

class graficosGUI:

    def __init__(self):
        calcular_intercept(robo=robo, bola=bola)
        equacaoDeslocamentoRetaRobo(robo=robo, bola=bola)
        
        th = atan(robo.coefAngular)
        listaXrobo = []
        listaYrobo = []
        listaXbola = []
        listaYbola = []
        eixoX = []
        vx_bola = []
        vy_bola = []
        vx_robo = []
        vy_robo = []
        ax_bola = []
        ay_bola = []
        ax_robo = []
        ay_robo = []
        ax_bola = []
        ay_bola = []
        ax_robo = []
        ay_robo = []
        listaDist = []
        i = 0
        distGrf = 10
        auxPos = 0
        while i < bola.inct:

            robo.atualizaAlcance(i)
            decompoeDeslocamentoRobo(robo=robo, bola=bola)
            velMedia = (robo.retornaVelocidade(0) + robo.retornaVelocidade(t=i)) / 2

            if robo.pos_x0 >= bola.retornaPosX(0):
                listaXrobo.append((robo.pos_x0 - (robo.retornaAlcance(i) * (velMedia*cos(th)))))
                listaYrobo.append((robo.pos_y0 - (robo.retornaAlcance(i) * (velMedia*sin(th)))))
            else:
                listaXrobo.append(robo.pos_x0 + (robo.alcance * cos(th)))
                listaYrobo.append(robo.pos_y0 + (robo.alcance * sin(th)))
            distGrf = sqrt((bola.retornaPosX(i) - (listaXrobo[auxPos]))**2 + (bola.retornaPosY(i) - (listaYrobo[auxPos]))**2)    
            listaDist.append(distGrf)
            listaXbola.append(bola.retornaPosX(t=i))
            listaYbola.append(bola.retornaPosY(t=i))
            eixoX.append(i)
            vx_bola.append(bola.retornaVelX(i))
            vy_bola.append(bola.retornaVelY(i))
            vx_robo.append(robo.retornaVelocidade(i)*cos(th))
            vy_robo.append(robo.retornaVelocidade(i)*sin(th))
            ax_bola.append(bola.retornaAclX(i))
            ay_bola.append(bola.acel_y)
            ax_robo.append(robo.aceleracao*cos(th))
            ay_robo.append(robo.aceleracao*sin(th))
            i += 0.01
            auxPos += 1
        for i in range(len(listaDist)):
            if listaDist[i] < robo.raio + bola.raio:
                bola.inct = i
                print(f"bola.inct = {bola.inct}")
                break    
        
        def plot1():
            ax1.scatter(listaXrobo, listaYrobo, c='r', label= 'robo')
            ax1.scatter(listaXbola, listaYbola, c='b', label='bola')
            ax1.legend(loc='upper left')
            self.canvas1.draw()

        def plot2():
            ax2.scatter(eixoX, listaXbola, c ='b', label='Coordenada X da bola')
            ax2.scatter(eixoX, listaYbola, c ='y', label='Coordenada Y da bola')
            ax2.scatter(eixoX, listaXrobo, c='r', label ='Coordenada X do robô')
            ax2.scatter(eixoX, listaYrobo, c='g', label='Coordenada Y do robô')
            ax2.legend(loc='upper left')
            self.canvas2.draw()
            
        def plot3():
            ax3.scatter(eixoX, vx_bola, c = 'b', label='Vx da bola')
            ax3.scatter(eixoX, vy_bola, c = 'y', label='Vy da bola')
            ax3.scatter(eixoX, vx_robo, c= 'r', label='Vx do robô')
            ax3.scatter(eixoX, vy_robo, c = 'g', label='Vy do robô')
            ax3.legend(loc='upper left')
            self.canvas3.draw()
        
        def plot4():
            ax4.scatter(eixoX, ax_bola, c = 'b', label='Ax da bola')
            ax4.scatter(eixoX, ay_bola, c = 'y', label='Ay da bola')
            ax4.scatter(eixoX, ax_robo, c= 'r', label='Ax do robô')
            ax4.scatter(eixoX, ay_robo, c = 'g', label='Ay do robô')
            ax4.legend(loc='upper left')
            self.canvas4.draw()
        
        def plot5():
            ax5.scatter(eixoX, listaDist, c = 'b', label='Distância')
            self.canvas5.draw()

        self.janelaPrincipal = tk.Tk()
        self.janelaPrincipal.geometry("1440x1000")
        self.janelaPrincipal.title("Projeto OraBolas - Gráficos")

        self.titulo = tk.Label(self.janelaPrincipal, text ="Gráficos", font=('Inter', 32))
        self.titulo.pack(padx=10, pady=10, anchor="nw")

        self.botAprofundamento = tk.Button(self.janelaPrincipal, text="Aprofundamento >", font=('inter', 14))
        self.botAprofundamento.place(x=1200, y=800)

        self.nb = ttk.Notebook(self.janelaPrincipal, width=1400, height=900)

        self.frame1 = ttk.Frame(self.nb)
        self.frame2 = ttk.Frame(self.nb)
        self.frame3 = ttk.Frame(self.nb)
        self.frame4 = ttk.Frame(self.nb)
        self.frame5 = ttk.Frame(self.nb)

        fonteTitulo = {'family' : 'sans serif', 'size' : 20}
        fonteEixo = {'family' : 'sans serif', 'size' : 15}

        self.fig1, ax1=plt.subplots(figsize=(12, 8))
        self.fig1, plt.title("Trajetórias", loc='left', pad=10, fontdict=fonteTitulo)
        self.fig1, plt.xlim([0, 9])
        self.fig1, plt.ylim([0, 6])
        self.fig1, plt.xlabel('X (m)', fontdict=fonteEixo, labelpad=5)
        self.fig1, plt.ylabel('Y (m)', fontdict=fonteEixo, labelpad=5)

        self.canvas1 = FigureCanvasTkAgg(self.fig1, self.frame1)
        self.canvas1.get_tk_widget().pack()

        self.button1 = tk.Button(self.frame1, text="Desenhar gráfico", command = plot1)
        self.button1.pack(pady=10)

        self.fig2, ax2=plt.subplots(figsize=(12,8))
        self.fig2, plt.title("Coordenadas em função do tempo", loc='left', fontdict=fonteTitulo)
        self.fig2, plt.xlim([0, bola.inct/100])
        self.fig2, plt.xlabel('Tempo (em centésimos de segundo)', fontdict=fonteEixo, labelpad=5)
        self.fig2, plt.ylabel('Posição (m)', fontdict=fonteEixo, labelpad=5)

        self.canvas2 = FigureCanvasTkAgg(self.fig2, self.frame2)
        self.canvas2.get_tk_widget().pack()

        self.button2 = tk.Button(self.frame2, text="Desenhar gráfico", command= plot2)
        self.button2.pack(pady=10)
        
        self.fig3, ax3=plt.subplots(figsize=(12, 8))
        self.fig3, plt.title("Velocidades (X e Y) em função do tempo", loc='left', pad=10, fontdict=fonteTitulo)
        self.fig3, plt.xlim([0, bola.inct/100])
        self.fig3, plt.xlabel('Tempo (em centésimos de segundo)', fontdict=fonteEixo, labelpad=5)
        self.fig3, plt.ylabel('Velocidade (m/s)', fontdict=fonteEixo, labelpad=5)

        self.canvas3 = FigureCanvasTkAgg(self.fig3, self.frame3)
        self.canvas3.get_tk_widget().pack()

        self.button3 = tk.Button(self.frame3, text="Desenhar gráfico", command=plot3)
        self.button3.pack(pady=10)
        
        self.fig4, ax4=plt.subplots(figsize=(12, 8))
        self.fig4, plt.title("Acelerações (X e Y) em função do tempo", loc='left', pad=10, fontdict=fonteTitulo)
        self.fig4, plt.xlim([0, bola.inct/100])
        self.fig4, plt.xlabel('Tempo (em centésimos de segundo)', fontdict=fonteEixo, labelpad=5)
        self.fig4, plt.ylabel('Aceleração (m/s²)', fontdict=fonteEixo, labelpad=5)

        self.canvas4 = FigureCanvasTkAgg(self.fig4, self.frame4)
        self.canvas4.get_tk_widget().pack()

        self.button4 = tk.Button(self.frame4, text="Desenhar gráfico", command=plot4)
        self.button4.pack(pady=10)
        
        self.fig5, ax5=plt.subplots(figsize=(12, 8))
        self.fig5, plt.title("Distância em função do tempo", loc='left', pad=10, fontdict=fonteTitulo)
        self.fig5, plt.xlim([0, bola.inct/100])
        self.fig5, plt.xlabel('Tempo (em centésimos de segundo)', fontdict=fonteEixo, labelpad=5)
        self.fig5, plt.ylabel('Distância (m)', fontdict=fonteEixo, labelpad=5)

        self.canvas5 = FigureCanvasTkAgg(self.fig5, self.frame5)
        self.canvas5.get_tk_widget().pack()

        self.button5 = tk.Button(self.frame5, text="Desenhar gráfico", command=plot5)
        self.button5.pack(pady=10)

        self.nb.add(self.frame1, text = "Gráfico 1")
        self.nb.add(self.frame2, text = "Gráfico 2")
        self.nb.add(self.frame3, text = "Gráfico 3")
        self.nb.add(self.frame4, text = "Gráfico 4")
        self.nb.add(self.frame5, text = "Gráfico 5")

        self.nb.pack(padx = 5, pady = 5, expand=True)

        self.janelaPrincipal.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.janelaPrincipal.mainloop()

    def onClosing(self):
        self.janelaPrincipal.destroy()

class inicioGUI:
    
    def __init__(self):    

        self.janelaPrincipal = tk.Tk()
        self.janelaPrincipal.geometry("1440x1000")
        self.janelaPrincipal.title("Projeto OraBolas")

        self.titulo = tk.Label(self.janelaPrincipal, text="Projeto OraBolas - CF2111", font=('Inter', 32))
        self.titulo.pack(padx=10, pady=10, anchor="nw")

        self.conteudo = ttk.Frame(self.janelaPrincipal)

        self.frameCompleto = ttk.Frame(self.conteudo)

        self.frameX = ttk.Frame(self.frameCompleto)

        self.labelX_InicialRobo = tk.Label(self.frameX, text="Digite a coordenada X da posição inicial do robô:", font=('Arial', 16))
        self.labelX_InicialRobo.pack(side="left", padx=5)
        self.valorX_InicialRobo = tk.Entry(self.frameX, font=('Arial', 16), width=10)
        self.valorX_InicialRobo.pack(side="right", padx=5)

        self.frameX.pack(pady=60)

        self.frameY = ttk.Frame(self.frameCompleto)

        self.labelY_InicialRobo = tk.Label(self.frameY, text="Digite a coordenada Y da posição inicial do robô:", font=('Arial', 16))
        self.labelY_InicialRobo.pack(side="left", padx=5)
        self.valorY_InicialRobo = tk.Entry(self.frameY,  width=10, font=('Arial', 16))
        self.valorY_InicialRobo.pack(side="right", padx=5)

        self.frameY.pack(pady=30)

        self.frameCompleto.pack(anchor="center")

        self.button = tk.Button(self.conteudo, text="Iniciar", font=('Arial', 18), command=lambda:self.iniciar(robo, bola, pag))
        self.button.pack(padx=10, pady=10)

        self.conteudo.pack(expand=1)
    
        self.janelaPrincipal.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.janelaPrincipal.mainloop()

    def iniciar(self, robo, bola, pag):
        robo.pos_x0 = float(self.valorX_InicialRobo.get())
        robo.pos_y0 = float(self.valorY_InicialRobo.get())
        self.janelaPrincipal.destroy()
        
    def onClosing(self):
        if msgbox.askyesnocancel(title="Sair", message="Deseja realmente sair?"):
            self.janelaPrincipal.destroy()
            exit

class aprofundamentoGUI:
    def __init__(self, bola):

        self.janelaAprofundamento = tk.Tk()
        self.janelaAprofundamento.geometry("1440x1000")
        self.janelaAprofundamento.title("Projeto OraBolas")
        
        self.titulo = tk.Label(self.janelaAprofundamento, text="Aprofundamento", font=('Inter', 32))
        self.titulo.pack(padx=10, pady=10, anchor="nw")

        self.tituloSlider = tk.Label(self.janelaAprofundamento, text="Tempo (em centésimos de segundo)", font=('Helvetica Neue', 20))
        self.tituloSlider.pack()
        self.textodeteste = tk.StringVar()

        self.auxSlider = tk.DoubleVar()
        self.slider = tk.Scale(self.janelaAprofundamento, variable=self.textodeteste, from_=0, to=(auxTempoInc/100), orient=HORIZONTAL, length="1000")
        self.slider.pack(anchor=CENTER)

        self.button = tk.Button(self.janelaAprofundamento, text="Exibir informações", command=self.janelaAprofundamento.update_idletasks())
        self.button.pack(anchor=CENTER)

        self.labelteste = tk.Label(self.janelaAprofundamento, textvariable=self.textodeteste, font=('Helvetica Neue', 20))
        self.labelteste.pack(anchor=CENTER, pady=10)

        self.janelaAprofundamento.mainloop()

# -------------------------------------------

# ---- INICIALIZAÇÃO DOS OBJETOS PARA EXECUÇÃO DO PROGRAMA PRINCIPAL ----

robo = Robo()

bola = Bola()

pag = Pag()

# -----------------------------------------------------------------------

inicioGUI() # INICIALIZAÇÃO DA INTERFACE GRÁFICA DO INÍCIO DO PROGRAMA

auxTempoInc = bola.inct # VARIÁVEL QUE VAI ARMAZENAR O MOMENTO NO TEMPO EM QUE OCORRE A INTERCEPTAÇÃO

graficosGUI()
print(f"auxtempoinc = {bola.inct}")
aprofundamentoGUI(bola=bola)
