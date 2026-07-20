from enum import Enum
from datetime import datetime, timedelta

from PySide6.QtCore import QObject, Signal, QTimer



class PomodoroTimerController(QObject):
    # Signals
    finished = Signal()
    time_changed = Signal()
    mode_changed = Signal()
    period_changed = Signal()

    class PomodoroTimerException(Exception):
        def __init__(self, message: str):
            super().__init__(message)

    class Mode(Enum):
        WORK = 1
        REST = 2
        IDLE = 3

    def __init__(self, parent: QObject = None, timer_interval_ms: int = 1000):
        super().__init__(parent)
        self._work_time_interval : timedelta = timedelta()
        self._rest_time_interval : timedelta = timedelta()
        self._number_of_cycles = 0
        self._current_cycle = 1
        self._elapsed_time : timedelta = timedelta()
        self._start_time = None
        self._current_mode = self.Mode.IDLE
        self._next_mode = self.Mode.WORK
        self._timer = QTimer(self)
        self._timer.setInterval(timer_interval_ms)
        self._timer.timeout.connect(self.__tick)
        self._auto_start = False


    @property
    def elapsedTime(self) -> timedelta:
        """Get elapsed time."""
        return self._elapsed_time
    
    @elapsedTime.setter
    def elapsedTime(self, value: timedelta):
        self._elapsed_time = value
        self.time_changed.emit()

    @property
    def currentMode(self):
        """Get current mode."""
        return self._current_mode
    
    @currentMode.setter
    def currentMode(self, mode: Mode):
        if self._current_mode != mode:
            self._current_mode = mode
            self.mode_changed.emit()

    @property
    def newPeriodAutoStart(self):
        """Start new periods automatically."""
        return self._auto_start
    
    @newPeriodAutoStart.setter
    def newPeriodAutoStart(self, new_period_auto_start: bool):
        self._auto_start = new_period_auto_start

    
    @property
    def numberOfCycles(self):
        """Get total number of cycles."""
        return self._number_of_cycles
    
    @numberOfCycles.setter
    def numberOfCycles(self, number_of_cycles: int):
        self._number_of_cycles = number_of_cycles


    @property
    def workTimeInterval(self) -> timedelta:
        """Work time interval"""
        return self._work_time_interval
    
    @workTimeInterval.setter
    def workTimeInterval(self, interval: timedelta):
        self._work_time_interval = interval


    @property
    def restTimeInterval(self) -> timedelta:
        """Rest time interval."""
        return self._rest_time_interval
    
    @restTimeInterval.setter
    def restTimeInterval(self, interval: timedelta):
        self._rest_time_interval = interval

    @property
    def currentIntervalProgress(self):
        """Get progress in percents for current interval."""
        if self._start_time is None:
            raise self.PomodoroTimerException("Сan't get current progress. Timer has not been started")
        time_interval_current_mode_total_seconds = self.__get_time_interval().total_seconds()
        # Time Interval for current mode is not zero
        if time_interval_current_mode_total_seconds != 0:
            progress_value = int(self.elapsedTime.total_seconds() / self.__get_time_interval().total_seconds() * 100)
        # If not
        else:
            # Consider that progress is 100 percents
            progress_value = 100
        return progress_value 


    def toggle_pause(self):
        match self._current_mode:
            case self.Mode.WORK | self.Mode.REST:
                self._timer.stop()
                self.currentMode = self.Mode.IDLE
            case self.Mode.IDLE:
                self.start()
            case _:
                raise self.PomodoroTimerException("Can't pause in this mode")
    
    def start(self):
        self.currentMode = self._next_mode
        if self._start_time is None:
            self._start_time = datetime.now()
        self._timer.start()

    def stop(self):
        self._timer.stop()
        self._current_cycle = 1
        self._start_time = None
        self.currentMode = self.Mode.IDLE
        self.elapsedTime = timedelta()
        self.finished.emit()


    def __tick(self):
        self.elapsedTime = datetime.now() - self._start_time
        if self.elapsedTime > self.__get_time_interval():
            self.__period_finished()



    def __get_next_mode(self):
         match self._current_mode:
            case self.Mode.WORK:
                # If rest time is not zero, we change to rest
                if self._rest_time_interval > timedelta():
                    return self.Mode.REST
                else:
                    # mode stays the same
                    return self.Mode.WORK
            case self.Mode.REST:
                return self.Mode.WORK
            case _:
                raise self.PomodoroTimerException("Error: next mod can be obtained only if current mode is WORK or REST")


    def __get_time_interval(self):
        """Get time interval for current mode"""
        match self._current_mode:
            case self.Mode.WORK:
                return self._work_time_interval
            case self.Mode.REST:
                return self._rest_time_interval
            case self.Mode.IDLE:
                raise self.PomodoroTimerException("An attempt to get time interval for IDLE mode")
            case _:
                raise self.PomodoroTimerException("An attempt to get time interval for undefined mode")

    def __period_finished(self):
        self._next_mode = self.__get_next_mode()
        self._start_time = None
        # If a period finished in rest, it means that cycle is finished, too.
        # Also we finish cycle if rest time is zero
        if self._current_mode == self.Mode.REST or self._rest_time_interval == timedelta():
            self._current_cycle += 1
            if self._current_cycle > self.numberOfCycles:
                self.stop()
        else:
            if self._auto_start:
                self.start()
            else:
                self.toggle_pause()
                # Next toggle_pause will run new period, so we need to reset an elapsed time to main all variables in consistent state
                self.elapsedTime = timedelta()
        self.period_changed.emit()