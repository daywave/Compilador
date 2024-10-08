import ply.lex as lex

# Lista de tokens
tokens = [
    'PROGRAMA', 'SI', 'SINO', 'FSI', 'HACER', 'HASTA', 'MIENTRAS',
    'LEER', 'ESCRIBIR', 'FLOTANTE', 'ENTERO', 'BOOLEANO', 'NO',
    'AND', 'OR', 'VERDADERO', 'FALSO', 'SUMA', 'RESTA', 'MULT',
    'DIV', 'POTENCIA', 'MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL',
    'IGUAL', 'DISTINTO', 'ASIGNACION', 'PUNTOCOMA', 'COMA', 'PARIZQ',
    'PARDER', 'LLAVIZQ', 'LLAVDER', 'ID', 'NUMERO', 'BREAK', 'THEN',
    'NUMERO_HEX'
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

# Expresiones regulares para tokens compuestos
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'ID')  # Verificar si es una palabra reservada
    return t

def t_NUMERO(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        with open("Errores.txt", "a") as archivo_errores:
            archivo_errores.write(f"Error: valor numérico inválido '{t.value}' en línea {t.lineno}\n")
        t.value = 0
    return t

def t_NUMERO_HEX(t):
    r'0x[0-9a-fA-F]+'
    t.value = int(t.value, 16)
    return t

# Comentarios
def t_COMENTARIO_UNA_LINEA(t):
    r'//.*'
    pass  # Ignorar comentarios de una sola línea

def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    pass  # Ignorar comentarios de múltiples líneas

# Manejar espacios y saltos de línea
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    with open("Errores.txt", "a") as archivo_errores:
        archivo_errores.write(f"Caracter ilegal '{t.value[0]}' en la línea {t.lineno}\n")
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Función para analizar el código y escribir tokens y errores en archivos
def analizar_codigo(codigo):
    lexer.input(codigo)

    # Limpiar archivos previos
    with open("Tokens.txt", "w") as archivo_tokens, open("Errores.txt", "w") as archivo_errores:
        pass

    while True:
        tok = lexer.token()
        if not tok:
            break
        with open("Tokens.txt", "a") as archivo_tokens:
            archivo_tokens.write(f"{tok.value}\t{tok.type}\tLínea {tok.lineno}\n")
