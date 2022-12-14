import sys
import datetime

from PySide6.QtCore import Signal
from PySide6.QtCore import QTime, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QLabel, QPushButton

DEBUG = True

import sys
import time
import threading


loglock = threading.Lock()

def log(s, *a):
	
    """打印日志到标准输出"""
    if DEBUG:
        loglock.acquire()
        try:
            print('%s:%s' % (time.ctime(), (s % a)))
            sys.stdout.flush()
        finally:
            loglock.release()
            

class TimerLabel(QLabel):
    doubleClicked = Signal()
    prepared = Signal()
    started = Signal()
    paused = Signal()
    restarted = Signal()
    resetSignal = Signal()
    refreshed = Signal()
    stopped = Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__start_hour = 0
        self.__start_min = 0
        self.__start_sec = 0

        self.__end_hour = 0
        self.__end_min = 0
        self.__end_sec = 0

        self.__startTime = QTime()
        self.__endTime = QTime()
        self.__format = 'hh:mm:ss'

        self.__timer = QTimer(self)
        self.__timer.setSingleShot(False)
        self.__timer.timeout.connect(self.__timerTicking)
        self.__timer_interval = -1

        self.__is_after_stop_reset_time = False

        # init end time (00:00:00 by default)
        self.setEndHMS()

    def __initUi(self):
        self.setStartHMS()

    def setAfterStopResetTime(self):
        self.__is_after_stop_reset_time = True

    def resetAfterStopResetTime(self):
        self.__is_after_stop_reset_time = False

    def setTimerReverse(self, f: bool):
        if f:
            self.__timer_interval = -1
        else:
            self.__timer_interval = 1

    def setStartHMS(self):
        self.__startTime.setHMS(self.__start_hour, self.__start_min, self.__start_sec)
        time_left_text = self.__startTime.toString(self.__format)
        self.setText(time_left_text)

    def setEndHMS(self):
        self.__endTime.setHMS(self.__end_hour, self.__end_min, self.__end_sec)
        self.__end_text_time = self.__endTime.addSecs(-1).toString(self.__format)

    def setStartHour(self, h: int):
        self.__start_hour = h
        self.setStartHMS()

    def setStartMinute(self, m: int):
        self.__start_min = m
        self.setStartHMS()

    def setStartSecond(self, s: int):
        self.__start_sec = s
        self.setStartHMS()

    def setEndHour(self, h: int):
        self.__end_hour = h
        self.__setEndHMS()

    def setEndMinute(self, m: int):
        self.__end_min = m
        self.__setEndHMS()

    def setEndSecond(self, s: int):
        self.__end_sec = s
        self.__setEndHMS()

    def __prepareToTimer(self):
        self.__timerTicking()
        self.prepared.emit()

    def start(self):
        self.__timer.singleShot(self.__startTime.msec(), self.__prepareToTimer)
        # update the timer every second
        self.__timer.start(1)
        self.started.emit()

    def __isTimesUp(self, time_left_text):
        return self.__end_text_time == time_left_text

    def __timerTicking(self):
        try:
            self.__startTime = self.__startTime.addMSecs(self.__timer_interval)
            # self.__startTime = self.__startTime.addSecs(self.__timer_interval)
            time_left_text = self.__startTime.toString(self.__format)
            # log(time_left_text)
            if self.__isTimesUp(time_left_text):
                self.stop()
            else:
                self.setText(time_left_text)
        except Exception as e:
            print(e)
            print(sys.exc_info()[2].tb_lineno)
            print(sys.exc_info())

    def pause(self):
        self.__timer.stop()
        self.paused.emit()

    def restart(self):
        self.__timer.start()
        self.restarted.emit()

    def __resetStartTime(self):
        self.__startTime = QTime(self.__start_hour, self.__start_min, self.__start_sec)
        self.setText(self.__startTime.toString(self.__format))

    def __resetTimer(self):
        self.__resetStartTime()
        self.__timer.stop()
        self.__timer.timeout.disconnect(self.__timerTicking)

    def reset(self):
        self.__resetTimer()
        self.resetSignal.emit()

    def refresh(self):
        self.__resetStartTime()
        self.refreshed.emit()

    def stop(self):
        if DEBUG:
            log('stop')
        try:
            if self.__is_after_stop_reset_time:
                self.__resetTimer()
            self.__timer.stop()
            self.stopped.emit()
        except Exception as e:
            print(e)
            print(sys.exc_info()[2].tb_lineno)
            print(sys.exc_info())

    def isPaused(self) -> bool:
        return self.__timer.isActive()

    def mouseDoubleClickEvent(self, e):
        self.doubleClicked.emit()
        return super().mouseDoubleClickEvent(e)

    def setEndTimeText(self):
        self.setText(self.__end_text_time)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    lbl = TimerLabel(alignment=QtCore.Qt.AlignCenter)
    lbl.setFont(QtGui.QFont("Roman times", 28, QtGui.QFont.Bold))
    lbl.setStartHour(0)
    lbl.setStartMinute(0)
    lbl.setStartSecond(10)


    def start():
        log('start')
        lbl.setStartMinute(0)
        lbl.setStartSecond(10)
        lbl.start()

    lay = QGridLayout()
    lay.addWidget(lbl)
    startButton = QPushButton("start")
    startButton.clicked.connect(start)
    lay.addWidget(startButton)

    widget = QWidget()
    widget.setLayout(lay)
    widget.setWindowTitle('倒计时')
    widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    widget.resize(400, 200)
    widget.show()

    lbl.start()

    sys.exit(app.exec_())
