from dataclasses import dataclass, field, fields
from datetime import timedelta, datetime
from enum import StrEnum
from typing import List, Optional

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

@dataclass
class Task:
    class Status(StrEnum):
        OPEN = "Open"
        CLOSED = "Closed"
        POSTPONED = "Postponed"

    name: str = field(metadata={"alias": "Name"})
    open_time: datetime = field(metadata={"alias": "Open time"})
    time_spent: timedelta = field(metadata={"alias": "Time spent (H:M)"})
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
        self._tasks = tasks or [Task("test", datetime(1999, 5, 12), timedelta(), Task.Status.OPEN)]
        self._fields = fields(Task)

    def rowCount(self, parent=QModelIndex()):
        return len(self._tasks)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self._fields)
    
    def flags(self, index):
        default_flags = super().flags(index)

        field_info = self._fields[index.column()]

        # Only name and status columns are modifiable
        if field_info.name in ("name", "status"):
            return default_flags | Qt.ItemFlag.ItemIsEditable
        
        return default_flags & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable


    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """Returns data to display according to cell role."""
        if not index.isValid():
            return None
        
        task = self._tasks[index.row()]
        field_info = self._fields[index.column()]
        value = getattr(task, field_info.name)

        match role:
            case Qt.ItemDataRole.DisplayRole:
                 match value:
                    case StrEnum():
                        return value.value
                    case datetime():
                        return value.strftime("%Y-%m-%d %H:%M")
                    case timedelta():
                        total_minutes = int(value.total_seconds() // 60)
                        hours, minutes = divmod(total_minutes, 60)
                        return f"{hours}:{minutes}"
                    case _:
                        return str(value)
            case Qt.ItemDataRole.EditRole:
                return value
            case Qt.ItemDataRole.UserRole:
                if field_info.name == "status":
                    return [item.value for item in Task.Status]


        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            field_info = self._fields[section]
            return field_info.metadata.get("alias", field_info.name)
        return None
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False
    
        task = self._tasks[index.row()]
        field_info = self._fields[index.column()]

        match field_info.name:
            case "name":
                task.name = str(value).strip()
            case "status":
                task.status = Task.Status(value)
            case _:
                return False
            
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])

        return True    
    
    def add_task(self, task: Task):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._tasks.append(task)
        self.endInsertRows()

    def remove_task(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self._tasks.pop(row)
        self.endRemoveRows()