from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel, QLineEdit, QRadioButton, QVBoxLayout, QFrame, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import os
import ODE

def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Практикум по ЭВМ. Питеркин Дмитрий, гр. 304.')
        self.setGeometry(100, 100, 1100, 510)
        self.setFixedWidth(1100)
        self.setFixedHeight(510)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax1 = self.figure.add_subplot(121)
        self.ax2 = self.figure.add_subplot(122)
        self.plot_widget = QWidget(self)
        self.plot_widget.setGeometry(280, 10, 800, 400)
        plot_box = QVBoxLayout()
        plot_box.addWidget(self.canvas)
        self.plot_widget.setLayout(plot_box)

        self.label0 = QLabel("C =",self)
        self.label1 = QLabel("V0 =", self)
        self.label2 = QLabel("t_stop =", self)
        self.label3 = QLabel("dt =", self)
        self.label4 = QLabel("eps =", self)
        self.label0.move(30,30)
        self.label1.move(30, 70)
        self.label2.move(30, 110)
        self.label3.move(30, 150)
        self.label4.move(30, 190)
        
        self.label5 = QLabel("", self)
        self.label6 = QLabel("", self)
        self.label7 = QLabel("", self)
        self.label5.setGeometry(750, 405, 400, 30)
        self.label6.setGeometry(750, 425, 400, 30)
        self.label7.setGeometry(750, 445, 400, 30)
        self.label12 = QLabel("Задача М2.2 (Э). Трофическая цепь (замкнутая экосистема)", self)
        self.label12.setGeometry(750, 475, 315, 30)
        self.label12.setFrameStyle(QFrame.Panel)
        
        self.label8 = QLabel("E1 =",self)
        self.label9 = QLabel("E2 =", self)
        self.label10 = QLabel("R =", self)
        self.label8.move(160, 30)
        self.label9.move(160, 70)
        self.label10.move(160, 110)
        
        self.label8 = QLabel("0.1",self)
        self.label9 = QLabel("0.2", self)
        self.label10 = QLabel("5", self)
        self.label8.setGeometry(200, 30, 50, 30)
        self.label9.setGeometry(200, 70, 50, 30)
        self.label10.setGeometry(200, 110, 50, 30)
        self.label8.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label9.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label10.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        self.lineEdit1=QLineEdit(self)
        self.lineEdit2 = QLineEdit(self)
        self.lineEdit3 = QLineEdit(self)
        self.lineEdit4 = QLineEdit(self)
        self.lineEdit5 = QLineEdit(self)
        self.lineEdit1.setGeometry(75, 30, 50, 30)
        self.lineEdit2.setGeometry(75, 70, 50, 30)
        self.lineEdit3.setGeometry(75, 110, 50, 30)
        self.lineEdit4.setGeometry(75, 150, 50, 30)
        self.lineEdit5.setGeometry(75, 190, 50, 30)
        self.lineEdit1.setText("10")
        self.lineEdit2.setText("0.02")
        self.lineEdit3.setText("1000")
        self.lineEdit4.setText("0.01")
        self.lineEdit5.setText("0.1")
        
        self.label_choice = QLabel("Начать из точки:", self)
        self.label_choice.setGeometry(150, 145, 100, 30)
        self.r0 = QRadioButton("Особая точка 0", self)
        self.r1 = QRadioButton("Особая точка 1", self)
        self.r2 = QRadioButton("Особая точка 2", self)
        self.r0.move(150, 170)
        self.r1.move(150, 190)
        self.r2.move(150, 210)
        self.r0.clicked.connect(lambda: self.clickBox(0))
        self.r1.clicked.connect(lambda: self.clickBox(1))
        self.r2.clicked.connect(lambda: self.clickBox(2))
        self.r0.setChecked(True)
        self.starting_point = 0
        
        self.label_error = QLabel("", self)
        self.label_error.setGeometry(370, 200, 400, 30)
        
        self.button = QPushButton('Посчитать и нарисовать', self)
        self.button.setGeometry(20, 455, 250, 40)
        self.button.clicked.connect(self.plot)
        
        self.label11 = QLabel("Заготовки бифуркаций параметров:", self)
        self.label11.setGeometry(30, 240, 200, 30)
        
        self.ex1 = QPushButton('Седло - Неустойчивый фокус - Седло (А)', self)
        self.ex2 = QPushButton('Седло - Неустойчивый фокус - Седло (Б)', self)
        self.ex3 = QPushButton('Седло - Устойчивый фокус - Седло', self)
        self.ex4 = QPushButton('Седло - Устойчивый узел - Седло', self)
        self.ex5 = QPushButton('Седло - Седло - Устойчивый узел', self)
        self.ex6 = QPushButton('Устойчивый узел - Седло - Седло', self)
        self.ex7 = QPushButton('Устойчивый узел - Седло - Неустойчивый узел', self)
        self.ex1.setGeometry(20, 270, 250, 25)
        self.ex2.setGeometry(20, 295, 250, 25)
        self.ex3.setGeometry(20, 320, 250, 25)
        self.ex4.setGeometry(20, 345, 250, 25)
        self.ex5.setGeometry(20, 370, 250, 25)
        self.ex6.setGeometry(20, 395, 250, 25)
        self.ex7.setGeometry(20, 420, 250, 25)
        self.ex1.clicked.connect(lambda: self.example(1))
        self.ex2.clicked.connect(lambda: self.example(2))
        self.ex3.clicked.connect(lambda: self.example(3))
        self.ex4.clicked.connect(lambda: self.example(4))
        self.ex5.clicked.connect(lambda: self.example(5))
        self.ex6.clicked.connect(lambda: self.example(6))
        self.ex7.clicked.connect(lambda: self.example(7))
        
        self.image = QLabel(self)
        pixmap = QPixmap(resource_path("equation.png")).scaledToHeight(80, Qt.SmoothTransformation)
        self.image.setGeometry(290, 405, 600, 100)
        self.image.setPixmap(pixmap)
        
        self.plot()
        self.show()
    
    def clickBox(self, point):
        self.starting_point = point
        
    def example(self, n):
        if n == 1:
            self.lineEdit1.setText("20")
            self.lineEdit2.setText("0.25")
            self.lineEdit3.setText("300")
            self.lineEdit4.setText("0.01")
            self.lineEdit5.setText("0.1")
            self.r1.setChecked(True)
            self.starting_point = 1
        if n == 2:
            self.lineEdit1.setText("20")
            self.lineEdit2.setText("0.25")
            self.lineEdit3.setText("300")
            self.lineEdit4.setText("0.01")
            self.lineEdit5.setText("0.1")
            self.r0.setChecked(True)
            self.starting_point = 0
        if n == 3:
            self.lineEdit1.setText("10")
            self.lineEdit2.setText("0.1")
            self.lineEdit3.setText("300")
            self.lineEdit4.setText("0.01")
            self.lineEdit5.setText("0.1")
            self.r0.setChecked(True)
            self.starting_point = 0
        if n == 4:
            self.lineEdit1.setText("3")
            self.lineEdit2.setText("1")
            self.lineEdit3.setText("150")
            self.lineEdit4.setText("0.01")
            self.lineEdit5.setText("0.1")
            self.r0.setChecked(True)
            self.starting_point = 0
        if n == 5:
            self.lineEdit1.setText("1")
            self.lineEdit2.setText("1")
            self.lineEdit3.setText("150")
            self.lineEdit4.setText("0.01")
            self.lineEdit5.setText("0.1")
            self.r0.setChecked(True)
            self.starting_point = 0
        if n == 6:
            self.lineEdit1.setText("0.2")
            self.lineEdit2.setText("0.2")
            self.lineEdit3.setText("150")
            self.lineEdit4.setText("0.01")
            self.lineEdit5.setText("0.1")
            self.r0.setChecked(True)
            self.starting_point = 0
        if n == 7:
            self.lineEdit1.setText("0.2")
            self.lineEdit2.setText("0.01")
            self.lineEdit3.setText("150")
            self.lineEdit4.setText("0.01")
            self.lineEdit5.setText("0.1")
            self.r0.setChecked(True)
            self.starting_point = 0
            
    
    def plot(self):
        self.ax1.clear()
        self.ax2.clear()
        self.label_error.setText("")
        
        if len(self.lineEdit1.text())!=0:
            self.C=float(self.lineEdit1.text())
        else:
            self.C = 10
            self.lineEdit1.setText("10")
        if len(self.lineEdit2.text()) != 0:
            self.V0=float(self.lineEdit2.text())
        else:
            self.V0 = 0.02
            self.lineEdit2.setText("0.02")
        if len(self.lineEdit3.text()) != 0:
            self.t_stop=float(self.lineEdit3.text())
        else:
            self.t_stop = 2500
            self.lineEdit3.setText("2500")
        if len(self.lineEdit4.text()) != 0:
            self.dt=float(self.lineEdit4.text())
        else:
            self.dt = 0.01
            self.lineEdit4.setText("0.01")
        if len(self.lineEdit5.text()) != 0:
            self.eps=float(self.lineEdit5.text())
        else:
            self.eps = 0.1
            self.lineEdit5.setText("0.1")
        
        try:
            response0, response1, response2 = ODE.thing(self.ax1, self.ax2, self.C, self.V0, self.t_stop, self.dt, self.eps, self.starting_point)
            self.label5.setText(response0)
            self.label6.setText(response1)
            self.label7.setText(response2)
        except Exception as e:
            self.label_error.setText(str(e))
        
        plt.tight_layout()
        plt.gcf().subplots_adjust(bottom=0.12, top=0.9, wspace=0.25)
        self.canvas.draw()
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    w = Window()
    app.exec_()