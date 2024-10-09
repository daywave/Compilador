class AnalizadorSemantico:
    def __init__(self, tabla_simbolos):
        self.tabla_simbolos = tabla_simbolos  # La tabla de símbolos con la que trabajar
        self.errores_semanticos = []

    def verificar_nodo(self, nodo):
        if nodo[0] == 'declaracion':
            self.verificar_declaracion(nodo)
        elif nodo[0] == 'asignacion':
            self.verificar_asignacion(nodo)
        elif nodo[0] == 'expresion_binaria':
            return self.verificar_operacion(nodo)
        # Aquí puedes añadir más casos como control, lectura, escritura, etc.

    def verificar_declaracion(self, nodo):
        tipo_var = nodo[1]  # Tipo de variable
        lista_vars = nodo[2]  # Lista de identificadores
        for var in self.extraer_identificadores(lista_vars):
            if self.tabla_simbolos.existe(var):
                self.errores_semanticos.append(f"Error: La variable {var} ya está declarada.")
            else:
                self.tabla_simbolos.agregar_a_tabla(var, tipo_var, 'N/A', 0)

    def verificar_asignacion(self, nodo):
        variable = nodo[1]
        valor_asignado = nodo[2]
        tipo_variable = self.tabla_simbolos.obtener_tipo(variable)
        tipo_valor_asignado = self.verificar_nodo(valor_asignado)
        
        if tipo_variable != tipo_valor_asignado:
            self.errores_semanticos.append(f"Error: No se puede asignar {tipo_valor_asignado} a la variable {variable} de tipo {tipo_variable}")

    def verificar_operacion(self, nodo):
        tipo_izq = self.verificar_nodo(nodo[2])
        tipo_der = self.verificar_nodo(nodo[3])
        if tipo_izq != tipo_der:
            self.errores_semanticos.append(f"Error de tipos: No se puede operar {tipo_izq} con {tipo_der}")
        return 'float' if tipo_izq == 'float' or tipo_der == 'float' else 'int'

    def extraer_identificadores(self, nodo):
        if nodo[0] == 'lista_ids':
            return [nodo[1]] + self.extraer_identificadores(nodo[2]) if len(nodo) > 2 else [nodo[1]]
        return [nodo]

    def obtener_errores(self):
        return self.errores_semanticos

# Ejemplo de cómo usar el analizador semántico
def analizar_semantico(arbol, tabla_simbolos):
    analizador = AnalizadorSemantico(tabla_simbolos)
    analizador.verificar_nodo(arbol)
    return analizador.obtener_errores()
