from datetime import timedelta

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTableView, QHeaderView, 
                             QDateTimeEdit, QComboBox)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QDateTime

from src.models.tasklist_model import TaskListModel, Task

class TaskListView(QWidget):
    def __init__(self):
        super().__init__()
        self.model = TaskListModel()
        self.view = QTableView(self)
        self.view.setModel(self.model)

        main_layout = QVBoxLayout(self)

        # Input form
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Task name...")

        self.datetime_input = QDateTimeEdit(self)
        self.datetime_input.setDateTime(QDateTime.currentDateTime())

        self.button_add = QPushButton("Add", self)
        self.button_add.clicked.connect(self.add_task)

        input_layout.addWidget(self.task_input, stretch=3)
        input_layout.addWidget(self.datetime_input, stretch=1)
        input_layout.addWidget(self.button_add, stretch=1)

        # Columns appearance
        header = self.view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
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
        open_time = self.datetime_input.dateTime().toPython()
        self.model.add_task(Task(name, open_time, timedelta(), Task.Status.OPEN))
        self.task_input.clear()

    def delete_task(self):
        selected_indexes = self.view.selectionModel().selectedRows()
        if selected_indexes:
            # Grab row of a first selected cell
            row = selected_indexes[0].row()
            self.model.remove_task(row)
