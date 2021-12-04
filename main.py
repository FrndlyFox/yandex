import sys
import sqlite3
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from UI.main import Ui_MainWindow as MainUI
from UI.add import Ui_Form as AddUi
from UI.edit import Ui_Form as EditUi


class Main(QtWidgets.QMainWindow, MainUI):
	def __init__(self):
		super().__init__()
		self.clicked = False
		self.setupUi(self)
		self.setup_ui()

	def setup_ui(self):
		self.update_btn.clicked.connect(self.update)
		self.add_btn.clicked.connect(self.add)
		self.edit_btn.clicked.connect(self.edit)
		self.update()

	def update(self):
		db = Qt.QSqlDatabase().addDatabase('QSQLITE')
		db.setDatabaseName('data/coffee.sqlite')
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

	def add(self):
		self.add_form = Add()
		self.add_form.show()

	def edit(self):
		self.edit_form = Edit()
		self.edit_form.show()


class Add(QtWidgets.QWidget, AddUi):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setup_ui()

	def setup_ui(self):
		self.save_btn.clicked.connect(self.save)

	def save(self):
		id = self.id_edit.text()
		name = self.name_edit.text()
		degree = self.degree_edit.text()
		type = self.type_edit.text()
		desc = self.desc_edit.text()
		price = self.price_edit.text()
		volume = self.vol_edit.text()
		db = Qt.QSqlDatabase().addDatabase('QSQLITE')
		db.setDatabaseName('data/coffee.sqlite')
		db.open()
		qry = Qt.QSqlQuery(db)
		qry.prepare(f'INSERT INTO coffee_info (id, name, roast_degree, type, description, price, volume) \
					  VALUES ("{id}", "{name}", "{degree}", "{type}", "{desc}", "{price}", "{volume}")')
		qry.exec()
		db.close()
		self.close()


class Edit(QtWidgets.QWidget, EditUi):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setup_ui()
		self.load()

	def setup_ui(self):
		self.save_btn.clicked.connect(self.save)
		self.coffee_list.currentRowChanged.connect(self.select)

	def load(self):
		with sqlite3.connect('data/coffee.sqlite') as connection:
			self.res = connection.cursor().execute('SELECT * FROM coffee_info').fetchall()
			self.res = list(map(list, self.res))
			names = list(map(lambda x: x[1], self.res))
			self.coffee_list.clear()
			self.coffee_list.addItems(names)
			self.coffee_list.setCurrentRow(0)

	def save(self):
		curr_row = self.coffee_list.currentRow()
		id = self.id_edit.text()
		name = self.name_edit.text()
		degree = self.degree_edit.text()
		type = self.type_edit.text()
		desc = self.desc_edit.text()
		price = self.price_edit.text()
		volume = self.vol_edit.text()
		query = f'UPDATE coffee_info SET \
				  id = "{id}", \
				  name = "{name}", \
				  roast_degree = "{degree}", \
				  type = "{type}", \
				  description = "{desc}", \
				  price = "{price}", \
				  volume = "{volume}" \
				  WHERE \
				  id = "{self.res[curr_row][0]}"'
		db = Qt.QSqlDatabase().addDatabase('QSQLITE')
		db.setDatabaseName('data/coffee.sqlite')
		db.open()
		qry = Qt.QSqlQuery(db)
		qry.prepare(query)
		qry.exec()
		db.commit()
		db.close()
		self.close()

	def select(self, row):
		self.id_edit.setText(str(self.res[row][0]))
		self.name_edit.setText(str(self.res[row][1]))
		self.degree_edit.setText(str(self.res[row][2]))
		self.type_edit.setText(str(self.res[row][3]))
		self.desc_edit.setText(str(self.res[row][4]))
		self.price_edit.setText(str(self.res[row][5]))
		self.vol_edit.setText(str(self.res[row][6]))

def except_hook(cls, exception, traceback):
	sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	form = Main()
	form.show()
	sys.excepthook = except_hook
	sys.exit(app.exec())
