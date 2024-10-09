from PyQt5.QtGui import QStandardItemModel, QStandardItem

class SymbolTable:
    def __init__(self):
        self.tabla_simbolos = {}  # Diccionario para manejar los símbolos

    def extraer_identificadores(self, nodo):
        if isinstance(nodo, tuple) and nodo[0] == 'lista_ids':
            if len(nodo) > 2:
                return self.extraer_identificadores(nodo[1]) + ", " + self.extraer_identificadores(nodo[2])
            elif len(nodo) > 1:
                return self.extraer_identificadores(nodo[1])
        return str(nodo)

    def evaluar_expresion(self, nodo):
        """Evalúa una expresión binaria o numérica."""
        if isinstance(nodo, tuple):
            if nodo[0] == 'expresion_binaria':
                operador = nodo[1]
                lado_izquierdo = self.evaluar_expresion(nodo[2])
                lado_derecho = self.evaluar_expresion(nodo[3])

                # Convertir los operandos a float si son números en formato string
                if isinstance(lado_izquierdo, str) and lado_izquierdo.replace('.', '', 1).isdigit():
                    lado_izquierdo = float(lado_izquierdo)
                if isinstance(lado_derecho, str) and lado_derecho.replace('.', '', 1).isdigit():
                    lado_derecho = float(lado_derecho)

                # Realizar la operación según el operador
                if isinstance(lado_izquierdo, (int, float)) and isinstance(lado_derecho, (int, float)):
                    if operador == '+':
                        return lado_izquierdo + lado_derecho
                    elif operador == '-':
                        return lado_izquierdo - lado_derecho
                    elif operador == '*':
                        return lado_izquierdo * lado_derecho
                    elif operador == '/':
                        if lado_derecho != 0:
                            return lado_izquierdo / lado_derecho
                        else:
                            return 'Error: División por cero'
                    elif operador == '%':
                        return lado_izquierdo % lado_derecho
                else:
                    return 'Error: Operandos no numéricos'
            elif nodo[0] == 'numero':
                return float(nodo[1])  # Convertir el número a float
            elif nodo[0] == 'variable':
                variable = nodo[1]
                if variable in self.tabla_simbolos:
                    return self.tabla_simbolos[variable]['valor']
        return nodo

    def agregar_a_tabla(self, variable, tipo, valor, linea):
        """Agrega o actualiza una variable en la tabla de símbolos."""
        valor_evaluado = self.evaluar_expresion(valor)  # Evaluar la expresión antes de almacenar
        if variable in self.tabla_simbolos:
            # Actualizamos el valor y agregamos la nueva línea si no está ya registrada
            if linea not in self.tabla_simbolos[variable]['lineas']:
                self.tabla_simbolos[variable]['lineas'].append(linea)
            self.tabla_simbolos[variable]['valor'] = valor_evaluado  # Actualizamos el valor
        else:
            # Si la variable no está, la agregamos a la tabla
            self.tabla_simbolos[variable] = {
                'tipo': tipo,
                'valor': valor_evaluado,
                'lineas': [linea]
            }

    def procesar_expresion(self, nodo, linea_actual):
        """Procesa una expresión para encontrar variables y actualizar la tabla de símbolos."""
        if isinstance(nodo, tuple):
            if nodo[0] == 'identificador':  # Es un identificador, es un uso de una variable
                variable = nodo[1]
                if variable in self.tabla_simbolos:
                    self.agregar_a_tabla(variable, self.tabla_simbolos[variable]['tipo'], self.tabla_simbolos[variable]['valor'], linea_actual)
            # Procesar subnodos recursivamente
            for subnodo in nodo[1:]:
                self.procesar_expresion(subnodo, linea_actual)

    def generar_tabla_simbolos(self, ast, tablaSimbolosWidget):
        modelo_tabla = QStandardItemModel()
        modelo_tabla.setHorizontalHeaderLabels(['Localización', 'Variable', 'Tipo', 'Valor', 'Líneas'])

        self.tabla_simbolos = {}

        def procesar_nodo(nodo, linea_actual):
            if isinstance(nodo, tuple):
                if nodo[0] == 'declaracion':
                    variables = self.extraer_identificadores(nodo[2])  # Obtener todas las variables
                    tipo = str(nodo[1])  # Tipo de variable (por ejemplo, 'int')
                    valor = 'N/A'  # Valor inicial
                    for variable in variables.split(', '):  # Procesar cada variable de la lista
                        self.agregar_a_tabla(variable, tipo, valor, linea_actual)
                elif nodo[0] == 'asignacion':
                    variable = nodo[1]  # Nombre de la variable
                    valor = nodo[2]  # Valor asignado (puede ser una expresión compleja)
                    self.agregar_a_tabla(variable, self.tabla_simbolos[variable]['tipo'], valor, linea_actual)

                    linea_actual += 1

                if nodo[0] in ['if', 'while', 'do', 'read', 'write']:
                    self.procesar_expresion(nodo[1], linea_actual)

                for subnodo in nodo[1:]:
                    linea_actual = procesar_nodo(subnodo, linea_actual)
            elif isinstance(nodo, list):
                for subnodo in nodo:
                    linea_actual = procesar_nodo(subnodo, linea_actual)

            # Retornar la línea actual para el siguiente nodo
            return linea_actual

        # Incrementar la línea actual para cada nodo en el AST
        linea_actual = 1
        for nodo in ast:
            linea_actual = procesar_nodo(nodo, linea_actual)

        # Formatear y agregar los datos a la tabla de símbolos
        for loc, (variable, datos) in enumerate(self.tabla_simbolos.items(), start=1):
            lineas_formato = ', '.join(map(str, datos['lineas']))  # Formato de líneas

            # Verificar si el valor es un número flotante y redondearlo a 4 decimales
            if isinstance(datos['valor'], float):
                valor_formateado = f"{datos['valor']:.4f}"
            else:
                valor_formateado = str(datos['valor'])

            # Crear los items para cada columna
            loc_item = QStandardItem(str(loc))  # Localización (número de entrada en la tabla)
            var_item = QStandardItem(variable)  # Nombre de la variable
            tipo_item = QStandardItem(datos['tipo'])  # Tipo de la variable
            valor_item = QStandardItem(valor_formateado)  # Valor de la variable (redondeado si es float)
            lineas_item = QStandardItem(f"[{lineas_formato}]")  # Líneas donde aparece la variable

            # Agregar la fila a la tabla
            modelo_tabla.appendRow([loc_item, var_item, tipo_item, valor_item, lineas_item])

        # Asignar el modelo al widget de la tabla de símbolos
        tablaSimbolosWidget.setModel(modelo_tabla)
