import ply.yacc as yacc
from analizador_lexico import tokens

# Clase Nodo para representar el árbol sintáctico
class Nodo:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, nodo_hijo):
        self.hijos.append(nodo_hijo)

    def __repr__(self):
        return f"Nodo({self.tipo}, {self.valor}, {self.hijos})"

# Definición de las reglas de producción
def p_programa(p):
    '''
    programa : PROGRAMA LLAVIZQ list_decl list_sent LLAVDER
    '''
    nodo_programa = Nodo('Programa')
    nodo_programa.hijos.extend(p[3])  # lista de declaraciones
    nodo_programa.agregar_hijo(p[4])  # lista de sentencias
    p[0] = nodo_programa

def p_list_decl(p):
    '''
    list_decl : decl list_decl
              | decl
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # Concatenamos las declaraciones como una lista
    else:
        p[0] = [p[1]]  # Solo una declaración


def p_decl(p):
    '''
    decl : tipo list_id PUNTOCOMA
    '''
    nodo_decl = Nodo('declaracion')  # Nodo 'declaracion'
    for id_var in p[2]:
        nodo_decl.agregar_hijo(Nodo(id_var))  # Cada identificador como hijo del nodo 'declaracion'
    p[0] = nodo_decl  # Retorna el nodo de declaración

def p_tipo(p):
    '''
    tipo : ENTERO
         | FLOTANTE
         | BOOLEANO
    '''
    p[0] = Nodo('tipo', p[1])

def p_list_id(p):
    '''
    list_id : ID COMA list_id
            | ID
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]  # Lista de identificadores
    else:
        p[0] = [p[1]]  # Un solo identificador

def p_list_sent(p):
    '''
    list_sent : sent list_sent
              | empty
              | error PUNTOCOMA list_sent
    '''
    nodo_sent = Nodo('list_sent')
    if len(p) == 3:
        nodo_sent.agregar_hijo(p[1])
        nodo_sent.agregar_hijo(p[2])
        p[0] = nodo_sent
    elif len(p) == 4:
        print("Error de sintaxis en 'list_sent'")
        p[0] = p[3]
    else:
        p[0] = nodo_sent

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
        p[0] = Nodo('sent_if', p[3])
        p[0].agregar_hijo(p[6])
    else:
        p[0] = Nodo('sent_if', p[3])
        p[0].agregar_hijo(p[6])
        p[0].agregar_hijo(p[8])

def p_sent_while(p):
    '''
    sent_while : MIENTRAS PARIZQ exp_bool PARDER bloque
    '''
    p[0] = Nodo('sent_while', p[3])
    p[0].agregar_hijo(p[5])

def p_sent_do(p):
    '''
    sent_do : HACER bloque HASTA PARIZQ exp_bool PARDER PUNTOCOMA
    '''
    p[0] = Nodo('sent_do', p[5])
    p[0].agregar_hijo(p[2])

def p_sent_read(p):
    '''
    sent_read : LEER ID PUNTOCOMA
    '''
    p[0] = Nodo('sent_read', p[2])

def p_sent_write(p):
    '''
    sent_write : ESCRIBIR exp_bool PUNTOCOMA
    '''
    p[0] = Nodo('sent_write', p[2])

def p_bloque(p):
    '''
    bloque : LLAVIZQ list_sent LLAVDER
    '''
    p[0] = Nodo('bloque')
    p[0].agregar_hijo(p[2])

def p_sent_assign(p):
    '''
    sent_assign : ID ASIGNACION exp_bool PUNTOCOMA
    '''
    p[0] = Nodo('sent_assign', p[1])
    p[0].agregar_hijo(p[3])

def p_sent_break(p):
    '''
    sent_break : BREAK PUNTOCOMA
    '''
    p[0] = Nodo('sent_break')

def p_exp_bool(p):
    '''
    exp_bool : exp_bool OR comb
             | comb
    '''
    if len(p) == 4:
        p[0] = Nodo('exp_bool')
        p[0].agregar_hijo(p[1])
        p[0].agregar_hijo(Nodo('or'))
        p[0].agregar_hijo(p[3])
    else:
        p[0] = p[1]

def p_comb(p):
    '''
    comb : comb AND igualdad
         | igualdad
    '''
    if len(p) == 4:
        p[0] = Nodo('comb')
        p[0].agregar_hijo(p[1])
        p[0].agregar_hijo(Nodo('and'))
        p[0].agregar_hijo(p[3])
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
            p[0] = Nodo('igualdad')
            p[0].agregar_hijo(p[1])
            p[0].agregar_hijo(Nodo('=='))
            p[0].agregar_hijo(p[3])
        else:
            p[0] = Nodo('igualdad')
            p[0].agregar_hijo(p[1])
            p[0].agregar_hijo(Nodo('!='))
            p[0].agregar_hijo(p[3])
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
        p[0] = Nodo('rel', p[2])
        p[0].agregar_hijo(p[1])
        p[0].agregar_hijo(p[3])
    else:
        p[0] = p[1]

def p_expr(p):
    '''
    expr : expr SUMA term
         | expr RESTA term
         | term
    '''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = Nodo('expr')
            p[0].agregar_hijo(p[1])
            p[0].agregar_hijo(Nodo('+'))
            p[0].agregar_hijo(p[3])
        else:
            p[0] = Nodo('expr')
            p[0].agregar_hijo(p[1])
            p[0].agregar_hijo(Nodo('-'))
            p[0].agregar_hijo(p[3])
    else:
        p[0] = p[1]

def p_term(p):
    '''
    term : term MULT unario
         | term DIV unario
         | unario
    '''
    if len(p) == 4:
        if p[2] == '*':
            p[0] = Nodo('term')
            p[0].agregar_hijo(p[1])
            p[0].agregar_hijo(Nodo('*'))
            p[0].agregar_hijo(p[3])
        else:
            p[0] = Nodo('term')
            p[0].agregar_hijo(p[1])
            p[0].agregar_hijo(Nodo('/'))
            p[0].agregar_hijo(p[3])
    else:
        p[0] = p[1]

def p_unario(p):
    '''
    unario : NO unario
           | RESTA unario
           | factor
    '''
    if len(p) == 3:
        if p[1] == 'not':
            p[0] = Nodo('unario', 'not')
            p[0].agregar_hijo(p[2])
        else:
            p[0] = Nodo('unario', '-')
            p[0].agregar_hijo(p[2])
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
        p[0] = p[2]
    else:
        p[0] = Nodo('factor', p[1])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    if p:
        print(f"Error de sintaxis en token {p.type} en la línea {p.lineno}, columna {p.lexpos}")
        parser.errok()
    else:
        print("Error de sintaxis en EOF")

# Construir el analizador sintáctico
parser = yacc.yacc()

def analizar_sintactico(data):
    try:
        resultado = parser.parse(data)
        return resultado, None  # Retorna el AST y sin errores
    except Exception as e:
        return None, str(e)  # Retorna None para el AST y el mensaje de error
