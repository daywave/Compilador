from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegularExpression

class Highlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # Definir los formatos de texto para diferentes tipos de tokens
        self.highlightingRules = []

        # Formato para palabras reservadas
        reservedWordsFormat = QTextCharFormat()
        reservedWordsFormat.setForeground(QColor("blue"))
        reservedWordsFormat.setFontWeight(QFont.Bold)
        keywords = [
            "program", "int", "float", "bool", "if", "else", "then", "fi", "do", "while", "until", 
            "read", "write", "true", "false", "and", "or", "not"
        ]
        for word in keywords:
            pattern = f"\\b{word}\\b"
            self.highlightingRules.append((QRegularExpression(pattern), reservedWordsFormat))

        # Formato para números
        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor("darkMagenta"))
        self.highlightingRules.append((QRegularExpression("\\b[0-9]+(\\.[0-9]+)?\\b"), numberFormat))

        # Formato para comentarios
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("green"))
        commentFormat.setFontItalic(True)
        self.highlightingRules.append((QRegularExpression("//[^\n]*"), commentFormat))
        self.highlightingRules.append((QRegularExpression("/\\*.*\\*/"), commentFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = pattern
            matchIterator = expression.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                start, length = match.capturedStart(), match.capturedLength()
                self.setFormat(start, length, format)

        self.setCurrentBlockState(0)
