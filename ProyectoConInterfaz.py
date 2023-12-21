import numpy as np
import itertools
from collections import defaultdict
import streamlit as st
from scipy.stats import wasserstein_distance

st.title("GRAN PROYECTO DE UNOS ESTUDIANTES GANADORES")

#---------------------------------------------------------------------------------------------------

# Matriz de transición proporcionada
trans_matrix = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 1],
                         [0, 0, 0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0, 0]])

# Espacio para mostrar matriz
st.write("Matriz:")
st.write(trans_matrix)


combinaciones =[(0,0,0),(1,0,0),(0,1,0),(1,1,0),(0,0,1),(1,0,1),(0,1,1),(1,1,1)]



#------- ELIMINA DE LA COMBINACION DE PROXIMOS, EL PROXIMO QUE NO SE NECESITA---------------------------------
def eliminar_proximos_sin_usar(combinaciones, indices=None):
    if indices is None:
        return "No se han proporcionado índices para eliminar", combinaciones

    combinaciones_modificadas = combinaciones.copy()
    for indice in sorted(indices, reverse=True):
        combinaciones_modificadas = [tupla[:indice] + tupla[indice + 1:] for tupla in combinaciones_modificadas]

    return combinaciones_modificadas



#------------- Eliminar duplicados  ----------------------------------
def juntarProximosRepetidos(combinaciones_resultantes):
  nueva_lista_sin_duplicados = []
  conjunto_visto = set()
  for dupla in combinaciones_resultantes:
      if dupla not in conjunto_visto:
          nueva_lista_sin_duplicados.append(dupla)
          conjunto_visto.add(dupla)
  return nueva_lista_sin_duplicados

#---------------- Identificar las posiciones de las duplicaciones ---------------------------
def posicionesDuplicadas(combinaciones_resultantes):
  posiciones_duplicadas = defaultdict(list)
  for i, dupla in enumerate(combinaciones_resultantes):
      posiciones_duplicadas[dupla].append(i)

  # Obtener la lista de posiciones de duplicados
  lista_posiciones_duplicadas = [(posiciones[0], posiciones[1]) for posiciones in posiciones_duplicadas.values() if len(posiciones) > 1]
  return lista_posiciones_duplicadas

#---------------- Crea metriz con suma de combinaciones repetidas y matriz mandada ---------------------------
def eliminar_proximo(trans_matrix, lista_posiciones_duplicadas):
    matriz_resultante = np.zeros((8, len(lista_posiciones_duplicadas)))

    for idx, posiciones in enumerate(lista_posiciones_duplicadas):
        matriz_resultante[:, idx] = np.sum(trans_matrix[:, posiciones], axis=1)

    return matriz_resultante

def eliminar_actual(trans_matrix, lista_posiciones_duplicadas):
    matriz_resultante = np.zeros((len(lista_posiciones_duplicadas), trans_matrix.shape[1]))

    for idx, posiciones in enumerate(lista_posiciones_duplicadas):
        matriz_resultante[idx, :] = np.sum(trans_matrix[posiciones, :], axis=0) / len(posiciones)

    return matriz_resultante

def eliminarVacioActual(matriz):
    matriz_resultante = np.sum(matriz, axis=0) / matriz.shape[0]
    return matriz_resultante

def eliminarVacioProximo(matriz):
    matriz_resultante = np.sum(matriz, axis=1, keepdims=True)
    return matriz_resultante








#-----------------------------------------

def marginacionEstadoActual(columnas_a_eliminar_actual, matriz_proximo_eliminado,claveDescomposicion): #[
  combinaciones_resultantes_columnas = combinaciones
  segundoEliminar = False
  for columna in columnas_a_eliminar_actual:
      
      claveDescomposicion[columna+3] = 0
      print("Key estado con actual: ",claveDescomposicion)
      
      if segundoEliminar:
          columna -= 1
      else:
          segundoEliminar = True

      indice_a_eliminar_columna = [columna]

      combinaciones_resultantes_columnas = eliminar_proximos_sin_usar(combinaciones_resultantes_columnas, indice_a_eliminar_columna)

      print("\nCombinaciones Resultantes para Columnas:")
      print(combinaciones_resultantes_columnas)

      nueva_lista_sin_duplicados_columnas = juntarProximosRepetidos(combinaciones_resultantes_columnas)
      lista_posiciones_duplicadas_columnas = posicionesDuplicadas(combinaciones_resultantes_columnas)
      combinaciones_resultantes_columnas = nueva_lista_sin_duplicados_columnas
      print("Nueva lista sin duplicados para Columnas:", nueva_lista_sin_duplicados_columnas)
      print("Posiciones de duplicados para Columnas:", lista_posiciones_duplicadas_columnas)

      matriz_proximo_eliminado = eliminar_actual(matriz_proximo_eliminado, lista_posiciones_duplicadas_columnas)

      print("\nMatriz Resultante después de eliminar columna:")
      print(matriz_proximo_eliminado)
      
      
  return combinaciones_resultantes_columnas, matriz_proximo_eliminado,claveDescomposicion


def marginacionEstadoProximo(proximos_a_eliminar,claveDescomposicion): #  ?/ABC  [?,?,?,1,1,1]

  proximos_a_eliminar.sort()
  
  matriz_proximo_eliminado =[]
  combinaciones_resultantes = combinaciones
  matriz_proximo_eliminado = trans_matrix
  segundoEliminar = False
  for proximo in proximos_a_eliminar:
      
    claveDescomposicion[proximo] = 0
    print("Key estado solo con proximo: ",claveDescomposicion)

    if segundoEliminar:
        proximo -= 1
    else:
        segundoEliminar = True
        
    

    indice_a_eliminar = [proximo]

    combinaciones_resultantes = eliminar_proximos_sin_usar(combinaciones_resultantes, indice_a_eliminar)

    print("COMBINACION RESULTANTE")
    print(combinaciones_resultantes)


    nueva_lista_sin_duplicados  = juntarProximosRepetidos(combinaciones_resultantes)
    lista_posiciones_duplicadas = posicionesDuplicadas(combinaciones_resultantes)
    combinaciones_resultantes = nueva_lista_sin_duplicados
    print("Nueva lista sin duplicados:", nueva_lista_sin_duplicados)
    print("Posiciones de duplicados:", lista_posiciones_duplicadas)

    # Ejemplo de uso
    matriz_proximo_eliminado = eliminar_proximo(matriz_proximo_eliminado, lista_posiciones_duplicadas)


    print("\nMatriz Resultante después de eliminar A:")
    print(matriz_proximo_eliminado)
    
    

  return matriz_proximo_eliminado,claveDescomposicion



def generarListaDescomposiciones(lista):
    ones = [i for i, x in enumerate(lista) if x == 1]
    n = len(ones)
    
    results = []
    for i in range(2**n):
        sub1 = lista[:] 
        sub2 = lista[:]
        
        for j in range(n):
            if (i >> j) % 2 == 1:
                sub1[ones[j]] = 0
                sub2[ones[j]] = 1
            else: 
                sub1[ones[j]] = 1
                sub2[ones[j]] = 0
        
        if sub1.count(1) > 0 and sub2.count(1) > 0:
            if [sub2, sub1] not in results:
                results.append([sub1, sub2])
        
    return results
  
def conversorClaveAEstadosEliminar(lista):
    proximos_a_eliminar_origin  = []
    columnas_a_eliminar_actual = []

    # Procesar las primeras 3 posiciones de la lista
    if lista[:3] != (0, 0, 0):
      for i in range(3):
          if lista[i] == 0:
             proximos_a_eliminar_origin.append(i)
    else:
      proximos_a_eliminar_origin.append(5)

    # Procesar las últimas 3 posiciones de la lista
    if lista[3:] != (0, 0, 0):
      for i in range(3, 6):
          if lista[i] == 0:
              columnas_a_eliminar_actual.append(i - 3)
    else:
      columnas_a_eliminar_actual.append(5)

    return proximos_a_eliminar_origin, columnas_a_eliminar_actual
  
def conversorEstadosEliminarAClave(proximos_a_eliminar, columnas_a_eliminar_actual, estadoACtual):
    lista_resultante = [1, 1, 1, 1, 1, 1]

    if len(proximos_a_eliminar)>0 and proximos_a_eliminar[0]!=5:
      for i in proximos_a_eliminar:
          lista_resultante[i] = 0

    if len(columnas_a_eliminar_actual)>0 and columnas_a_eliminar_actual[0]!=5:
      for j in columnas_a_eliminar_actual:
          lista_resultante[j + 3] = 0

    # Añadir ceros si las listas están vacías
    if not proximos_a_eliminar:
        lista_resultante[:3] = [1,1,1]
    elif proximos_a_eliminar[0]==5:
        lista_resultante[:3] = [0,0,0]


    if not columnas_a_eliminar_actual and len(estadoACtual)==3:
        lista_resultante[3:] = [1,1,1]
    elif columnas_a_eliminar_actual[0]==5:
        lista_resultante[3:] = [0,0,0]

    return lista_resultante

def productoTensor(resultado_en_tuplas):
  resultado = []
  if len(resultado_en_tuplas) == 2:
    print("TOTAL DE LOS TOTALES")
    for elemento_1 in resultado_en_tuplas[0]:
        for elemento_2 in resultado_en_tuplas[1]:
            resultado.append(elemento_1 * elemento_2)
  elif len(resultado_en_tuplas) == 3:
    print("TOTAL DE LOS TOTALES")
    for elemento_1 in resultado_en_tuplas[0]:
        for elemento_2 in resultado_en_tuplas[1]:
          for elemento_3 in resultado_en_tuplas[2]:
            resultado.append(elemento_1 * elemento_2 * elemento_3)
  
  return resultado
    
      


def calculoProbabilidadComposicion(columnas_a_eliminar_actual,proximos_a_eliminar,estadoActual):
  if  len(str(estadoActual)) == 3 and (len(proximos_a_eliminar) == 0 or proximos_a_eliminar[0]!=5) and len(columnas_a_eliminar_actual) >0 and columnas_a_eliminar_actual[0] != 5:
      claveDescomposicion = [1,1,1,1,1,1]
      matrizMarginadoProximos,claveDescomposicion = marginacionEstadoProximo(proximos_a_eliminar,claveDescomposicion)
      posicionSolucion = combinaciones.index(tuple(int(d) for d in str(estadoActual)))
      
      mi_tupla_clave = tuple(claveDescomposicion)
      diccionarioDescomposicion[mi_tupla_clave] = matrizMarginadoProximos[posicionSolucion]
      print("SOLUCION :")
      print(matrizMarginadoProximos[posicionSolucion])
      return matrizMarginadoProximos[posicionSolucion]
      
  #Proceso cuando hay un vacio en estado actual   
  elif len(columnas_a_eliminar_actual)>0 and columnas_a_eliminar_actual[0] == 5:
      claveDescomposicion = [1,1,1,0,0,0]
      matrizMarginadoProximos,claveDescomposicion = marginacionEstadoProximo(proximos_a_eliminar,claveDescomposicion)
      resultadoVacioActual= eliminarVacioActual(matrizMarginadoProximos)
      
      mi_tupla_clave = tuple(claveDescomposicion)
      diccionarioDescomposicion[mi_tupla_clave] = resultadoVacioActual
      print("TOTAL cuando hay un vacio en estado actual")
      print(resultadoVacioActual)
      return resultadoVacioActual

  #Proceso cuando hay un vacio en estado proximo  
  elif len(proximos_a_eliminar) > 0 and proximos_a_eliminar[0]==5:
      claveDescomposicion = [0,0,0,1,1,1]
      combinacion, matriz,claveDescomposicion =  marginacionEstadoActual(columnas_a_eliminar_actual, trans_matrix,claveDescomposicion)
      resultadoVacioProximo= eliminarVacioProximo(matriz)
      posicionSolucion = combinacion.index(tuple(int(d) for d in str(estadoActual)))
      
      mi_tupla_clave = tuple(claveDescomposicion)
      diccionarioDescomposicion[mi_tupla_clave] = resultadoVacioProximo[posicionSolucion]
      print("Matriz resultante cuando hay un vacio en estado proximo ")
      print(resultadoVacioProximo)
      print("TOTAL cuando hay un vacio en estado proximo")
      print(resultadoVacioProximo[posicionSolucion])
      return resultadoVacioProximo[posicionSolucion]

      
  else:
      listaSolucion = []
      estadosProximoTotales = [0,1,2]

      set_eliminar = set(proximos_a_eliminar)
      set_estados = set(estadosProximoTotales)
      # Obtener los valores que no se repiten en ambas listas
      estadoProximosCalcular = list(set_estados - set_eliminar)

      print(estadoProximosCalcular)


      for proximos_a_eliminarInt in estadoProximosCalcular:
        
        claveDescomposicion = [1,1,1,1,1,1]
          

        if len(estadoProximosCalcular) == 1: 
          proximos_a_eliminar = proximos_a_eliminar
        else:
          proximos_a_eliminar.append(proximos_a_eliminarInt)
          print(proximos_a_eliminar)
      

        
        matrizMarginadoProximos,claveDescomposicion = marginacionEstadoProximo(proximos_a_eliminar,claveDescomposicion) 
        combinacion, matriz,claveDescomposicion =  marginacionEstadoActual(columnas_a_eliminar_actual, matrizMarginadoProximos,claveDescomposicion)

        posicionSolucion = combinacion.index(tuple(int(d) for d in str(estadoActual)))
        print("SOLUCION PARCIAL------------------------------------------------------:")
        
        print(matriz[posicionSolucion])

        mi_tupla_clave = tuple(claveDescomposicion)
        diccionarioDescomposicion[mi_tupla_clave] = matriz[posicionSolucion]
        
        listaSolucion.append(matriz[posicionSolucion])
    
        proximos_a_eliminar = proximos_a_eliminar_origin.copy()




        matrizResultante = juntarProximosRepetidos(eliminar_proximos_sin_usar(combinaciones,proximos_a_eliminar))
        print(matrizResultante)

        print("Solucion SUBTOTAL para aplicar tensor")

        # Convertir los arrays en tuplas
        resultado_en_tuplas = [tuple(arr) for arr in listaSolucion]

        print(resultado_en_tuplas)


        if len(estadoProximosCalcular) == 1: 
          resultado = matriz[posicionSolucion]
        else:
          resultado = productoTensor(resultado_en_tuplas)
          
      
      return resultado
    

def calcularNuevoEstado(estadoActual,columnas_a_eliminar_actual_original,columnas_a_eliminar_actual):
  diccionarioEstadoUsar = {}

  estados = [0,1,2]

  cont = 0
  for estado in estados:
      if estado in columnas_a_eliminar_actual_original:
          diccionarioEstadoUsar[estado]= "null"
      else:
          diccionarioEstadoUsar[estado]= estadoActual[cont]
          cont += 1

  set_eliminar = set(columnas_a_eliminar_actual)
  set_estados = set(estados)
  # Obtener los valores que no se repiten en ambas listas
  estadoProximo = list(set_estados - set_eliminar)
  valores = [diccionarioEstadoUsar[clave] for clave in estadoProximo]

  # Unir los valores en un string
  resultado = ''.join(valores)

  return resultado
      
# ----------------------------------------------------------------------------------------------
estadoActualOriginal = st.text_input("Estado actual")
proximos_a_eliminar_originTxt = st.text_input("Próximos a eliminar")
try:
    proximos_a_eliminar_origin = [int(x) for x in proximos_a_eliminar_originTxt.split(",")]
except ValueError:
    st.error("Por favor ingrese solo números separados por comas")

columnas_a_eliminar_actual_originalTxt = st.text_input("Actuales a eliminar")
try:
    columnas_a_eliminar_actual_original = [int(x) for x in columnas_a_eliminar_actual_originalTxt.split(",")]
except ValueError:
    st.error("Por favor ingrese solo números separados por comas")


estadoActual = estadoActualOriginal
columnas_a_eliminar_actual = columnas_a_eliminar_actual_original.copy()   
proximos_a_eliminar = proximos_a_eliminar_origin.copy() # BC   C/C

emd_distance_min = 10000000000
descomposicionOptima = ""


diccionarioDescomposicion = {}
claveDescomposicion = [1,1,1,1,1,1]


distribucionOriginal = calculoProbabilidadComposicion(columnas_a_eliminar_actual,proximos_a_eliminar,estadoActual)
print("ORIGINAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL", distribucionOriginal)


claveDistribucionOriginal =  conversorEstadosEliminarAClave(proximos_a_eliminar_origin, columnas_a_eliminar_actual,estadoActual)  

particiones = generarListaDescomposiciones(claveDistribucionOriginal)

for particion in particiones:
    listSubResultadosParticionados = []
    for lista in particion:
      
      parteCombinacionEntrante = tuple(lista)
      
      #Pregunta si esa composicion ya existe en el diccionario o no
      if parteCombinacionEntrante in diccionarioDescomposicion:
        
        valor = diccionarioDescomposicion[parteCombinacionEntrante]
        
        listSubResultadosParticionados.append(valor)
      else:
        proximos_a_eliminar = []
        columnas_a_eliminar_actual = []
        
        proximos_a_eliminar, columnas_a_eliminar_actual = conversorClaveAEstadosEliminar(parteCombinacionEntrante)
        
        estadoActual = calcularNuevoEstado(estadoActualOriginal,columnas_a_eliminar_actual_original,columnas_a_eliminar_actual)
        
        listSubResultadosParticionados.append(calculoProbabilidadComposicion(columnas_a_eliminar_actual,proximos_a_eliminar,estadoActual))

    print("LISTA PARA HACER TENSOR: ")
    resultado_en_tuplas = [tuple(arr) for arr in listSubResultadosParticionados]
    
    productoTensorComposicion = productoTensor(resultado_en_tuplas)
    
    emd_distance = wasserstein_distance(distribucionOriginal, productoTensorComposicion)
    print("EMD:",emd_distance)
    
    if emd_distance == 0:
      emd_distance_min = emd_distance
      descomposicionOptima = particion
      break
      
    elif emd_distance < emd_distance_min:
      emd_distance_min = emd_distance
      descomposicionOptima = particion

# Espacio para mostrar lista
st.write("Descomposición óptima:")
st.write(descomposicionOptima)

# Espacio para mostrar número
st.write("EMD Distance:")  
st.write(emd_distance_min)
      
      
print("SOLUCION OPTMIA: ")
print(emd_distance_min)
print("------------")
print(descomposicionOptima)
      
 
    
    
    
    
    
print("LISTA DE DESCOMPOSICIONES REALIZADAS")

for clave, valor in diccionarioDescomposicion.items():
    print(f"{clave}:")
    for fila in valor:
           print(f"\t{fila}")
    print()
    
    
    





    
#resultado = []
#listaSolucion = [(0.5, 0.5), (1.0, 0.0)]
#print(productoTensor(listaSolucion))