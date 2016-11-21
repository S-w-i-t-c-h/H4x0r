from PyQt5 import QtWidgets, QtCore, QtGui, Qsci

class Window(Qsci.QsciScintilla):
    ARROW_MARKER_NUM = 8
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        self.setWindowTitle("Code Editor")
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon))
        
        font = QtGui.QFont("Courier New", 10)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setMarginsFont(font)
        
        fontmetrics = QtGui.QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsForegroundColor(QtGui.QColor("#00f"))
        self.setMarginsBackgroundColor(QtGui.QColor("#111"))
        
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.on_margin_clicked)
        
        self.markerDefine(Qsci.QsciScintilla.RightArrow, self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QtGui.QColor("#ee1111"), self.ARROW_MARKER_NUM)
        
        self.setAutoIndent(True)
        self.setIndentationWidth(4)
        self.setIndentationGuides(True)
        self.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)
        
        self.setFolding(Qsci.QsciScintilla.BoxedTreeFoldStyle)
        self.setFoldMarginColors(QtGui.QColor("#111"), QtGui.QColor("#111"))
        
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QtGui.QColor("#222"))
        
        self.setAutoCompletionSource(Qsci.QsciScintilla.AcsDocument)
        self.setAutoCompletionThreshold(4)
        
        self.lexer = Qsci.QsciLexerPython()
        self.lexer.setDefaultFont(self.font())
        self.lexer.setDefaultPaper(QtGui.QColor("#000"))
        self.lexer.setDefaultColor(QtGui.QColor("#FFF"))
        
        colors = {"FunctionMethodName": "#0000ff", "ClassName": "#0000ff", "Comment": "#dd0000", "Decorator": "#ff7700", "Keyword": "#ff7700"}
        colors.update({key: "#00aa00" for key in ["UnclosedString", "DoubleQuotedString", "SingleQuotedString", "TripleDoubleQuotedString", "TripleSingleQuotedString"]})
        
        for key, color in colors.items():
            try:
                style = getattr(self.lexer, key)
                self.lexer.setColor(QtGui.QColor(color), style)
                self.lexer.setFont(QtGui.QFont(self.font()), style)
            except:
                pass
            
        self.setLexer(self.lexer)
        self.SendScintilla(Qsci.QsciScintilla.SCI_SETHSCROLLBAR, 0)
        
    def on_margin_clicked(self, nmargin, nline, modifiers):
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)
