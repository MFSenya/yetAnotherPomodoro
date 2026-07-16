from datetime import timedelta

import pytest
from PySide6.QtTest import QSignalSpy

from src.views.components.pomodorotimer.pomodorotimer_controller import PomodoroTimerController

class TestPomodoroTimerControllerSignals:
    def test_timer_runs_to_completion_and_emits_finished_in_auto_run_mode(self, qtbot):
        """Check that timer finishes successfully and gives signal finished,
          when new period auto start option is enabled."""
        timer_controller = PomodoroTimerController(timer_interval_ms=10)
        timer_controller.numberOfCycles = 1
        timer_controller.newPeriodAutoStart = True
        timer_controller.workTimeInterval = timedelta(milliseconds=50)
        timer_controller.restTimeInterval = timedelta(milliseconds=5)

        with qtbot.waitSignal(timer_controller.finished, timeout=100):
            timer_controller.start()


    def test_timer_runs_to_completion_and_emits_finished_if_resumed_manually(self, qtbot):
        """Check that timer finishes successfully and gives signal finished,
           when it resumed manually after first period finish and auto pause."""
        timer_controller = PomodoroTimerController(timer_interval_ms=10)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=50)
        timer_controller.restTimeInterval = timedelta(milliseconds=5)

        period_spy = QSignalSpy(timer_controller.period_changed)
        finished_spy = QSignalSpy(timer_controller.finished)

        timer_controller.start()

        # Wait for period change
        qtbot.waitUntil(lambda: period_spy.count() >= 1, timeout=100)
        assert timer_controller.currentMode == timer_controller.Mode.IDLE
        timer_controller.toggle_pause()
        # Wait for finish signal
        qtbot.waitUntil(lambda: finished_spy.count() == 1, timeout=100)
        assert timer_controller.currentMode == timer_controller.Mode.IDLE

    def test_timer_stops_and_emits_finished_if_stopped_manually(self, qtbot):
        """Check that timer gives signal finished, when it stopped manually."""
        timer_controller = PomodoroTimerController(timer_interval_ms=10)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=50)
        timer_controller.restTimeInterval = timedelta(milliseconds=5)

        finished_spy = QSignalSpy(timer_controller.finished)

        timer_controller.start()
        timer_controller.stop()
        # Wait for finish signal
        qtbot.waitUntil(lambda: finished_spy.count() == 1, timeout=100)
        assert timer_controller.currentMode == timer_controller.Mode.IDLE


    def test_timer_emits_period_changed_and_paused_automatically(self, qtbot):
        """Check that after change of a period timer pauses automatically."""
        timer_controller = PomodoroTimerController(timer_interval_ms=10)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=5)

        with qtbot.waitSignal(timer_controller.period_changed, timeout=100):
            timer_controller.start()
        
        assert timer_controller.currentMode == timer_controller.Mode.IDLE
