class Nodo:
    def __init__(self, tipoNodo=None, linea=0):
        self.hijos = [None, None, None]  # Máximo de 3 hijos, puede variar
        self.hermanos = None
        self.linea = linea
        self.tipoNodo = tipoNodo  # Sentencia, Expresion o Declaracion
        self.tipoDec = None  # int, float o boolean
        self.tipoSen = None  # if, while, ...
        self.tipoExp = None  # Id, Constante, Operador
        self.nomIdExp = None  # Nombre del identificador en expresiones
        self.valCteExp = None  # Valor de constante en expresiones
        self.OpExp = None  # Operador en expresiones
        self.error = None  # Manejo de errores
