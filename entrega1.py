from simpleai.search import SearchProblem, breadth_first, depth_first, greedy, astar
from simpleai.search.viewers import WebViewer, BaseViewer
import random

#definimos la cantidad de aparatos en el tablero inicial
def cantAparatos():
    n = random.randrange(15)
    return n

#generamos las posiciones de los aparatos aleatoriamente y se verifica que no haya en la salida aparatos
def generarPosicionAleatoria():
    for i in cantAparatos():
        filaAparato = random.randrange(4)
        columnaAparato = random.randrange(4)

        if (filaAparato == 3) and (columnaAparato == 3):
            generarPosicionAleatoria()
        else:
            lista = (filaAparato, columnaAparato,300)
        return tuple(lista)


INICIAL = (((1,2,300),(2,0,300),(3,0,300)),(3,3))#utilizamos esta forma para la entrega

    #Con el método generarPosicionAleatoria() generariamos las N posiciones aleatoriamente.
    #generarPosicionAleatoria()

GOAL = (((3,3,None),(3,3,None),(3,3,None)),(3,3))#utilizamos esta forma para la entrega

    #Con las lineas comentadas a continuacion generariamos GOAL, de manera automatica.
    #for i in cantAparatos():
    #    i = (3,3,None)


#BOMBEROBOT = (3,3)


def tuple2list(t):
    return [list(x) for x in t]


def list2tuple(t):
    return tuple(tuple(x) for x in t)



class BombeRobotProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL

    def cost(self, state1, action, state2):
        #El costo de la acción en este caso va a ser 1
        return 1

    def actions(self, state):

        filaRobot, columnaRobot, articulo = state[-1]

        available_actions = []

        compartePosicion = True

        x, y, z = state[1] #Estado Robot

        #desplazar robot:
        for i in range(0, 2): #cantAparatos() para el caso de N articulos
            a,b,c = state[0][i]
            if  (x == a) & (y == b):
                available_actions.append([0],[i],[z-150])
                if x > 0:
                # moverse arriba
                    available_actions.append([0][i][a-1])
                    available_actions.append([1][x-1][y])
                # moverse abajo
                if x < 3:
                    available_actions.append([0][i][a+1])
                    available_actions.append([1][x+1][y])
                # moverse izquierda
                if y > 0:
                    available_actions.append([0][i][b-1])
                    available_actions.append([1][x][y-1])
                # moverse derecha
                if y < 3:
                    available_actions.append([0][i][b+1])
                    available_actions.append([1][x][y+1])
            else:
                compartePosicion = False

        if compartePosicion == True:
             # moverse arriba
             if x > 0:
                 # moverse arriba
                 available_actions.append([1][x-1][y])
             # moverse abajo
             if x < 3:
                 available_actions.append([1][x+1][y])
             # moverse izquierda
             if y > 0:
                 available_actions.append([1][x][y-1])
             # moverse derecha
             if y < 3:
                 available_actions.append([1][x][y+1])
        return available_actions
        #falta la parte de enfriar aparatos que no sabiamos como hacer

    def result(self, state, action):
        #falta hacer las comprobaciones necesarias para saber que tiene que hacer el robot
        return action


    def heuristic(self, state):
        for i in range(state[0]): #recorrer los aparatos
            numero_fila = numero_fila + abs((3,3) - state[0][i]) #calcula la distancia en filas del aparato a la salida
            numero_columna = numero_columna + abs((3,3) - state[0][i])#calcula la distancia en columnas del aparato a la salida
            dist_manhattan = dist_manhattan + (((numero_fila + numero_columna)+1))#calcula distancia de manhattan y suma la accion de enfriar el aparato



def resolver(metodo_busqueda, posiciones_aparatos):
    visor = BaseViewer()

    if metodo_busqueda == "breadth_first":
        resultado = breadth_first(BombeRobotProblem(INICIAL), graph_search=True)
        return resultado

    if metodo_busqueda == "depth_first":
        resultado = depth_first(BombeRobotProblem(INICIAL), graph_search=True)
        return resultado

    if metodo_busqueda == "greedy":
        resultado = greedy(BombeRobotProblem(INICIAL), graph_search=True)
        return resultado

    if metodo_busqueda == "astar":
        resultado = astar(BombeRobotProblem(INICIAL), graph_search=True)
        return resultado



if __name__ == '__main__':
    visor = BaseViewer()
    #result = breadth_first(BombeRobotProblem(INICIAL), graph_search=True,viewer=visor)
    #result = depth_first(BombeRobotProblem(INICIAL), graph_search=True,viewer=visor)
    #result = greedy(BombeRobotProblem(INICIAL), graph_search=True, viewer=visor)
    result = astar(BombeRobotProblem(INICIAL), graph_search=True, viewer=visor)

