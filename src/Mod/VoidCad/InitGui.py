import FreeCADGui as Gui
from PySide import QtWidgets

class VoidCadWorkbench(Workbench):
    "VoidCad Custom Full-Screen Interface"
    Icon = """
        /* XPM */
        static const char * voidcad_icon_xpm[] = {
        "16 16 2 1",
        "  c None",
        ". c #000000",
        "                ",
        "                ",
        "                ",
        "  ............  ",
        "  .          .  ",
        "  .  ......  .  ",
        "  .  .    .  .  ",
        "  .  .    .  .  ",
        "  .  ......  .  ",
        "  .          .  ",
        "  ............  ",
        "                ",
        "                ",
        "                "
        };
        """
    MenuText = "VoidCad"
    ToolTip = "VoidCad Custom Interface"

    def __init__(self):
        self.hidden_toolbars = []
        self.hidden_docks = []

    def Initialize(self):
        # This is run when FreeCAD starts up
        pass

    def Activated(self):
        mw = Gui.getMainWindow()
        if not mw:
            return
            
        toolbars_to_hide = ["Edit", "Clipboard", "Structure", "View", "Help", "File", "Macro", "Workbench"]
        
        self.hidden_toolbars = []
        # Find all toolbars and hide the ones we don't want
        for tb in mw.findChildren(QtWidgets.QToolBar):
            if tb.windowTitle() in toolbars_to_hide:
                if tb.isVisible():
                    tb.hide()
                    self.hidden_toolbars.append(tb)
        
        self.hidden_docks = []
        # Find all dock widgets and hide the Model one
        for dock in mw.findChildren(QtWidgets.QDockWidget):
            if "Model" in dock.windowTitle() or "Tasks" in dock.windowTitle():
                if dock.isVisible():
                    dock.hide()
                    self.hidden_docks.append(dock)

    def Deactivated(self):
        # Restore them when switching to another workbench
        for tb in self.hidden_toolbars:
            tb.show()
        self.hidden_toolbars.clear()
        
        for dock in self.hidden_docks:
            dock.show()
        self.hidden_docks.clear()

    def GetClassName(self):
        return "Gui::PythonWorkbench"

Gui.addWorkbench(VoidCadWorkbench())
