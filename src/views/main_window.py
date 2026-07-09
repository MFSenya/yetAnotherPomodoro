from PySide6.QtWidgets import QMainWindow

from .ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.startCycleButton.clicked.connect(self.on_start_cycle_button_clicked)
        self.ui.stopCycleButton.clicked.connect(self.on_stop_cycle_button_clicked)
        self.ui.pauseCycleButton.clicked.connect(self.on_pause_cycle_button_clicked)


    def on_start_cycle_button_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        
        # Calculate ticking time in seconds
        work_time = self.ui.workTimeTimeEdit.time()
        minutes = work_time.minute()
        seconds = work_time.second()
        tiking_time = minutes * 60 + seconds
        
        self.ui.pomodoroTimer.cycleTime = tiking_time
        self.ui.pomodoroTimer.start()
    
    def on_stop_cycle_button_clicked(self):
        self.ui.pomodoroTimer.stop()
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_pause_cycle_button_clicked(self):
        self.ui.pomodoroTimer.pause()
        self.ui.pauseCycleButton.text = "CONTINUE" if self.ui.pauseCycleButton.text == "PAUSE" else "PAUSE"