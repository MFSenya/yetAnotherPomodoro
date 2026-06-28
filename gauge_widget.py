from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect, Property
from PySide6.QtGui import QPainter, QColor, QPen


class GaugeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 25
        self._bg_color = QColor("#ffffff")
        self._progress_bar_color = QColor("#4a62ad")


    @Property(int)
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if value != self._value:
            self._value = max(0, min(value, 100))
            self.update()
        
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
        span_angle = int(-self._value * 16 * 3.6)
        painter.drawArc(scale_rect, 90 * 16, span_angle)
        # Нарисовать процент заполнения шкалы
        painter.setPen(QPen(QColor("#000000"), 20, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        font = painter.font()
        font.setBold(True)
        font.setPointSize(size / 5)
        painter.setFont(font)
        painter.drawText(scale_rect, Qt.AlignmentFlag.AlignCenter, f"{self._value}%")        
        painter.end()