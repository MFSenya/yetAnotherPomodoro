from PySide6.QtWidgets import QMainWindow, QTabWidget

from .components.pomodorotimer.pomodorotimer_view import PomodoroTimerView
from .tasklist_view import TaskListView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("yetAnotherPomodoro")
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)
        self.pomodoro_timer_view = PomodoroTimerView()
        self.tasklist_view = TaskListView()
        self.tabs.addTab(self.pomodoro_timer_view, "Timer")
        self.tabs.addTab(self.tasklist_view, "Tasks")
        self.tabs.setTabPosition(QTabWidget.West)