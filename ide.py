import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import lexico  # Importa el módulo lexico que contiene el lexer
import sintactico

class IDE:
    def __init__(self, root):
        self.root = root
        self.root.title("IDE - Compilador Personal")
        self.root.geometry("1200x800")
        self.root.configure(bg='#282C34')

        # Inicializa el lexer
        self.lexer = lexico.lexer

        self.create_menu_bar()
        self.create_code_editor()
        self.create_analysis_tabs()
        self.create_error_tabs()
        self.create_status_bar()

        self.file_path = None  # Para rastrear el archivo actual

        # Paleta de colores para los tokens
        self.token_colors = {
            'PROGRAMA': "#56B6C2",
            'SI': "#56B6C2",
            'SINO': "#56B6C2",
            'FSI': "#56B6C2",
            'HACER': "#56B6C2",
            'HASTA': "#56B6C2",
            'MIENTRAS': "#56B6C2",
            'LEER': "#56B6C2",
            'ESCRIBIR': "#56B6C2",
            'FLOTANTE': "#56B6C2",
            'ENTERO': "#56B6C2",
            'BOOLEANO': "#56B6C2",
            'NO': "#56B6C2",
            'AND': "#56B6C2",
            'OR': "#56B6C2",
            'VERDADERO': "#56B6C2",
            'FALSO': "#56B6C2",
            'SUMA': "#E06C75",
            'RESTA': "#E06C75",
            'MULT': "#E06C75",
            'DIV': "#E06C75",
            'POTENCIA': "#E06C75",
            'MENOR': "#E06C75",
            'MENORIGUAL': "#E06C75",
            'MAYOR': "#E06C75",
            'MAYORIGUAL': "#E06C75",
            'IGUAL': "#E06C75",
            'DISTINTO': "#E06C75",
            'ASIGNACION': "#E06C75",
            'PUNTOCOMA': "#E06C75",
            'COMA': "#E06C75",
            'PARIZQ': "#E06C75",
            'PARDER': "#E06C75",
            'LLAVIZQ': "#E06C75",
            'LLAVDER': "#E06C75",
            'ID': "#61AFEF",
            'NUMERO': "#D19A66",
            'BREAK': "#E06C75",
            'THEN': "#E06C75"
        }

        self.syntactic_text = None

    def create_menu_bar(self):
        menu_bar = tk.Menu(self.root, bg='#21252B', fg='#ABB2BF', activebackground='#61AFEF', activeforeground='#282C34')
        file_menu = tk.Menu(menu_bar, tearoff=0, bg='#21252B', fg='#ABB2BF')
        file_menu.add_command(label="Nuevo", command=self.new_file)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)
        file_menu.add_command(label="Guardar como", command=self.save_as_file)
        file_menu.add_command(label="Cerrar", command=self.close_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0, bg='#21252B', fg='#ABB2BF')
        edit_menu.add_command(label="Cortar", command=self.cut_text)
        edit_menu.add_command(label="Copiar", command=self.copy_text)
        edit_menu.add_command(label="Pegar", command=self.paste_text)
        menu_bar.add_cascade(label="Editar", menu=edit_menu)

        run_menu = tk.Menu(menu_bar, tearoff=0, bg='#21252B', fg='#ABB2BF')
        run_menu.add_command(label="Compilar", command=self.compile_code)
        menu_bar.add_cascade(label="Ejecutar", menu=run_menu)

        self.root.config(menu=menu_bar)

    def create_code_editor(self):
        self.code_editor_frame = tk.Frame(self.root, bg='#282C34')
        self.code_editor_frame.pack(fill="both", expand=True)

        self.line_numbers = tk.Text(self.code_editor_frame, width=4, padx=3, takefocus=0, border=0, background='#2C313C', fg='#ABB2BF', state='disabled')
        self.line_numbers.pack(side="left", fill="y")

        self.code_editor = tk.Text(self.code_editor_frame, wrap="none", undo=True, bg='#282C34', fg='#ABB2BF', insertbackground='#ABB2BF')
        self.code_editor.pack(side="left", fill="both", expand=True)
        self.code_editor.bind("<KeyRelease>", self.on_key_release)
        self.code_editor.bind("<MouseWheel>", self.update_cursor_position)

        self.scrollbar = tk.Scrollbar(self.code_editor_frame, orient="vertical", command=self.sync_scroll, bg='#21252B')
        self.scrollbar.pack(side="right", fill="y")

        self.code_editor.config(yscrollcommand=self.scrollbar.set)
        self.line_numbers.config(yscrollcommand=self.scrollbar.set)

        self.update_line_numbers()

    def sync_scroll(self, *args):
        self.code_editor.yview(*args)
        self.line_numbers.yview(*args)

    def update_line_numbers(self):
        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', 'end')
        current_line = 1
        while True:
            line_info = self.code_editor.dlineinfo(f"{current_line}.0")
            if line_info is None:
                break
            self.line_numbers.insert('end', f"{current_line}\n")
            current_line += 1
        self.line_numbers.config(state='disabled')

    def update_cursor_position(self, event=None):
        row, col = self.code_editor.index(tk.INSERT).split(".")
        self.cursor_position_label.config(text=f"Línea: {row}, Columna: {col}")
        self.update_line_numbers()

    def create_analysis_tabs(self):
        self.analysis_tabs = ttk.Notebook(self.root)
        self.analysis_tabs.pack(fill="both", expand=True)

        self.lexical_tab = tk.Frame(self.analysis_tabs, bg='#282C34')
        self.lexical_tree = ttk.Treeview(self.lexical_tab, columns=("Token", "Valor", "Fila", "Columna"), show='headings')
        self.lexical_tree.heading("Token", text="Token")
        self.lexical_tree.heading("Valor", text="Valor")
        self.lexical_tree.heading("Fila", text="Fila")
        self.lexical_tree.heading("Columna", text="Columna")
        self.lexical_tree.pack(fill="both", expand=True)

        self.syntactic_tab = tk.Frame(self.analysis_tabs, bg='#282C34')
        self.syntactic_tree = ttk.Treeview(self.syntactic_tab)
        self.syntactic_tree.pack(fill="both", expand=True)

        self.semantic_tab = tk.Frame(self.analysis_tabs, bg='#282C34')
        self.intermediate_code_tab = tk.Frame(self.analysis_tabs, bg='#282C34')
        self.compilation_output_tab = tk.Frame(self.analysis_tabs, bg='#282C34')
        self.compilation_output_text = tk.Text(self.compilation_output_tab, wrap="none", state="disabled", bg='#282C34', fg='#ABB2BF', insertbackground='#ABB2BF')
        self.compilation_output_text.pack(fill="both", expand=True)

        self.analysis_tabs.add(self.lexical_tab, text="Análisis léxico")
        self.analysis_tabs.add(self.syntactic_tab, text="Análisis sintáctico")
        self.analysis_tabs.add(self.semantic_tab, text="Análisis semántico")
        self.analysis_tabs.add(self.intermediate_code_tab, text="Código intermedio")
        self.analysis_tabs.add(self.compilation_output_tab, text="Salida de compilación")

    def create_error_tabs(self):
        self.error_tabs = ttk.Notebook(self.root)
        self.error_tabs.pack(fill="both", expand=True)

        self.error_tab = tk.Frame(self.error_tabs, bg='#282C34')
        self.error_text = tk.Text(self.error_tab, wrap="none", state="disabled", bg='#282C34', fg='#ABB2BF', insertbackground='#ABB2BF')
        self.error_text.pack(fill="both", expand=True)

        self.symbol_table_tab = tk.Frame(self.error_tabs, bg='#282C34')
        self.execution_result_tab = tk.Frame(self.error_tabs, bg='#282C34')

        self.error_tabs.add(self.error_tab, text="Errores compilación")
        self.error_tabs.add(self.symbol_table_tab, text="Tabla de símbolos")
        self.error_tabs.add(self.execution_result_tab, text="Resultado ejecución")

    def create_status_bar(self):
        self.status_bar = tk.Frame(self.root, bg='#21252B')
        self.status_bar.pack(fill='x', side='bottom')
        self.cursor_position_label = tk.Label(self.status_bar, text='Línea: 1, Columna: 0', bg='#21252B', fg='#ABB2BF')
        self.cursor_position_label.pack(side='right')

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, "w") as file:
                    content = self.code_editor.get("1.0", "end-1c")
                    file.write(content)
                    messagebox.showinfo("Guardar", "Archivo guardado con éxito")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".c", filetypes=[("C Files", ".c"), ("All Files", ".*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    content = self.code_editor.get("1.0", "end-1c")
                    file.write(content)
                    self.file_path = file_path  # Actualizar la ruta del archivo actual
                    messagebox.showinfo("Guardar como", "Archivo guardado con éxito")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def close_file(self):
        self.code_editor.delete("1.0", "end")
        self.file_path = None

    def cut_text(self):
        self.code_editor.event_generate("<<Cut>>")

    def copy_text(self):
        self.code_editor.event_generate("<<Copy>>")

    def paste_text(self):
        self.code_editor.event_generate("<<Paste>>")

    def execute_code(self, code):
        variables = {}
        output = ""
        for line in code.split('\n'):
            line = line.split('//')[0]  # Remove single-line comments
            line = line.split('/*')[0]  # Remove multi-line comments for simplicity
            line = line.strip()
            if line.startswith('write '):
                var_name = line.split()[1].strip(';')
                if var_name in variables:
                    output += str(variables[var_name]) + '\n'
            elif '=' in line:
                parts = line.split('=')
                if len(parts) == 2:
                    var_name, value = parts
                    var_name = var_name.strip()
                    value = value.strip(';').strip()
                    try:
                        value = self.evaluate_expression(value)
                    except ValueError:
                        pass
                    variables[var_name] = value
        return output

    def evaluate_expression(self, expression):
        try:
            return int(expression)
        except ValueError:
            pass
        try:
            return float(expression)
        except ValueError:
            pass
        return expression

    def compile_code(self):
        code = self.code_editor.get("1.0", "end-1c")
        self.perform_lexical_analysis(code)
        self.perform_syntactic_analysis(code)
        self.display_compilation_output("Compilación realizada con éxito")

        # Ejecutar el código compilado y mostrar la salida
        output = self.execute_code(code)
        self.display_execution_output(output)

    def perform_lexical_analysis(self, code):
        self.lexer.input(code)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        self.display_lexical_analysis(tokens)
        return tokens

    def display_lexical_analysis(self, tokens):
        self.lexical_tree.delete(*self.lexical_tree.get_children())
        for token in tokens:
            self.lexical_tree.insert("", "end", values=(token.type, token.value, token.lineno, token.lexpos))

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
        self.syntactic_tree.delete(*self.syntactic_tree.get_children())
        self.populate_tree_view(self.syntactic_tree, ast)

    def populate_tree_view(self, tree, node, parent=""):
        if isinstance(node, tuple):
            tag = node[0]
            # Insert the node and get its id
            tree_id = tree.insert(parent, "end", text=tag, open=True)
            # Recursively populate the tree for each child node
            for child in node[1:]:
                self.populate_tree_view(tree, child, parent=tree_id)
        elif isinstance(node, list):
            for child in node:
                self.populate_tree_view(tree, child, parent)
        else:
            # If the node is a leaf, insert it directly
            tree.insert(parent, "end", text=node)

    def display_syntactic_error(self, error):
        self.error_text.config(state="normal")
        self.error_text.delete("1.0", "end")
        self.error_text.insert("end", f"Error: {error}\n")
        self.error_text.config(state="disabled")

    def highlight_syntax(self, code):
        self.clear_tags()
        tokens = self.perform_lexical_analysis(code)
        for token in tokens:
            start_index = f"1.0+{token.lexpos}c"
            end_index = f"1.0+{token.lexpos + len(str(token.value))}c"
            color = self.token_colors.get(token.type, "#FFFFFF")
            self.code_editor.tag_add(token.type, start_index, end_index)
            self.code_editor.tag_config(token.type, foreground=color)

    def clear_tags(self):
        for tag in self.code_editor.tag_names():
            self.code_editor.tag_remove(tag, "1.0", tk.END)

    def on_key_release(self, event):
        self.update_line_numbers()
        self.update_cursor_position()
        self.highlight_syntax(self.code_editor.get("1.0", "end-1c"))

    def new_file(self):
        self.code_editor.delete("1.0", "end")
        self.file_path = None

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".c", filetypes=[("C Files", "*.c"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.code_editor.delete("1.0", "end")
                    self.code_editor.insert("1.0", content)
                    self.file_path = file_path
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def display_execution_output(self, output):
        self.execution_result_tab = tk.Frame(self.error_tabs, bg='#282C34')
        self.execution_result_text = tk.Text(self.execution_result_tab, wrap="none", state="normal", bg='#282C34',
                                             fg='#ABB2BF', insertbackground='#ABB2BF')
        self.execution_result_text.pack(fill="both", expand=True)
        self.execution_result_text.delete("1.0", "end")
        self.execution_result_text.insert("end", output)
        self.execution_result_text.config(state="disabled")
        self.error_tabs.add(self.execution_result_tab, text="Resultado ejecución")

if __name__ == "__main__":
    root = tk.Tk()
    app = IDE(root)
    root.mainloop()