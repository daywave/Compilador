import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView, QFileDialog, QTreeWidgetItem, QTextEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont

from analizador_lexico import analizar_codigo  # Importar el analizador léxico
from analizador_sintaxis import analizar_sintactico  # Importar el analizador sintáctico
from syntax_highlighter import Highlighter
from symtab import SymbolTable


class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ide.ui", self)  # Cargar el archivo .ui
        
        self.symbol_table = SymbolTable()  # Instancia de la tabla de símbolos
        # Configurar el resaltador de sintaxis
        self.highlighter = Highlighter(self.seccionCodigo.document())
        # Conectar las acciones de los botones
        self.actionLexico.triggered.connect(self.realizar_analisis_lexico)
        self.actionSintactico.triggered.connect(self.realizar_analisis_sintactico)

        # Configurar modelo de la tabla para mostrar los tokens
        self.modelo_lexico = QStandardItemModel()
        self.modelo_lexico.setHorizontalHeaderLabels(['Tipo', 'Valor', 'Línea'])
        self.resultadoLexico.setModel(self.modelo_lexico)

    def realizar_analisis_lexico(self):
        # Obtener el código del QTextEdit llamado "seccionCodigo"
        codigo = self.seccionCodigo.toPlainText()

        # Llamar al análisis léxico y generar los archivos de tokens y errores
        analizar_codigo(codigo)

        # Leer errores desde el archivo
        with open("Errores.txt", 'r') as archivo_errores:
            errores = archivo_errores.readlines()

        # Si hay errores léxicos, mostrarlos en el QTextEdit "errorLexico"
        if errores:
            self.mostrar_errores_lexicos(errores)
            self.resultadoLexico.setModel(None)  # Limpiar la tabla de tokens
        else:
            # Si no hay errores, mostrar los tokens
            self.mostrar_resultado_lexico("Tokens.txt")

    def realizar_analisis_sintactico(self):
        # Leer el código nuevamente para análisis sintáctico
        codigo = self.seccionCodigo.toPlainText()

        # Fase 2: Realizar el análisis sintáctico si no hay errores léxicos
        ast, errores_sintacticos = analizar_sintactico(codigo)

        # Leer y mostrar los errores sintácticos desde el archivo
        with open("ErroresSintacticos.txt", "r") as archivo_errores:
            errores = archivo_errores.read()
            if errores.strip() != "Sin errores sintácticos":
                self.errorSintactico.setText(errores)
                self.resultadoSintactico.clear()
                self.tablaSimbolos.setModel(None)  # Limpiar la tabla de símbolos
            else:
                # Mostrar el árbol sintáctico en el QTreeWidget
                with open("ArbolSintactico.txt", "r") as archivo_arbol:
                    arbol = eval(archivo_arbol.read())  # Convertir el string a estructura de Python
                    self.mostrar_arbol_sintactico(arbol)

                # Generar la tabla de símbolos y mostrarla en el QTableView
                self.symbol_table.generar_tabla_simbolos(ast, self.tablaSimbolos)

    def mostrar_errores_lexicos(self, errores):
        # Limpiar el QTextEdit "errorLexico" antes de mostrar nuevos errores
        self.errorLexico.clear()
        for error in errores:
            self.errorLexico.append(error)

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

# Función principal para ejecutar el IDE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = IDE()
    ventana.show()
    sys.exit(app.exec_())
