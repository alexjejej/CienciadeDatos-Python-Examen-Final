"""
Created on Thu Jun 29 14:41:34 2023

@author: alexg
"""

import csv
from datetime import datetime, date
import sys
import matplotlib.pyplot as plt
import numpy as np


def parse_csv(datos, select = None, types = None, has_headers = True, silence_errors = False):
    '''
    Parsea un archivo CSV en una lista de registros.
    Se puede seleccionar sólo un subconjunto de las columnas, determinando el parámetro select, 
    que debe ser una lista de nombres de las columnas a considerar.
    '''
    filas = csv.reader(datos)

        # Lee los encabezados del archivo en caso de poner false en has_headers
    if has_headers:
            encabezados = next(filas)

            # Si se indicó un selector de columnas,
            # buscar los índices de las columnas especificadas.
            # Y en ese caso achicar el conjunto de encabezados para diccionarios
    
            if select:
                indices = [encabezados.index(nombre_columna) for nombre_columna in select]
                encabezados = select
            else:
                indices = []
    
            registros = []
            for fila in filas:
                if not fila:    # Saltear filas vacías
                    continue
                
                #Atrapar los errores del tipo ValueError
                try:
                    
                    # Filtrar la fila si se especificaron columnas
                    if indices:
                        fila = [fila[index] for index in indices]
                    if types:
                        fila = [func(val) for func, val in zip(types, fila) ]
                    # Armar el diccionario
                    registro = dict(zip(encabezados, fila))
                    registros.append(registro)
                
                except ValueError as e:
                    #En caso de silenciar errores:
                    if not silence_errors:    
                        print(f'No pude convertir {fila}')
                        print("Motivo: ", e)
        #En caso de tener headers
    else:
            
            #Si se manda como parametro que seleccione y a su vez que no hay encabezado
            if select:
                raise RuntimeError("Para seleccionar, necesito encabezados")
            else:
                registros = []
                for fila in filas:
                    if not fila:    # Saltear filas vacías
                        continue                   
                    #Atrapar los errores del tipo ValueError
                    try:
                        # Armar la lista de tuplas
                        if types:
                            fila = [func(val) for func, val in zip(types, fila) ]
                        registros.append(tuple(fila))
                        
                    except ValueError as e:
                        #En caso de silenciar errores:
                        if not silence_errors:    
                            print(f'No pude convertir {fila}')
                            print("Motivo: ", e)
    return registros

def leer_archivo(nombre_archivo):
    '''
    Procesa el archivo 
    '''
    archivo = []
    archivo_dicts = []
    with open(nombre_archivo) as archivo:
        archivo_dicts = parse_csv(archivo)
        
    return archivo_dicts

def fecha_limite(anios):
    '''
    Devuelve la fecha de hoy en formato '%d/%m/%Y'
    '''
    #Obtenemos fecha hoy
    hoy = date.today()
    limiteanio = hoy.year - int(anios)
    limitefecha = date(year = limiteanio, month = hoy.month, day = hoy.day)
    fecha = str(limitefecha)
    fechaformato = datetime.strptime(fecha, '%Y-%m-%d')
    return fechaformato
    
def CursadaAprobada(datos,anios):
    '''
    A partir de un conjunto de datos leidos de un csv imprime
    los nombres de aquelles alumnes que hayan aprobado la cursada 
    hace m ́as de N años pero que nunca rindieron el final.
    '''
    fecha = fecha_limite(anios)
    
    for registro in datos:
        
        registrofecha = datetime.strptime(registro["fecha_fin_cursada"], '%Y-%m-%d')
        
        if (registro["nota_final"]=="" and registrofecha>=fecha):
            print(registro["nombre"])
        
def scatter(datos):
    '''
    Crea un scatter a partir de una lista de datos dados
    '''
    #Ponemos el titulo y los ejes
    plt.title("Examen final vs meses")
    y = []
    x = []
    datosnuevos = []
    plt.xlabel('Diferencia de meses')
    plt.ylabel('Nota final')
    
    #Accedemos a los datos
    for registro in datos:
        if (registro["nota_final"]==""):
            continue
        else:
            #obtenemos la fecha en tipo datetime
            fechafin = datetime.strptime(registro["fecha_fin_cursada"], '%Y-%m-%d')
            fechafinal = datetime.strptime(registro["fecha_final"], '%Y-%m-%d')
            #diferencia de meses
            diferencia = (fechafinal.year - fechafin.year) * 12 + fechafinal.month - fechafin.month
            #Agregamos los datos a un lote
            lote = [int(registro["nota_final"]),diferencia]
            datosnuevos.append(lote)
    
    #ordenamos la tupla
    ordenados = sorted(datosnuevos, key=lambda llave: llave[0])
    for i in ordenados:    
        y.append(i[1])
        x.append(i[0])
    plt.plot(y,x,'o')
    plt.show()

Archivo = leer_archivo('../Data/EstudiantesAprobados.csv')
scatter(Archivo)
CursadaAprobada(Archivo, 2)


def f_principal(parametros):
    Archivo = leer_archivo(parametros[1])
    CursadaAprobada(Archivo, parametros[2])
    scatter(Archivo)


#%%
#Sólo si el script está siendo ejecutado como el script principal
if __name__ == '__main__':
    if len(sys.argv) == 3:
        f_principal(sys.argv)
    else:
        print(f"Error, formato incorrecto. Formato correcto: {sys.argv[0]}, Archivo, Años")