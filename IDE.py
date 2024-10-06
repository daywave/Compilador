from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView, QTableWidgetItem, QFileDialog, QTreeWidgetItem, QTextEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
from lexico import analizar  # Importar la función del analizador léxico
import sintactico  # Importar el módulo del analizador sintáctico
from semantico import analizar_semantico
import traceback

import sys

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("ide.ui", self)
        
        # Conectar las acciones del menú
        self.actionNuevo.triggered.connect(self.newFile)
        self.actionAbrir.triggered.connect(self.openFile)
        self.actionGuardar.triggered.connect(self.saveFile)
        self.actionGuardar_como.triggered.connect(self.saveAsFile)
        self.actionDeshacer.triggered.connect(self.undo)
        self.actionCopiar.triggered.connect(self.copy)
        self.actionCortar.triggered.connect(self.cut)
        self.actionPegar.triggered.connect(self.paste)
        
        # Crear modelos para QTableView
        self.modelo_lexico = QStandardItemModel()
        self.resultadoLexico.setModel(self.modelo_lexico)
        
        # Conectar el botón Compilar al análisis léxico y sintáctico
        self.menuCompilar.triggered.connect(self.compilarCodigo)

        self.errorTextEdit = self.findChild(QTextEdit, 'errorTextEdit')
        self.errorText = QTextEdit()

    def compilarCodigo(self):
        # Obtener el texto del editor de código
        codigo = self.seccionCodigo.toPlainText()
        # Realizar el análisis léxico
        tokens_encontrados = analizar(codigo)
        # Mostrar los resultados en el QTableView
        self.mostrarResultadosLexicos(tokens_encontrados)
        # Realizar el análisis sintáctico
        #self.perform_syntactic_analysis(codigo)

        arbol_sintactico, error_sintactico = sintactico.analizar_sintactico(codigo)
        
        if error_sintactico:
            self.display_syntactic_error(error_sintactico)
        else:
            self.display_syntactic_tree(arbol_sintactico)

            #realizar analisis semantico
            try:
                errores_semanticos = analizar_semantico(arbol_sintactico)
                if errores_semanticos:
                    self.display_semantic_error(errores_semanticos)
                else:
                    self.display_semantic_success()
            except Exception as e:
                error_msg = f"Error en el análisis semántico: \n{str(e)}\n\n"
                error_msg += f"Traceback: \n{''.join(traceback.format_tb(e.__traceback__))}"
                self.display_semantic_error([error_msg])

    
    def display_semantic_error(self, title, message):
        error_text = f"{title}:\n{message}"
        if hasattr(self, 'errorTextEdit'):
            self.errorTextEdit.setPlainText(error_text)
        else:
            print(error_text)
    
    def display_success(self, message):
        if hasattr(self, 'errorTextEdit'):
            self.errorTextEdit.setPlainText(message)
        else:
            print(message)
    
    def display_semantic_error(self, errores):
        error_text = "Errores semánticos:\n + '\n'.join(errores)"
        self.errorText.setPlainText(error_text)

    def display_semantic_success(self):
        self.errorText.setPlainText("Análisis semántico exitoso")
    
    def mostrarResultadosLexicos(self, tokens):
        # Limpiar el modelo anterior
        self.modelo_lexico.clear()
        # Establecer las etiquetas de encabezado
        self.modelo_lexico.setHorizontalHeaderLabels(['Tipo', 'Valor', 'Línea'])
        # Llenar el modelo con los tokens encontrados
        for token in tokens:
            tipo_item = QStandardItem(token.type)
            valor_item = QStandardItem(str(token.value))
            linea_item = QStandardItem(str(token.lineno))
            self.modelo_lexico.appendRow([tipo_item, valor_item, linea_item])

    def perform_syntactic_analysis(self, code):
        try:
            result, error = sintactico.analizar_sintactico(code)
            if error:
                self.display_syntactic_error(error)
            else:
                self.display_syntactic_tree(result)
        except Exception as e:
            self.display_syntactic_error(str(e))

    def display_syntactic_tree(self, ast):
        # Limpiar el árbol sintáctico anterior
        self.resultadoSintactico.clear()
        # Crear el nodo raíz
        root = QTreeWidgetItem(self.resultadoSintactico)
        root.setText(0, "AST")
        # Poblamos el árbol con el resultado del AST
        self.populate_tree_view(self.resultadoSintactico, ast, root)
        # Expandir todos los elementos para una mejor visualización
        self.resultadoSintactico.expandAll()

    def populate_tree_view(self, tree_widget, node, parent):
        if isinstance(node, tuple):
            # El primer elemento del tuple es el nombre del nodo
            node_item = QTreeWidgetItem(parent)
            node_item.setText(0, node[0])
            # Recorrer los hijos del nodo
            for child in node[1:]:
                self.populate_tree_view(tree_widget, child, node_item)
        elif isinstance(node, list):
            # Si el nodo es una lista, recorremos sus elementos
            for child in node:
                self.populate_tree_view(tree_widget, child, parent)
        else:
            # Si el nodo es una hoja, se agrega directamente
            leaf_item = QTreeWidgetItem(parent)
            leaf_item.setText(0, str(node))

    def display_syntactic_error(self, error):
        # Mostramos el error en un QPlainTextEdit o QTextEdit
        self.errorText.setPlainText(f"Error: {error}")

    def newFile(self):
        self.seccionCodigo.clear()
        self.modelo_lexico.clear()  # Limpiar la tabla léxica
        self.resultadoSintactico.clear()  # Limpiar el árbol sintáctico
        self.errorText.clear()  # Limpiar el texto de error

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Archivos de texto (*.txt);;Todos los archivos (*)")
        if filename:
            with open(filename, 'r') as file:
                self.seccionCodigo.setPlainText(file.read())

    def saveFile(self):
        if hasattr(self, 'current_file'):
            with open(self.current_file, 'w') as file:
                file.write(self.seccionCodigo.toPlainText())
        else:
            self.saveAsFile()

    def saveAsFile(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar archivo como", "", "Archivos de texto (*.txt);;Todos los archivos (*)")
        if filename:
            with open(filename, 'w') as file:
                file.write(self.seccionCodigo.toPlainText())
            self.current_file = filename

    def undo(self):
        self.seccionCodigo.undo()

    def copy(self):
        self.seccionCodigo.copy()

    def cut(self):
        self.seccionCodigo.cut()

    def paste(self):
        self.seccionCodigo.paste()