import ply.yacc as yacc
from analizador_lexico import tokens  # Importar los tokens desde el analizador léxico

# Definimos la precedencia de los operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL', 'DISTINTO'),
    ('left', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    ('right', 'NO'),
)

# Lista para almacenar errores
errores_sintacticos = []

# Definimos la gramática
def p_program(p):
    '''program : PROGRAMA LLAVIZQ instrucciones LLAVDER'''
    p[0] = ('program', p[3])

def p_instrucciones(p):
    '''instrucciones : instrucciones instruccion
                     | instruccion'''
    if len(p) == 3:
        p[0] = ('instrucciones', p[1], p[2])
    else:
        p[0] = ('instrucciones', p[1])

def p_instruccion(p):
    '''instruccion : declaracion
                   | asignacion
                   | control
                   | lectura
                   | escritura'''
    p[0] = p[1]

def p_declaracion(p):
    '''declaracion : ENTERO lista_ids PUNTOCOMA
                   | FLOTANTE lista_ids PUNTOCOMA
                   | BOOLEANO lista_ids PUNTOCOMA'''
    p[0] = ('declaracion', p[1], p[2])


def p_expresion_booleana(p):
    '''expresion : VERDADERO
                 | FALSO'''
    p[0] = ('booleano', p[1])

def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    p[0] = ('operacion_logica', p[2], p[1], p[3])

def p_instruccion_break(p):
    '''instruccion : BREAK PUNTOCOMA'''
    p[0] = ('break',)

def p_expresion_negacion(p):
    '''expresion : NO expresion'''
    p[0] = ('negacion', p[2])

def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    p[0] = ('operacion_logica', p[2], p[1], p[3])

def p_expresion_potencia(p):
    '''expresion : expresion POTENCIA expresion'''
    p[0] = ('potencia', p[1], p[3])


def p_lista_ids(p):
    '''lista_ids : lista_ids COMA ID
                 | ID'''
    if len(p) == 4:
        p[0] = ('lista_ids', p[1], p[3])
    else:
        p[0] = ('lista_ids', p[1])

def p_asignacion(p):
    '''asignacion : ID ASIGNACION expresion PUNTOCOMA'''
    p[0] = ('asignacion', p[1], p[3])

def p_expresion_binaria(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULT expresion
                 | expresion DIV expresion'''
    p[0] = ('expresion_binaria', p[2], p[1], p[3])

def p_expresion_parentesis(p):
    '''expresion : PARIZQ expresion PARDER'''
    p[0] = p[2]

def p_expresion_numero(p):
    '''expresion : NUMERO
                 | NUMERO_HEX'''
    p[0] = ('numero', p[1])

def p_expresion_id(p):
    '''expresion : ID'''
    p[0] = ('variable', p[1])

def p_control_while(p):
    '''control : MIENTRAS PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER'''
    p[0] = ('while', p[3], p[6])

def p_control_if(p):
    '''control : SI PARIZQ expresion PARDER THEN LLAVIZQ instrucciones LLAVDER fsi'''
    p[0] = ('if', p[3], p[7], p[9])

def p_fsi(p):
    '''fsi : FSI
           | SINO LLAVIZQ instrucciones LLAVDER FSI'''
    if len(p) == 2:
        p[0] = ('fi',)
    else:
        p[0] = ('else', p[3], 'fi')

def p_control_do_until(p):
    '''control : HACER LLAVIZQ instrucciones LLAVDER HASTA PARIZQ expresion PARDER PUNTOCOMA'''
    p[0] = ('do_until', p[3], p[7])

def p_lectura(p):
    '''lectura : LEER ID PUNTOCOMA'''
    p[0] = ('lectura', p[2])

def p_escritura(p):
    '''escritura : ESCRIBIR ID PUNTOCOMA'''
    p[0] = ('escritura', p[2])

# Manejo de errores
def p_error(p):
    global errores_sintacticos
    if p:
        error_msg = f"Error sintáctico en token '{p.value}', línea {p.lineno}"
        errores_sintacticos.append(error_msg)
    else:
        errores_sintacticos.append("Error sintáctico en el final del archivo")

def p_expresion_comparativa(p):
    '''expresion : expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MENORIGUAL expresion
                 | expresion MAYORIGUAL expresion
                 | expresion IGUAL expresion
                 | expresion DISTINTO expresion'''
    p[0] = ('comparacion', p[2], p[1], p[3])

# Construir el analizador
parser = yacc.yacc()

# Función para analizar el código
def analizar_sintactico(codigo):
    global errores_sintacticos
    errores_sintacticos = []  # Reiniciar lista de errores
    arbol_sintactico = parser.parse(codigo)

    # Guardar el árbol en un archivo
    with open("ArbolSintactico.txt", "w") as f:
        f.write(str(arbol_sintactico))

    # Guardar los errores en un archivo
    with open("ErroresSintacticos.txt", "w") as f:
        if errores_sintacticos:
            for error in errores_sintacticos:
                f.write(error + "\n")
        else:
            f.write("Sin errores sintácticos")

    return arbol_sintactico, errores_sintacticos
