from datetime import timedelta
from dataclasses import dataclass

from PySide6.QtWidgets import QWidget, QStackedWidget, QPushButton, QGridLayout, QTimeEdit, QSpinBox, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Property, Qt, QRect, QTime, Signal

from .pomodorotimer_controller import PomodoroTimerController


class PomodoroTimerView(QStackedWidget):

    class StartScreen(QWidget):
        start_button_clicked = Signal()
        def __init__(self, controller: PomodoroTimerController):
            super().__init__()
            self._controller = controller
            # Buttons
            self._button_start_cycle = QPushButton("Start")
            self._button_start_cycle.setStyleSheet("margin: 10px;")
            self._button_start_cycle.clicked.connect(self.__on_button_start_cycle_click)
            # TimeEdits
            time_edit_display_format = "mm"
            set_calendar_popup = False
            self._time_edit_work_time_interval = QTimeEdit()
            self._time_edit_work_time_interval.setDisplayFormat(time_edit_display_format)
            self._time_edit_work_time_interval.setCalendarPopup(set_calendar_popup)
            self._time_edit_work_time_interval.setMinimumTime(QTime(0, 1))
            self._time_edit_rest_time_interval = QTimeEdit()
            self._time_edit_rest_time_interval.setDisplayFormat(time_edit_display_format)
            self._time_edit_rest_time_interval.setCalendarPopup(set_calendar_popup)
            # Other
            self._spinbox_number_of_cycles = QSpinBox(minimum=1)
            self._spinbox_number_of_cycles.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
            # Layout
            _layout = QGridLayout()
            _layout.addWidget(self._time_edit_work_time_interval, 0, 0)
            _layout.addWidget(self._time_edit_rest_time_interval, 0, 1)
            _layout.addWidget(self._spinbox_number_of_cycles, 1, 0, 1, 2, alignment=Qt.AlignHCenter)
            _layout.addWidget(self._button_start_cycle, 2, 0, 1, 2)
            # Settings
            self.setLayout(_layout)
        
        def __on_button_start_cycle_click(self):
            self._controller.numberOfCycles = self._spinbox_number_of_cycles.value()
            self._controller.workTimeInterval = timedelta(minutes=self._time_edit_work_time_interval.time().minute())
            self._controller.restTimeInterval = timedelta(minutes=self._time_edit_rest_time_interval.time().minute())
            self._controller.start()
            self.start_button_clicked.emit()



    class WorkScreen(QWidget):
        stop_button_clicked = Signal()
        toggle_pause_button_clicked = Signal()

        class ProgressBar(QWidget):
            def __init__(self):
                super().__init__()
                self._value = 0
                self._bg_color = QColor("#ffffff")
                self._progress_bar_color = QColor("#4a62ad")
                self._central_text = ""

            @Property(QColor)
            def barColor(self) -> QColor:
                return self._progress_bar_color
            
            @barColor.setter
            def barColor(self, color):
                # Qt Designer can pass color in different formats, 
                # so we need to force cast to QColor
                self._progress_bar_color = QColor(color)
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
                self.update()

            @property
            def centralText(self):
                """Text in the bar center"""
                return self._central_text

            @centralText.setter
            def centralText(self, text: str):
                self._central_text = text
                

            def paintEvent(self, event):
                painter = QPainter(self)
                # Enable antialiasing
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                # Draw background
                painter.fillRect(self.rect(), self.backgroundColor)
                # Draw bar
                size = min(self.width(), self.height()) - 40
                x = (self.width() - size) // 2
                y = (self.height() - size) // 2
                progress_bar_rect = QRect(x, y, size, size)
                painter.setPen(QPen(QColor("#eaeaea"), 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                painter.drawEllipse(progress_bar_rect)
                painter.setPen(QPen(self.barColor, 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                span_angle = int(-self.progressValue * 16 * 3.6)
                painter.drawArc(progress_bar_rect, 90 * 16, span_angle)
                # Draw central text
                painter.setPen(QPen(QColor("#000000"), 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                font = painter.font()
                font.setBold(True)
                font.setPointSize(size / 5)
                painter.setFont(font)
                painter.drawText(progress_bar_rect, Qt.AlignmentFlag.AlignCenter, f"{self.centralText}")        
                painter.end()

        @dataclass
        class DefaultState:
            progress_bar_color : QColor
            button_stop_cycle_text: str = "Stop"
            button_toggle_pause_text: str = "Pause"

        def __return_to_default_view(self):
            self._progress_bar.barColor = self._default_state.progress_bar_color
            self.button_toggle_pause.setText(self._default_state.button_toggle_pause_text)

        def __init__(self, controller: PomodoroTimerController):
            super().__init__()
            self._progress_bar = self.ProgressBar()
            self._default_state = self.DefaultState(self._progress_bar.barColor)
            # Buttons
            self.button_stop_cycle = QPushButton(self._default_state.button_stop_cycle_text, self)
            self.button_stop_cycle.setStyleSheet("margin: 10px;")
            self.button_stop_cycle.clicked.connect(self.__on_stop_cycle_button_clicked)
            self.button_toggle_pause = QPushButton(self._default_state.button_toggle_pause_text, self)
            self.button_toggle_pause.setStyleSheet("margin: 10px;")
            self.button_toggle_pause.clicked.connect(self.__on_toggle_pause_button_clicked)
            # Controller
            self._controller = controller
            self._controller.time_changed.connect(self.__on_controller_time_changed)
            # Layout
            layout = QGridLayout()
            layout.addWidget(self.button_toggle_pause, 1, 0)
            layout.addWidget(self.button_stop_cycle, 1, 1)
            layout.addWidget(self._progress_bar, 0, 0, 1, 2)
            self.setLayout(layout)

        def __on_controller_time_changed(self):
            self._progress_bar.progressValue = self._controller.currentIntervalProgress

        def __on_stop_cycle_button_clicked(self):
            self._controller.stop()
            # so that progress bar doesn't contain an old value
            self._progress_bar.progressValue = 0
            self.__return_to_default_view()
            self.stop_button_clicked.emit()

        def __on_toggle_pause_button_clicked(self):
            def add_fancy_stuff():
                if self._controller.currentMode == self._controller.Mode.IDLE:
                    toggle_pause_button_text = "Continue"
                    # reduce bar color saturation
                    h, s, v, a = self._progress_bar.barColor.getHsv()
                    s_reduced = int(s * 0.5)
                    progress_bar_color = QColor.fromHsv(h, s_reduced, v, a)
                    self._progress_bar.barColor = progress_bar_color
                    self.button_toggle_pause.setText(toggle_pause_button_text)
                else:
                    self.__return_to_default_view()
            self._controller.toggle_pause()
            # so that the progress bar renders up to the current progress value
            self._progress_bar.update()
            add_fancy_stuff()
            self.toggle_pause_button_clicked.emit()


    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self._controller =  controller if controller is not None else PomodoroTimerController()
        self.start_screen = self.StartScreen(self._controller)
        self.work_screen = self.WorkScreen(self._controller)
        # Windows
        self.addWidget(self.start_screen)
        self.addWidget(self.work_screen)
        # Subscribe to window signals
        self.start_screen.start_button_clicked.connect(self.__on_button_start_cycle_clicked)
        self.work_screen.stop_button_clicked.connect(self._on_button_stop_cycle_clicked)
        
        # Settings
        self.setCurrentIndex(0)
        self.setMinimumSize(400, 400)
        
    def __on_button_start_cycle_clicked(self):
        # Switch to Work screen
        self.setCurrentIndex(1)

    def _on_button_stop_cycle_clicked(self):
        # Switch to Start screen
        self.setCurrentIndex(0)

    def _on_button_toggle_pause_clicked(self):
        pass
