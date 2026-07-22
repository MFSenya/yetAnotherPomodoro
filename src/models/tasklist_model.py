from datetime import timedelta, datetime
from enum import StrEnum

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from sqlalchemy import create_engine, inspect, Interval, DateTime, String, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    class Status(StrEnum):
        OPEN = "Open"
        CLOSED = "Closed"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, info={"alias": "Name"})
    open_time = Column(DateTime, info={"alias": "Open time"})
    time_spent = Column(Interval, info={"alias": "Time spent (H:M)"})
    status = Column(String, info={"alias": "Status"})

    
    def __init__(self, name: str, open_time: datetime, time_spent: timedelta, status: Status):
        self.name = name
        self.open_time = open_time
        self.time_spent = time_spent
        self.status = status

    @classmethod
    def get_field_meta(cls, field_name: str) -> dict:
        """Get metadata for a field."""
        column = cls.__table__.columns.get(field_name)
        if column is not None:
            return column.info
        raise AttributeError(f"Class {cls.__name__} doesn't have field with name {field_name}")

    @classmethod
    def get_headers(cls) -> list[str]:
        headers = []
        for column in cls.__table__.columns:
            if column.name != 'id':
                # Gat alias from info, if it is not there, use the columns with the name
                headers.append(column.info.get("alias", column.name))
        return headers
        

engine = create_engine('sqlite:///db/task_database.db', echo=False)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

class TaskListModel(QAbstractTableModel):
    def __init__(self, opened_tasks_max_num: int, parent=None):
        """
        
        Args:
            opened_tasks_max_num(int): max number of simultaneously opened tasks
            parent: parent model

        """
        super().__init__(parent)
        self._session = SessionLocal()
        self._tasks : list[Task] = self._session.query(Task).all()
        self._headers = Task.get_headers()
        self._column_map = [column.key for column in inspect(Task).attrs if column.key != "id"]
        self._opened_tasks_max_num = opened_tasks_max_num


    def rowCount(self, parent=None):
        return len(self._tasks)
    
    def columnCount(self, parent=None):
        return len(self._headers)
    
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        
        default_flags = super().flags(index)

        field_name = self._column_map[index.column()]
        # Only name and status columns are modifiable
        if field_name in ("name", "status"):
            return default_flags | Qt.ItemFlag.ItemIsEditable
        
        return default_flags & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable


    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """Returns data to display according to cell role."""
        if not index.isValid():
            return None
        
        task = self._tasks[index.row()]
        field_name = self._column_map[index.column()]
        value = getattr(task, field_name)

        match role:
            case Qt.ItemDataRole.DisplayRole:
                 match value:
                    case Task.Status if field_name == "status":
                        return value.value
                    case datetime() if field_name == "open_time":
                        return value.strftime("%Y-%m-%d %H:%M")
                    case timedelta() if field_name == "time_spent":
                        total_minutes = int(value.total_seconds() // 60)
                        hours, minutes = divmod(total_minutes, 60)
                        return f"{hours}:{minutes}"
                    case _:
                        return str(value)
            case Qt.ItemDataRole.EditRole:
                    return value
            case Qt.ItemDataRole.UserRole:
                if field_name == "status":
                    return [item.value for item in Task.Status] if self._can_open_new_task() else [Task.Status.CLOSED]
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._headers[section]
        return None
    
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False
    
        task = self._tasks[index.row()]
        field_name = self._column_map[index.column()]

        try:
            match field_name:
                case "name":
                    setattr(task, field_name, str(value).strip())
                case "status":
                    setattr(task, field_name, Task.Status(value))
                case _:
                    return False

            self._session.commit()    
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
            return True
        except Exception as e:
            self._session.rollback()
            print(f"An error occurred while saving the field {field_name}: {e}")
        
        return False
    
    def _can_open_new_task(self) -> bool:
        return sum(1 for task in self._tasks if task.status == Task.Status.OPEN) < self._opened_tasks_max_num
    
    def add_task(self, name: str, open_time: datetime):
        # if max number of opened task exceeded than tasks create as closed
        status = Task.Status.OPEN if self._can_open_new_task() else Task.Status.CLOSED
        new_task = Task(name=name, open_time=open_time, time_spent=timedelta(), status=status)
        self._session.add(new_task)

        try:
            self._session.commit()
            self._session.refresh(new_task)

            row_count = self.rowCount()
            self.beginInsertRows(QModelIndex(), row_count, row_count)
            self._tasks.append(new_task)
            self.endInsertRows()
            return True
        except Exception as e:
            self._session.rollback()
            print(f"An error occured while adding a task: {e}")
            return False



    def remove_task(self, row):
        if row < 0 or row >= self.rowCount():
            return False

        task_to_delete = self._tasks[row]
        self._session.delete(task_to_delete)

        try:
            self._session.commit()

            self.beginRemoveRows(QModelIndex(), row, row)
            self._tasks.pop(row)
            self.endRemoveRows()
            return True
        except Exception as e:
            self._session.rollback()
            print(f"An error occured while removing a task: {e}")
            return False