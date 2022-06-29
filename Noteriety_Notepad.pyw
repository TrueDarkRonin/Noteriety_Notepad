import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPlainTextEdit, QToolBar, \
                            QAction, QFileDialog, QMessageBox, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence
from PyQt5.QtPrintSupport import QPrintDialog

# TODO 
# Collapsable sections
# Add headers and dividers button
# Opacity and colour slider


# Create Action method for object creation later
def create_action(parent, icon_path, action_name, set_status_tip, trigger_method):
    action = QAction(QIcon(icon_path), action_name, parent)
    action.setStatusTip(set_status_tip)
    action.triggered.connect(trigger_method)
    return action


class Application(QMainWindow):
    """Class constructor. Create QTWindow with basic attributes to be inherited
       Filters for specified text doc types
       Assigns icon and constructs editor and container"""
    def __init__(self):
        # --------------------
        # Constructor
        # --------------------

        super().__init__()
        self.setWindowIcon(QIcon('Icons/Notepad_Doc.ico'))
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width, self.screen_height)

        self.filterTypes = 'Text Document (*.txt);; Python (*.py);; Markdown(*.md)'

        self.path = None

        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixed_font.setPointSize(12)

        main_layout = QVBoxLayout()

        # Editor
        self.editor = QPlainTextEdit()
        self.editor.setFont(fixed_font)
        main_layout.addWidget(self.editor)

        # Status Bar
        self.status = self.statusBar()

        # Word Count
        self.word_count = QLabel()
        main_layout.addWidget(self.word_count)
        self.word_count.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        # Container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Palette
        self.setStyleSheet("background-color: #2f2f2f; color: #acacac")
        self.setWindowOpacity(0.95)

        # --------------------
        # File Menu
        # --------------------

        file_menu = self.menuBar().addMenu("&File")

        # --------------------
        # File Toolbar
        # --------------------

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(Qt.BottomToolBarArea, file_toolbar)

        """
        File Actions - Open, Save, Save As, Print
        """
        open_file_action = create_action(self,
                                         'Icons/Open_File.ico',
                                         "Open File. . .",
                                         "Open File",
                                         self.open_file)
        open_file_action.setShortcut(QKeySequence.Open)

        save_file_action = create_action(self,
                                         'Icons/Save.ico',
                                         "Save",
                                         "Save",
                                         self.file_save)
        save_file_action.setShortcut(QKeySequence.Save)

        save_as_action = create_action(self,
                                       'Icons/Save_As.ico',
                                       "Save As. . .",
                                       "Save As",
                                       self.file_save_as)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))

        print_action = create_action(self,
                                     'Icons/Print.ico',
                                     "Print File",
                                     "Print File",
                                     self.print_file)
        print_action.setShortcut(QKeySequence.Print)

        # Add Separator
        file_menu.addSeparator()
        file_toolbar.addSeparator()

        file_menu.addActions([open_file_action, save_file_action, save_as_action, print_action])
        file_toolbar.addActions([open_file_action, save_file_action, save_as_action, print_action])

        # --------------------
        # Edit Menu
        # --------------------

        edit_menu = self.menuBar().addMenu('&Edit')

        # --------------------
        # Edit Toolbar
        # --------------------

        edit_toolbar = QToolBar('Edit')
        edit_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(Qt.BottomToolBarArea, edit_toolbar)

        """
        Edit Actions - Undo, Redo, Clear, Cut, Copy, Paste, Select All
        """
        undo_action = create_action(self,
                                    'Icons/Undo.ico',
                                    "Undo",
                                    "Undo",
                                    self.editor.undo)
        undo_action.setShortcut(QKeySequence.Undo)

        redo_action = create_action(self,
                                    'Icons/Redo.ico',
                                    "Redo",
                                    "Redo",
                                    self.editor.redo)
        redo_action.setShortcut(QKeySequence.Redo)

        clear_action = create_action(self,
                                     'Icons/Clear.ico',
                                     "Clear",
                                     "Clear",
                                     self.clear_content)
        clear_action.setShortcut(QKeySequence("Ctrl+Shift+D"))

        cut_action = create_action(self,
                                   'Icons/Cut.ico',
                                   "Cut",
                                   "Cut",
                                   self.editor.cut)
        cut_action.setShortcut(QKeySequence.Cut)

        copy_action = create_action(self,
                                    'Icons/Copy.ico',
                                    "Copy",
                                    "Copy",
                                    self.editor.copy)
        copy_action.setShortcut(QKeySequence.Copy)

        paste_action = create_action(self,
                                     'Icons/Paste.ico',
                                     "Paste",
                                     "Paste",
                                     self.editor.paste)
        paste_action.setShortcut(QKeySequence.Paste)

        select_all_action = create_action(self,
                                          'Icons/Select_All.ico',
                                          "Select All",
                                          "Select All",
                                          self.editor.selectAll)
        select_all_action.setShortcut(QKeySequence.SelectAll)

        edit_menu.addActions([undo_action, redo_action])
        edit_toolbar.addActions([undo_action, redo_action])

        # Add Separator
        edit_menu.addSeparator()
        edit_toolbar.addSeparator()

        edit_menu.addActions([clear_action, cut_action, copy_action, paste_action, select_all_action])
        edit_toolbar.addActions([clear_action, cut_action, copy_action, paste_action, select_all_action])

        # --------------------
        # Format Menu
        # --------------------

        format_menu = self.menuBar().addMenu('&Format')

        # --------------------
        # Format Toolbar
        # --------------------

        format_toolbar = QToolBar('Format')
        format_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(Qt.BottomToolBarArea, format_toolbar)

        """
        Format Actions - Wrap Text
        """
        wrap_text_action = create_action(self,
                                         'Icons/Wrap_Text.ico',
                                         "Wrap Text",
                                         "Wrap Text",
                                         self.toggle_wrap_text)
        wrap_text_action.setShortcut(QKeySequence("Ctrl+Shift+W"))

        # Add Separator
        format_menu.addSeparator()
        format_toolbar.addSeparator()

        format_menu.addActions([wrap_text_action])
        format_toolbar.addActions([wrap_text_action])

        # --------------------
        # Misc Menu
        # --------------------

        misc_menu = self.menuBar().addMenu('&Misc')

        # --------------------
        # Misc Toolbar
        # --------------------

        misc_toolbar = QToolBar('Misc')
        misc_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(Qt.BottomToolBarArea, misc_toolbar)

        """
        Misc Actions - Word Count
        """

        misc_menu.addActions([])
        misc_toolbar.addActions([])

        self.word_count_update()
        self.update_title()

    # --------------------
    # Methods
    # --------------------

    def clear_content(self):
        self.editor.setPlainText("")
        self.word_count_update()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(parent=self,
                                              caption="Open File",
                                              directory=" ",
                                              filter=self.filterTypes)
        if path:
            try:
                with open(path, 'r') as file:
                    text = file.read()
                    file.close()
            except Exception as err:
                self.dialog_message(str(err))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.word_count_update()
                self.update_title()
                self.word_count_update()

    def file_save(self):
        if self.path is None:
            self.file_save_as()
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.path, 'w') as file:
                    file.write(text)
                    file.close()
                self.word_count_update()
            except Exception as err:
                self.dialog_message(str(err))

    def file_save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File As", " ", self.filterTypes)
        text = self.editor.toPlainText()
        if not path:
            return
        else:
            try:
                with open(path, 'w') as file:
                    file.write(text)
                    file.close()
            except Exception as err:
                self.dialog_message(str(err))
            else:
                self.path = path
                self.word_count_update()
                self.update_title()

    def toggle_wrap_text(self):
        self.editor.setLineWrapMode(not self.editor.lineWrapMode())
        self.word_count_update()

    def print_file(self):
        print_dialog = QPrintDialog()
        if print_dialog.exec_():
            self.editor.print_(print_dialog.printer())

    def update_title(self):
        self.setWindowTitle("{0} - Noteriety".format(os.path.basename(self.path) if self.path else "Untitled"))

    def dialog_message(self, message):
        dialog = QMessageBox(self)
        dialog.setText(message)
        dialog.setIcon(QMessageBox.Critical)
        dialog.show()

    def word_count_update(self):
        text = self.editor.toPlainText()
        split_text = text.split()
        word_count = str(len(split_text))
        char_count = str(sum(len(i) for i in text))
        self.word_count.setText(f"W: {word_count} C: {char_count}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = Application()
    notepad.show()
    sys.exit(app.exec_())
