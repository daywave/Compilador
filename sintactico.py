import ply.yacc as yacc
from lexico import tokens

# Definición de las reglas de producción
def p_programa(p):
    '''
    programa : PROGRAMA LLAVIZQ list_decl list_sent LLAVDER
    '''
    p[0] = ('programa', p[3], p[4])

def p_list_decl(p):
    '''
    list_decl : list_decl decl
              | decl
              | empty
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_decl(p):
    '''
    decl : tipo list_id PUNTOCOMA
    '''
    p[0] = ('decl', p[1], p[2])

def p_tipo(p):
    '''
    tipo : ENTERO
         | FLOTANTE
         | BOOLEANO
    '''
    p[0] = p[1]

def p_list_id(p):
    '''
    list_id : list_id COMA ID
            | ID
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_list_sent(p):
    '''
    list_sent : list_sent sent
              | sent
              | empty
    '''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

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
    sent_if : SI PARIZQ exp_bool PARDER bloque SINO bloque FSI
            | SI PARIZQ exp_bool PARDER bloque FSI
    '''
    if len(p) == 9:
        p[0] = ('sent_if', p[3], p[5], p[7])
    else:
        p[0] = ('sent_if', p[3], p[5], None)

def p_sent_while(p):
    '''
    sent_while : MIENTRAS PARIZQ exp_bool PARDER bloque
    '''
    p[0] = ('sent_while', p[3], p[5])

def p_sent_do(p):
    '''
    sent_do : HACER bloque HASTA PARIZQ exp_bool PARDER PUNTOCOMA
    '''
    p[0] = ('sent_do', p[2], p[5])

def p_sent_read(p):
    '''
    sent_read : LEER ID PUNTOCOMA
    '''
    p[0] = ('sent_read', p[2])

def p_sent_write(p):
    '''
    sent_write : ESCRIBIR exp_bool PUNTOCOMA
    '''
    p[0] = ('sent_write', p[2])

def p_bloque(p):
    '''
    bloque : LLAVIZQ list_sent LLAVDER
    '''
    p[0] = ('bloque', p[2])

def p_sent_assign(p):
    '''
    sent_assign : ID ASIGNACION exp_bool PUNTOCOMA
    '''
    p[0] = ('sent_assign', p[1], p[3])

def p_sent_break(p):
    '''
    sent_break : BREAK PUNTOCOMA
    '''
    p[0] = ('sent_break',)

def p_exp_bool(p):
    '''
    exp_bool : exp_bool OR comb
             | comb
    '''
    if len(p) == 4:
        p[0] = ('exp_bool', p[1], 'or', p[3])
    else:
        p[0] = p[1]

def p_comb(p):
    '''
    comb : comb AND igualdad
         | igualdad
    '''
    if len(p) == 4:
        p[0] = ('comb', p[1], 'and', p[3])
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
            p[0] = ('igualdad', p[1], '==', p[3])
        else:
            p[0] = ('igualdad', p[1], '!=', p[3])
    else:
        p[0] = p[1]

def p_rel(p):
    '''
    rel : expr op_rel expr
        | expr
    '''
    if len(p) == 4:
        p[0] = ('rel', p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_op_rel(p):
    '''
    op_rel : MENOR
           | MENORIGUAL
           | MAYOR
           | MAYORIGUAL
    '''
    p[0] = p[1]

def p_expr(p):
    '''
    expr : expr SUMA term
         | expr RESTA term
         | term
    '''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = ('expr', p[1], '+', p[3])
        else:
            p[0] = ('expr', p[1], '-', p[3])
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
            p[0] = ('term', p[1], '*', p[3])
        else:
            p[0] = ('term', p[1], '/', p[3])
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
            p[0] = ('unario', 'not', p[2])
        else:
            p[0] = ('unario', '-', p[2])
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
        p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    print(f"Error de sintaxis: {p}")

# Construir el analizador sintáctico
parser = yacc.yacc()

def analizar_sintactico(data):
    try:
        resultado = parser.parse(data)
        return resultado, None  # Retorna el AST y sin errores
    except Exception as e:
        return None, str(e)  # Retorna None para el AST y el mensaje de error
