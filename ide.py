import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView, QFileDialog, QTreeWidgetItem, QTextEdit, QLineEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont

from analizador_lexico import analizar_codigo
from analizador_sintaxis import analizar_sintactico, Nodo
from syntax_highlighter import Highlighter

class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ide.ui", self)
        
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

        # Modelo para la tabla de tokens
        self.modelo_lexico = QStandardItemModel()
        self.modelo_lexico.setHorizontalHeaderLabels(['Tipo', 'Valor', 'Línea'])
        self.resultadoLexico.setModel(self.modelo_lexico)

    def actualizar_posicion(self):
        cursor = self.seccionCodigo.textCursor()
        linea = cursor.blockNumber() + 1
        columna = cursor.columnNumber() + 1
        self.mostrarCursor.setText(f"Línea: {linea}, Columna: {columna}")

    def actualizar_numeros_linea(self):
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
        ast, _ = analizar_sintactico(codigo)
        
        if ast:
            self.mostrar_arbol_sintactico(ast)
        else:
            self.mostrar_errores_sintacticos(["Error durante el análisis sintáctico"])

    def mostrar_resultado_lexico(self, archivo_tokens):
        self.modelo_lexico.clear()
        self.modelo_lexico.setHorizontalHeaderLabels(['Tipo', 'Valor', 'Línea'])

        with open(archivo_tokens, 'r') as file:
            tokens = file.readlines()
            for token in tokens:
                datos = token.strip().split('\t')
                if len(datos) == 3:
                    fila = [QStandardItem(dato) for dato in datos]
                    self.modelo_lexico.appendRow(fila)

        self.resultadoLexico.setModel(self.modelo_lexico)

    def mostrar_errores_lexicos(self, archivo_errores):
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
        self.resultadoSintactico.clear()
        font = QFont()
        font.setPointSize(12)
        self.resultadoSintactico.setFont(font)

        def construir_nodo_arbol(raiz, nodo):
            if isinstance(nodo, Nodo):
                nuevo_nodo = QTreeWidgetItem([str(nodo.tipo)])
                raiz.addChild(nuevo_nodo)
                if nodo.valor:
                    valor_nodo = QTreeWidgetItem([f"Valor: {nodo.valor}"])
                    nuevo_nodo.addChild(valor_nodo)
                for hijo in nodo.hijos:
                    construir_nodo_arbol(nuevo_nodo, hijo)

        raiz = QTreeWidgetItem(self.resultadoSintactico)
        raiz.setText(0, "Programa")
        construir_nodo_arbol(raiz, ast)
        self.resultadoSintactico.expandToDepth(2)  # Expandir hasta el segundo nivel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = IDE()
    ventana.show()
    sys.exit(app.exec_())
