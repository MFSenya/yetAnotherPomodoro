from datetime import timedelta
from collections.abc import Sequence

from PySide6.QtWidgets import (QStyledItemDelegate, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTableView, QHeaderView, 
                             QComboBox, QAbstractItemView, QStyle)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QDateTime

from ..models.tasklist_model import TaskListModel

class TaskListView(QWidget):

    class ColumnComboBoxViewDelegate(QStyledItemDelegate):
        """Replaces Editor with QComboBox."""

        def createEditor(self, parent, option, index):
            items = index.model().get_allowed_values_for_column(index)

            if items is not None and isinstance(items, Sequence):
                editor = QComboBox(parent)
                editor.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
                editor.setAutoFillBackground(True)
                editor.addItems(items)
                return editor

            return super().createEditor(parent, option, index)
        
        def setEditorData(self, editor, index):
            if isinstance(editor, QComboBox):
                current_text = index.model().data(index, Qt.ItemDataRole.EditRole)
                pos = editor.findText(str(current_text))
                if pos >= 0:
                    editor.setCurrentIndex(pos)
            else:
                super().setEditorData(editor, index)

        def setModelData(self, editor, model, index):
            if isinstance(editor, QComboBox):
                model.setData(index, editor.currentText(), Qt.ItemDataRole.EditRole)
            else:
                super().setModelData(editor, model, index)

    def __init__(self, model: TaskListModel):
        super().__init__()
        self.model = model
        self.view = QTableView(self)
        self.view.setModel(self.model)
        self.view.horizontalHeader().setHighlightSections(False)
        self.view.verticalHeader().setVisible(False)
        self.view.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.view.setItemDelegateForColumn(3, self.ColumnComboBoxViewDelegate(self.view))
        main_layout = QVBoxLayout(self)

        # Input form
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter task name...")

        self.button_add = QPushButton("Add", self)
        self.button_add.clicked.connect(self.add_task)

        input_layout.addWidget(self.task_input, stretch=3)
        input_layout.addWidget(self.button_add, stretch=1)

        # Columns appearance
        header = self.view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        
        self.button_delete = QPushButton("Delete selected task", self)
        self.button_delete.clicked.connect(self.delete_task)
        
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.view)
        main_layout.addWidget(self.button_delete)

    def add_task(self):
        name = self.task_input.text().strip()
        if not name:
            return
        open_time = QDateTime().currentDateTime().toPython()
        self.model.add_task(name, open_time)
        self.task_input.clear()

    def delete_task(self):
        selected_indexes = self.view.selectionModel().selectedRows()
        if selected_indexes:
            # Grab row of a first selected cell
            row = selected_indexes[0].row()
            self.model.remove_task(row)
