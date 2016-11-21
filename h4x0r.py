import os, sys, time, urllib3, qdarkstyle, traceback, importlib
from PyQt5 import QtWidgets, QtCore, QtGui
import importlib.util


    
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        
        self.setWindowTitle("H4x0r")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))
        
        self.setWindowState(QtCore.Qt.WindowMaximized)
        
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        
        QtCore.QCoreApplication.setApplicationName("H4x0r")
        QtCore.QCoreApplication.setApplicationVersion("0.1")
        QtCore.QCoreApplication.setOrganizationName("BlackSecurity")
        QtCore.QCoreApplication.setOrganizationDomain("")

        self.location = os.path.dirname(os.path.realpath(__file__))
        self.Time = lambda: time.ctime().split(" ")[3]
        self.icon = lambda i: self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_" + i)) if hasattr(QtWidgets.QStyle, "SP_" + i) else None
        
        
        
        font = QtGui.QFont("Courier New", 10)
        font.setFixedPitch(True)
        self.setFont(font)
        
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.setCentralWidget(self.splitter)
        
        self.window = QtWidgets.QDockWidget("H4x0r Central Window")
        self.window.setFeatures(self.window.NoDockWidgetFeatures)
        self.splitter.addWidget(self.window)

        self.setupActivityWindow()
        self.log("Starting activity window ...")
        self.log("Starting tools explorer ...")
        self.setupToolsExplorer()

        self.log("Starting exception handler ...")
        sys.excepthook = self.handleException
        
        self.log("H4x0r v0x01 BETA 0 Ready ...")
        self.statusBar().showMessage("Ready ...")
        
        self.show()

    def log(self, text, log=0, color=None, bold=False):
        win = self.activityWindow.widget(log)
        win.moveCursor(QtGui.QTextCursor.End)
        win.insertHtml("<span {}>[{}] {}{}</span><br>".format("color='{}'".format(color) if color else "", self.Time(), "<b>" if bold else "", text, "</b>" if bold else ""))
        win.moveCursor(QtGui.QTextCursor.End)
        
    def handleException(self, exception, message, exc_traceback):
        if issubclass(exception, KeyboardInterrupt):
            if QtGui.qApp:
                QtGui.qApp.quit()
                
        filename, line, dummy, dummy = traceback.extract_tb(exc_traceback).pop()
        filename = os.path.basename(filename)
        
        self.log("{} line {} - {}: {}".format(filename, line, exception.__name__, message), 1)
        
    def loadModule(self, module=""):
        if module:
            module = importlib.import_module("modules." + module)
        else:
            module, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", self.location + "\\modules", "Python Files (*.py)")
            if module == __file__:
                self.log("Can't import h4x0r!", 1)
            else:
                module_dir, module_file = os.path.split(module)
                module_name, module_ext = os.path.splitext(module_file)
                spec = importlib.util.spec_from_file_location(module_name, module)
                module = spec.loader.load_module()
                
        if hasattr(module, "Window"):
            window = module.Window()
            title = window.windowTitle()
            icon = window.windowIcon()
            if icon.isNull(): icon = self.icon("FileIcon")
            if not title: title = "Untitled"
            if not isinstance(window, QtWidgets.QWidget) and not issubclass(window, QtWidgets.QWidget): raise Exception("")
            if title: existing = self.tools.findItems(title, QtCore.Qt.MatchExactly)
            else: existing = None
            if existing:
                print(existing)
                item = existing[0]
                item.widget = window
                item.setIcon(icon)
                item.setText(title)
                self.log("Successfully reloaded module {}!".format(repr(title)))
            else:
                row = QtWidgets.QListWidgetItem(icon, title)
                row.widget = window
                self.tools.addItem(row)
                self.log("Successfully loaded module {}!".format(repr(title)))

    def changeWindow(self, window):
        self.window.setWidget(window)
        self.window.setWindowTitle("H4x0r Central Window - {}".format(window.windowTitle() or "Untitled Application"))

    def ToolButton(self, icon, title="", tooltip="", shortcut="", callback=None, enabled=True, hidden=False):
        button = QtWidgets.QToolButton(icon=self.icon(icon), text=title, toolTip=tooltip, shortcut=shortcut, enabled=enabled,
                                       toolButtonStyle=QtCore.Qt.ToolButtonIconOnly if title is "" else QtCore.Qt.ToolButtonTextBesideIcon)
        
        if callback: button.clicked.connect(callback)
        if hidden: button.hide()
        return button
    
    def setupToolsExplorer(self):
        dock = QtWidgets.QDockWidget("H4x0r Tools Explorer")
        dock.setMaximumWidth(dock.width() / 3)
        dock.setFeatures(dock.NoDockWidgetFeatures)

        widget = QtWidgets.QWidget()
        widget.setLayout(QtWidgets.QVBoxLayout())
        dock.setWidget(widget)

        toolbar = QtWidgets.QToolBar("")
        self.importToolBtn = self.ToolButton("DialogOpenButton", "Import Application", "Import an application ...", "Ctrl+O", self.loadModule)

        toolbar.addWidget(self.importToolBtn)
        widget.layout().addWidget(toolbar)


        
        self.tools = QtWidgets.QListWidget(wordWrap=True)
        # Uncomment this to get a list of all icons avaiable
        #for attr in dir(QtWidgets.QStyle):
        #    if attr.startswith("SP_"):
        #        self.tools.addItem(QtWidgets.QListWidgetItem(self.icon(attr[3:]), attr[3:]))
        for module in os.listdir(self.location + "\\modules"):
            try:
                if not module.startswith("__") and module.endswith(".py"):
                    self.loadModule(module[:-3])
            except Exception as e:
                self.log("Failed to load module {} ...<br> &nbsp;&nbsp;&nbsp;&nbsp;{}".format(repr(module), str(e)), 1)

        self.tools.itemClicked.connect(lambda item: self.changeWindow(item.widget))

        widget.layout().addWidget(self.tools)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

    def setupActivityWindow(self):
        dock = QtWidgets.QDockWidget("Activity Window")
        dock.setMaximumHeight(dock.height() / 3)
        dock.setFeatures(dock.NoDockWidgetFeatures)
        dock.setWidget(QtWidgets.QTabWidget())

        window = dock.widget()
        window.setMovable(False)
        window.setTabPosition(1)
        window.setTabsClosable(False)

        appLogs = QtWidgets.QTextEdit()
        appLogs.setReadOnly(True)
        appLogs.setFont(self.font())
        window.addTab(appLogs, "Application Logs")
        
        errLogs = QtWidgets.QTextEdit()
        errLogs.setReadOnly(True)
        errLogs.setFont(self.font())
        window.addTab(errLogs, "Error Logs")
        
        self.splitter.addWidget(dock)
        self.activityWindow = window



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    app.exec_()
