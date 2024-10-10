import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView, QFileDialog, QTreeWidgetItem, QTextEdit, QLineEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont

from analizador_lexico import analizar_codigo
from analizador_sintaxis import analizar_sintactico
from syntax_highlighter import Highlighter
from symtab import SymbolTable
from analizador_semantico import analizar_semantico

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ide.ui", self)
        
        self.symbol_table = SymbolTable()
        self.highlighter = Highlighter(self.seccionCodigo.document())

        # Conectar los widgets necesarios
        self.seccionCodigo = self.findChild(QTextEdit, 'seccionCodigo')
        self.mostrarCursor = self.findChild(QLineEdit, 'mostrarCursor')
        self.mostrarLinea = self.findChild(QTextEdit, 'mostrarLinea')

        # Asegurarse de que mostrarLinea sea de solo lectura
        self.mostrarLinea.setReadOnly(True)
        
        # Conectar señales
        self.seccionCodigo.cursorPositionChanged.connect(self.actualizar_posicion)
        self.seccionCodigo.textChanged.connect(self.actualizar_numeros_linea)
        
        # Inicializar los valores
        self.actualizar_numeros_linea()
        self.actualizar_posicion()

        self.actionLexico.triggered.connect(self.realizar_analisis_lexico)
        self.actionSintactico.triggered.connect(self.realizar_analisis_sintactico)
        self.actionSemantico.triggered.connect(self.realizar_analisis_semantico)

        self.modelo_lexico = QStandardItemModel()
        self.modelo_lexico.setHorizontalHeaderLabels(['Tipo', 'Valor', 'Línea'])
        self.resultadoLexico.setModel(self.modelo_lexico)
    
    def actualizar_posicion(self):
        # Obtener la posición del cursor
        cursor = self.seccionCodigo.textCursor()
        linea = cursor.blockNumber() + 1
        columna = cursor.columnNumber() + 1
        self.mostrarCursor.setText(f"Línea: {linea}, Columna: {columna}")

    def actualizar_numeros_linea(self):
        # Obtener el número total de líneas
        total_lineas = self.seccionCodigo.document().blockCount()
        numeros_linea = "\n".join(str(i + 1) for i in range(total_lineas))
        self.mostrarLinea.setPlainText(numeros_linea)


    def realizar_analisis_lexico(self):
        codigo = self.seccionCodigo.toPlainText()
        analizar_codigo(codigo)
        self.mostrar_resultado_lexico("Tokens.txt")
        self.mostrar_errores_lexicos("Errores.txt")

    def realizar_analisis_sintactico(self):
        codigo = self.seccionCodigo.toPlainText()
        ast, errores_sintacticos = analizar_sintactico(codigo)
        
        if errores_sintacticos:
            self.mostrar_errores_sintacticos(errores_sintacticos)
        else:
            self.mostrar_arbol_sintactico(ast)
            self.symbol_table.generar_tabla_simbolos(ast, self.tablaSimbolos)

    def realizar_analisis_semantico(self):
        codigo = self.seccionCodigo.toPlainText()
        ast, errores_sintacticos = analizar_sintactico(codigo)

        if errores_sintacticos:
            self.errorSemantico.setText("No se puede realizar el análisis semántico debido a errores sintácticos.")
            return

        errores_semanticos = analizar_semantico(ast, self.symbol_table)

        if errores_semanticos:
            self.mostrar_errores_semanticos(errores_semanticos)
        else:
            self.mostrar_resultado_semantico(ast)

    def mostrar_resultado_lexico(self, archivo_tokens):
        # Limpiar el modelo anterior
        self.modelo_lexico.clear()
        self.modelo_lexico.setHorizontalHeaderLabels(['Tipo', 'Valor', 'Línea'])

        # Leer los resultados del archivo de tokens
        with open(archivo_tokens, 'r') as file:
            tokens = file.readlines()
            for token in tokens:
                datos = token.strip().split('\t')  # Suponiendo que los tokens están separados por tabulación
                if len(datos) == 3:  # Verificar que haya tres columnas: Tipo, Valor, Línea
                    fila = [QStandardItem(dato) for dato in datos]
                    self.modelo_lexico.appendRow(fila)

        # Asignar el modelo al QTableView
        self.resultadoLexico.setModel(self.modelo_lexico)

    def mostrar_errores_lexicos(self, archivo_errores):
        # Limpiar el QTextEdit "errorLexico" antes de mostrar nuevos errores
        self.errorLexico.clear()
        with open(archivo_errores, 'r') as archivo:
            errores = archivo.readlines()
            for error in errores:
                self.errorLexico.append(error.strip())

    def mostrar_errores_sintacticos(self, errores):
        self.errorSintactico.clear()
        for error in errores:
            self.errorSintactico.append(str(error))

    def mostrar_arbol_sintactico(self, ast):
        # Limpiar el QTreeWidget antes de agregar el árbol
        self.resultadoSintactico.clear()
        font = QFont()
        font.setPointSize(15)  # Puedes cambiar este valor al tamaño de fuente que desees
        self.resultadoSintactico.setFont(font)

        # Función recursiva para construir el árbol con anotaciones
        def construir_nodo_arbol(raiz, nodo):
            if isinstance(nodo, tuple):
                # Añadir anotación si el nodo contiene información adicional (tipo, valor, etc.)
                if len(nodo) > 2:
                    nuevo_nodo = QTreeWidgetItem([f"{nodo[0]} (tipo: {nodo[1]}, valor: {nodo[2]})"])
                else:
                    nuevo_nodo = QTreeWidgetItem([nodo[0]])
                raiz.addChild(nuevo_nodo)
                for subnodo in nodo[1:]:
                    construir_nodo_arbol(nuevo_nodo, subnodo)
            elif isinstance(nodo, list):
                for subnodo in nodo:
                    construir_nodo_arbol(raiz, subnodo)
            else:
                nuevo_nodo = QTreeWidgetItem([str(nodo)])
                raiz.addChild(nuevo_nodo)

        # Crear el nodo raíz del árbol sintáctico
        raiz = QTreeWidgetItem(self.resultadoSintactico)
        raiz.setText(0, "Programa")

        # Construir el árbol desde el AST
        construir_nodo_arbol(raiz, ast)

        # Expandir todo el árbol para que se vea completo
        self.resultadoSintactico.expandAll()

    def mostrar_errores_semanticos(self, errores):
        self.errorSemantico.clear()
        for error in errores:
            self.errorSemantico.append(str(error))

    def mostrar_resultado_semantico(self, ast):
        self.symbol_table.generar_tabla_simbolos(ast, self.resultadoSemantic)
        self.errorSemantico.clear()
        self.errorSemantico.append("Análisis semántico completado sin errores.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = IDE()
    ventana.show()
    sys.exit(app.exec_())
