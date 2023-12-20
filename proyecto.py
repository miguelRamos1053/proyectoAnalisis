import numpy as np
import itertools
from collections import defaultdict



# Matriz de transición proporcionada
trans_matrix = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 1],
                         [0, 0, 0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 1, 0, 0, 0, 0]])

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

def marginacionEstadoActual(columnas_a_eliminar_actual, matriz_proximo_eliminado): #[
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
      
      
  return combinaciones_resultantes_columnas, matriz_proximo_eliminado


def marginacionEstadoProximo(proximos_a_eliminar): #  ?/ABC  [?,?,?,1,1,1]

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
    
    

  return matriz_proximo_eliminado


# P(BC | C = 100)

estadoActual = "11"
#posicionEstadoActual = combinaciones.index(tuple(int(d) for d in str(estadoActual)))

proximos_a_eliminar = [0,1] # BC   C/C
columnas_a_eliminar_actual = []

diccionarioDescomposicion = {}

claveDescomposicion = [1,1,1,1,1,1]


if len(str(estadoActual)) == 3:
    claveDescomposicion = [1,1,1,1,1,1]
    matrizMarginadoProximos = marginacionEstadoProximo(proximos_a_eliminar)
    posicionSolucion = combinaciones.index(tuple(int(d) for d in str(estadoActual)))
    print("SOLUCION :")
    print(matrizMarginadoProximos[posicionSolucion])
    
elif not columnas_a_eliminar_actual:
    matrizMarginadoProximos = marginacionEstadoProximo(proximos_a_eliminar)
    resultadoVacioActual= eliminarVacioActual(matrizMarginadoProximos)
    print("TOTAL DE LOS TOTALES")
    print(resultadoVacioActual)
    
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
    

      
      matrizMarginadoProximos = marginacionEstadoProximo(proximos_a_eliminar) #     0-1
      combinacion, matriz =  marginacionEstadoActual(columnas_a_eliminar_actual, matrizMarginadoProximos)

      posicionSolucion = combinacion.index(tuple(int(d) for d in str(estadoActual)))
      print("SOLUCION PARCIAL------------------------------------------------------:")
      
      print(matriz[posicionSolucion])

      mi_tupla_clave = tuple(claveDescomposicion)
      diccionarioDescomposicion[mi_tupla_clave] = matriz[posicionSolucion]

      listaSolucion.append(matriz[posicionSolucion])

      proximos_a_eliminar.pop()




      matrizResultante = juntarProximosRepetidos(eliminar_proximos_sin_usar(combinaciones,proximos_a_eliminar))
      print(matrizResultante)

      print("Solucion SUBTOTAL")

      # Convertir los arrays en tuplas
      resultado_en_tuplas = [tuple(arr) for arr in listaSolucion]

      print(resultado_en_tuplas)


      print("TOTAL DE LOS TOTALES")
      resultado = []
      
      

      if len(resultado_en_tuplas) == 2:
        for elemento_1 in resultado_en_tuplas[0]:
            for elemento_2 in resultado_en_tuplas[1]:
                resultado.append(elemento_1 * elemento_2)
        print(resultado)
      elif len(resultado_en_tuplas) == 3:
        for elemento_1 in resultado_en_tuplas[0]:
            for elemento_2 in resultado_en_tuplas[1]:
              for elemento_3 in resultado_en_tuplas[2]:
                resultado.append(elemento_1 * elemento_2 * elemento_3)
        print(resultado)

      else:
        print(resultado_en_tuplas)



print("LISTA DE DESCOMPOSICIONES REALIZADAS")

for clave, valor in diccionarioDescomposicion.items():
    print(f"{clave}:")
    for fila in valor:
           print(f"\t{fila}")
    print()

