import os
import FreeCAD as App
import FreeCADGui as Gui

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
        "                ",
        "                "
        };
        """
    MenuText = "VoidCad"
    ToolTip = "VoidCad Custom Interface"

    def __init__(self):
        self.hidden_toolbars = []
        self.hidden_docks = []
        self.original_stylesheet = ""

    def Initialize(self):
        # Explicitly ENABLE the Start page, because VoidCad styles its cards to act as our dashboard
        param = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Start")
        param.SetBool("ShowOnStartup", True)
        
        # Create a custom VoidCad command so the toolbar isn't entirely empty
        class VoidCadDummyCommand:
            def GetResources(self):
                return {'Pixmap'  : 'Std_New',
                        'MenuText': 'VoidCad Action',
                        'ToolTip' : 'Demonstration action for VoidCad'}
            def Activated(self):
                App.Console.PrintMessage("VoidCad Action called!\n")
            def getattr(self, name): return None 
            def IsActive(self): return True
            
        Gui.addCommand('VoidCad_Dummy', VoidCadDummyCommand())
        self.appendMenu("VoidCad", ["VoidCad_Dummy"])
        self.appendToolbar("VoidCad Quick", ["VoidCad_Dummy"])

    def Activated(self):
        App.Console.PrintMessage("VoidCad: Activated() called.\n")
        from PySide6 import QtCore, QtWidgets
        mw = Gui.getMainWindow()
        if not mw:
            App.Console.PrintError("VoidCad: getMainWindow() returned None.\n")
            return
            
        # Defer the UI modifications by 500ms to allow FreeCAD's Start tab to finish opening so we can kill it
        QtCore.QTimer.singleShot(500, self._delayed_startup)
        
    def _delayed_startup(self):
        from PySide6 import QtWidgets
        mw = Gui.getMainWindow()
        if not mw:
            App.Console.PrintError("VoidCad: getMainWindow() returned None.\n")
            return
            
        # Ensure the Start page is open if no documents exist, so the user has the "New File" cards
        if not App.ActiveDocument:
            try:
                # Force load the Start module so its commands are registered
                App.getModule("Start")
            except:
                pass
            Gui.runCommand("Start_Start")
            
        toolbars_to_hide = ["Edit", "Clipboard", "Structure", "View", "Help", "File", "Macro", "Workbench"]
        self.hidden_toolbars = []
        for tb in mw.findChildren(QtWidgets.QToolBar):
            if tb.windowTitle() in toolbars_to_hide:
                if tb.isVisible():
                    tb.hide()
                    self.hidden_toolbars.append(tb)
        
        self.hidden_docks = []
        for dock in mw.findChildren(QtWidgets.QDockWidget):
            if "Model" in dock.windowTitle() or "Tasks" in dock.windowTitle():
                if dock.isVisible():
                    dock.hide()
                    self.hidden_docks.append(dock)

        # Apply custom Material 3 stylesheet
        app = QtWidgets.QApplication.instance()
        if app:
            self.original_stylesheet = app.styleSheet()
            
            home_path = App.getHomePath()
            user_path = App.getUserAppDataDir()
            
            mod_path = ""
            if os.path.exists(os.path.join(home_path, "Mod", "VoidCad", "VoidCad.qss")):
                mod_path = os.path.join(home_path, "Mod", "VoidCad", "VoidCad.qss")
            elif os.path.exists(os.path.join(user_path, "Mod", "VoidCad", "VoidCad.qss")):
                mod_path = os.path.join(user_path, "Mod", "VoidCad", "VoidCad.qss")
            elif os.path.exists(os.path.join(os.path.dirname(os.path.dirname(home_path)), "Library", "Mod", "VoidCad", "VoidCad.qss")):
                mod_path = os.path.join(os.path.dirname(os.path.dirname(home_path)), "Library", "Mod", "VoidCad", "VoidCad.qss")
                
            if mod_path and os.path.exists(mod_path):
                with open(mod_path, 'r') as f:
                    app.setStyleSheet(f.read())
                App.Console.PrintMessage("VoidCad: Applied stylesheet from {}\n".format(mod_path))
            else:
                App.Console.PrintWarning("VoidCad: VoidCad.qss not found. Looked in {} and {}\n".format(home_path, user_path))

    def Deactivated(self):
        from PySide6 import QtWidgets
        # Restore them when switching to another workbench
        for tb in self.hidden_toolbars:
            tb.show()
        self.hidden_toolbars.clear()
        
        for dock in self.hidden_docks:
            dock.show()
        self.hidden_docks.clear()
        
        # Restore original stylesheet
        app = QtWidgets.QApplication.instance()
        if app:
            app.setStyleSheet(self.original_stylesheet)

    def GetClassName(self):
        return "Gui::PythonWorkbench"

# Force VoidCad to be the default start-up workbench for FreeCAD
# This overrides any existing user settings so the user is always greeted by the custom UI
param = App.ParamGet("User parameter:BaseApp/Preferences/General")
param.SetString("AutoloadModule", "VoidCadWorkbench")

Gui.addWorkbench(VoidCadWorkbench())
