from PySide6.QtWidgets import QMainWindow, QStackedWidget

from .components.pomodorotimer.pomodorotimer_view import PomodoroTimerView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget(self)
        self.pomodoro_timer = PomodoroTimerView()
        self.stacked_widget.addWidget(self.pomodoro_timer)
        self.setCentralWidget(self.stacked_widget)