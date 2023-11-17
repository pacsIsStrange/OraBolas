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
        self.aceleracao = 2.8 # Ref.: IC-Tastringes-2007 (moodle)
        self.pos_x0 = posicao_x
        self.pos_y0 = posicao_y
        self.raio = 0.09
        self.coefAngular = 0
        self.grfX = 0 # deslocamento do robo no eixo x em funçao do tempo
        self.grfY = 0 # deslocamento do robô no eixo Y em função do tempo
        self.alcance = 0.09
        self.pos_x = posicao_x
        self.pos_y = posicao_y
        self.massa = 0.171
        

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
        self.massa = 0.3

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

    def __init__(self, bola):
        
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
        self.janelaPrincipal.geometry("933x720")
        self.janelaPrincipal.title("Projeto OraBolas - Gráficos")
        self.titulo = tk.Label(self.janelaPrincipal, text ="Gráficos", font=('Inter', 32))
        self.titulo.pack(padx=10, pady=3, anchor="nw")

        self.botAprofundamento = tk.Button(self.janelaPrincipal, text="Aprofundamento >", font=('inter', 14), command=self.onClosingbotao)
        self.botAprofundamento.pack(anchor='se', padx=5)

        self.nb = ttk.Notebook(self.janelaPrincipal, width=1400, height=900)

        self.frame1 = ttk.Frame(self.nb)
        self.frame2 = ttk.Frame(self.nb)
        self.frame3 = ttk.Frame(self.nb)
        self.frame4 = ttk.Frame(self.nb)
        self.frame5 = ttk.Frame(self.nb)

        fonteTitulo = {'family' : 'sans serif', 'size' : 20}
        fonteEixo = {'family' : 'sans serif', 'size' : 15}

        self.fig1, ax1=plt.subplots(figsize=(12, 8))
        self.fig1, plt.title("Trajetórias no campo", loc='left', pad=10, fontdict=fonteTitulo)
        self.fig1, plt.xlim([0, 9])
        self.fig1, plt.ylim([0, 6])
        self.fig1, plt.xlabel('X (m)', fontdict=fonteEixo, labelpad=5)
        self.fig1, plt.ylabel('Y (m)', fontdict=fonteEixo, labelpad=5)

        self.canvas1 = FigureCanvasTkAgg(self.fig1, self.frame1)
        self.canvas1.get_tk_widget().pack()
        plot1()

        self.fig2, ax2=plt.subplots(figsize=(12,8))
        self.fig2, plt.title("Coordenadas (X e Y) em função do tempo", loc='left', fontdict=fonteTitulo)
        self.fig2, plt.xlim([0, bola.inct/100])
        self.fig2, plt.xlabel('Tempo (em centésimos de segundo)', fontdict=fonteEixo, labelpad=5)
        self.fig2, plt.ylabel('Posição (m)', fontdict=fonteEixo, labelpad=5)

        self.canvas2 = FigureCanvasTkAgg(self.fig2, self.frame2)
        self.canvas2.get_tk_widget().pack()
        plot2()
        
        self.fig3, ax3=plt.subplots(figsize=(12, 8))
        self.fig3, plt.title("Velocidades (X e Y) em função do tempo", loc='left', pad=10, fontdict=fonteTitulo)
        self.fig3, plt.xlim([0, bola.inct/100])
        self.fig3, plt.xlabel('Tempo (em centésimos de segundo)', fontdict=fonteEixo, labelpad=5)
        self.fig3, plt.ylabel('Velocidade (m/s)', fontdict=fonteEixo, labelpad=5)

        self.canvas3 = FigureCanvasTkAgg(self.fig3, self.frame3)
        self.canvas3.get_tk_widget().pack()
        plot3()
        
        self.fig4, ax4=plt.subplots(figsize=(12, 8))
        self.fig4, plt.title("Acelerações (X e Y) em função do tempo", loc='left', pad=10, fontdict=fonteTitulo)
        self.fig4, plt.xlim([0, bola.inct/100])
        self.fig4, plt.xlabel('Tempo (em centésimos de segundo)', fontdict=fonteEixo, labelpad=5)
        self.fig4, plt.ylabel('Aceleração (m/s²)', fontdict=fonteEixo, labelpad=5)

        self.canvas4 = FigureCanvasTkAgg(self.fig4, self.frame4)
        self.canvas4.get_tk_widget().pack()
        plot4
        
        self.fig5, ax5=plt.subplots(figsize=(12, 8))
        self.fig5, plt.title("Distância em função do tempo", loc='left', pad=10, fontdict=fonteTitulo)
        self.fig5, plt.xlim([0, bola.inct/100])
        self.fig5, plt.xlabel('Tempo (em centésimos de segundo)', fontdict=fonteEixo, labelpad=5)
        self.fig5, plt.ylabel('Distância (m)', fontdict=fonteEixo, labelpad=5)

        self.canvas5 = FigureCanvasTkAgg(self.fig5, self.frame5)
        self.canvas5.get_tk_widget().pack()
        plot5()

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
        exit

    def onClosingbotao(self):
        self.janelaPrincipal.destroy()
        aprofundamentoGUI(bola=bola)

class inicioGUI:
    
    def __init__(self):    

        self.janelaPrincipal = tk.Tk()
        self.janelaPrincipal.geometry("933x720")
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

        self.button = tk.Button(self.conteudo, text="Iniciar", font=('Arial', 18), command=lambda:self.iniciar(robo))
        self.button.pack(padx=10, pady=10)

        self.conteudo.pack(expand=1)
    
        self.janelaPrincipal.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.janelaPrincipal.mainloop()

    def iniciar(self, robo):
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
        self.janelaAprofundamento.geometry("933x720")
        self.janelaAprofundamento.title("Projeto OraBolas")
        
        self.titulo = tk.Label(self.janelaAprofundamento, text="Aprofundamento", font=('Inter', 32))
        self.titulo.pack(padx=10, pady=10, anchor="nw")

        self.botAprofundamento = tk.Button(self.janelaAprofundamento, text="Gráficos >", font=('inter', 14), command=self.onClosingbotao)
        self.botAprofundamento.pack(anchor='se', padx=5)

        self.tituloSlider = tk.Label(self.janelaAprofundamento, text="Tempo (em centésimos de segundo)", font=('Inter', 20))
        self.tituloSlider.pack()

        self.valorDoSlider = tk.IntVar()

        self.slider = tk.Scale(self.janelaAprofundamento, variable=self.valorDoSlider, from_=0, to=(bola.inct/100), orient=HORIZONTAL, length="1000")
        self.slider.pack(anchor=CENTER)

        self.botaoAtualizar = tk.Button(self.janelaAprofundamento, text="Atualizar valores", font=('Inter', 20), bg='blue', command=self.atualizar)
        self.botaoAtualizar.pack(anchor=CENTER, pady=5)

        self.labelteste = tk.Label(self.janelaAprofundamento, textvariable=self.valorDoSlider, font=('Inter', 20))
        self.labelteste.pack(anchor=CENTER, pady=10)

        self.varPx_robo = tk.DoubleVar()
        self.varPy_robo = tk.DoubleVar()
        self.varV_robo = tk.DoubleVar()
        self.varA_robo = tk.DoubleVar()
        self.varPx_bola = tk.DoubleVar()
        self.varPy_bola = tk.DoubleVar()
        self.varV_bola = tk.DoubleVar()
        self.varA_bola = tk.DoubleVar()
        self.varFr_robo = tk.DoubleVar()
        self.varAr_bola = tk.DoubleVar()

        self.stringPx_robo = tk.StringVar() 
        self.stringPy_robo = tk.StringVar() 
        self.stringV_robo = tk.StringVar() 
        self.stringA_robo = tk.StringVar() 
        self.stringPx_bola = tk.StringVar() 
        self.stringPy_bola = tk.StringVar() 
        self.stringV_bola = tk.StringVar()
        self.stringA_bola = tk.StringVar()
        self.stringFr_robo = tk.StringVar()
        self.stringAr_bola = tk.StringVar()

        self.labelFrame = tk.LabelFrame(self.janelaAprofundamento, labelanchor='n', font=('Inter', 16))
        self.labelFrame.pack(ipadx=1300, ipady=600)

        self.labelFrame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.labelFrame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.labelPx_robo = tk.Label(self.labelFrame, textvariable=self.stringPx_robo,font=('Inter', 16))
        self.labelPx_robo.grid(row=0, column=1, sticky='w')
        self.labelPy_robo = tk.Label(self.labelFrame, textvariable=self.stringPy_robo, font=('Inter', 16))
        self.labelPy_robo.grid(row=1, column=1, sticky='w')
        self.labelV_robo = tk.Label(self.labelFrame, textvariable=self.stringV_robo, font=('Inter', 16))
        self.labelV_robo.grid(row=2, column=1, sticky='w')
        self.labelA_robo = tk.Label(self.labelFrame, textvariable=self.stringA_robo, font=('Inter', 16))
        self.labelA_robo.grid(row=3, column=1, sticky='w')
        self.labelFr_robo = tk.Label(self.labelFrame, textvariable=self.stringFr_robo, font=('Inter', 16))
        self.labelFr_robo.grid(row=4, column=1, sticky='w')

        self.labelPx_bola = tk.Label(self.labelFrame, textvariable=self.stringPx_bola, font=('Inter', 16))
        self.labelPx_bola.grid(row=0, column=3, sticky='w')
        self.labelPy_bola = tk.Label(self.labelFrame, textvariable=self.stringPy_bola, font=('Inter', 16))
        self.labelPy_bola.grid(row=1, column=3, sticky='w')
        self.labelV_bola = tk.Label(self.labelFrame, textvariable=self.stringV_bola, font=('Inter', 16))
        self.labelV_bola.grid(row=2, column=3, sticky='w')
        self.labelA_bola = tk.Label(self.labelFrame, textvariable=self.stringA_bola, font=('Inter', 16))
        self.labelA_bola.grid(row=3, column=3, sticky='w')
        self.labelAr_bola = tk.Label(self.labelFrame, textvariable=self.stringAr_bola, font=('Inter', 16))
        self.labelAr_bola.grid(row=4, column=3, sticky='w')

        self.labelObs = tk.Label(self.labelFrame, text="*F -> força aplicada pelo robô ao entrar em contato com um objeto\n**A -> aceleração causada pelo impacto do robô na bola caso ocorra no tempo indicado", font=('Inter', 8), anchor='w')
        self.labelObs.grid(column=0, row=5, columnspan=2, sticky='sw', pady=5, padx=5)

        self.janelaAprofundamento.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.janelaAprofundamento.mainloop()

    def onClosing(self):
        self.janelaAprofundamento.destroy()
        exit

    def onClosingbotao(self):
        self.janelaAprofundamento.destroy()
        graficosGUI(bola=bola)

    def atualizar(self):
        if robo.pos_x0 >= bola.retornaPosX(0):
            self.varPx_robo.set(robo.pos_x0 - (robo.retornaAlcance(self.valorDoSlider.get()) * (velMedia*cos(th))))
            self.varPy_robo.set(robo.pos_y0 - (robo.retornaAlcance(self.valorDoSlider.get()) * (velMedia*sin(th))))
        else:
            self.varPx_robo.set(robo.pos_x0 + (robo.retornaAlcance(self.valorDoSlider.get()) * (velMedia*cos(th))))
            self.varPy_robo.set(robo.pos_y0 + (robo.retornaAlcance(self.valorDoSlider.get()) * (velMedia*sin(th))))
        if self.valorDoSlider.get() == 0:
            self.varPx_robo.set(robo.pos_x0)
            self.varPy_robo.set(robo.pos_y0)
        self.varV_robo.set(robo.retornaVelocidade(self.valorDoSlider.get()))
        self.varA_robo.set(robo.aceleracao)
        self.varFr_robo.set(robo.massa * self.varV_robo.get())
        self.varPx_bola.set(bola.retornaPosX(self.valorDoSlider.get()))
        self.varPy_bola.set(bola.retornaPosY(self.valorDoSlider.get()))
        self.varV_bola.set(sqrt(bola.retornaVelX(self.valorDoSlider.get())**2 + bola.retornaVelY(self.valorDoSlider.get())**2))
        self.varA_bola.set(sqrt(bola.retornaAclX(self.valorDoSlider.get())**2 + bola.acel_y**2))
        self.varAr_bola.set(self.varFr_robo.get() * bola.massa)

        self.stringPx_robo.set(f"Posição do robô em X: {self.varPx_robo.get():.2f}m")
        self.stringPy_robo.set(f"Posição do robô em Y: {self.varPy_robo.get():.2f}m")
        self.stringV_robo.set(f"Velocidade do robô: {self.varV_robo.get():.2f}m/s")
        self.stringA_robo.set(f"Aceleração do robô: {self.varA_robo.get():.2f}m/s²")
        self.stringFr_robo.set(f"F* do robô: {self.varFr_robo.get():.2f}N")

        self.stringPx_bola.set(f"Posição da bola em X: {self.varPx_bola.get():.2f}m")
        self.stringPy_bola.set(f"Posição da bola em Y: {self.varPy_bola.get():.2f}m")
        self.stringV_bola.set(f"Velocidade da bola: {self.varV_bola.get():.2f}m/s")
        self.stringA_bola.set(f"Aceleração da bola: {self.varA_bola.get():.2f}m/s²")
        self.stringAr_bola.set(f"A** da bola: {self.varAr_bola.get():.2f}m/s²")
# -------------------------------------------

# ---- INICIALIZAÇÃO DOS OBJETOS PARA EXECUÇÃO DO PROGRAMA PRINCIPAL ----

robo = Robo()

bola = Bola()

# -----------------------------------------------------------------------

inicioGUI() # INICIALIZAÇÃO DA INTERFACE GRÁFICA DO INÍCIO DO PROGRAMA

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

graficosGUI(bola=bola)
