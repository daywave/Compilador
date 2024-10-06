import ast

class AnalizadorSemantico:
    def __init__(self):
        self.tabla_simbolos = {}
        self.errores = []

    

    def analizar(self, arbol_sintactico):
        if arbol_sintactico is None:
            self.errores.append("Error: El árbol sintáctico es None")
            return self.errores
        
        print(f"Estructura del árbol sintáctico: {self.estructura_arbol(arbol_sintactico)}")
        self.visitar(arbol_sintactico)
        return self.errores
    
    def estructura_arbol(self, nodo, nivel=0):
        if isinstance(nodo, (list, tuple)):
            return f"{'  ' * nivel}{type(nodo).__name__}[{len(nodo)}]: {[self.estructura_arbol(hijo, nivel+1) for hijo in nodo]}"
        else:
            return f"{'  ' * nivel}{type(nodo).__name__}: {nodo}"
        
    def visitar(self, nodo):
        if not isinstance(nodo, (list, tuple)):
            print(f"Nodo no es lista o tupla: {nodo}")
            return

        if len(nodo) == 0:
            print("Nodo es una lista o tupla vacía")
            return

        tipo_nodo = nodo[0] if isinstance(nodo[0], str) else type(nodo[0]).__name__
        metodo = getattr(self, f'visitar_{tipo_nodo}', self.visitar_desconocido)
        return metodo(nodo)

    def visitar_desconocido(self, nodo):
        print(f"Nodo desconocido: {nodo[0] if len(nodo) > 0 else 'vacío'}")

    def visitar_programa(self, nodo):
        if len(nodo) < 3:
            self.errores.append(f"Error: Nodo 'programa' no tiene suficientes elementos: {nodo}")
            return
        self.visitar(nodo[1])  # list_decl
        self.visitar(nodo[2])  # list_sent

    def visitar_decl(self, nodo):
        tipo = nodo[1]
        for var in nodo[2]:
            if var in self.tabla_simbolos:
                self.errores.append(f"Error semántico: Variable '{var}' ya declarada")
            else:
                self.tabla_simbolos[var] = {'tipo': tipo}

    def visitar_sent_assign(self, nodo):
        var = nodo[1]
        valor = self.visitar(nodo[2])
        if var not in self.tabla_simbolos:
            self.errores.append(f"Error semántico: Variable '{var}' no declarada")
        else:
            tipo_var = self.tabla_simbolos[var]['tipo']
            tipo_valor = self.inferir_tipo(valor)
            if tipo_var != tipo_valor:
                self.errores.append(f"Error semántico: Asignación de tipo incorrecto a '{var}'")

    def visitar_sent_if(self, nodo):
        condicion = self.visitar(nodo[1])
        if self.inferir_tipo(condicion) != 'BOOLEANO':
            self.errores.append("Error semántico: La condición del if debe ser booleana")
        self.visitar(nodo[2])  # bloque then
        if len(nodo) > 3:
            self.visitar(nodo[3])  # bloque else

    def visitar_sent_while(self, nodo):
        condicion = self.visitar(nodo[1])
        if self.inferir_tipo(condicion) != 'BOOLEANO':
            self.errores.append("Error semántico: La condición del while debe ser booleana")
        self.visitar(nodo[2])  # bloque

    def visitar_sent_do(self, nodo):
        self.visitar(nodo[1])  # bloque
        condicion = self.visitar(nodo[2])
        if self.inferir_tipo(condicion) != 'BOOLEANO':
            self.errores.append("Error semántico: La condición del do-until debe ser booleana")

    def visitar_sent_read(self, nodo):
        var = nodo[1]
        if var not in self.tabla_simbolos:
            self.errores.append(f"Error semántico: Variable '{var}' no declarada")

    def visitar_sent_write(self, nodo):
        self.visitar(nodo[1])

    def visitar_exp_bool(self, nodo):
        if len(nodo) == 4:
            izq = self.visitar(nodo[1])
            der = self.visitar(nodo[3])
            if self.inferir_tipo(izq) != 'BOOLEANO' or self.inferir_tipo(der) != 'BOOLEANO':
                self.errores.append("Error semántico: Operación booleana con operandos no booleanos")
        else:
            return self.visitar(nodo[1])

    def inferir_tipo(self, nodo):
        if isinstance(nodo, tuple):
            if nodo[0] in ['NUMERO', 'ID']:
                return 'ENTERO' if isinstance(nodo[1], int) else 'FLOTANTE'
            elif nodo[0] in ['VERDADERO', 'FALSO']:
                return 'BOOLEANO'
            elif nodo[0] in ['exp_bool', 'comb', 'igualdad', 'rel']:
                return 'BOOLEANO'
            elif nodo[0] in ['expr', 'term', 'unario']:
                return 'ENTERO'  # Simplificación, podría ser FLOTANTE en algunos casos
        return 'DESCONOCIDO'

def analizar_semantico(arbol_sintactico):
    analizador = AnalizadorSemantico()
    errores = analizador.analizar(arbol_sintactico)
    return errores