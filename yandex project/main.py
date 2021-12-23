import sqlite3
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import re
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5 import uic
import sys


class MyWidget(QMainWindow):
    def __init__(self):
        self.website_list = []
        self.w2 = ClssDialog()
        super().__init__()
        uic.loadUi('design/Qtdesign.ui', self)
        self.initUI()

    def initUI(self):
        self.Tabl()
        self.Tabl1()
        self.pushButton_2.clicked.connect(self.add_dome)
        self.pushButton_3.clicked.connect(self.from_dome)
        self.pushButton_4.clicked.connect(self.del_from_hosts)
        self.pushButton.clicked.connect(self.show_window_2)
        self.pushButton_5.clicked.connect(self.Tabl)


    def block_website(self):  # добавить домен в файл hosts
        host_path = "C:/Windows/System32/drivers/etc/hosts"  # путь к папке hosts не на диске C
        redirect = "127.0.0.1"
        file = open(host_path, "r+")
        content = file.read()
        if '127.0.0.1 localhost' in content:
            pass
        else:
            file.write("\n" + '127.0.0.1 localhost' + '\n')
            print('localhost')
        print(self.website_list)
        for website in self.website_list:
            print(1)
            if website in content:
                print(2)
                pass
            else:
                print(3)
                file.write("\n" + redirect + " " + str(website) + "\n")
        file.close()

    def add_dome(self):  # добавить в базу данных домены
        if len(self.lineEdit.text()) != 0:
            con = sqlite3.connect("dome.sqlite")
            cur = con.cursor()
            cur.execute("""INSERT INTO added(dome_name) VALUES(?)""", (self.lineEdit.text(),))
            self.lineEdit.setText('')

            msg = QMessageBox()
            msg.setText("Домен добавлен")
            msg.exec_()

            con.commit()
            con.close()
        else:
            msg2 = QMessageBox()
            msg2.setText("Вы не ввели домен")
            msg2.exec_()

    def from_dome(self):  # список сайтов. Просто занесение сайтов в список сразу после добавления в базу
        con = sqlite3.connect("dome.sqlite")
        cur = con.cursor()
        lisst = cur.execute("""SELECT dome_name FROM added""").fetchall()
        for i in lisst:
            self.website_list.append(*i)
        con.commit()
        con.close()
        self.block_website()

    def del_from_hosts(self):  # удаление сайта из файлф hosts
        if len(self.lineEdit_2.text()) != 0:
            with open('C:/Windows/System32/drivers/etc/hosts') as f:
                lines = f.readlines()
            str = self.lineEdit_2.text()  # ввод сайта который нужно удалить тоже изменить на ввод из qt
            pattern = re.compile(re.escape(str))
            with open('C:/Windows/System32/drivers/etc/hosts', 'w') as f:
                for line in lines:
                    result = pattern.search(line)
                    if result is None:
                        f.write(line)
            con = sqlite3.connect("dome.sqlite")
            cur = con.cursor()
            cur.execute("""INSERT INTO deleted(name) VALUES(?)""", (str,))
            cur.execute("""DELETE from added
                                where dome_name = ?""", (self.lineEdit_2.text(),))
            con.commit()
            con.close()

            self.lineEdit_2.setText('')
            msg1 = QMessageBox()
            msg1.setText("Домен разблокирован")
            msg1.exec_()

        else:
            msg2 = QMessageBox()
            msg2.setText("Вы не ввели домен")
            msg2.exec_()

    def show_window_2(self):  # открытие 2  окна
        self.w2.show()

    def Tabl(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        db.setDatabaseName('dome.sqlite')
        # И откроем подключение
        db.open()

        # QTableView - виджет для отображения данных из базы
        view = self.Zablock
        # Создадим объект QSqlTableModel,
        # зададим таблицу, с которой он будет работать,
        #  и выберем все данные
        model = QSqlTableModel(self, db)
        model.setTable('added')
        model.select()

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        view.setModel(model)
        self.Tabl1()
        
    def Tabl1(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        db.setDatabaseName('dome.sqlite')
        # И откроем подключение
        db.open()

        # QTableView - виджет для отображения данных из базы
        view = self.Unlock
        # Создадим объект QSqlTableModel,
        # зададим таблицу, с которой он будет работать,
        #  и выберем все данные
        model = QSqlTableModel(self, db)
        model.setTable('deleted')
        model.select()

        # Для отображения данных на виджете
        # свяжем его и нашу модель данных
        view.setModel(model)


class ClssDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design/untitled.ui', self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())