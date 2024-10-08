from PyQt5.QtGui import QStandardItemModel, QStandardItem
from nodo import Nodo  # Importamos la clase Nodo

class SymbolTable:
    def __init__(self):
        self.tabla_simbolos = {}  # Usamos un diccionario para manejar los símbolos

    def extraer_identificadores(self, nodo):
        """Extrae los identificadores de un nodo."""
        if isinstance(nodo, Nodo) and nodo.tipoNodo == 'ListaIdentificadores':
            # Extraemos los identificadores recursivamente
            id1 = self.extraer_identificadores(nodo.hijos[0]) if nodo.hijos[0] else ''
            id2 = self.extraer_identificadores(nodo.hijos[1]) if nodo.hijos[1] else ''
            return id1 + (', ' if id1 and id2 else '') + id2
        return nodo.nomIdExp

    def agregar_a_tabla(self, variable, tipo, valor, linea):
        """Agrega o actualiza una variable en la tabla de símbolos."""
        if variable in self.tabla_simbolos:
            if linea not in self.tabla_simbolos[variable]['lineas']:
                self.tabla_simbolos[variable]['lineas'].append(linea)
            self.tabla_simbolos[variable]['valor'] = valor
        else:
            self.tabla_simbolos[variable] = {
                'tipo': tipo,
                'valor': valor,
                'lineas': [linea]
            }

    def procesar_expresion(self, nodo, linea_actual):
        """Procesa una expresión para detectar variables y actualizar la tabla de símbolos."""
        if isinstance(nodo, Nodo):
            if nodo.tipoNodo == 'variable':  # Si es un identificador (uso de una variable)
                variable = nodo.nomIdExp
                if variable in self.tabla_simbolos:
                    self.agregar_a_tabla(variable, self.tabla_simbolos[variable]['tipo'], self.tabla_simbolos[variable]['valor'], linea_actual)
            for hijo in nodo.hijos:
                if hijo:
                    self.procesar_expresion(hijo, linea_actual)

    def generar_tabla_simbolos(self, ast, tablaSimbolosWidget):
        modelo_tabla = QStandardItemModel()
        modelo_tabla.setHorizontalHeaderLabels(['Localización', 'Variable', 'Tipo', 'Valor', 'Líneas'])

        self.tabla_simbolos = {}  # Reiniciamos la tabla de símbolos

        def procesar_nodo(nodo, linea_actual):
            if isinstance(nodo, Nodo):
                if nodo.tipoNodo == 'Declaracion':
                    variables = self.extraer_identificadores(nodo.hijos[0])
                    tipo = nodo.tipoDec
                    valor = 'N/A'
                    for variable in variables.split(', '):
                        self.agregar_a_tabla(variable, tipo, valor, linea_actual)
                elif nodo.tipoNodo == 'Asignacion':
                    variable = nodo.nomIdExp
                    valor = nodo.hijos[0]
                    self.agregar_a_tabla(variable, self.tabla_simbolos.get(variable, {}).get('tipo', 'Desconocido'), valor, linea_actual)
                if nodo.tipoNodo in ['While', 'If']:
                    self.procesar_expresion(nodo.hijos[0], linea_actual)
                for hijo in nodo.hijos:
                    if hijo:
                        procesar_nodo(hijo, linea_actual)

        linea_actual = 1
        procesar_nodo(ast, linea_actual)

        for loc, (variable, datos) in enumerate(self.tabla_simbolos.items(), start=1):
            lineas_formato = ', '.join(map(str, datos['lineas']))
            loc_item = QStandardItem(str(loc))
            var_item = QStandardItem(variable)
            tipo_item = QStandardItem(datos['tipo'])
            valor_item = QStandardItem(str(datos['valor']))
            lineas_item = QStandardItem(f"[{lineas_formato}]")

            modelo_tabla.appendRow([loc_item, var_item, tipo_item, valor_item, lineas_item])

        tablaSimbolosWidget.setModel(modelo_tabla)
