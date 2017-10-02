from simpleai.search import SearchProblem, breadth_first, depth_first, greedy, astar
from simpleai.search.viewers import WebViewer, BaseViewer
import random

#definimos la cantidad de aparatos en el tablero inicial
# def cantAparatos():
#     n = random.randrange(15)
#     return n

# #generamos las posiciones de los aparatos aleatoriamente y se verifica que no haya en la salida aparatos
# def generarPosicionAleatoria():
#     for i in cantAparatos():
#         filaAparato = random.randrange(4)
#         columnaAparato = random.randrange(4)

#         if (filaAparato == 3) and (columnaAparato == 3):
#             generarPosicionAleatoria()
#         else:
#             lista = (filaAparato, columnaAparato,300)
#         return tuple(lista)


INICIAL = (([[1,2],300],[[1,2],300],[[1,2],300]),(1,2))#utilizamos esta forma para la entrega

    #Con el metodo generarPosicionAleatoria() generariamos las N posiciones aleatoriamente.
    #generarPosicionAleatoria()

#GOAL = (([[3,3],None],[[3,3],None],[[3,3],None]),(3,3))#utilizamos esta forma para la entrega

    #Con las lineas comentadas a continuacion generariamos GOAL, de manera automatica.
    #for i in cantAparatos():
    #    i = (3,3,None)


#BOMBEROBOT = (3,3)


def tuple2list(t):
    return [list(x) for x in t]


def list2tuple(t):
    return tuple(tuple(x) for x in t)


def actionToList(t):
    aparatos = []
    for i in range(len(t[0])):
        aparatos.append([list(t[0][i][0]) ,t[0][i][1] ])

    a1 = [aparatos , list(t[1])]
    return (a1)

def actionToTuple(t):
    aparatos = []
    for i in range(len(t[0])):
        aparatos.append( (tuple(t[0][i][0]) ,t[0][i][1]) )

    a1 = (tuple(aparatos) , tuple(t[1]))
    return (a1)

def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)


def adyacentes (t):
    x=t[0]
    y=t[1]

    movimientos = []

    #Arriba
    if x>0 :
        movimientos.append(['arriba',[x-1,y] , None])

    #abajo
    if x<3 :
        movimientos.append(['abajo',[x+1,y], None])

    #Izquierda
    if y>0 :
        movimientos.append(['izquierda',[x,y-1], None])

    #Derecha
    if y<3 :
        movimientos.append(['derecha',[x,y+1], None])

    return movimientos



class BombeRobotProblem(SearchProblem):
    def is_goal(self, state):
        
        stateList = actionToList(state)
        #obtengo los aparatos
        aparatos = stateList[0]

        #bandera para saber si todos los aparatos estan en salida
        salidaLlena = True

        for i in aparatos:
                if i[0] != [3,3]:
                    salidaLlena = False
        return salidaLlena

    def cost(self, state1, action, state2):
        #El costo de la accion en este caso va a ser 1
        return 1

    def actions(self,state):

        #La lista de acciones es la siguiente:
        #["Accion a realizar" , [coordenadas] , aparato que se mueve]
        #["arriba" , [0,1] , none] se mueve el robot arriba
        #["arribaaparato" , [0,1] , 1] se mueve el aparato 1 para arriba

        stateList = actionToList(state)

        #obtengo los aparatos
        aparatos = stateList[0]

        #si alguna aparato exploto
        for aparato in aparatos:
            if aparato[1] > 500:
                return []

        robot = stateList[1]
        available_actions = []


        #----------------moverRobot------------

        #obtengo los movimientos
        movimientos = adyacentes(robot)

        #aniado los movimientos a la lista de acciones disponibles
        for i in movimientos:
            available_actions.append(i)


        #----------------moveAparato------------
        #si hay un aparato en el mismo lugar que el robot puedo enfriar o empujar
        if robot != [3,3]:
            enfriar = False

            #por cada aparato veo si esta en la posicion del robot, agrego los movimientos
            for i , aparato in enumerate(aparatos):
                if (list(aparato[0]) == robot):
                    enfriar = True
                    for j in movimientos:
                        a= j[0] + "-Aparato"
                        b = j[1]
                        c = i
                        e = [a,b,c]
                        available_actions.append(e)           

        #----------------Enfriar------------
            if enfriar:
                available_actions.append(["enfriar" , robot , None])


        return available_actions
        

    def result(self,state, action):
        
        return state


    def heuristic(self, state):
        robot = state[1]
        aparato = 0

        for i in range(len(state[0])):
           if state[0][i][0] != [3,3]:
                dist_manhattan = manhattan_distance(robot, state[0][i][0])
                if i == 0:
                    mascercano = dist_manhattan
                    aparato = i
                elif dist_manhattan < mascercano:
                    mascercano = dist_manhattan
                    aparato = i

        heu = mascercano

        for i in range(len(state[0])): #recorrer los aparatos
            if state[0][i][0] != [3,3]:
                if state[0][i][0] == state[0][aparato][0]:
                    dist_manhattan = manhattan_distance([3,3], state[0][i][0])
                    heu = heu + dist_manhattan
                else:
                    dist_manhattan = manhattan_distance([3,3], state[0][i][0])
                    heu = heu + (dist_manhattan * 2)
            

        return heu



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
    #visor = WebViewer()

    #result = breadth_first(BombeRobotProblem(INICIAL), graph_search=True,viewer=visor)
    #result = depth_first(BombeRobotProblem(INICIAL), graph_search=True,viewer=visor)
    #result = greedy(BombeRobotProblem(INICIAL), graph_search=True, viewer=visor)
    result = astar(BombeRobotProblem(INICIAL), graph_search=True, viewer=visor)

    #print result
    print ('CAMINO COMPLETO')
    print (result.path())
    print ('LARGO CAMINO:', len(result.path()))
    print (visor.stats)
