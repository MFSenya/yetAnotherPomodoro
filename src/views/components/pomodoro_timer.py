from enum import Enum
from dataclasses import dataclass

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect, QTimer, Property, Signal
from PySide6.QtGui import QPainter, QColor, QPen




class PomodoroTimer(QWidget):
    # Custom signals for communication with an interface
    finished = Signal()
    cycle_finished = Signal()

    class Mode(Enum):
        WORK = 1
        REST = 2
        IDLE = 3


    def __init__(self, parent=None):
        super().__init__(parent)
        self._bg_color = QColor("#ffffff")
        self._progress_bar_color = QColor("#4a62ad")
        self._cycle_time = 0
        self._rest_time = 0
        self._total_number_of_cycles = 0
        self._curent_cycle = 0
        self._current_time = 0
        self._mode = self.Mode.IDLE
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.tick)
        self._next_period_auto_run = False

    def __get_remaining_time(self):
        match self._mode:
            case self.Mode.WORK:
                return self._cycle_time
            case self.Mode.REST:
                return self._rest_time
            case self.Mode.IDLE:
                raise RuntimeError("Attempt to get ramaining time in IDLE mode")
            case _:
                raise RuntimeError("Attempt to get remaining time in undefined mode")

    @property
    def mode(self):
        """Current work mode."""
        return self._mode

    @property
    def restPeriodAutoRun(self):
        """ Start the next rest period automatically."""
        return self._next_period_auto_run
    
    @restPeriodAutoRun.setter
    def restPeriodAutoRun(self, rest_period_auto_run):
        self._next_period_auto_run = rest_period_auto_run

    @property
    def currentCycle(self):
        return self._curent_cycle
    
    @property
    def numberOfCycles(self):
        return self._total_number_of_cycles

    @property
    def progress(self):
        if self._cycle_time == 0:
            return 0
        return int(self._current_time / self.__get_remaining_time() * 100)
    
    @property
    def cycleTime(self):
        return self._cycle_time
    
    @cycleTime.setter
    def cycleTime(self, cycle_time):
        """Set cycle time
        
        Args:
            cycle_time: cycle time in seconds
        """
        self._cycle_time = cycle_time

    @property
    def restTime(self):
        return self._rest_time
    
    @cycleTime.setter
    def restTime(self, rest_time):
        """Set rest time
        
        Args:
            rest_time: rest time in seconds
        """
        self._rest_time = rest_time
        
    @Property(QColor)
    def progressBarColor(self):
        return self._progress_bar_color
    
    @progressBarColor.setter
    def progressBarColor(self, color):
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

    def start(self):
        self._curent_cycle = 1
        self._timer.start(1000)
    
    def stop(self):
        self._timer.stop()

    def pause(self):
        if self._timer.isActive():
            self._timer.stop()
    
    def resume(self):
        if not self._timer.isActive():
            self._timer.start()

    
    def tick(self):
        if self._current_time < self.__get_remaining_time():
            self._current_time += 1
            self.update()
        else:
            if self.currentCycle <= self.numberOfCycles:
                if self.restPeriodAutoRun:
                    self.start()
                else:
                    self._mode = self.Mode.IDLE
                    self.cycleFinished.emit()
            else:
                self._timer.stop()
                self.finished.emit()


    def paintEvent(self, event):
        painter = QPainter(self)
        # Enable antialiasing
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Draw background
        painter.fillRect(self.rect(), self.backgroundColor)
        # Draw scale
        size = min(self.width(), self.height()) - 40
        x = (self.width() - size) // 2
        y = (self.height() - size) // 2
        scale_rect = QRect(x, y, size, size)
        painter.setPen(QPen(QColor("#eaeaea"), 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawEllipse(scale_rect)
        painter.setPen(QPen(self.progressBarColor, 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        span_angle = int(-self.progress * 16 * 3.6)
        painter.drawArc(scale_rect, 90 * 16, span_angle)
        # Нарисовать процент заполнения шкалы
        painter.setPen(QPen(QColor("#000000"), 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        font = painter.font()
        font.setBold(True)
        font.setPointSize(size / 5)
        painter.setFont(font)
        painter.drawText(scale_rect, Qt.AlignmentFlag.AlignCenter, f"{self.currentCycle}/{self.numberOfCycles}\n{self.progress} %")        
        painter.end()