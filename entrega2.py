from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE,
                             LEAST_CONSTRAINING_VALUE,
                             HIGHEST_DEGREE_VARIABLE)


variables = list(range(25))

# variable 0 = Posicion 1
# variable 1 = Posicion 2
# variable 2 = Posicion 3
# variable 3 = Posicion 4
# variable 4 = Posicion 5
# variable 5 = Armadura de color Rojo
# variable 6 = Armadura de color Verde
# variable 7 = Armadura de color Blanco
# variable 8 = Armadura de color Amarillo
# variable 9 = Armadura de color Azul
# variable 10 = Arma Martillo de Guerra
# variable 11 = Arma Hacha Danesa
# variable 12 = Arma Lanza
# variable 13 = Arma Espada
# variable 14 = Arma Garrote
# variable 15 = Escudo Trebol
# variable 16 = Escudo Cruz
# variable 17 = Escudo Mil pajaros diferentes
# variable 18 = Escudo Dragon
# variable 19 = Escudo Arbol
# variable 20 = Amuleto Pendiente con forma de triangulo
# variable 21 = Amuleto Anillo con dibujo de Herrero
# variable 22 = Amuleto Pulsera de oro
# variable 23 = Amuleto Cinturon de cuero decorado
# variable 24 = Amuleto Moneda de Oro Britanica


dominios = {0: ['AGNAR'],
            1: ['BJARNI', 'CNUT', 'DIARF', 'EGIL' ],
            2: ['BJARNI', 'CNUT', 'DIARF', 'EGIL' ],
            3: ['BJARNI', 'CNUT', 'DIARF', 'EGIL' ],
            4: ['BJARNI', 'CNUT', 'DIARF', 'EGIL' ],
            5: ['BJARNI'],
            6: ['AGNAR', 'CNUT', 'DIARF', 'EGIL' ],
            7: ['AGNAR', 'CNUT', 'DIARF', 'EGIL' ],
            8: ['AGNAR', 'CNUT', 'DIARF', 'EGIL' ],
            9: ['AGNAR', 'CNUT', 'DIARF', 'EGIL' ],
            10: ['AGNAR', 'BJARNI', 'DIARF', 'EGIL' ],
            11: ['AGNAR', 'BJARNI', 'DIARF', 'EGIL' ],
            12: ['AGNAR', 'BJARNI', 'DIARF', 'EGIL' ],
            13: ['AGNAR', 'BJARNI', 'DIARF', 'EGIL' ],
            14: ['CNUT'],
            15: ['DIARF'],
            16: ['AGNAR', 'BJARNI', 'CNUT', 'EGIL' ],
            17: ['AGNAR', 'BJARNI', 'CNUT', 'EGIL' ],
            18: ['AGNAR', 'BJARNI', 'CNUT', 'EGIL' ],
            19: ['AGNAR', 'BJARNI', 'CNUT', 'EGIL' ],
            20: ['EGIL' ],
            21: ['AGNAR', 'BJARNI', 'CNUT', 'DIARF' ],
            22: ['AGNAR', 'BJARNI', 'CNUT', 'DIARF' ],
            23: ['AGNAR', 'BJARNI', 'CNUT', 'DIARF' ],
            24: ['AGNAR', 'BJARNI', 'CNUT', 'DIARF' ]}


restricciones = []


def izquierda(variables, values):
    # Verifica que la primera variable (vik_1) este a la izquierda de la otra variable (vik_2)
    vik_1, vik_2 = values[0:2]
    posiciones = values[2:7]
    posicion_1 = None
    posicion_2 = None
    for index in range(5):
        if posicion_1 is None:
            if posiciones[index] == vik_1:
                posicion_1 = index
        if posicion_2 is None:
            if posiciones[index] == vik_2:
                posicion_2 = index

    if (posicion_1 is None) or (posicion_2 is None):
        return False
    else:
        return (posicion_1 < posicion_2)

def compara(variables, values):
    #Compara que dos elementos pertenezcan al mismo vikingo
    return values[0] == values[1]

def al_lado(variables, values):
    # Verifica que dos vikingos se encuentren al lado
    vik_1, vik_2 = values[0:2]
    posiciones = values[2:7]
    posicion_1 = None
    posicion_2 = None
    for index in range(5):
        if posicion_1 is None:
            if posiciones[index] == vik_1:
                posicion_1 = index
        if posicion_2 is None:
            if posiciones[index] == vik_2:
                posicion_2 = index

    if (posicion_1 is None) or (posicion_2 is None):
        return False
    else:
        return abs(posicion_1 - posicion_2) == 1

def distintos(variables, values):
    #Compara que no haya vikingos con la misma armadura, escudo, arma o amuleto
    return len(set(values)) == 5

#Compara que no haya vikingos con la misma armadura, escudo, arma o amuleto
for index in range(0,24,5):
    var1 = index
    var2 = var1 + 1
    var3 = var2 + 1
    var4 = var3 + 1
    var5 = var4 + 1
    restricciones.append(((variables[var1], variables[var2], variables[var3], variables[var4], variables[var5]), distintos))



#El guerrero de verde era famoso por su escudo con una cruz dibujada.
restricciones.append(((variables[6], variables[16]), compara))

#El guerrero que usaba un martillo de guerra, tenía un anillo con un dibujo de un herrero para la suerte
restricciones.append(((variables[10], variables[21]), compara))

#El jefe recuerda que el guerrero de amarillo usaba un hacha danesa
restricciones.append(((variables[8], variables[11]), compara))

#El guerrero del centro tenía un bello escudo decorado con dibujos de mil pájaros diferentes.
restricciones.append(((variables[2], variables[17]), compara))

#El jefe insiste que el guerrero que usaba espada, usaba un escudo decorado con un dibujo de un dragón
restricciones.append(((variables[13], variables[18]), compara))

#Agnar dice que un guerrero que se ubicaba al lado suyo, usaba armadura azul
restricciones.append(((variables[1], variables[9]), compara))

#El guerrero de la lanza siempre estaba al lado del guerrero del escudo con dibujo de árbol
restricciones.append(((variables[12], variables[19], variables[0], variables[1], variables[2], variables[3], variables[4]), al_lado))

#El guerrero que usaba un cinturón de cuero decorado como amuleto, se ubicaba al lado del guerrero del hacha danesa
restricciones.append(((variables[23], variables[11], variables[0], variables[1], variables[2], variables[3], variables[4]), al_lado))

#El guerrero que usaba lanza, se ubicaba al lado del guerrero que usaba una brillante pulsera de oro para la suerte.
restricciones.append(((variables[12], variables[22], variables[0], variables[1], variables[2], variables[3], variables[4]), al_lado))

#El jefe asegura que el guerrero que se vestía de verde, siempre se ubicaba a la izquierda del guerrero de blanco
restricciones.append(((variables[6], variables[7], variables[0], variables[1], variables[2], variables[3], variables[4]), izquierda))



def resolver(metodo_busqueda, iteraciones):
    #visor = BaseViewer()

    problema = CspProblem(variables, dominios, restricciones)

    if metodo_busqueda == 'backtrack':
        resultado = backtrack(problema, value_heuristic=LEAST_CONSTRAINING_VALUE,
                              variable_heuristic=MOST_CONSTRAINED_VARIABLE)
        return resultado

    if metodo_busqueda == 'min_conflicts':
        resultado = min_conflicts(problema, iterations_limit=iteraciones)
        return resultado


if __name__ == '__main__':

    problema = CspProblem(variables, dominios, restricciones)

    #resultado = backtrack(problema, value_heuristic=LEAST_CONSTRAINING_VALUE,
    #                      variable_heuristic=MOST_CONSTRAINED_VARIABLE)

    resultado = min_conflicts(problema, iterations_limit=50)

    print(resultado)