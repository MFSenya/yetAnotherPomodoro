from dataclasses import dataclass, field, fields
from datetime import timedelta, datetime
from enum import Enum
from typing import List, Optional

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

@dataclass
class Task:
    class Status(Enum):
        OPEN = 1
        CLOSED = 2
        POSTPONED = 3

    name: str = field(metadata={"alias": "Name"})
    open_time: datetime = field(metadata={"alias": "Open time"})
    time_spent: timedelta = field(metadata={"alias": "Time spent"})
    status: Status = field(metadata={"alias": "Status"})

    @classmethod
    def get_field_meta(cls, field_name: str) -> dict:
        """Get metadata for a field."""
        for f in fields(cls):
            if f.name == field_name:
                return f.metadata
        raise AttributeError(f"Class {cls.__name__} doesn't have field with name {field_name}")

class TaskListModel(QAbstractTableModel):
    def __init__(self, tasks: Optional[List[Task]] = None):
        super().__init__()
        self._tasks = tasks or []
        self._fields = fields(Task)

    def rowCount(self, parent=QModelIndex()):
        return len(self._tasks)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self._fields)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """Returns data to display according to cell role."""
        if not index.isValid():
            return None
        
        task = self._tasks[index.row()]
        field_info = self._fields[index.column()]
        value = getattr(task, field_info.name)

        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, Enum):
                return value.value
            return str(value)
    
        if role == Qt.ItemDataRole.EditRole:
            return value
        
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            field_info = self._fields[section]
            return field_info.metadata.get("alias", field_info.name)
        return None
    
    def add_task(self, task: Task):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._tasks.append(task)
        self.endInsertRows()

    def remove_task(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self._tasks.pop(row)
        self.endRemoveRows()