import ply.yacc as yacc
from lexico import tokens

# Definimos la clase base para todas las instrucciones
class Instruccion:
    pass

# Clases que representan diferentes tipos de instrucciones
class Programa(Instruccion):
    def __init__(self, declaraciones, sentencias):
        self.declaraciones = declaraciones
        self.sentencias = sentencias

class Declaracion(Instruccion):
    def __init__(self, tipo, identificadores):
        self.tipo = tipo
        self.identificadores = identificadores

class Asignacion(Instruccion):
    def __init__(self, id, expresion):
        self.id = id
        self.expresion = expresion

class If(Instruccion):
    def __init__(self, condicion, sentencias_then, sentencias_else=None):
        self.condicion = condicion
        self.sentencias_then = sentencias_then
        self.sentencias_else = sentencias_else

class Mientras(Instruccion):
    def __init__(self, condicion, sentencias):
        self.condicion = condicion
        self.sentencias = sentencias

class HacerMientras(Instruccion):
    def __init__(self, sentencias, condicion):
        self.sentencias = sentencias
        self.condicion = condicion

class Leer(Instruccion):
    def __init__(self, id):
        self.id = id

class Escribir(Instruccion):
    def __init__(self, id):
        self.id = id

class Bloque(Instruccion):
    def __init__(self, sentencias):
        self.sentencias = sentencias

class ExpresionBooleana(Instruccion):
    def __init__(self, izquierda, operador, derecha=None):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

class ExpresionNumerica(Instruccion):
    def __init__(self, izquierda, operador=None, derecha=None):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

# Definición de las reglas de producción
def p_programa(p):
    '''
    programa : PROGRAMA LLAVIZQ list_decl list_sent LLAVDER
             | error LLAVDER
    '''
    if len(p) == 6:
        p[0] = Programa(p[3], p[4])  # Genera el AST
    else:
        print("Error de sintaxis en 'programa'")

def p_list_decl(p):
    '''
    list_decl : decl list_decl
              | empty
    '''
    p[0] = [p[1]] + p[2] if len(p) == 3 else []

def p_decl(p):
    '''
    decl : tipo list_id PUNTOCOMA
    '''
    p[0] = Declaracion(p[1], p[2])  # Genera la declaración

def p_tipo(p):
    '''
    tipo : ENTERO
         | FLOTANTE
         | BOOLEANO
    '''
    p[0] = p[1]

def p_list_id(p):
    '''
    list_id : ID COMA list_id
            | ID
    '''
    p[0] = [p[1]] + p[3] if len(p) == 4 else [p[1]]

def p_list_sent(p):
    '''
    list_sent : sent list_sent
              | empty
              | error PUNTOCOMA list_sent
    '''
    p[0] = [p[1]] + p[2] if len(p) == 3 else []

def p_sent(p):
    '''
    sent : sent_if
         | sent_while
         | sent_do
         | sent_read
         | sent_write
         | bloque
         | sent_assign
         | sent_break
    '''
    p[0] = p[1]

def p_sent_if(p):
    '''
    sent_if : SI PARIZQ exp_bool PARDER THEN bloque FSI
            | SI PARIZQ exp_bool PARDER THEN bloque SINO bloque FSI
    '''
    if len(p) == 8:
        p[0] = If(p[3], p[5])  # Genera la instrucción if
    else:
        p[0] = If(p[3], p[5], p[7])  # Genera la instrucción if-else

def p_sent_while(p):
    '''
    sent_while : MIENTRAS PARIZQ exp_bool PARDER bloque
    '''
    p[0] = Mientras(p[3], p[5])  # Genera la instrucción mientras

def p_sent_do(p):
    '''
    sent_do : HACER bloque HASTA PARIZQ exp_bool PARDER PUNTOCOMA
    '''
    p[0] = HacerMientras(p[2], p[5])  # Genera la instrucción hacer-mientras

def p_sent_read(p):
    '''
    sent_read : LEER ID PUNTOCOMA
    '''
    p[0] = Leer(p[2])  # Genera la instrucción leer

def p_sent_write(p):
    '''
    sent_write : ESCRIBIR exp_bool PUNTOCOMA
    '''
    p[0] = Escribir(p[2])  # Genera la instrucción escribir

def p_bloque(p):
    '''
    bloque : LLAVIZQ list_sent LLAVDER
    '''
    p[0] = Bloque(p[2])  # Genera el bloque de instrucciones

def p_sent_assign(p):
    '''
    sent_assign : ID ASIGNACION exp_bool PUNTOCOMA
    '''
    p[0] = Asignacion(p[1], p[3])  # Genera la instrucción de asignación

def p_sent_break(p):
    '''
    sent_break : BREAK PUNTOCOMA
    '''
    p[0] = ('sent_break',)  # Puedes implementar una clase similar si es necesario.

def p_exp_bool(p):
    '''
    exp_bool : exp_bool OR comb
             | exp_bool AND comb
             | comb
    '''
    if len(p) == 4:
        if p[2] == 'or':
            p[0] = ExpresionBooleana(p[1], 'or', p[3])  # Genera la expresión booleana con OR
        elif p[2] == 'and':  # Manejo del operador &&
            p[0] = ExpresionBooleana(p[1], 'and', p[3])  # Genera la expresión booleana con AND
    else:
        p[0] = p[1]  # Retorna la expresión booleana simple


def p_comb(p):
    '''
    comb : comb AND igualdad
         | igualdad
    '''
    if len(p) == 4:
        p[0] = ExpresionBooleana(p[1], 'and', p[3])  # Genera la combinación de expresiones
    else:
        p[0] = p[1]

def p_igualdad(p):
    '''
    igualdad : igualdad IGUAL rel
             | igualdad DISTINTO rel
             | rel
    '''
    if len(p) == 4:
        if p[2] == '==':
            p[0] = ExpresionBooleana(p[1], '==', p[3])  # Genera la igualdad
        else:
            p[0] = ExpresionBooleana(p[1], '!=', p[3])  # Genera la desigualdad
    else:
        p[0] = p[1]

def p_rel(p):
    '''
    rel : expr MENOR expr
        | expr MAYOR expr
        | expr MENORIGUAL expr
        | expr MAYORIGUAL expr
        | expr
    '''
    if len(p) == 4:
        p[0] = ExpresionBooleana(p[1], p[2], p[3])  # Genera la relación
    else:
        p[0] = p[1]

def p_expr(p):
    '''
    expr : expr SUMA term
         | expr RESTA term
         | term
    '''
    if len(p) == 4:
        p[0] = ExpresionNumerica(p[1], p[2], p[3])  # Genera la expresión numérica
    else:
        p[0] = p[1]

def p_term(p):
    '''
    term : term MULT unario
         | term DIV unario
         | unario
    '''
    if len(p) == 4:
        p[0] = ExpresionNumerica(p[1], p[2], p[3])  # Genera la expresión de término
    else:
        p[0] = p[1]

def p_unario(p):
    '''
    unario : NO unario
           | RESTA unario
           | factor
    '''
    if len(p) == 3:
        p[0] = ExpresionNumerica(p[1], p[2])  # Genera la expresión unaria
    else:
        p[0] = p[1]

def p_factor(p):
    '''
    factor : PARIZQ exp_bool PARDER
           | ID
           | NUMERO
           | VERDADERO
           | FALSO
    '''
    if len(p) == 4:
        p[0] = p[2]  # Retorna la expresión entre paréntesis
    else:
        p[0] = p[1]  # Retorna el identificador o el número

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    if p:
        print(f"Error de sintaxis en la línea {p.lineno}, columna {p.lexpos}: '{p.value}'")
    else:
        print("Error de sintaxis: se esperaba más entrada")

    # Recuperación básica
    while True:
        tok = parser.token()
        if not tok or tok.type in ['PUNTOCOMA', 'LLAVDER']:
            break

# Construir el analizador sintáctico
parser = yacc.yacc()

def analizar_sintactico(data):
    try:
        resultado = parser.parse(data)
        return resultado, None  # Retorna el AST y sin errores
    except Exception as e:
        return None, str(e)  # Retorna None para el AST y el mensaje de error
