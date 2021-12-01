import sys
from random import randint as rand
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class Main(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.clicked = False
		self.setupUi()

	def setupUi(self):
		uic.loadUi('UI.ui', self)
		self.btn.clicked.connect(self.click)
		self.sz = (self.size().width(), self.size().height())

	def click(self):
		self.clicked = True
		self.update()

	def paintEvent(self, event):
		if self.clicked:
			self.btn.hide()
			qp = QtGui.QPainter()
			qp.begin(self)
			qp.setBrush(QtGui.QColor(255, 255, 0))
			for i in range(rand(1, 5)):
				rad = rand(5, 20)
				pos = [rand(0, self.sz[0] - rad * 2), rand(0, self.sz[1] - rad * 2)]
				qp.drawEllipse(pos[0], pos[1], rad * 2, rad * 2)
			qp.end()


def except_hook(cls, exception, traceback):
	sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	form = Main()
	form.show()
	sys.excepthook = except_hook
	sys.exit(app.exec())
