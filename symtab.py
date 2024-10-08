from PyQt5.QtGui import QStandardItemModel, QStandardItem

class SymbolTable:
    def __init__(self):
        self.tabla_simbolos = {}  # Usamos un diccionario para manejar los símbolos

    def extraer_identificadores(self, nodo):
        if isinstance(nodo, tuple) and nodo[0] == 'lista_ids':
            # Verificamos que el nodo tenga los elementos antes de acceder a ellos
            if len(nodo) > 2:
                return self.extraer_identificadores(nodo[1]) + ", " + self.extraer_identificadores(nodo[2])
            elif len(nodo) > 1:
                return self.extraer_identificadores(nodo[1])
        # Si no es una lista de identificadores, simplemente devolvemos el identificador
        return str(nodo)

    def agregar_a_tabla(self, variable, tipo, valor, linea):
        """Agrega o actualiza una variable en la tabla de símbolos."""
        if variable in self.tabla_simbolos:
            # Si la variable ya está, actualizamos el valor y agregamos la nueva línea si no está ya registrada
            if linea not in self.tabla_simbolos[variable]['lineas']:
                self.tabla_simbolos[variable]['lineas'].append(linea)
            self.tabla_simbolos[variable]['valor'] = valor  # Se actualiza el valor si es necesario
        else:
            # Si la variable no está, la agregamos a la tabla
            self.tabla_simbolos[variable] = {
                'tipo': tipo,
                'valor': valor,
                'lineas': [linea]
            }

    def procesar_expresion(self, nodo, linea_actual):
        """Revisa cualquier expresión para encontrar variables y actualizar la tabla de símbolos."""
        if isinstance(nodo, tuple):
            if nodo[0] == 'identificador':  # Si es un identificador, es un uso de una variable
                variable = nodo[1]
                if variable in self.tabla_simbolos:
                    self.agregar_a_tabla(variable, self.tabla_simbolos[variable]['tipo'], self.tabla_simbolos[variable]['valor'], linea_actual)
            # Procesar recursivamente los subnodos
            for subnodo in nodo[1:]:
                self.procesar_expresion(subnodo, linea_actual)

    def generar_tabla_simbolos(self, ast, tablaSimbolosWidget):
        modelo_tabla = QStandardItemModel()
        modelo_tabla.setHorizontalHeaderLabels(['Localización', 'Variable', 'Tipo', 'Valor', 'Líneas'])

        # Reiniciamos la tabla de símbolos antes de generar una nueva
        self.tabla_simbolos = {}

        def procesar_nodo(nodo, linea_actual):
            if isinstance(nodo, tuple):
                # Detectar declaraciones y asignaciones
                if nodo[0] == 'declaracion':
                    # Caso de declaración
                    variables = self.extraer_identificadores(nodo[2])  # Obtener todas las variables
                    tipo = str(nodo[1])  # Tipo de variable (por ejemplo, 'int')
                    valor = 'N/A'  # Valor inicial
                    for variable in variables.split(', '):  # Procesar cada variable de la lista
                        self.agregar_a_tabla(variable, tipo, valor, linea_actual)
                elif nodo[0] == 'asignacion':
                    # Caso de asignación
                    variable = nodo[1]  # Nombre de la variable
                    valor = nodo[2]  # Valor asignado
                    self.agregar_a_tabla(variable, self.tabla_simbolos[variable]['tipo'], valor, linea_actual)

                # Procesar otras expresiones o usos de variables (por ejemplo, en condiciones de if/while)
                if nodo[0] in ['while', 'if']:
                    self.procesar_expresion(nodo[1], linea_actual)  # Procesar la condición del while o if

                # Procesar subnodos recursivamente y actualizamos la línea si es necesario
                for subnodo in nodo[1:]:
                    procesar_nodo(subnodo, linea_actual)
            elif isinstance(nodo, list):
                for subnodo in nodo:
                    procesar_nodo(subnodo, linea_actual)

        # Recorremos el AST e incrementamos la línea actual donde encontramos usos de variables
        linea_actual = 1
        for nodo in ast:
            procesar_nodo(nodo, linea_actual)
            linea_actual += 1  # Suposición: un nodo por línea de código

        # Formatear y agregar los datos a la tabla de símbolos
        for loc, (variable, datos) in enumerate(self.tabla_simbolos.items(), start=1):
            lineas_formato = ', '.join(map(str, datos['lineas']))  # Convertir las líneas a un formato legible

            # Crear los items para cada columna
            loc_item = QStandardItem(str(loc))  # Localización (número de entrada en la tabla)
            var_item = QStandardItem(variable)  # Nombre de la variable
            tipo_item = QStandardItem(datos['tipo'])  # Tipo de la variable
            valor_item = QStandardItem(str(datos['valor']))  # Valor de la variable (si tiene)
            lineas_item = QStandardItem(f"[{lineas_formato}]")  # Líneas donde aparece la variable

            # Agregar la fila a la tabla
            modelo_tabla.appendRow([loc_item, var_item, tipo_item, valor_item, lineas_item])

        # Asignar el modelo al widget de la tabla de símbolos
        tablaSimbolosWidget.setModel(modelo_tabla)
