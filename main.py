import sys
from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic

class Main(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.clicked = False
		self.setupUi()

	def setupUi(self):
		uic.loadUi('main.ui', self)
		self.update_btn.clicked.connect(self.update)
		self.update()

	def update(self):
		db = Qt.QSqlDatabase().addDatabase('QSQLITE')
		db.setDatabaseName('coffee.sqlite')
		db.open()
		qry = Qt.QSqlQuery(db)
		qry.prepare('SELECT * FROM coffee_info')
		qry.exec()
		model = Qt.QSqlQueryModel()
		model.setQuery(qry)
		while model.canFetchMore():
			model.fetchMore()
		db.close()
		self.table.setModel(model)


def except_hook(cls, exception, traceback):
	sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	form = Main()
	form.show()
	sys.excepthook = except_hook
	sys.exit(app.exec())
