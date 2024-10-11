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


# Manejo de operadores lógicos
t_AND = r'and'
t_OR = r'or'

# Expresión regular para palabras reservadas e identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'ID')  # Chequear si es palabra reservada
    return t

# Expresión regular para números enteros y flotantes
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    try:
        if '.' in t.value:
            t.value = float(t.value)  # Convertir a float si contiene un punto decimal
        else:
            t.value = int(t.value)  # Convertir a int si no contiene punto decimal
    except ValueError:
        print(f"Error: valor numérico inválido '{t.value}' en la línea {t.lineno}")
        t.value = 0
    return t


# Manejo de comentarios de una sola línea
def t_COMENTARIO_UNA_LINEA(t):
    r'//.*'
    pass  # Ignorar comentarios

# Manejo de comentarios multilínea
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    pass  # Ignorar comentarios

# Manejo de espacios en blanco y tabulaciones
t_ignore = ' \t'

# Manejo de nuevas líneas para mantener el número de línea actualizado
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores léxicos
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Función para analizar el código
def analizar_codigo(codigo):
    lexer.input(codigo)

    # Limpiar archivos previos
    with open("Tokens.txt", "w") as archivo_tokens, open("Errores.txt", "w") as archivo_errores:
        pass

    # Proceso de análisis
    while True:
        tok = lexer.token()
        if not tok:
            break
        with open("Tokens.txt", "a") as archivo_tokens:
            archivo_tokens.write(f"{tok.value}\t{tok.type}\tLínea {tok.lineno}\n")

