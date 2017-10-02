from simpleai.search import SearchProblem, breadth_first, depth_first, greedy, astar
from simpleai.search.viewers import WebViewer, BaseViewer
import random


#INICIAL = (([[1,2],300],[[1,2],300],[[1,2],300]),(1,2))#utilizamos esta forma para la entrega


#GOAL = (([[3,3],None],[[3,3],None],[[3,3],None]),(3,3))#utilizamos esta forma para la entrega



def tuple2list(t):
    return [list(x) for x in t]


def list2tuple(t):
    return tuple(tuple(x) for x in t)


def stateToList(t): #hacemos que todo el estado se convierta en lista para poder trabajar en el
    aparatos = []
    for i in range(len(t[0])):
        aparatos.append([list(t[0][i][0]) ,t[0][i][1] ])

    a1 = [aparatos , list(t[1])]
    return (a1)

def stateToTuple(t): #volvemos a poner todo el estado en tupla
    aparatos = []
    for i in range(len(t[0])):
        aparatos.append( (tuple(t[0][i][0]) ,t[0][i][1]) )

    a1 = (tuple(aparatos) , tuple(t[1]))
    return (a1)

def manhattan_distance(start, end): #funcion que hace distancia de manhattan
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)


def adyacentes (t): #descubre las posiciones adyacentes al robot
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


def subirTemp (state): #funcion para hacer subir los 25 grados de cada aparato
    aparatos = state[0]
    listState = []
    
    #se recorren todos los aparatos y se les suma 25 grados 
    for i in aparatos:
        if i[0] != [3,3]:
            a = list(i)
            a[1] = a[1] +25
            listState.append(a)
    
    return [listState , state[1]]


class BombeRobotProblem(SearchProblem):
    def is_goal(self, state):
        
        stateList = stateToList(state)
        #obtengo los aparatos
        aparatos = stateList[0]

        #bandera para saber si todos los aparatos estan en salida
        salidaLlena = True

        for i in aparatos:
                if i[0] != [3,3]: #revisa si existe algun aparato que no se encuentra en la salida
                    salidaLlena = False
        
        return salidaLlena

    def cost(self, state1, action, state2):
        #El costo de la accion en este caso va a ser 1
        return 1

    def actions(self,state):

        #La lista de acciones es la siguiente:
        #["Accion a realizar" , [coordenadas] , "aparato que se mueve"]
        #["arriba" , [0,1] , none] se mueve el robot arriba
        #["arriba-Aparato" , [0,1] , 1] se mueve el aparato 1 para arriba
        #en el caso de enfriar solo estan las coordenadas y la accion es "enfriar"

        stateList = stateToList(state)

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
        
        #pasamos todo el estado a lista para poder trabajar en el
        state =stateToList(state)
       
        #subimos temperatura de cada aparato
        state = subirTemp(state)
        
        robot = state[1]
        aparatos = state[0]

        #miramos que tipo de accion es y asi saber cual aplicar
        if (action[2] == None):
            if (action[0] == "enfriar"):
                for i in range(len(aparatos)):
                    if aparatos[i][0] == robot:
                        aparatos[i][1] = aparatos[i][1] - 150
            else:
                robot[0] = action[1][0]
                robot[1] = action[1][1]
        else:
            aparatos[action[2]][0][0] = action[1][0]
            aparatos[action[2]][0][1] = action[1][1]
            if (aparatos[action[2]][0] == [3,3]):
                aparatos[action[2]][1] = None
            robot[0] = action[1][0]
            robot[1] = action[1][1]
        
        #state = [aparatos , robot]

        return stateToTuple(state)


    def heuristic(self, state):
        robot = state[1]
        aparato = 0

        #descubrimos cual es el aparato mas cercano al robot y calculamos su distancia de manhattan a el
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

        #hacemos distancia de manhattan por cada aparato que no sea el mas cercano al robot, desde la salida hasta cada uno
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

    posiciones_aparatos = [(1,2),(2,0),(3,0)]

    posapar = []

    for i in posiciones_aparatos:
        posapar.append((tuple(i) , 300))

    INICIAL =  (tuple(posapar) , (3,3))

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

    posiciones_aparatos = [(1,2),(2,0),(3,0)]

    posapar = []

    for i in posiciones_aparatos:
        posapar.append((tuple(i) , 300))

    INICIAL =  (tuple(posapar) , (3,3))


    result = breadth_first(BombeRobotProblem(INICIAL), graph_search=True,viewer=visor)
    #result = depth_first(BombeRobotProblem(INICIAL), graph_search=True,viewer=visor)
    #result = greedy(BombeRobotProblem(INICIAL), graph_search=True, viewer=visor)
    #result = astar(BombeRobotProblem(INICIAL), graph_search=True, viewer=visor)

    #print result
    print ('CAMINO COMPLETO')
    print (result.path())
    print ('LARGO CAMINO:', len(result.path()))
    print (visor.stats)