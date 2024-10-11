# symtab.py
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def insert(self, name, tipo, valor, linea):
        if name in self.symbols:
            print(f"Advertencia: La variable '{name}' ya estaba definida. Actualizando su valor.")
        self.symbols[name] = {
            'tipo': tipo,
            'valor': valor,
            'linea': linea
        }

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        else:
            raise NameError(f"Variable '{name}' no definida")

    def print_table(self):
        print("Tabla de Símbolos:")
        for name, attributes in self.symbols.items():
            print(f"Nombre: {name}, Tipo: {attributes['tipo']}, Valor: {attributes['valor']}, Línea: {attributes['linea']}")

    def generate_qt_model(self):
        from PyQt5.QtGui import QStandardItemModel, QStandardItem
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Nombre', 'Tipo', 'Valor', 'Línea'])

        for name, attributes in self.symbols.items():
            row = [
                QStandardItem(name),
                QStandardItem(attributes['tipo']),
                QStandardItem(str(attributes['valor'])),
                QStandardItem(str(attributes['linea']))
            ]
            model.appendRow(row)

        return model
