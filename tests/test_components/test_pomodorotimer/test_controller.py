from datetime import timedelta

from PySide6.QtTest import QSignalSpy
from PySide6.QtCore import QEventLoop

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

    def test_timer_elapsed_time_updates_correctly_after_series_of_ticks(self, qapp):
        """Check that timer ellapsed time updates correctly after series of ticks."""
        timer_interval_ms = 10
        timer_controller = PomodoroTimerController(timer_interval_ms=timer_interval_ms)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=100*timer_interval_ms)

        loop = QEventLoop()
        count = 0
        number_of_ticks_to_wait = 10
        def on_time_changed():
            nonlocal count
            count += 1
            if count == number_of_ticks_to_wait:
                loop.quit()

        timer_controller.time_changed.connect(on_time_changed)
        timer_controller.start()
        loop.exec()

        expected_time = timedelta(milliseconds=number_of_ticks_to_wait * timer_interval_ms)
        actual_time = timer_controller.elapsedTime
        allowed_delta = timedelta(milliseconds=timer_interval_ms*3) 
        assert abs(actual_time - expected_time) <= allowed_delta, f"Expected elapsed time: {expected_time}, Actual elapsed time: {actual_time}"