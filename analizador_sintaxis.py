import ply.yacc as yacc
import pickle

from analizador_lexico import tokens  # Importar los tokens desde el analizador léxico
from nodo import Nodo  # Importamos la clase Nodo para manejar la estructura del AST

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
    '''program : PROGRAMA LLAVIZQ instrucciones_opt LLAVDER'''
    nodo = Nodo(tipoNodo="Programa", linea=p.lineno(1))
    nodo.hijos[0] = p[3]  # Instrucciones
    p[0] = nodo

# Opcional: las instrucciones pueden ser vacías
def p_instrucciones_opt(p):
    '''instrucciones_opt : instrucciones
                         | empty'''
    p[0] = p[1]

def p_instrucciones(p):
    '''instrucciones : instrucciones instruccion
                     | instruccion'''
    nodo = Nodo(tipoNodo="Instrucciones", linea=p.lineno(1))
    if len(p) == 3:
        nodo.hijos[0] = p[1]
        nodo.hijos[1] = p[2]
    else:
        nodo.hijos[0] = p[1]
    p[0] = nodo

def p_empty(p):
    '''empty :'''
    p[0] = None

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
    nodo = Nodo(tipoNodo="Declaracion", linea=p.lineno(1))
    nodo.tipoDec = p[1]  # Tipo de declaración
    nodo.hijos[0] = p[2]  # Lista de identificadores
    p[0] = nodo


def p_asignacion(p):
    '''asignacion : ID ASIGNACION expresion PUNTOCOMA'''
    nodo = Nodo(tipoNodo="Asignacion", linea=p.lineno(1))
    nodo.nomIdExp = p[1]  # Guardamos el identificador
    nodo.hijos[0] = p[3]  # Expresión asignada
    p[0] = nodo

def p_expresion_binaria(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULT expresion
                 | expresion DIV expresion'''
    nodo = Nodo(tipoNodo="ExpresionBinaria", linea=p.lineno(2))
    nodo.OpExp = p[2]  # Guardamos el operador
    nodo.hijos[0] = p[1]  # Lado izquierdo
    nodo.hijos[1] = p[3]  # Lado derecho
    
    # Asignar el tipo resultante según las reglas
    tipo_resultante = verificar_tipos(p[1].tipoExp, p[3].tipoExp, p[2])
    nodo.tipoExp = tipo_resultante  # Establecer el tipo de la expresión resultante
    p[0] = nodo

def p_expresion_comparativa(p):
    '''expresion : expresion MENOR expresion
                 | expresion MAYOR expresion
                 | expresion MENORIGUAL expresion
                 | expresion MAYORIGUAL expresion
                 | expresion IGUAL expresion
                 | expresion DISTINTO expresion'''
    nodo = Nodo(tipoNodo="Comparacion", linea=p.lineno(2))
    nodo.OpExp = p[2]  # Guardamos el operador
    nodo.hijos[0] = p[1]  # Lado izquierdo de la comparación
    nodo.hijos[1] = p[3]  # Lado derecho de la comparación
    p[0] = nodo


def p_lista_ids(p):
    '''lista_ids : lista_ids COMA ID
                 | ID'''
    if len(p) == 4:
        nodo = Nodo(tipoNodo="ListaIdentificadores", linea=p.lineno(2))
        nodo.hijos[0] = p[1]  # Primer identificador
        nodo.hijos[1] = p[3]  # Segundo identificador
    else:
        nodo = Nodo(tipoNodo="Identificador", linea=p.lineno(1))
        nodo.nomIdExp = p[1]
    p[0] = nodo


def verificar_tipos(tipo_izq, tipo_der, operador):
    # Definir reglas para las operaciones entre tipos
    if tipo_izq == "int" and tipo_der == "int":
        return "int"
    elif tipo_izq == "double" or tipo_der == "double":
        return "double"
    elif tipo_izq == "float" or tipo_der == "float":
        return "float"
    else:
        raise TypeError(f"Operación no permitida entre {tipo_izq} y {tipo_der}")

def p_expresion_booleana(p):
    '''expresion : VERDADERO
                 | FALSO'''
    nodo = Nodo(tipoNodo="Booleano", linea=p.lineno(1))
    nodo.valCteExp = p[1]  # Guardamos el valor booleano
    p[0] = nodo

def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    nodo = Nodo(tipoNodo="OperacionLogica", linea=p.lineno(2))
    nodo.OpExp = p[2]  # Guardamos el operador lógico
    nodo.hijos[0] = p[1]
    nodo.hijos[1] = p[3]
    p[0] = nodo

def p_expresion_negacion(p):
    '''expresion : NO expresion'''
    nodo = Nodo(tipoNodo="Negacion", linea=p.lineno(1))
    nodo.hijos[0] = p[2]  # Expresión a negar
    p[0] = nodo

def p_expresion_numero(p):
    '''expresion : NUMERO
                 | NUMERO_HEX'''
    nodo = Nodo(tipoNodo="Numero", linea=p.lineno(1))
    nodo.valCteExp = p[1]  # Guardamos el valor del número
    p[0] = nodo

def p_expresion_potencia(p):
    '''expresion : expresion POTENCIA expresion'''
    nodo = Nodo(tipoNodo="Potencia", linea=p.lineno(2))
    nodo.hijos[0] = p[1]  # Base
    nodo.hijos[1] = p[3]  # Exponente
    p[0] = nodo


def p_control_do_until(p):
    '''control : HACER LLAVIZQ instrucciones LLAVDER HASTA PARIZQ expresion PARDER PUNTOCOMA'''
    nodo = Nodo(tipoNodo="DoUntil", linea=p.lineno(1))
    nodo.hijos[0] = p[3]  # Instrucciones dentro del bucle
    nodo.hijos[1] = p[6]  # Condición del "hasta"
    p[0] = nodo


def p_control_while(p):
    '''control : MIENTRAS PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER'''
    nodo = Nodo(tipoNodo="While", linea=p.lineno(1))
    nodo.hijos[0] = p[3]  # Condición
    nodo.hijos[1] = p[6]  # Cuerpo del while
    p[0] = nodo

def p_control_if(p):
    '''control : SI PARIZQ expresion PARDER THEN LLAVIZQ instrucciones LLAVDER fsi'''
    nodo = Nodo(tipoNodo="If", linea=p.lineno(1))
    nodo.hijos[0] = p[3]  # Condición
    nodo.hijos[1] = p[7]  # Instrucciones del bloque if
    nodo.hijos[2] = p[9]  # Else o fsi
    p[0] = nodo

def p_fsi(p):
    '''fsi : FSI
           | SINO LLAVIZQ instrucciones LLAVDER FSI'''
    nodo = Nodo(tipoNodo="Fi", linea=p.lineno(1))
    if len(p) == 2:
        nodo.tipoSen = "FinIf"
    else:
        nodo.tipoSen = "Else"
        nodo.hijos[0] = p[3]  # Instrucciones del else
    p[0] = nodo

def p_lectura(p):
    '''lectura : LEER ID PUNTOCOMA'''
    nodo = Nodo(tipoNodo="Lectura", linea=p.lineno(1))
    nodo.nomIdExp = p[2]  # Identificador que se va a leer
    p[0] = nodo

def p_escritura(p):
    '''escritura : ESCRIBIR ID PUNTOCOMA'''
    nodo = Nodo(tipoNodo="Escritura", linea=p.lineno(1))
    nodo.nomIdExp = p[2]  # Identificador que se va a escribir
    p[0] = nodo

def p_lista_ids(p):
    '''lista_ids : lista_ids COMA ID
                 | ID'''
    if len(p) == 4:
        nodo = Nodo(tipoNodo="ListaIdentificadores", linea=p.lineno(2))
        nodo.hijos[0] = p[1]  # Primer identificador
        nodo.hijos[1] = p[3]  # Segundo identificador
    else:
        nodo = Nodo(tipoNodo="Identificador", linea=p.lineno(1))
        nodo.nomIdExp = p[1]
    p[0] = nodo

def p_instruccion_break(p):
    '''instruccion : BREAK PUNTOCOMA'''
    p[0] = Nodo(tipoNodo="Break", linea=p.lineno(1))



# Manejo de errores
def p_error(p):
    global errores_sintacticos
    if p:
        error_msg = f"Error sintáctico en token '{p.value}', línea {p.lineno}"
        errores_sintacticos.append(error_msg)
    else:
        errores_sintacticos.append("Error sintáctico en el final del archivo")

# Construir el analizador
parser = yacc.yacc()

# Función para analizar el código
def analizar_sintactico(codigo):
    global errores_sintacticos
    errores_sintacticos = []  # Reiniciar lista de errores
    arbol_sintactico = parser.parse(codigo)

    # Guardar el árbol en un archivo con pickle
    with open("ArbolSintactico.pkl", "wb") as f:
        pickle.dump(arbol_sintactico, f)

    # Guardar los errores en un archivo
    with open("ErroresSintacticos.txt", "w") as f:
        if errores_sintacticos:
            for error in errores_sintacticos:
                f.write(error + "\n")
        else:
            f.write("Sin errores sintácticos")

    return arbol_sintactico, errores_sintacticos
