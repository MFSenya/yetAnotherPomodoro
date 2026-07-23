from datetime import timedelta

import pytest
from PySide6.QtTest import QSignalSpy
from PySide6.QtCore import QEventLoop

from src.views.components.pomodorotimer.pomodorotimer_controller import PomodoroTimerController

timer_interval_ms = 10

class TestPomodoroTimerControllerSignals:

    def run_and_wait_for_ticks(self, controller: PomodoroTimerController, number_of_ticks, launch_timer_func=None):
        """Run controller and wait for a specified number of ticks."""
        # Use start if launch_method isn't specified
        if launch_timer_func is None:
            launch_timer_func = lambda controller : controller.start()
        loop = QEventLoop()
        count = 0
        def on_time_changed():
            nonlocal count
            count += 1
            if count == number_of_ticks:
                loop.quit()
        controller.time_changed.connect(on_time_changed)
        launch_timer_func(controller)
        loop.exec()
        controller.time_changed.disconnect(on_time_changed)

    def compare_elapsed_time(self, controller: PomodoroTimerController, expected_time: timedelta, allowed_delta):
        """Compare timer elapsed time with expected value."""
        actual_time = controller.currentPeriodElapsedTime
        assert abs(actual_time - expected_time) <= allowed_delta, f"Expected elapsed time: {expected_time}, Actual elapsed time: {actual_time}"


    def test_timer_runs_to_completion_and_emits_finished_in_auto_run_mode(self, qtbot):
        """Check that timer finishes successfully and gives signal finished,
          when new period auto start option is enabled."""
        timer_controller = PomodoroTimerController(timer_interval_ms=timer_interval_ms)
        timer_controller.numberOfCycles = 1
        timer_controller.newPeriodAutoStart = True
        timer_controller.workTimeInterval = timedelta(milliseconds=50)
        timer_controller.restTimeInterval = timedelta(milliseconds=5)

        with qtbot.waitSignal(timer_controller.finished, timeout=100):
            timer_controller.start()


    def test_timer_runs_to_completion_and_emits_finished_if_resumed_manually(self, qtbot):
        """Check that timer finishes successfully and gives signal finished,
           when it resumed manually after first period finish and auto pause."""
        timer_controller = PomodoroTimerController(timer_interval_ms=timer_interval_ms)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=5*timer_interval_ms)
        timer_controller.restTimeInterval = timedelta(milliseconds=5*timer_interval_ms)

        finished_spy = QSignalSpy(timer_controller.finished)

        timer_controller.start()
        # Wait for the work interval end (add an extra milliseconds to ensure that we wait long enough)
        qtbot.wait((timer_controller.workTimeInterval.total_seconds())*1000 + 100)
        assert timer_controller.currentMode == timer_controller.Mode.IDLE
        # Resume
        timer_controller.toggle_pause()
        # Wait for finish signal
        qtbot.waitUntil(lambda: finished_spy.count() == 1, timeout=100)
        assert timer_controller.currentMode == timer_controller.Mode.IDLE

    def test_timer_stops_and_emits_finished_if_stopped_manually(self, qtbot):
        """Check that timer stops correctly and gives signal finished, when it stopped manually."""
        timer_controller = PomodoroTimerController(timer_interval_ms=timer_interval_ms)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=50 * timer_interval_ms)
        timer_controller.restTimeInterval = timedelta(milliseconds=5 * timer_interval_ms)

        finished_spy = QSignalSpy(timer_controller.finished)
        self.run_and_wait_for_ticks(timer_controller, 10)
        timer_controller.stop()
        # Wait for finish signal
        qtbot.waitUntil(lambda: finished_spy.count() == 1, timeout=100)
        assert timer_controller.currentPeriodElapsedTime == timedelta()
        assert timer_controller.currentMode == timer_controller.Mode.IDLE


    def test_timer_pauses_automatically_after_work_interval_end(self, qtbot):
        """Check that pauses automatically after work interval end."""
        timer_controller = PomodoroTimerController(timer_interval_ms=timer_interval_ms)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=5*timer_interval_ms)

        timer_controller.start()
        # Wait for the work interval end (add an extra milliseconds to ensure that we wait long enough)
        qtbot.wait(timer_controller.workTimeInterval.total_seconds()*1000 + 100)
        assert timer_controller.currentMode == timer_controller.Mode.IDLE

    def test_timer_elapsed_time_updates_correctly_after_a_series_of_ticks(self, qapp):
        """Check that timer ellapsed time updates correctly after a series of ticks."""
        timer_controller = PomodoroTimerController(timer_interval_ms=timer_interval_ms)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=100*timer_interval_ms)
        timer_controller.restTimeInterval = timedelta(milliseconds=10*timer_interval_ms)

        number_of_ticks_to_wait = 10
        self.run_and_wait_for_ticks(timer_controller, number_of_ticks_to_wait)
        expected_time = timedelta(milliseconds=number_of_ticks_to_wait * timer_interval_ms)
        allowed_delta = timedelta(milliseconds=timer_interval_ms*3) 
        self.compare_elapsed_time(timer_controller, expected_time, allowed_delta)

    def test_timer_progress_updates_correctly_after_a_series_of_ticks(self, qapp):
        """Check that timer progress time updates correctly after a series of ticks."""
        timer_controller = PomodoroTimerController(timer_interval_ms=timer_interval_ms)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=100*timer_interval_ms)
        timer_controller.restTimeInterval = timedelta(milliseconds=10*timer_interval_ms)

        self.run_and_wait_for_ticks(timer_controller, 10)
        expected_progress = 10
        actual_progress = timer_controller.currentIntervalProgress
        allowed_delta = 1
        assert timer_controller.currentMode == timer_controller.Mode.WORK
        assert abs(actual_progress - expected_progress) <= allowed_delta, f"Expected progress: {expected_progress}, Actual progress: {actual_progress}"

    def test_timer_stops_correctly_in_idle_mode(self, qapp):
        """Test stop in IDLE mode."""
        timer_controller = PomodoroTimerController(timer_interval_ms=timer_interval_ms)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=100*timer_interval_ms)
        timer_controller.restTimeInterval = timedelta(milliseconds=10*timer_interval_ms)
        number_of_ticks_to_wait = 10
        self.run_and_wait_for_ticks(timer_controller, number_of_ticks_to_wait)
        timer_controller.toggle_pause()
        expected_time = timedelta(milliseconds=number_of_ticks_to_wait * timer_interval_ms)
        allowed_delta = timedelta(milliseconds=timer_interval_ms*3) 
        self.compare_elapsed_time(timer_controller, expected_time, allowed_delta)
        assert timer_controller.currentMode == timer_controller.Mode.IDLE
        timer_controller.stop()
        assert timer_controller.currentMode == timer_controller.Mode.IDLE
        assert timer_controller.currentPeriodElapsedTime == timedelta()

    def test_timer_resumes_correctly_after_a_pause(self, qapp):
        """Test resume after a pause."""
        timer_controller = PomodoroTimerController(timer_interval_ms=timer_interval_ms)
        timer_controller.numberOfCycles = 1
        timer_controller.workTimeInterval = timedelta(milliseconds=100*timer_interval_ms)
        timer_controller.restTimeInterval = timedelta(milliseconds=10*timer_interval_ms)
        number_of_ticks_to_wait = 10
        # Pause after some number of ticks
        self.run_and_wait_for_ticks(timer_controller, number_of_ticks_to_wait)
        timer_controller.toggle_pause()
        expected_time_before_pause = timedelta(milliseconds=number_of_ticks_to_wait * timer_interval_ms)
        allowed_delta = timedelta(milliseconds=timer_interval_ms*3) 
        self.compare_elapsed_time(timer_controller, expected_time_before_pause, allowed_delta)
        assert timer_controller.currentMode == timer_controller.Mode.IDLE
        # Resume
        self.run_and_wait_for_ticks(timer_controller, number_of_ticks_to_wait, lambda controller: controller.toggle_pause())
        assert timer_controller.currentMode == timer_controller.Mode.WORK
        expected_time_after_pause = expected_time_before_pause + timedelta(milliseconds=number_of_ticks_to_wait * timer_interval_ms)
        self.compare_elapsed_time(timer_controller, expected_time_after_pause, allowed_delta)


class TestPomodoroTimerControllerBehavior:
    def test_cannot_get_progress_for_timer_that_has_not_been_started(self):
        with pytest.raises(PomodoroTimerController.PomodoroTimerException, match="Сan't get current progress. Timer has not been started"):
            timer_controller = PomodoroTimerController(timer_interval_ms=timer_interval_ms)
            timer_controller.currentIntervalProgress
