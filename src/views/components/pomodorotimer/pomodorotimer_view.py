from PySide6.QtWidgets import QWidget, QStackedWidget, QPushButton, QGridLayout, QTimeEdit
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Property, Qt, QRect, QTime

from .pomodorotimer_controller import PomodoroTimerController


class PomodoroTimerView(QStackedWidget):

    class StartScreen(QWidget):
        def __init__(self):
            super().__init__()
            # Buttons
            self.button_start_cycle = QPushButton("Start", self)
            self.button_start_cycle.setStyleSheet("margin: 10px;")
            # TimeEdits configuration
            time_edit_display_format = "mm"
            set_calendar_popup = False
            self.time_edit_work_time_interval = QTimeEdit()
            self.time_edit_work_time_interval.setDisplayFormat(time_edit_display_format)
            self.time_edit_work_time_interval.setCalendarPopup(set_calendar_popup)
            self.time_edit_rest_time_interval = QTimeEdit()
            self.time_edit_rest_time_interval.setDisplayFormat(time_edit_display_format)
            self.time_edit_rest_time_interval.setCalendarPopup(set_calendar_popup)
            # Layout
            layout = QGridLayout(self)
            layout.addWidget(self.time_edit_work_time_interval, 0, 0)
            layout.addWidget(self.time_edit_rest_time_interval, 0, 1)
            layout.addWidget(self.button_start_cycle, 1, 0, 1, 2)
            # Settings
            self.setLayout(layout)

    class WorkScreen(QWidget):

        class ProgressBar(QWidget):
            def __init__(self):
                super().__init__()
                self._value = 0

            @Property(QColor)
            def barColor(self):
                return self._progress_bar_color
            
            @barColor.setter
            def barColor(self, color):
                # Qt Designer can pass color in different formats, 
                # so we need to force cast to QColor
                self._progress_bar_color = QColor(color)
                # Redraw after gauge color change
                self.update()


            @Property(QColor)
            def backgroundColor(self):
                return self._bg_color
            
            @backgroundColor.setter
            def backgroundColor(self, color):
                # Qt Designer can pass color in different formats, 
                # so we need to force cast to QColor
                self._bg_color = QColor(color)
                # Redraw after gauge color change
                self.update() 

            @property
            def progressValue(self):
                """Progress value."""
                return self._value
            
            @progressValue.setter
            def progressValue(self, value: int):
                self._value = value
            

            def paintEvent(self, event):
                self.painter = QPainter(self)
                # Enable antialiasing
                self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                # Draw background
                self.painter.fillRect(self.rect(), self.backgroundColor)
                # Draw scale
                size = min(self.width(), self.height()) - 40
                x = (self.width() - size) // 2
                y = (self.height() - size) // 2
                scale_rect = QRect(x, y, size, size)
                self.painter.setPen(QPen(QColor("#eaeaea"), 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                self.painter.drawEllipse(scale_rect)
                self.painter.setPen(QPen(self.barColor, 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                span_angle = int(-self.progressValue * 16 * 3.6)
                self.painter.drawArc(scale_rect, 90 * 16, span_angle)

        def __init__(self):
            super().__init__()
            # Buttons
            self.button_stop_cycle = QPushButton("Stop", self)
            self.button_stop_cycle.setStyleSheet("margin: 10px;")
            self.button_toggle_pause = QPushButton("Pause", self)
            self.button_toggle_pause.setStyleSheet("margin: 10px;")
            self.progress_bar = self.ProgressBar()

            # Layout
            layout = QGridLayout()
            layout.addWidget(self.button_toggle_pause, 0, 1)
            layout.addWidget(self.button_stop_cycle, 1, 1)
            layout.addWidget(self.progress_bar, 0, 0, 1, 2)
            self.setLayout(layout)


    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        if controller is None:
            self.controller = PomodoroTimerController()
        self.start_screen = self.StartScreen()
        self.work_screen = self.WorkScreen()

        # Windows
        self.addWidget(self.start_screen)
        self.addWidget(self.work_screen)

        # Settings
        self.setCurrentIndex(0)
        self.setMinimumSize(400, 400)


        