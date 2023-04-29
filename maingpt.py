import sys
import subprocess
import tempfile
import os
import keyword
import json
from program import *
from program2 import *
from create_files import create_file_structure
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor

from PyQt5.QtWidgets import *

class NaturalLanguageInputWidget(QWidget):
    def __init__(self, parent=None):
        super(NaturalLanguageInputWidget, self).__init__(parent)

        layout = QHBoxLayout()

        # Browse location input
        browse_label = QLabel("Project Location:")
        self.browse_line_edit = QLineEdit()
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_project_location)
        browse_button.setStyleSheet("background-color: #48b7d2;")
        layout.addWidget(browse_label)
        layout.addWidget(self.browse_line_edit)
        layout.addWidget(browse_button)

        # Project name input
        project_name_label = QLabel("Project Name:")
        self.project_name_line_edit = QLineEdit()
        layout.addWidget(project_name_label)
        layout.addWidget(self.project_name_line_edit)

        # Project description input
        project_description_label = QLabel("Project Description:")
        self.project_description_line_edit = QLineEdit()
        layout.addWidget(project_description_label)
        layout.addWidget(self.project_description_line_edit)

        # # Project description input
        # project_description_label = QLabel("Project Description:")
        # self.project_description_text_edit = QPlainTextEdit()
        # self.project_description_text_edit.setFixedHeight(20)
        # self.project_description_text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # layout.addWidget(project_description_label)
        # layout.addWidget(self.project_description_text_edit)

        # Generate button
        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self.generate_project_from_description)
        generate_button.setStyleSheet("background-color: #23DB27;")
        layout.addWidget(generate_button)

        self.setLayout(layout)
        # self.setStyleSheet("background-color: lightgreen;")

    def browse_project_location(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Project Location")
        if directory:
            self.browse_line_edit.setText(directory)

    def generate_project_from_description(self):
        project_location = self.browse_line_edit.text()
        project_name = self.project_name_line_edit.text()
        project_description = self.project_description_line_edit.text()

        if not project_location or not project_name or not project_description:
            QMessageBox.information(self, "Error", "Please fill in all fields.")
            return

        project_folder = os.path.join(project_location, project_name)
        os.makedirs(project_folder, exist_ok=True)

        title = Title()
        title.add_project({project_description})
        file_structure_w= title.display_title()

        # Find the index of the first curly brace
        brace_idx = file_structure_w.find('{')
        # Remove leading whitespace before the first curly brace
        if brace_idx > 0:
            file_structure_w = file_structure_w[brace_idx:]
            json_obj = json.loads(file_structure_w)
        # Dump the JSON object as a single-line string
        # retur=json.dumps(json_obj, separators=(',', ':'))

        file_structure_waste = json.dumps(json_obj, separators=(',', ':'))
        file_structure = json.loads(file_structure_waste)
 
        create_file_structure(project_folder, file_structure)

        QMessageBox.information(self, "Success", f"Project '{project_name}' has been generated at {project_folder}.")


class TerminalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        # Create the text edit for terminal output
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("background-color: black; color: white; font-family: 'Courier New'; font-size: 12px;")

        # Create the line edit for input
        self.line_edit = QLineEdit(self)
        self.line_edit.setStyleSheet("background-color: black; color: white; font-family: 'Courier New'; font-size: 12px;")
        self.line_edit.returnPressed.connect(self.execute_command)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)

    def execute_command(self):
        cmd = self.line_edit.text()
        self.text_edit.append(f"{cmd}\n")
        self.line_edit.clear()

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stdout:
            self.text_edit.append(stdout.decode())
        if stderr:
            self.text_edit.append(stderr.decode())

        self.text_edit.append("\n")
        self.text_edit.verticalScrollBar().setValue(self.text_edit.verticalScrollBar().maximum())


class InstallLibrariesDialog(QDialog):
    def __init__(self, libraries):
        super().__init__()

        self.setWindowTitle("Install Libraries")
        layout = QVBoxLayout()

        self.checkboxes = []

        for library in libraries:
            # checkbox = QCheckBox(f"pip install {library}")
            checkbox = QCheckBox(library)
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_selected_libraries(self):
        selected_libraries = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        return selected_libraries

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # Define keyword and operator formats
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Bold)

        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor("#dd00ff"))

        self.keyword_formats = {}
        for word in keyword.kwlist:
            pattern = r'\b{}\b'.format(word)
            regex = QRegExp(pattern)
            self.keyword_formats[regex] = keyword_format

        self.operator_format = operator_format

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#00aa00"))

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor("#FF0000"))

    def highlightBlock(self, text):
        # Apply keyword and operator formats
        for regex, fmt in self.keyword_formats.items():
            index = regex.indexIn(text)
            while index >= 0:
                length = regex.matchedLength()
                self.setFormat(index, length, fmt)
                index = regex.indexIn(text, index + length)

        for char in "=+-*/%&|^~<>!\\}{)(":
            index = text.find(char)
            while index >= 0:
                self.setFormat(index, 1, self.operator_format)
                index = text.find(char, index + 1)

        # Apply string format to text inside double quotes
        start_index = 0
        while True:
            start_index = text.find('"', start_index)
            if start_index == -1:
                break

            end_index = text.find('"', start_index + 1)
            if end_index == -1:
                end_index = len(text)

            self.setFormat(start_index, end_index - start_index + 1, self.string_format)
            start_index = end_index + 1

        # Apply string format to text inside single quotes
        start_index = 0
        while True:
            start_index = text.find("'", start_index)
            if start_index == -1:
                break

            end_index = text.find("'", start_index + 1)
            if end_index == -1:
                end_index = len(text)

            self.setFormat(start_index, end_index - start_index + 1, self.string_format)
            start_index = end_index + 1

        # Apply comment format to text after # that precedes double or single quotes
        hash_index = text.find("#")
        if hash_index >= 0:
            double_quote_index = text.find('"')
            single_quote_index = text.find("'")
            if double_quote_index == -1 and single_quote_index == -1:
                self.setFormat(hash_index, len(text) - hash_index, self.comment_format)
            elif double_quote_index == -1 or hash_index < double_quote_index:
                if single_quote_index == -1 or hash_index < single_quote_index:
                    self.setFormat(hash_index, len(text) - hash_index, self.comment_format)



class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 110)
        layout.setSpacing(0)

        self.line_number_widget = QTextEdit(self)
        self.line_number_widget.setReadOnly(True)
        self.line_number_widget.setObjectName("line_number_widget")
        self.line_number_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.line_number_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.line_number_widget.setMaximumSize(30, 15) # Set minimum size for width and height

        layout.addWidget(self.line_number_widget)

    def update_line_numbers(self):
        # Update line numbers
        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        lines = []
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top <= self.editor.viewport().height():
            if block.isVisible() and bottom >= 0:
                number = str(block_number + 1)
                lines.append(number)
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1

        # Set line numbers to QTextEdit
        self.line_number_widget.setPlainText("\n".join(lines))
        width = self.line_number_widget.fontMetrics().width(lines[-1]) + 5
        self.line_number_widget.setMinimumWidth(width)

        # Resize the widget to fit the layout
        self.line_number_widget.adjustSize()
        self.setMinimumWidth(self.line_number_widget.width())
        self.setMinimumHeight(self.line_number_widget.height())



class ResizableSelectionBoxCodeEditor(QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.highlighter = PythonHighlighter(self.document())
        self.selection_box = QRubberBand(QRubberBand.Rectangle, self)
        self.selection_box.setGeometry(0, 0, self.viewport().width(), 50)
        self.selection_box.show()
        self.drag_start_position = None
        self.resize_start_position = None
        self.resize_margin = 5

        self.line_number_area = LineNumberArea(self)
        self.line_number_area.update_line_numbers()

        self.blockCountChanged.connect(self.line_number_area.update_line_numbers)
        self.updateRequest.connect(self.line_number_area.update_line_numbers)
        self.cursorPositionChanged.connect(self.line_number_area.update_line_numbers)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.selection_box.setGeometry(0, self.selection_box.y(), self.viewport().width(), self.selection_box.height())
        self.line_number_area.update_line_numbers()

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self.selection_box.move(0, self.selection_box.y() - dy)
        self.line_number_area.update_line_numbers()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.selection_box.geometry().contains(event.pos()):
                if abs(event.pos().y() - self.selection_box.y()) <= self.resize_margin:
                    # Top edge clicked
                    self.resize_start_position = event.pos()
                    self.setCursor(Qt.SizeVerCursor)
                elif abs(event.pos().y() - self.selection_box.y() - self.selection_box.height()) <= self.resize_margin:
                    # Bottom edge clicked
                    self.resize_start_position = event.pos()
                    self.setCursor(Qt.SizeVerCursor)
                else:
                    self.drag_start_position = event.pos()
                event.accept()
            else:
                super(ResizableSelectionBoxCodeEditor, self).mousePressEvent(event)
        else:
            super(ResizableSelectionBoxCodeEditor, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_start_position is not None:
            dy = event.pos().y() - self.drag_start_position.y()
            new_y = self.selection_box.y() + dy
            self.selection_box.move(0, new_y)
            self.drag_start_position = event.pos()
            event.accept()
        elif self.resize_start_position is not None:
            dy = event.pos().y() - self.resize_start_position.y()
            new_height = self.selection_box.height() + dy
            if event.pos().y() < self.selection_box.y():
                # Top edge dragged
                new_y = self.selection_box.y() + dy
                self.selection_box.setGeometry(0, new_y, self.selection_box.width(), new_height)
            else:
                # Bottom edge dragged
                self.selection_box.resize(self.selection_box.width(), new_height)
            self.resize_start_position = event.pos()
            event.accept()
        else:
            super(ResizableSelectionBoxCodeEditor, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.drag_start_position is not None:
                self.drag_start_position = None
                event.accept()
            elif self.resize_start_position is not None:
                self.resize_start_position = None
                self.unsetCursor()
                event.accept()
            else:
                super(ResizableSelectionBoxCodeEditor, self).mouseReleaseEvent(event)
        else:
            super(ResizableSelectionBoxCodeEditor, self).mouseReleaseEvent(event)

    def get_covered_lines(self):
        start_line = self.firstVisibleBlock().blockNumber()
        y = self.selection_box.y()
        start_line += round(y / self.fontMetrics().height())
        end_line = start_line + round(self.selection_box.height() / self.fontMetrics().height())

        return start_line, end_line

    def get_covered_columns(self):
        start_col = round(self.selection_box.x() / self.fontMetrics().horizontalAdvance(' '))
        end_col = start_col + round(self.selection_box.width() / self.fontMetrics().horizontalAdvance(' '))

        return start_col, end_col

class CodeEditorTab(QWidget):
    def __init__(self, file_path=None, content=None):
        super().__init__()

        self.file_path = file_path
        self.input_text = ""

        layout = QVBoxLayout()

        self.code_editor = ResizableSelectionBoxCodeEditor()
        if content:
            self.code_editor.setPlainText(content)
        layout.addWidget(self.code_editor)

        input_layout = QHBoxLayout()

        self.language_input = QLineEdit()
        self.language_input.setPlaceholderText("Type here...")

        self.language_input.textChanged.connect(self.update_input_text)
        input_layout.addWidget(self.language_input)

        self.generate_button = QPushButton("Generate")
        self.generate_button.setStyleSheet("background-color: #23DB27;")
        self.generate_button.clicked.connect(self.generate_code)
        input_layout.addWidget(self.generate_button)

        self.selection_box_toggle = QPushButton()
        self.selection_box_toggle.setCheckable(True)
        self.selection_box_toggle.setFixedSize(20, 20)
        self.selection_box_toggle.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                border-radius: 10px;
                box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2);
            }
            QPushButton:checked {
                background-color: #0056B3;
                border-radius: 10px;
                box-shadow: inset 3px 3px 5px rgba(0, 0, 0, 0.2);
            }
        """)
        self.selection_box_toggle.toggled.connect(self.toggle_selection_box)
        input_layout.addWidget(self.selection_box_toggle)

        self.install_libraries_button = QPushButton("Install Libraries")
        self.install_libraries_button.setStyleSheet("background-color: #9BFC05;")
        self.install_libraries_button.clicked.connect(self.install_libraries)
        input_layout.addWidget(self.install_libraries_button)

        self.import_libraries_button = QPushButton("Import Libraries")
        self.import_libraries_button.setStyleSheet("background-color: #0BD7FF;")
        self.import_libraries_button.clicked.connect(self.import_libraries)
        input_layout.addWidget(self.import_libraries_button)

        layout.addLayout(input_layout)

        self.setLayout(layout)


    def update_input_text(self, text):
        self.input_text = text
    def generate_code(self):
        try:
            # If the radio button is checked
            if self.selection_box_toggle.isChecked():
                start_line, end_line = self.code_editor.get_covered_lines()
                start_col, end_col = self.code_editor.get_covered_columns()

                lines = self.code_editor.toPlainText().splitlines()
                selected_lines = lines[start_line:end_line + 1]

                # Trim the lines based on the start and end columns
                selected_lines[0] = selected_lines[0][start_col:]
                selected_lines[-1] = selected_lines[-1][:end_col]

                selected_text = "\n".join(selected_lines)
                prompt = f"{self.input_text} in the following program:\n\n {selected_text} "
                # with open("demo1.txt", "w") as file:
                #     file.write(prompt)


                generated_code = generate_code(prompt)
                # with open("demo3.txt", "w") as file:
                #     file.write(generated_code)
                # Replace the selected code with the generated code
                replaced_lines = lines[:start_line] + generated_code.splitlines() + lines[end_line + 1:]
                replaced_code = "\n".join(replaced_lines)
                self.code_editor.setPlainText(replaced_code)

            # If the radio button is not checked
            else:
                content = self.code_editor.toPlainText()
                prompt = f"{self.input_text} in the following program, write full code again:\n\n {content}"
                # with open("demo1.txt", "w") as file:
                #     file.write(prompt)

                generated_code = generate_code(prompt)

                # Replace the content with the generated code
                self.code_editor.setPlainText(generated_code)

        except Exception as e:
            print("Error:", e)

    def install_libraries(self):
        content = self.code_editor.toPlainText()
        # with open("demo3.txt", "w") as file:
        #     file.write(content)

        demo='''provide the libraries need to install in python dictionary format with full command to install in curly braces like {'pip install flask','pip install pyqt5',.......}'''
        prompt = f" {demo} in the following program:\n\n {content}"
        # with open("demo4.txt", "w") as file:
        #     file.write(prompt)


        generated_output = generate_code(prompt)

        # with open("demo4.txt", "w") as file:
        #     file.write(generated_output)
        try:
            libraries = eval(generated_output)
        except:
            QMessageBox.warning(self, "Error", "Failed to parse the generated output.")
            return

        install_dialog = InstallLibrariesDialog(libraries)
        result = install_dialog.exec()

        if result == QDialog.Accepted:
            selected_libraries = install_dialog.get_selected_libraries()
            for library in selected_libraries:
                os.system(library)

    def import_libraries(self):
        try:
            # If the radio button is checked, use the text within the selection box
            if self.selection_box_toggle.isChecked():
                start_line, end_line = self.code_editor.get_covered_lines()
                start_col, end_col = self.code_editor.get_covered_columns()

                lines = self.code_editor.toPlainText().splitlines()
                selected_lines = lines[start_line:end_line + 1]

                # Trim the lines based on the start and end columns
                selected_lines[0] = selected_lines[0][start_col:]
                selected_lines[-1] = selected_lines[-1][:end_col]

                selected_text = "\n".join(selected_lines)
                demo='''just only provide the libraries/framework/module needed to be imported in the following program like "import json\\nimport os\\nimport sys\\nfrom ..... import ....\n and so on....", don't write any code(like balance continuation code for the program) for the program other than import libraries(just start from import)\n\n in the following program:\n'''
                prompt = f" {demo}\n\n {selected_text}"
                # with open("demo5.txt", "w") as file:
                #     file.write(prompt)


                generated_output = generate_code(prompt)
                # with open("demo6.txt", "w") as file:
                #     file.write(generated_output)

            # If the radio button is not checked, use the whole content of the tab
            else:
                content = self.code_editor.toPlainText()
                demo='''just only provide the libraries needed to be imported in the following program like "import json\nimport os\nimport sys\nfrom PyQt5.QtGui import QColor, QTextCursor\nand so on....'''
                prompt = f" {demo}:\n\n {content}"
                # with open("demo6.txt", "w") as file:
                #     file.write(prompt)

                generated_output = generate_code(prompt)
            self.process_imports_output(generated_output)
        except Exception as e:
            print("Error:", e)

    def process_imports_output(self, output):
        imports = output.strip().split('\n')
        current_content = self.code_editor.toPlainText()
        new_content = "\n".join(imports) + "\n" + current_content
        self.code_editor.setPlainText(new_content)

    def toggle_selection_box(self, checked):
        if checked:
            self.code_editor.selection_box.show()
        else:
            self.code_editor.selection_box.hide()

class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.init_menu_bar()
        self.init_toolbar() 
        self.init_code_editor()
        self.init_project_explorer()
        self.init_natural_language_input()
        self.init_output_panel()
        self.init_solution_panel()
        self.init_status_bar()
        self.init_vertical_menu()
        self.setWindowTitle("GPT CODE EDITOR")
        self.showMaximized()
    # def init_code_editor(self):
    #     self.code_editor = ResizableSelectionBoxCodeEditor(self)
    #     self.setCentralWidget(self.code_editor)
    def init_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        view_menu = menu_bar.addMenu("View")
        tools_menu = menu_bar.addMenu("Tools")
        help_menu = menu_bar.addMenu("Help")

        new_project_action = QAction("New Project", self)
        new_project_action.triggered.connect(self.new_project)
        file_menu.addAction(new_project_action)

        open_project_action = QAction("Open Project", self)
        open_project_action.triggered.connect(self.open_project)
        file_menu.addAction(open_project_action)

        save_project_action = QAction("Save Project", self)
        save_project_action.triggered.connect(self.save_project)
        file_menu.addAction(save_project_action)

        close_action = QAction("Close", self)
        close_action.setShortcut(QKeySequence.Quit)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)

        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_current_tab)
        file_menu.addAction(save_action)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)

        find_replace_action = QAction("Find/Replace", self)
        find_replace_action.setShortcut(QKeySequence.Find)
        find_replace_action.triggered.connect(self.find_replace)
        edit_menu.addAction(find_replace_action)

        toggle_natural_language_input_action = QAction("Toggle Natural Language Input", self, checkable=True)
        toggle_natural_language_input_action.setChecked(True)
        toggle_natural_language_input_action.triggered.connect(self.toggle_natural_language_input)
        view_menu.addAction(toggle_natural_language_input_action)

        toggle_project_explorer_action = QAction("Project Explorer", self, checkable=True)
        toggle_project_explorer_action.setChecked(True)
        toggle_project_explorer_action.triggered.connect(self.toggle_project_explorer)
        view_menu.addAction(toggle_project_explorer_action)

        toggle_output_panel_action = QAction("Output Panel", self, checkable=True)
        toggle_output_panel_action.setChecked(True)
        toggle_output_panel_action.triggered.connect(self.toggle_output_panel)
        view_menu.addAction(toggle_output_panel_action)

        toggle_solution_panel_action = QAction("Solution Panel", self, checkable=True)
        toggle_solution_panel_action.setChecked(True)
        toggle_solution_panel_action.triggered.connect(self.toggle_solution_panel)
        view_menu.addAction(toggle_solution_panel_action)

        library_management_action = QAction("Library Management", self)
        library_management_action.triggered.connect(self.library_management)
        tools_menu.addAction(library_management_action)

        model_deployment_action =model_deployment_action = QAction("Model Deployment", self)
        model_deployment_action.triggered.connect(self.model_deployment)
        tools_menu.addAction(model_deployment_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.settings)
        tools_menu.addAction(settings_action)

        documentation_action = QAction("Documentation", self)
        documentation_action.triggered.connect(self.documentation)
        help_menu.addAction(documentation_action)

        tutorials_action = QAction("Tutorials", self)
        tutorials_action.triggered.connect(self.tutorials)
        help_menu.addAction(tutorials_action)

        support_forum_action = QAction("Support Forum", self)
        support_forum_action.triggered.connect(self.support_forum)
        help_menu.addAction(support_forum_action)

    def init_toolbar(self):
        toolbar = self.addToolBar("Toolbar")
        toolbar.setMovable(False)

        new_project_action = QAction("New Project", self)
        new_project_action.triggered.connect(self.new_project)
        toolbar.addAction(new_project_action)

        open_project_action = QAction("Open Project", self)
        open_project_action.triggered.connect(self.open_project)
        toolbar.addAction(open_project_action)

        save_project_action = QAction("Save Project", self)
        save_project_action.triggered.connect(self.save_project)
        toolbar.addAction(save_project_action)

        run_code_action = QAction("Run Code", self)
        run_code_action.triggered.connect(self.run_code)
        toolbar.addAction(run_code_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.settings)
        toolbar.addAction(settings_action)

        solution_action = QAction(QIcon("solution_icon.png"), "Solution", self)
        solution_action.triggered.connect(self.show_solution)
        toolbar.addAction(solution_action)

    def init_vertical_menu(self):
        vertical_menu = QToolBar("Vertical Menu", self)
        vertical_menu.setOrientation(Qt.Vertical)
        vertical_menu.setIconSize(QSize(48, 48))
        vertical_menu.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        natural_language_input_button = QToolButton()
        natural_language_input_button.setText("")
        natural_language_input_button.setCheckable(True)
        natural_language_input_button.setChecked(True)
        natural_language_input_button.clicked.connect(self.toggle_natural_language_input)
        vertical_menu.addWidget(natural_language_input_button)

        project_explorer_button = QToolButton()
        project_explorer_button.setText("")
        project_explorer_button.setCheckable(True)
        project_explorer_button.setChecked(True)
        project_explorer_button.clicked.connect(self.toggle_project_explorer)
        vertical_menu.addWidget(project_explorer_button)

        output_panel_button = QToolButton()
        output_panel_button.setText("")
        output_panel_button.setCheckable(True)
        output_panel_button.setChecked(True)
        output_panel_button.clicked.connect(self.toggle_output_panel)
        vertical_menu.addWidget(output_panel_button)

        solution_panel_button = QToolButton()
        solution_panel_button.setText("")
        solution_panel_button.setCheckable(True)
        solution_panel_button.setChecked(True)
        solution_panel_button.clicked.connect(self.toggle_solution_panel)
        vertical_menu.addWidget(solution_panel_button)

        self.addToolBar(Qt.LeftToolBarArea, vertical_menu)



    def init_code_editor(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)  # Add close button to each tab
        self.tab_widget.tabCloseRequested.connect(self.close_tab)  # Connect close button to a function
        self.setCentralWidget(self.tab_widget)
        # self.code_editor = ResizableSelectionBoxCodeEditor(self)
        # self.setCentralWidget(self.code_editor)

    def on_file_clicked(self, index):
        # Get the file path from the index
        file_path = self.file_system_model.filePath(index)
        
        # Check if the selected item is a file (not a directory)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                file_contents = file.read()
                self.code_editor.setPlainText(file_contents)


    def init_project_explorer(self):
        self.project_explorer = QDockWidget("Project Explorer", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_explorer)

     # Disable the close button and float button, keeping the title at the top
        self.project_explorer.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.project_explorer.setTitleBarWidget(QWidget(self.project_explorer))


        file_system_model = QFileSystemModel()
        file_system_model.setRootPath("")

        tree_view = QTreeView()
        tree_view.setModel(file_system_model)
        tree_view.setRootIndex(file_system_model.index("."))
        tree_view.doubleClicked.connect(self.open_file_in_tab)
        tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        tree_view.customContextMenuRequested.connect(self.show_project_explorer_context_menu)
        self.project_explorer.setWidget(tree_view)

    def show_project_explorer_context_menu(self, point):
        index = self.project_explorer.widget().indexAt(point)
        if not index.isValid():
            return

        menu = QMenu()
        new_file_action = QAction("New File", self)
        new_file_action.triggered.connect(lambda: self.create_new_file(index))
        menu.addAction(new_file_action)

        menu.exec_(self.project_explorer.widget().viewport().mapToGlobal(point))

    def create_new_file(self, index):
        file_path = self.project_explorer.widget().model().filePath(index)
        if os.path.isfile(file_path):
            file_path = os.path.dirname(file_path)

        file_name, ok = QInputDialog.getText(self, "New File", "Enter file name with extension:")
        if ok and file_name:
            new_file_path = os.path.join(file_path, file_name)
            with open(new_file_path, "w"):
                pass
            self.project_explorer.widget().setRootIndex(self.project_explorer.widget().model().index("."))


    def open_file_in_tab(self, index):
        file_path = self.project_explorer.widget().model().filePath(index)
        if not os.path.isfile(file_path):
            return

        for i in range(self.tab_widget.count()):
            if self.tab_widget.widget(i).file_path == file_path:
                self.tab_widget.setCurrentIndex(i)
                break
        else:
            with open(file_path, "r") as file:
                content = file.read()

            new_tab = CodeEditorTab(file_path=file_path, content=content)
            tab_index = self.tab_widget.addTab(new_tab, os.path.basename(file_path))
            self.tab_widget.setCurrentIndex(tab_index)

    def close_tab(self, index):
        self.tab_widget.removeTab(index)
         
    # New slot to handle opening files from the project explorer
    def open_file_from_explorer(self, index):
        file_path = self.sender().model().filePath(index)
        file_info = QFileInfo(file_path)

        if file_info.isFile():
            with open(file_path, "r") as file:
                file_content = file.read()

            self.code_editor.setPlainText(file_content)
            self.setWindowTitle(f"NLP Code Editor - {file_path}")

    def init_natural_language_input(self):
        self.natural_language_input_widget = NaturalLanguageInputWidget(self)
        

        natural_language_input_dock = QDockWidget("Natural Language Input", self)
        natural_language_input_dock.setWidget(self.natural_language_input_widget)
        self.addDockWidget(Qt.TopDockWidgetArea, natural_language_input_dock)

     # Disable the close button and float button, keeping the title at the top
        natural_language_input_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        natural_language_input_dock.setTitleBarWidget(QWidget(natural_language_input_dock))
            
    def init_output_panel(self):
        self.output_panel = QDockWidget("Output Panel", self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.output_panel)

     # Disable the close button and float button, keeping the title at the top
        self.output_panel.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.output_panel.setTitleBarWidget(QWidget(self.output_panel))

        # Split the output panel into two parts: Output & Terminal
        splitter = QSplitter(Qt.Horizontal)

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        splitter.addWidget(self.output)

        # Terminal
        self.terminal = TerminalWidget()
        splitter.addWidget(self.terminal)

        self.output_panel.setWidget(splitter)


    def send_text_to_process(self, text):
        self.process.write(text.encode())
########
    def generate_solution(self, content=None):
        try:
            self.code_editor = ResizableSelectionBoxCodeEditor()
            if content:
                self.code_editor.setPlainText(content) 
            # input_content= self.code_editor.setPlainText(content) 
            # content = self.tab_widget.currentWidget().widget().toPlainText()         
            error_text = self.output.toPlainText()
            if not error_text:
                QMessageBox.information(self, "Solution", "There is no error to generate a solution for.")
                return

            error_lines = error_text.split("\n")
            error_message_lines = []
            collecting_error_message = False

            for line in error_lines:
                if line.startswith("Error:"):
                    collecting_error_message = True
                    error_message = line[6:].strip()
                    error_message_lines.append(error_message)
                elif collecting_error_message:
                    if line.strip() == "":
                        break
                    error_message_lines.append(line.strip())
            else:
                QMessageBox.information(self, "Solution", "No error message found in the output.")
                return
            content = self.code_editor.toPlainText()
            # with open("demo7.txt", "w") as file:
            #     file.write(content)
            # error_message_lines now contains all the lines after "Error:" until an empty line
            full_error_message = '\n'.join(error_message_lines)

            prompt = f" provide solution for the following error:\n{full_error_message}\n\n########\n which accured in the following program:\n\n {content}"
            # with open("demo6.txt", "w") as file:
            #     file.write(prompt)


            generated_output = generate_code(prompt)

            self.solution_text_edit.clear()
            self.solution_text_edit.setTextColor(Qt.blue)
            self.solution_text_edit.append("Error:\n"+full_error_message+"\n\n\nSolution:\n" + generated_output)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")


    def init_solution_panel(self):
        self.solution_panel = QDockWidget("Solution", self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.solution_panel)

     # Disable the close button and float button, keeping the title at the top
        self.solution_panel.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.solution_panel.setTitleBarWidget(QWidget(self.solution_panel))

        solution_widget = QWidget()
        solution_layout = QVBoxLayout()

        self.solution_text_edit = QTextEdit()
        self.solution_text_edit.setReadOnly(True)
        self.solution_text_edit.setStyleSheet("QTextEdit { background-color: #69FC6C; color: black; }")
        solution_layout.addWidget(self.solution_text_edit)

        self.solution_button = QPushButton("Get Solution")
        self.solution_button.setStyleSheet("background-color: #21D225;")
        self.solution_button.clicked.connect(self.generate_solution)

        solution_layout.addWidget(self.solution_button)

        solution_widget.setLayout(solution_layout)
        self.solution_panel.setWidget(solution_widget)

            
    def show_solution(self):
        # Get the error text from the output panel
        error_text = self.output_text_edit.toPlainText()

        # Use your trained model to get the solution for the error
        solution = self.get_solution_from_model(error_text)

        # Display the solution in the Solution panel
        self.solution_text_edit.setPlainText(solution)

    def get_solution_from_model(self, error_text):
        # Replace this placeholder code with your actual model usage
        solution = "Solution for the error: " + error_text
        return solution

    def on_ready_read_standard_output(self):
        codec = QTextCodec.codecForLocale()
        text = codec.toUnicode(self.process.readAllStandardOutput())
        self.terminal.moveCursor(QTextCursor.End)
        self.terminal.insertPlainText(text)

    def on_ready_read_standard_error(self):
        codec = QTextCodec.codecForLocale()
        text = codec.toUnicode(self.process.readAllStandardError())
        self.terminal.moveCursor(QTextCursor.End)
        self.terminal.insertPlainText(text)


    def init_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def new_project(self):
        project_name, ok = QInputDialog.getText(self, "New Project", "Project Name:")

        if ok and project_name:
            # Create a new project directory and set it as the current project path
            self.project_path = f"./{project_name}"
            os.makedirs(self.project_path, exist_ok=True)

            # Update the project explorer to show the new project directory
            file_system_model = QFileSystemModel()
            file_system_model.setRootPath(self.project_path)

            tree_view = QTreeView()
            tree_view.setModel(file_system_model)
            tree_view.setRootIndex(file_system_model.index(self.project_path))
            self.project_explorer.setWidget(tree_view)

    def open_project(self):
        project_path = QFileDialog.getExistingDirectory(self, "Open Project")

        if project_path:
            # Set the selected directory as the current project path
            self.project_path = project_path

            # Update the project explorer to show the opened project directory
            file_system_model = QFileSystemModel()
            file_system_model.setRootPath(self.project_path)

            tree_view = QTreeView()
            tree_view.setModel(file_system_model)
            tree_view.setRootIndex(file_system_model.index(self.project_path))
            self.project_explorer.setWidget(tree_view)

    def save_project(self):
        pass
        # if self.project_path:
        #     file_name, _ = QFileDialog.getSaveFileName(self, "Save Project", self.project_path)

        #     if file_name:
        #         with open(file_name, "w") as file:
        #             file.write(self.code_editor.toPlainText())
        # else:
        #     QMessageBox.warning(self, "Warning", "No project is open. Please open or create a project first.")

    def save_current_tab(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab is None:
            return

        file_path = current_tab.file_path
        if not file_path:
            return

        code = current_tab.code_editor.toPlainText()
        with open(file_path, "w") as file:
            file.write(code)



    def run_code(self):
        current_tab = self.tab_widget.currentWidget()
        if current_tab is None:
            return

        code = current_tab.code_editor.toPlainText()
        if not code:
            return

        # Create a custom input function that reads from the QLineEdit
        def custom_input(prompt):
            self.output.append(prompt)
            input_line_edit = QLineEdit(self.output_panel)
            input_line_edit.returnPressed.connect(lambda: input_line_edit.setProperty("done", True))
            self.output_panel.setWidget(input_line_edit)
            input_line_edit.setFocus()

            while not input_line_edit.property("done"):
                QApplication.processEvents()

            value = input_line_edit.text()
            self.output_panel.setWidget(self.output)
            return value

        # Redirect the input function to our custom input function
        sys.stdin.readline = custom_input

        # Run the code in a separate process and capture the output
        process = subprocess.Popen(["python", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()


        # Set the text color to green
        green = QColor(0, 0, 0)
        palette = self.output.palette()
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, green)
        self.output.setPalette(palette)

        # Display the output in the output panel
        self.output.clear()
        self.output.append("Output:\n" + stdout)
        if stderr:
            self.output.append("Error:")
            self.output.setTextColor(QColor(255, 0, 0))
            self.output.append(stderr)
            self.output.setTextColor(green)
        # Restore the original input function
        sys.stdin.readline = sys.__stdin__.readline




    def settings(self):
        pass
        # settings_dialog = QDialog(self)
        # settings_dialog.setWindowTitle("Settings")

        # # Add widgets and layouts for the settings dialog
        # # For example, you can add options for changing the theme or font of the code editor
        # layout = QVBoxLayout()

        # theme_label = QLabel("Theme:")
        # theme_combobox = QComboBox()
        # theme_combobox.addItems(["Default", "Dark"])
        # layout.addWidget(theme_label)
        # layout.addWidget(theme_combobox)

        # font_label = QLabel("Font:")
        # font_combobox = QFontComboBox()
        # layout.addWidget(font_label)
        # layout.addWidget(font_combobox)

        # ok_button = QPushButton("OK")
        # ok_button.clicked.connect(settings_dialog.accept)
        # layout.addWidget(ok_button)

        # settings_dialog.setLayout(layout)
        # result = settings_dialog.exec_()

        # if result == QDialog.Accepted:
        #     # Apply the selected settings
        #     selected_theme = theme_combobox.currentText()
        #     selected_font = font_combobox.currentFont()

        #     if selected_theme == "Default":
        #         self.code_editor.setStyleSheet("QPlainTextEdit { background-color: white; color: black; }")
        #     elif selected_theme == "Dark":
        #         self.code_editor.setStyleSheet("QPlainTextEdit { background-color: #272822; color: #f8f8f2; }")

        #     self.code_editor.setFont(selected_font)

    def undo(self):
        self.code_editor.undo()

    def redo(self):
        self.code_editor.redo()

    def cut(self):
        self.code_editor.cut()

    def copy(self):
        self.code_editor.copy()

    def paste(self):
        self.code_editor.paste()

    def find_replace(self):
        find_replace_dialog = QDialog(self)
        find_replace_dialog.setWindowTitle("Find & Replace")

        layout = QVBoxLayout()

        find_label = QLabel("Find:")
        find_line_edit = QLineEdit()
        layout.addWidget(find_label)
        layout.addWidget(find_line_edit)

        replace_label = QLabel("Replace with:")
        replace_line_edit = QLineEdit()
        layout.addWidget(replace_label)
        layout.addWidget(replace_line_edit)

        find_button = QPushButton("Find")
        find_button.clicked.connect(lambda: self.find(find_line_edit.text()))
        layout.addWidget(find_button)

        replace_button = QPushButton("Replace")
        replace_button.clicked.connect(lambda: self.replace(find_line_edit.text(), replace_line_edit.text()))
        layout.addWidget(replace_button)

        find_replace_dialog.setLayout(layout)
        find_replace_dialog.exec_()

    def find(self, text):
        if not self.code_editor.find(text):
            QMessageBox.information(self, "Find", "The specified text could not be found.")

    def replace(self, find_text, replace_text):
        cursor = self.code_editor.textCursor()

        if cursor.hasSelection() and cursor.selectedText() == find_text:
            cursor.insertText(replace_text)

        if not self.code_editor.find(find_text):
            QMessageBox.information(self, "Replace", "The specified text could not be found.")

    def toggle_natural_language_input(self, checked):
        if checked:
            self.natural_language_input_widget.show()
        else:
            self.natural_language_input_widget.hide()

    def toggle_project_explorer(self, checked):
        if checked:
            self.project_explorer.show()
        else:
            self.project_explorer.hide()

    def toggle_output_panel(self, checked):
        if checked:
            self.output_panel.show()
        else:
            self.output_panel.hide()

    def toggle_solution_panel(self, checked):
        if checked:
            self.solution_panel.show()
        else:
            self.solution_panel.hide()

    def library_management(self):
        pass

    def model_deployment(self):
        pass

    def documentation(self):
        pass

    def tutorials(self):
        pass

    def support_forum(self):
        pass

    def generate_code(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = CodeEditor()
    editor.show()

    # def close_application():
    #     response = QMessageBox.question(editor, "Exit", "Are you sure you want to exit?",
    #                                     QMessageBox.Yes | QMessageBox.No)
    #     if response == QMessageBox.Yes:
    #         sys.exit()

    # app.aboutToQuit.connect(close_application)
    sys.exit(app.exec_())
   

