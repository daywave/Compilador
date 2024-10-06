from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView, QTableWidgetItem, QFileDialog, QTreeWidgetItem, QTextEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
from lexico import analizar  
import sintactico  
from semantico import analizar_semantico
import traceback
import sys
import io 

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


        self.modelo_lexico = QStandardItemModel()
        self.resultadoLexico.setModel(self.modelo_lexico)
        self.actionCompilar.triggered.connect(self.compilarCodigo)
        self.errorTextEdit = self.mostrarErrores


        self.redirect_stderr()

    def redirect_stderr(self):
        """Redirige stderr a un stream que captura los errores."""
        self.stderr_buffer = io.StringIO()
        sys.stderr = self.stderr_buffer

    def compilarCodigo(self):
        try:
            codigo = self.seccionCodigo.toPlainText()

            self.mostrarErrores.clear()

            tokens_encontrados = analizar(codigo)
            self.mostrarResultadosLexicos(tokens_encontrados)
            arbol_sintactico, errores_sintacticos = sintactico.analizar_sintactico(codigo)

            if errores_sintacticos:
                for error in errores_sintacticos:
                    self.display_errors(error)  

            else:
                self.display_syntactic_tree(arbol_sintactico)

                try:
                    errores_semanticos = analizar_semantico(arbol_sintactico)
                    if errores_semanticos:
                        
                        for error in errores_semanticos:
                            self.display_errors(error)  # Mostrar cada error semántico en el widget
                    else:
                        self.display_success()  
                except Exception as e:
                    error_msg = f"Error en el análisis semántico: \n{str(e)}\n\n"
                    error_msg += f"Traceback: \n{''.join(traceback.format_tb(e.__traceback__))}"
                    self.display_errors(error_msg)

        except Exception as e:
            error_msg = f"Error en la compilación: \n{str(e)}\n\n"
            error_msg += f"Traceback: \n{''.join(traceback.format_tb(e.__traceback__))}"
            self.display_errors(error_msg) 

        self.display_captured_errors()

    def display_captured_errors(self):
        """Muestra los errores capturados de stderr en el widget de errores."""
        captured_errors = self.stderr_buffer.getvalue()
        if captured_errors:
            self.display_errors(captured_errors)
        self.stderr_buffer.truncate(0)

    def display_errors(self, error_msg):
        self.mostrarErrores.append(f"<span style='color:red;'>{error_msg}</span>")

    def display_success(self):
        self.mostrarErrores.append("<span style='color:green;'>Análisis semántico exitoso!</span>")

    def display_syntactic_tree(self, ast):
        self.resultadoSintactico.clear()
        # Crear el nodo raíz
        root = QTreeWidgetItem(self.resultadoSintactico)
        root.setText(0, "AST")
        # Poblamos el árbol con el resultado del AST
        self.populate_tree_view(self.resultadoSintactico, ast, root)
        
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
            for child in node:
                self.populate_tree_view(tree_widget, child, parent)
        else:
            leaf_item = QTreeWidgetItem(parent)
            leaf_item.setText(0, str(node))

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

    def newFile(self):
        self.seccionCodigo.clear()
        self.modelo_lexico.clear()  
        self.resultadoSintactico.clear()  
        self.mostrarErrores.clear()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())