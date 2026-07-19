from datetime import timedelta

from PySide6.QtWidgets import QWidget, QStackedWidget, QPushButton, QGridLayout, QTimeEdit, QSpinBox, QSizePolicy, QCheckBox, QSpacerItem
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
            self._button_start_cycle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            self._button_start_cycle.setStyleSheet("margin: 10px;")
            self._button_start_cycle.clicked.connect(self.__on_button_start_cycle_click)
            # TimeEdits
            time_edit_display_format = "mm"
            set_calendar_popup = False
            time_edit_style_sheet = """
                QTimeEdit {
                    selection-background-color: transparent;
                    selection-color: #000000;
                }   
            """
            self._time_edit_work_time_interval = QTimeEdit()
            self._time_edit_work_time_interval.setDisplayFormat(time_edit_display_format)
            self._time_edit_work_time_interval.setCalendarPopup(set_calendar_popup)
            self._time_edit_work_time_interval.setMinimumTime(QTime(0, 1))
            self._time_edit_work_time_interval.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            self._time_edit_work_time_interval.setStyleSheet(time_edit_style_sheet)
            self._time_edit_rest_time_interval = QTimeEdit()
            self._time_edit_rest_time_interval.setDisplayFormat(time_edit_display_format)
            self._time_edit_rest_time_interval.setCalendarPopup(set_calendar_popup)
            self._time_edit_rest_time_interval.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            self._time_edit_rest_time_interval.setStyleSheet(time_edit_style_sheet)
            # Other
            self._spinbox_number_of_cycles = QSpinBox(minimum=1)
            self._spinbox_number_of_cycles.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
            self._checkbox_next_period_auto_run = QCheckBox("Next period auto run")
            spacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
            # Layout
            _layout = QGridLayout()
            _layout.addWidget(self._time_edit_work_time_interval, 0, 0)
            _layout.addWidget(self._time_edit_rest_time_interval, 0, 1)
            _layout.addWidget(self._spinbox_number_of_cycles, 1, 0, 1, 2, alignment=Qt.AlignHCenter)
            _layout.addWidget(self._checkbox_next_period_auto_run, 2, 0, 1, 2, alignment=Qt.AlignHCenter)
            _layout.addItem(spacer, 3, 0)
            _layout.addWidget(self._button_start_cycle, 4, 0, 1, 2)
            _layout.setRowStretch(0, 1)
            _layout.setRowStretch(3, 2)
            _layout.setRowStretch(4, 2)
            # Settings
            self.setLayout(_layout)
        
        def __on_button_start_cycle_click(self):
            self._controller.numberOfCycles = self._spinbox_number_of_cycles.value()
            self._controller.workTimeInterval = timedelta(minutes=self._time_edit_work_time_interval.time().minute())
            self._controller.restTimeInterval = timedelta(minutes=self._time_edit_rest_time_interval.time().minute())
            self._controller.newPeriodAutoStart = self._checkbox_next_period_auto_run.isChecked()
            self._controller.start()
            self.start_button_clicked.emit()



    class WorkScreen(QWidget):
        stop_button_clicked = Signal()
        toggle_pause_button_clicked = Signal()

        class ProgressBar(QWidget):
            def __init__(self, controller: PomodoroTimerController):
                super().__init__()
                self._controller = controller
                self._controller.time_changed.connect(self.__on_controller_time_changed)
                self._controller.mode_changed.connect(self.__on_controller_mode_changed)
                self._value = 0
                self._background = QColor("#ffffff")
                self._progress_line_color = QColor("#4a62ad")
                self._bar_background_color = QColor("#eaeaea")
                self._central_text_color = QColor("#000000")
                self._central_text = ""

            @Property(QColor)
            def progressLineColor(self) -> QColor:
                return self._progress_line_color
            
            @progressLineColor.setter
            def progressLineColor(self, color):
                self._progress_line_color = QColor(color)
                self.update()

            @Property(QColor)
            def backgroundColor(self):
                return self._background
            
            @backgroundColor.setter
            def backgroundColor(self, color):
                self._background = QColor(color)
                self.update() 

            @Property(QColor)
            def barBackgroundColor(self):
                return self._bar_background_color
            
            @barBackgroundColor.setter
            def barBackgroundColor(self, color):
                self._bar_background_color = QColor(color)
                self.update()

            @Property(QColor)
            def centralTextColor(self):
                return self._central_text_color

            @centralTextColor.setter
            def centralTextColor(self, color):
                self._central_text_color = QColor(color)
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
                painter.setPen(QPen(self.barBackgroundColor, 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                painter.drawEllipse(progress_bar_rect)
                if self._controller.currentMode == self._controller.Mode.IDLE:
                    # reduce bar color saturation
                    h, s, v, a = self.progressLineColor.getHsv()
                    s_reduced = int(s * 0.5)
                    bar_color = QColor.fromHsv(h, s_reduced, v, a)
                else:
                    bar_color = self.progressLineColor
                painter.setPen(QPen(bar_color, 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                span_angle = int(-self.progressValue * 16 * 3.6)
                painter.drawArc(progress_bar_rect, 90 * 16, span_angle)
                # Draw central text
                painter.setPen(QPen(self.centralTextColor, 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                font = painter.font()
                font.setBold(True)
                font.setPointSize(size / 5)
                painter.setFont(font)
                painter.drawText(progress_bar_rect, Qt.AlignmentFlag.AlignCenter, f"{self.centralText}")        
                painter.end()

            def __on_controller_time_changed(self):
                self.progressValue = self._controller.currentIntervalProgress \
                                                if self._controller.currentMode != self._controller.Mode.IDLE \
                                                else 0
            
            def __on_controller_mode_changed(self):
                self.centralText = str(self._controller.currentMode.name)
                self.update()



        def __init__(self, controller: PomodoroTimerController):
            super().__init__()
            self._progress_bar = self.ProgressBar(controller)
            # Buttons
            buttons_margin = 5
            self.button_stop_cycle = QPushButton("Stop", self)
            self.button_stop_cycle.setStyleSheet(f"margin: {buttons_margin} px;")
            self.button_stop_cycle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.button_stop_cycle.clicked.connect(self.__on_stop_cycle_button_clicked)
            self.button_toggle_pause = QPushButton("Pause", self)
            self.button_toggle_pause.setStyleSheet(f"margin: {buttons_margin} px;")
            self.button_toggle_pause.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.button_toggle_pause.clicked.connect(self.__on_toggle_pause_button_clicked)
            # Controller
            self._controller = controller
            self._controller.mode_changed.connect(self.__on_controller_mode_changed)
            # Layout
            layout = QGridLayout()
            layout.addWidget(self.button_toggle_pause, 1, 0)
            layout.addWidget(self.button_stop_cycle, 1, 1)
            layout.addWidget(self._progress_bar, 0, 0, 1, 2)
            layout.setRowStretch(0, 5)
            layout.setRowStretch(1, 1)
            self.setLayout(layout)


        def __on_stop_cycle_button_clicked(self):
            self._controller.stop()
            self.stop_button_clicked.emit()

        def __on_toggle_pause_button_clicked(self):
            self._controller.toggle_pause()
            self.toggle_pause_button_clicked.emit()

        def __on_controller_mode_changed(self):
            if self._controller.currentMode == self._controller.Mode.IDLE:
                self.button_toggle_pause.setText("Continue")
            else:
                self.button_toggle_pause.setText("Pause")


    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self._controller =  controller if controller is not None else PomodoroTimerController()
        self.start_screen = self.StartScreen(self._controller)
        self.work_screen = self.WorkScreen(self._controller)
        # Windows
        self.addWidget(self.start_screen)
        self.addWidget(self.work_screen)
        # Subscribe signals
        self.start_screen.start_button_clicked.connect(self.__on_button_start_cycle_clicked)
        self.work_screen.stop_button_clicked.connect(self.__handle_end_of_work)
        self._controller.finished.connect(self.__handle_end_of_work)
        # Settings
        self.setCurrentIndex(0)
        self.setMinimumSize(300, 300)
        
    def __on_button_start_cycle_clicked(self):
        # Switch to Work screen
        self.setCurrentIndex(1)

    def __handle_end_of_work(self):
        # Switch to Start screen
        self.setCurrentIndex(0)


    def _on_button_toggle_pause_clicked(self):
        pass
