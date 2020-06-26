from tkinter import ttk
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import networkx as nx
import numpy as np
import string
import matplotlib.pyplot as plt
import application as app
from pandas import *


#Formata a impressão da matriz para um modelo mais bonito.
def generateText(result):
    a = result
    s = [[str(e) for e in row] for row in a]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = u'          '.join(u'{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    text = u'\n\n'.join(table)

    return text
        

def start():
    
    #Pega o valor dos campos coluna e linha informados pelo usuário
    entrada_dados = '{}{}'.format(column.get(),line.get())
    #Inicia um Grafo 
    G = nx.Graph()
    #Utiliza a função de inicialização do grafo, implementada em application
    app.initiateGraph(G)
    #Utiliza os valores informados pelo usuário nas funcöes que buscam a solução do passeio do cavalo.
    solution = app.convert_solution(app.find_solution(G, entrada_dados),G)    
    #Como o retorno acima, gera um texto para que seja impresso o tabuleiro de forma mais adequada
    text = generateText(solution)

    #Inicia a janela de resultado do programa.
    janela_resultado = tk.Toplevel()
    janela_resultado.title("Passeio do Cavalo - Grafos")
    janela_resultado.iconbitmap(r'horse.ico')
    janela_resultado.geometry("908x400")
    f = Frame(janela_resultado, width = 800)
    f.pack(pady=(10,0), fill = BOTH)
    filename = PhotoImage(file = "frame2.png")
    canvas = Canvas(janela_resultado, height = 279, width = 420)
    canvas.create_image(0,0,anchor = NW,image =filename)
    canvas.create_text(10,-2,anchor = NW, text= text)
    canvas.pack(padx = 30, pady =10)

    button = tk.Button(janela_resultado,
                       text="SAIR",
                       fg="red",
                       command=janela_resultado.destroy,
                       width=15)
    button.pack()
    janela_resultado.mainloop()




janela = tk.Tk()
janela.title("Passeio do Cavalo - Grafos")
janela.iconbitmap(r'horse.ico')
janela.geometry("590x400+400+100")



lbl = Label(janela,text = "Informe a posição inicial da peça:")
lbl.grid(column = 0, row = 0,sticky = W, padx = 26,pady = 15)
label_line = tk.Label(janela,
                    text = "Linha")
label_line.grid(column=0, row=1, padx=26, pady=0)
line = ttk.Combobox(janela,state="readonly",
                      values=[
                                    "0",
                                    "1",
                                    "2",
                                    "3",
                                    "4",
                                    "5",
                                    "6",
                                    "7"]
                                    )
line.current(0)
line.grid(column=0, row=3,padx=26, pady=0)

label_column = tk.Label(janela,
                    text = "Coluna")
label_column.grid(column=10, row=1, padx=26)
column = ttk.Combobox(janela,state="readonly",
                      values=[
                                    "A",
                                    "B",
                                    "C",
                                    "D",
                                    "E",
                                    "F",
                                    "G",
                                    "H",])
column.current(0)
column.grid(column=10, row=3, padx=26)



load = Image.open('chessboard.png')
render = ImageTk.PhotoImage(load)
img = Label(janela,image = render)
img.grid(column= 0, row = 7, padx = 26, pady = 20)

button = tk.Button(janela,
                   text="INICIAR",
                   fg="green",
                   command=start,
                   width = 15)
button.grid(column=10,row=20, pady = 20)

button = tk.Button(janela,
                   text="SAIR",
                   fg="red",
                   command=janela.destroy,
                   width = 15)
button.grid(column=20,row=20, pady = 20)
janela.mainloop()
