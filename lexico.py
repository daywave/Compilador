import ply.lex as lex

# Lista de tokens
tokens = [
    'PROGRAMA', 'SI', 'SINO', 'FSI', 'HACER', 'HASTA', 'MIENTRAS',
    'LEER', 'ESCRIBIR', 'FLOTANTE', 'ENTERO', 'BOOLEANO', 'NO',
    'AND', 'OR', 'VERDADERO', 'FALSO', 'SUMA', 'RESTA', 'MULT',
    'DIV', 'POTENCIA', 'MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL',
    'IGUAL', 'DISTINTO', 'ASIGNACION', 'PUNTOCOMA', 'COMA', 'PARIZQ',
    'PARDER', 'LLAVIZQ', 'LLAVDER', 'ID', 'NUMERO', 'BREAK', 'THEN',
    'NUMERO_HEX', 'CONCAT'
]

# Definición de palabras reservadas
reservadas = {
    'program': 'PROGRAMA',
    'if': 'SI',
    'else': 'SINO',
    'fi': 'FSI',
    'do': 'HACER',
    'until': 'HASTA',
    'while': 'MIENTRAS',
    'read': 'LEER',
    'write': 'ESCRIBIR',
    'float': 'FLOTANTE',
    'int': 'ENTERO',
    'bool': 'BOOLEANO',
    'not': 'NO',
    'and': 'AND',
    'or': 'OR',
    'true': 'VERDADERO',
    'false': 'FALSO',
    'break': 'BREAK',
    'then': 'THEN'
}

# Expresiones regulares para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_POTENCIA = r'\^'
t_MENOR = r'<'
t_MENORIGUAL = r'<='
t_MAYOR = r'>'
t_MAYORIGUAL = r'>='
t_IGUAL = r'=='
t_DISTINTO = r'!='
t_ASIGNACION = r'='
t_PUNTOCOMA = r';'
t_COMA = r','
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_LLAVIZQ = r'\{'
t_LLAVDER = r'\}'
t_CONCAT = r'&'  # Token para la concatenación

# Regla para identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reservadas:
        t.type = reservadas[t.value]  # Verifica si es palabra reservada
    elif len(t.value) > 30:  # Ejemplo de límite de longitud
        print(f"Error: identificador '{t.value}' demasiado largo.")
        t.type = 'ID'
    return t

# Regla para números
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print(f"Error: valor numérico inválido '{t.value}'")
        t.value = 0
    return t

# Regla para comentarios de una sola línea
def t_COMENTARIO_UNA_LINEA(t):
    r'//.*'
    pass  # Ignorar comentarios de una sola línea

# Regla para comentarios de múltiples líneas
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    pass  # Ignorar comentarios de múltiples líneas

# Regla para números hexadecimales
def t_NUMERO_HEX(t):
    r'0x[0-9a-fA-F]+'
    t.value = int(t.value, 16)
    return t

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Regla para manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para manejar errores
def t_error(t):
    print(f"Error: carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Función para analizar una cadena de entrada
def analizar(data):
    lexer.input(data)
    tokens_encontrados = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_encontrados.append(tok)
    return tokens_encontrados
