from tkinter import * 
import math
import numpy as np
from TkToolTip import ToolTip


root = Tk()
root.title('Калькулятор')
root.geometry('238x239')
root.resizable(False, False)

var_T = DoubleVar(value=10)
var_k = DoubleVar(value=4)
var_t = DoubleVar(value=7)
var_proc = DoubleVar(value=5)
var_E = DoubleVar(value=70)


def print_matrix_join(matrix):
    for row in matrix:
        print(' '.join(f"{x:6.2f}" for x in row))
    return

def calc(T, t, k, Pr, E):
  k = int(k)
  t = int(t)
  n = 10
  Pr = Pr/100
  tn = T/n
  sigma = 0.1
  u = math.exp(sigma * math.sqrt(T/n))
  d = 1/u
  p = (math.exp((Pr*tn))- d)/(u-d)
  q = 1 - p
#######
  prStavka = np.zeros((n+1, n+1))
  prStavka[n][0] = Pr*100

  j = 1
  for i in range(n-1, -1, -1):
      prStavka[i][j] = prStavka[i+1][j-1] * u 
      j = j + 1

  for i in range(n, -1, -1):  
    for j in range(1, n+1):  
        if prStavka[i][j] == 0:  
            prStavka[i][j] = prStavka[i][j-1] * d
########
  ZCB10 = np.zeros((n+1, n+1))
  for i in range(0, n+1):
    ZCB10[i][n] = 100

  g = 1
  for j in range(n-1, -1, -1): 
    for i in range(g, n+1):
        ZCB10[i][j] = (p * (ZCB10[i-1][j+1])/100 + q * (ZCB10[i][j+1])/100) / (1 + (prStavka[i][j])/100)
        ZCB10[i][j] = ZCB10[i][j]*100
    if j > 0: 
        g = g + 1
    if ZCB10[10][0] < 0:
      lblPriceResult.config(text=f"{0:.2f}%")
    else:
      lblPriceResult.config(text=f"{ZCB10[10][0]:.2f}%")
########

  ZCBt = np.zeros((t+1, t+1))
  for i in range(0, t+1):
    ZCBt[i][t] = 100
  
  rows = prStavka.shape[0]
  prStavkaС = prStavka[rows-(t+1):rows, 0:(t+1)].copy()

  g = 1
  for j in range(t-1, -1, -1): 
    for i in range(g, t+1):
        ZCBt[i][j] = (p * (ZCBt[i-1][j+1])/100 + q * (ZCBt[i][j+1])/100) / (1 + (prStavkaС[i][j])/100)
        ZCBt[i][j] = ZCBt[i][j]*100
    if j > 0: 
        g = g + 1
  lbl6Result.config(text=f"{(ZCB10[10][0]/ZCBt[t][0])*100:.2f}%")
########
 
  rows = ZCB10.shape[0]
  ZCB10C = ZCB10[rows-(k+1):rows, 0:(k+1)].copy()

  futV = ZCB10C

  g = 1
  for j in range(k-1, -1, -1): 
    for i in range(g, k+1):
        futV[i][j] = p * (futV[i-1][j+1])/100 + q * (futV[i][j+1])/100
        futV[i][j] = futV[i][j]*100
    if j > 0: 
        g = g + 1
  lbl7Result.config(text=f"{futV[k][0]:.2f}%")
########

  opCall = np.zeros((k+1, k+1))
  for i in range(0, k+1):
    opCall[i][k] = max(0, futV[i][k] - E)

  g = 1
  for j in range(k-1, -1, -1): 
    for i in range(g, k+1):
        a = p * (opCall[i-1][j+1]/100)
        b = q * (opCall[i][j+1]/100)
        c = math.exp((Pr*T)/k)
        d = futV[i][j]/100 - E/100
        opCall[i][j] = max((a + b)/(c), max(0, d))
        opCall[i][j] = opCall[i][j] * 100
    if j > 0: 
        g = g + 1

  lbl8Result.config(text=f"{opCall[k][0]:.2f}%")
  #return print(f"{print_matrix_join(futV)}\n{print_matrix_join(ZCB10C)} \n{print_matrix_join(opCall)}")
  return print("☼")



lblT = Label(root, text='T = ')
lblk = Label(root, text='k = ')
lblt = Label(root, text='t = ')
lblPr = Label(root, text='% = ')
lblT.place(x=20,y=0)
lblk.place(x=20,y=25)
lblt.place(x=22,y=50)
lblPr.place(x=129,y=0)
edtT = Spinbox(root, from_=0, to=100, increment=1, width=5, textvariable=var_T, state='readonly')
edtk = Spinbox(root, from_=0, to=10, increment=1, width=5, textvariable=var_k, state='readonly')
edtt = Spinbox(root, from_=0, to=10, increment=1, width=5, textvariable=var_t, state='readonly')
edtPr = Spinbox(root, from_=0, to=100, increment=0.5, width=5, textvariable=var_proc, state='readonly')
edtT.place(x=52,y=0)
edtk.place(x=52,y=25)
edtt.place(x=52,y=50)
edtPr.place(x=158,y=0)

lblPrice = Label(root, text='Цена ZCB₁₀: ')
lblPriceResult = Label(root, text='№№№')
lblPrice.place(x=20,y=100)
lblPriceResult.place(x=98,y=100)

lblE = Label(root, text='E = ')
edtE = Spinbox(root, from_=0, to=100, increment=0.5, width=5, textvariable=var_E, state='readonly')
lblE.place(x=133,y=25)
edtE.place(x=158,y=25)

lbl6 = Label(root, text='Форвард: ')
lbl6.place(x=20,y=125)
lbl6Result = Label(root, text='№№№')
lbl6Result.place(x=98,y=125)

lbl7 = Label(root, text='Фьючерс: ')
lbl7.place(x=20,y=150)
lbl7Result = Label(root, text='№№№')
lbl7Result.place(x=98,y=150)


lbl8 = Label(root, text='Опцион Call: ')
lbl8.place(x=20,y=175)
lbl8Result = Label(root, text='№№№')
lbl8Result.place(x=98,y=175)

btn1 = Button(root, text='Результат', command=lambda: calc(float(edtT.get()),float(edtt.get()),float(edtk.get()), float(edtPr.get()),float(edtE.get())))
btn1.place(x=85,y=200)




ToolTip(lblT, text="T — срок модели (лет). Используется для построения 10-периодной биномиальной модели процентной ставки.", delay=0.5)
ToolTip(lblt, text="t — момент исполнения форвардного контракта на бескупонную облигацию ZCB10.", delay=0.5)
ToolTip(lblk, text="k — момент исполнения фьючерсного контракта на облигацию ZCB10.", delay=0.5)
ToolTip(lblPr, text="r₀ — начальная процентная ставка (%). Используется для построения дерева ставок.", delay=0.5)
ToolTip(lblE, text="E — страйк опциона (%). Цена исполнения опциона Call на фьючерс.", delay=0.5)
ToolTip(lblPrice, text="Цена 10-летней бескупонной облигации ZCB10, рассчитанная по биномиальной модели ставок.", delay=0.5)
ToolTip(lbl6, text="Форвардная цена облигации ZCB10 с исполнением в момент времени t.", delay=0.5)
ToolTip(lbl7, text="Цена фьючерса на облигацию ZCB10 с исполнением в момент времени k (без дисконтирования).", delay=0.5)
ToolTip(lbl8, text="Цена американского опциона Call на фьючерс на облигацию ZCB10.", delay=0.5)

root.mainloop()