from simpleai.search import SearchProblem, breadth_first, depth_first, greedy, astar
from simpleai.search.viewers import WebViewer, BaseViewer
import random



#definimos la cantidad de aparatos en el tablero inicial
def cantAparatos():
    n = random.randrange(15)
    return n

#generamos las posiciones de los aparatos aleatoriamente y se verifica que no haya dos en una misma posicion, ni en la salida
def generarPosicionAleatoria():
    for i in cantAparatos():
        filaAparato = random.randrange(4)
        columnaAparato = random.randrange(4)

        if (filaAparato == 3) and (columnaAparato == 3):
            generarPosicionAleatoria()
        else:
            lista = (filaAparato, columnaAparato,300)
        return lista




INICIAL = (
        #generarPosicionAleatoria()
        #para el caso de la entrega se ejecuta sobre tres aparatos solamente, sino se aplica lo de arriba:
        (1,2,300),
        (2,0,300),
        (3,0,300),
)

GOAL = (
            #for i in cantAparatos():
            #    i = (3,3,None)
            #al igual que en INICIAL, se aplicaria lo de arriba del comentario pero para el caso de la entrega se usa lo de abajo:
            (3,3,None),
            (3,3,None),
            (3,3,None), 
)

BOMBEROBOT = (3,3,0)



def tuple2list(t):
    return [list(x) for x in t]


def list2tuple(t):
    return tuple(tuple(x) for x in t)



class BombeRobotProblem(SearchProblem):
    def is_goal(self, state):
        return state == GOAL

    def cost(self, state1, action, state2):
        return 1

    def actions(self, state):

        filaRobot, columnaRobot = state

        available_actions = []
        
        #desplazar robot:
        #moverse arriba
        if filaRobot > 0:
            available_actions.append(state[filaRobot - 1][columnaRobot])
        #moverse abajo
        if filaRobot < 3:
            available_actions.append(state[filaRobot + 1][columnaRobot])
        #moverse izquierda
        if columnaRobot > 0:
            available_actions.append(state[filaRobot][columnaRobot - 1])
        #moverse derecha
        if columnaRobot < 3:
            available_actions.append(state[filaRobot][columnaRobot + 1])


        #enfriar aparatos:
        



        return available_actions

    def result(self, state, action):
        pass

    def heuristic(self, state):
        pass


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


