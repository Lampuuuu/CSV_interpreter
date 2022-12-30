# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 20:56:17 2022

@author: glink
"""

import numpy as np
import matplotlib.pyplot as plt
import DyMat
import re
import pandas as pd
import natsort as ns

def get_profile(filename, what, when):
    res = DyMat.DyMatFile(filename)
    (time, time_name, time_description)=res.abscissa(list(res.names())[0])
    df = pd.DataFrame(columns=[time_name],data=time)
    index_time_plot=((df[time_name]-when)**2).idxmin()
    
    pattern = re.compile(what)
    vars=[]
    for var in res.names():
        if pattern.fullmatch(var) != None:
            #print(var, type(var))
            vars.append(var)
            df[var] = res.data(var)
    vars = ns.natsorted(vars)        
    profile = df[vars].loc[index_time_plot,:]
    return(profile)

def get_timeseries(filename, what):
    res = DyMat.DyMatFile(filename)
    (time, time_name, time_description)=res.abscissa(list(res.names())[0])
    df = pd.DataFrame(columns=[time_name],data=time)
    n_steps = len(time)
    pattern = re.compile(what)
    vars=[]
    for var in res.names():
        if pattern.fullmatch(var) != None:
            vars.append(var)
            if len(res.data(var))==n_steps:
                df[var] = res.data(var)
            else:
                df[var] = np.ones(n_steps)*res.data(var)[0]
    timeseries = df[vars].loc[:,:]
    return(timeseries, time, vars)
    

# Pfad zum Result-File: Siehe Arbeitsverzeichnis von OMEdit (Optionen->Allgemeine)
filename = "/tmp/OpenModelica_jens/OMEdit/HeatConduction.Heat_Cond_Compare/Heat_Cond_Compare_res.mat"


# Mit "what" wird ein regulärer Ausdruck, also ein Muster, übergeben (--> Google)
# ".*" bedeutet beliebiges Zeichen, beliebig oft --> alles einlesen

what = '.*'; (data, time, names) = get_timeseries(filename, what)

print(names) # Alle Namen im Datensatz ausgeben (braucht man nur, um die Variablen zu finden)


# Alle möglicherweise noch offenen Plot-Fenster schließen:
for i in range(0,10): plt.close(i)

plt.figure(1)

# Hier wird zunächst die Temperatur des 50. Elementes bei Stahl über der Zeit geplottet (über
# aluminium.n_disc klönnte man auch die Anzahl der Diskretisierungselemente auslesen):
plt.plot(time, data["steel.T[50]"]) 

# Jeder nachfolgende Plot-Befehl geht in das gleiche Fenster, hier in grün 
# mit Strichpunktlinie (nur um das Prinzip zu zeigen, wie man den 
# Linesyle ändert, siehe Doku matplotlib (--> Google)):
plt.plot(time, data["aluminium.T[50]"], color='green', linewidth=4, linestyle='dashdot') 
plt.grid()
plt.title('Temperaturen')
plt.xlabel('time [s]')
plt.ylabel('Temperature [K]')
# Zeitachse etwas kompakter darstellen:
axes = plt.gca()
axes.set_xlim([0, max(time)])

# Legende Hinzufügen
plt.legend(['T[50] Stahl', 'T[50] Aluminium'])


# Mit numpy, gradient kann man z.B. die Ableitung berechnen: diff berechnet einen Vektor mit 
# den Differenzen zwischen den benachbarten Elementen eines Vektors. Das Ergebnis 
# hat dann ein Element weniger als der ursprüngliche Vektor. Deshalb muss beim 
# Plotten auch der Zeitvektor um ein Element reduziert werden.


plt.figure(2)

dT_dx_Aluminium = np.gradient(data["aluminium.T[50]"], time)
dT_dx_Stahl     = np.gradient(data["steel.T[50]"], time)

     
plt.plot(time, dT_dx_Aluminium)     
plt.plot(time, dT_dx_Stahl)     

# Natürlich können Sie die Plots auch in sehr vielen Formaten abspeichern und zwar in :
plt.figure(1) # Anwählen der ersten Abbildung zum Abspeichern
# 1.) Vektor-Formate, u.a. pdf und svg (Office kann seit Version 2016 auch mit svg umgehen)
plt.savefig('test.pdf')
plt.savefig('test.svg')

# 2.) Bitmap-Formate, u.a. jpg und png (weniger "schön" als Vektor, da pixelig bzw recht groß)
plt.savefig('test_grob.jpg')
plt.savefig('test_fein.jpg', dpi=300)
plt.savefig('test_grob.png')
plt.savefig('test_fein.png', dpi=300)

#########################
# Plotten von Profilen

L =  data['aluminium.length'][0]
n_disc = data['aluminium.n_disc'][0]
# Damit linspace funktioniert, muss n_disc als Integer übergeben werden

x = np.linspace(0,L,int(n_disc))


T_Aluminium_Ende = get_profile(filename, 'aluminium.T\[.*\]', 1e5)

plt.figure(3)
plt.plot(x, T_Aluminium_Ende)

# Hier ein Beispiel, wie man mehrere Profile zu unterschiedlichen Zeitpunkten in
# ein Diagramm plotten kann:

plt.figure(4)
t_ende = max(time)
n_Zeitpunkte = 10
Zeitpunkte = np.linspace(0, t_ende, n_Zeitpunkte)

text_legend=[]
for t in Zeitpunkte:
    T_Aluminium  = get_profile(filename, 'aluminium.T\[.*\]', t)
    plt.plot(x, T_Aluminium)
    text_legend.append('t = {:6.1f}s'.format(t))
plt.legend(text_legend)