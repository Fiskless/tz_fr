import sys
import csv
import os
from dotenv import load_dotenv
import datetime

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, \
    QCheckBox, QDateEdit, QTabWidget, QWidget, QTableWidget, QHBoxLayout, \
    QTableWidgetItem, QApplication
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.Qt import Qt


import mariadb
from mariadb import IntegrityError


class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(500, 400)

        self.setWindowTitle('Телефонная книга')

        font = QFont('Times New Roman', 24, 75)
        self.main_text = QLabel(self)
        self.main_text.setText('Окно авторизации')
        self.main_text.move(100, 0)
        self.main_text.setFont(font)
        self.main_text.adjustSize()

        self.user_name = QLineEdit(self)
        self.user_name.setPlaceholderText('Имя пользователя')
        self.user_name.move(150, 80)
        self.user_name.resize(200, 30)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Пароль')
        self.password.setEchoMode(QLineEdit.Password)
        self.password.move(150, 130)
        self.password.resize(200, 30)

        self.incorrect_data = QLabel(self)
        self.incorrect_data.setText('Пользователь с такими данными не найден')
        self.incorrect_data.move(100, 180)
        self.incorrect_data.hide()

        self.log_in = QPushButton(self)
        self.log_in.move(10, 220)
        self.log_in.setFixedWidth(150)
        self.log_in.setFixedHeight(50)
        self.log_in.setText('Войти')
        self.log_in.setStyleSheet("QPushButton { background-color: green }")
        self.log_in.clicked.connect(self.evt_btn_log_in)

        self.registration = QPushButton(self)
        self.registration.move(175, 220)
        self.registration.setFixedWidth(150)
        self.registration.setFixedHeight(50)
        self.registration.setText('Регистрация')
        self.registration.clicked.connect(self.show_registration_window)
        self.registration.setStyleSheet(
            "QPushButton { background-color: gray }")

        self.cancel = QPushButton(self)
        self.cancel.move(340, 220)
        self.cancel.setFixedWidth(150)
        self.cancel.setFixedHeight(50)
        self.cancel.setText('Отмена')
        self.cancel.setStyleSheet("QPushButton { background-color: red }")
        self.cancel.clicked.connect(self.evt_btn_cancel)

        self.memory_about_user = QCheckBox('Запомнить меня', self)
        self.memory_about_user.move(120, 300)
        self.memory_about_user.toggled.connect(
            self.evt_memory_about_user_toggled)

        self.password_vision = QCheckBox('Показать пароль', self)
        self.password_vision.move(120, 320)
        self.password_vision.toggled.connect(self.evt_password_vision_toggled)

        self.password_recovery = ClickableLabel(self)
        self.password_recovery.setText('Забыли пароль?')
        self.password_recovery.setStyleSheet(
            "QLabel { color: blue; text-decoration: underline }")
        self.password_recovery.clicked.connect(
            self.evt_password_recovery_click)
        self.password_recovery.move(120, 360)

    def evt_password_recovery_click(self):
        self.password_recovery = DlgPasswordRecoveryWindow()
        self.password_recovery.show()

    def evt_btn_log_in(self):

        user_data = get_or_change_db_data(
            f"""(SELECT username, password FROM users 
            WHERE username='{self.user_name.text()}' 
            AND password='{self.password.text()}');""")

        if user_data.fetchall():
            self.contact_window = DlgContactWindow(self.user_name.text())
            self.contact_window.show()
            self.reminder_window = DlgReminderWindow()
            self.reminder_window.show()
            self.close()
        else:
            self.incorrect_data.show()

    def show_registration_window(self):
        self.registration_window = DlgRegistrationWindow()
        self.registration_window.show()

    def evt_btn_cancel(self):
        self.close()

    def evt_password_vision_toggled(self, is_checked):
        if is_checked:
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def evt_memory_about_user_toggled(self, is_checked):

        if is_checked:
            with open('login_data.csv', 'w') as f:
                file_writer = csv.writer(f)
                file_writer.writerow([self.user_name.text()])


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()
        QLabel.mousePressEvent(self, QMouseEvent)


class DlgRegistrationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(500, 400)

        self.setWindowTitle('Телефонная книга ')

        self.new_text = QLabel(self)
        font = QFont('Times New Roman', 24, 75)
        self.main_text = QLabel(self)
        self.main_text.setText('Регистрация')
        self.main_text.move(150, 0)
        self.main_text.setFont(font)
        self.main_text.adjustSize()

        self.user_name = QLineEdit(self)
        self.user_name.setPlaceholderText('Имя пользователя')
        self.user_name.move(150, 50)
        self.user_name.resize(200, 30)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Пароль')
        self.password.setEchoMode(QLineEdit.Password)
        self.password.move(150, 100)
        self.password.resize(200, 30)

        self.password_confirmation = QLineEdit(self)
        self.password_confirmation.setPlaceholderText('Повторите пароль')
        self.password_confirmation.setEchoMode(QLineEdit.Password)
        self.password_confirmation.move(150, 150)
        self.password_confirmation.resize(200, 30)

        self.birthday_date = QDateEdit(self)
        self.birthday_date.move(150, 200)
        self.birthday_date.resize(200, 30)
        self.birthday_date.setCalendarPopup(True)

        self.incorrect_data = QLabel(self)
        self.incorrect_data.setText('Пароли не совпадают')
        self.incorrect_data.move(150, 250)
        self.incorrect_data.hide()

        self.btn_ok = QPushButton(self)
        self.btn_ok.move(150, 300)
        self.btn_ok.setFixedWidth(90)
        self.btn_ok.setFixedHeight(50)
        self.btn_ok.setText('Ок')
        self.btn_ok.setStyleSheet("QPushButton { background-color: green }")
        self.btn_ok.clicked.connect(self.evt_btn_ok)

        self.cancel = QPushButton(self)
        self.cancel.move(260, 300)
        self.cancel.setFixedWidth(90)
        self.cancel.setFixedHeight(50)
        self.cancel.setText('Отмена')
        self.cancel.setStyleSheet("QPushButton { background-color: red }")
        self.cancel.clicked.connect(self.evt_btn_cancel)

        self.unique_username_fault = QLabel(self)
        self.unique_username_fault.setText(
            'Уже есть пользователь с таким именем. ВВедите другое.')
        self.unique_username_fault.move(50, 270)
        self.unique_username_fault.hide()

    def evt_btn_ok(self):
        try:
            if self.password.text() == self.password_confirmation.text():
                new_user = get_or_change_db_data(
                    f"""INSERT INTO users (username, password, birthday_date) 
                    VALUES ('{self.user_name.text()}', 
                            '{self.password.text()}', 
                            '{self.birthday_date.date().toPyDate()}')""")
                connect_db.commit()
                self.close()
            else:
                self.incorrect_data.show()
        except IntegrityError:
            self.unique_username_fault.show()

    def evt_btn_cancel(self):
        self.close()


class DlgPasswordRecoveryWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(500, 400)

        self.setWindowTitle('Телефонная книга ')

        self.new_text = QLabel(self)
        font = QFont('Times New Roman', 24, 75)
        self.main_text = QLabel(self)
        self.main_text.setText('Восстановление пароля')
        self.main_text.move(100, 0)
        self.main_text.setFont(font)
        self.main_text.adjustSize()

        self.user_name = QLineEdit(self)
        self.user_name.setPlaceholderText('Адрес электронной почты')
        self.user_name.move(150, 180)
        self.user_name.resize(200, 30)

        self.btn_ok = QPushButton(self)
        self.btn_ok.move(100, 240)
        self.btn_ok.setFixedWidth(140)
        self.btn_ok.setFixedHeight(50)
        self.btn_ok.setText('Сменить пароль')
        self.btn_ok.setStyleSheet("QPushButton { background-color: gray }")
        self.btn_ok.clicked.connect(self.evt_btn_ok)

        self.cancel = QPushButton(self)
        self.cancel.move(260, 240)
        self.cancel.setFixedWidth(140)
        self.cancel.setFixedHeight(50)
        self.cancel.setText('Отмена')
        self.cancel.setStyleSheet("QPushButton { background-color: red }")
        self.cancel.clicked.connect(self.evt_btn_cancel)

    def evt_btn_ok(self):
        self.close()

    def evt_btn_cancel(self):
        self.close()


class DlgContactWindow(QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle('Телефонная книжка')
        self.resize(800, 750)

        self.tabmain = QTabWidget()
        self.tabmain.setTabPosition(QTabWidget.West)
        self.setup_layout()
        self.update_table()

        font = QFont('Times New Roman', 14, 20)
        self.text = QLabel(self)
        self.text.setText(f'Вы зашли как:')
        self.text.move(440, 10)
        self.text.setAlignment(Qt.AlignRight)
        self.text.setFont(font)

        self.icon = QLabel(self)
        self.pixmap = QPixmap('pictures/icon.jpg')
        self.icon.setPixmap(self.pixmap)
        self.icon.move(400, 3)

        self.add_contact = QPushButton(self)
        self.add_contact.move(10, 5)
        self.add_contact.setFixedWidth(90)
        self.add_contact.setFixedHeight(30)
        self.add_contact.setText('Добавить')
        self.add_contact.setStyleSheet(
            "QPushButton { background-color: green }")
        self.add_contact.clicked.connect(self.evt_btn_add_contact)

        self.update_contact = QPushButton(self)
        self.update_contact.move(110, 5)
        self.update_contact.setFixedWidth(180)
        self.update_contact.setFixedHeight(30)
        self.update_contact.setText('Сохранить изменения')
        self.update_contact.setStyleSheet(
            "QPushButton { background-color: gray }")
        self.update_contact.clicked.connect(self.evt_btn_update_contact)

        self.delete_contact = QPushButton(self)
        self.delete_contact.move(300, 5)
        self.delete_contact.setFixedWidth(90)
        self.delete_contact.setFixedHeight(30)
        self.delete_contact.setText('Удалить')
        self.delete_contact.setStyleSheet(
            "QPushButton { background-color: red }")
        self.delete_contact.clicked.connect(self.evt_btn_delete_contact)

        self.log_out = QPushButton(self)
        self.log_out.move(690, 5)
        self.log_out.setFixedWidth(100)
        self.log_out.setFixedHeight(30)
        self.log_out.setText('Выйти')
        self.log_out.setStyleSheet(
            "QPushButton { background-color: white }")
        self.log_out.clicked.connect(self.evt_btn_log_out)

        self.user = QLabel(self)
        self.user.setFont(font)
        if os.path.exists('login_data.csv'):
            self.user.setText(f'{self.get_username_from_csv()}')
        else:
            self.user.setText(f'{username}')
        self.user.setStyleSheet(
            "QLabel { color: blue; text-decoration: underline }")
        self.user.move(560, 10)

    def get_username_from_csv(self):
        with open('login_data.csv', 'r') as f:
            file_reader = csv.reader(f)
            for name in file_reader:
                username = name[0]
        return username

    def evt_btn_log_out(self):
        self.close()
        self.logout = DlgMain()
        self.logout.show()
        if os.path.isfile('login_data.csv'):
            os.remove('login_data.csv')

    def evt_btn_add_contact(self):
        self.add_contact_to_pb = DlgAddContactToPhonebookWindow()
        self.add_contact_to_pb.show()
        self.close()


    def evt_btn_update_contact(self):
        current_row = self.table.currentRow()
        name = self.table.item(current_row, 0).text()
        phone = self.table.item(current_row, 1).text()
        birthday_date = datetime.datetime.strptime(
            self.table.item(current_row, 2).text(), '%d %B %Y').date()

        get_or_change_db_data(f"""UPDATE phone_book 
        SET name='{name}', phone='{phone}', birthday_date='{birthday_date}' 
        WHERE phone={value} """)
        connect_db.commit()

    def evt_btn_delete_contact(self):

        current_row = self.table.currentRow()
        name = self.table.item(current_row, 0).text()
        phone = self.table.item(current_row, 1).text()
        birthday_date = datetime.datetime.strptime(
            self.table.item(current_row, 2).text(), '%d %B %Y').date()
        self.table.removeRow(self.table.currentRow())

        get_or_change_db_data(f"""DELETE FROM phone_book 
        WHERE name='{name}' AND phone={phone} 
        AND birthday_date='{birthday_date}'""")
        connect_db.commit()

    def create_table(self, tab_name):
        self.widget = QWidget()
        self.tabmain.addTab(self.widget, tab_name)
        self.table = QTableWidget(self.widget)
        self.table.resize(780, 670)
        self.table.setRowCount(30)
        self.table.setColumnCount(3)
        self.table.horizontalHeader().setDefaultSectionSize(250)
        self.table.setHorizontalHeaderLabels(
            ["Имя", "Телефон", "Дата Рождения"])
        self.table.verticalHeader().hide()
        self.table.cellDoubleClicked.connect(self.doubleclick_table)

    def setup_layout(self):
        container = QWidget(self)
        container.move(0, 30)
        container.resize(800, 700)
        self.lytmain = QHBoxLayout(container)
        self.lytmain.addWidget(self.tabmain)

    def update_table(self):

        pages_list = ["АБВГ"]

        # pages_list = ['АБ', 'ВГ', 'ДЕ', 'ЖЗИЙ', 'КЛ', 'МН', 'ОП', 'РС',
        #                   'ТУ', 'ФХ', 'ЦЧШЦ', 'ЪЫЬЭ', 'ЮЯ']

        for character in pages_list:
            row_number_start_from = 0
            self.create_table(character)
            for letter in character:
                data_for_tables = get_or_change_db_data(
                        f""" SELECT name, phone, birthday_date
                        FROM phone_book WHERE name LIKE "{letter}%" """)
                rows = data_for_tables.fetchall()
                for row_number, row in enumerate(rows, start=row_number_start_from):
                    for column_number, column in enumerate(row):
                        if isinstance(column, datetime.date):
                            self.table.setItem(
                                row_number, column_number,
                                QTableWidgetItem(column.strftime('%d %B %Y')))
                        else:
                            self.table.setItem(row_number, column_number,
                                               QTableWidgetItem(str(column)))
                row_number_start_from = row_number_start_from+row_number+1
            self.table.sortItems(0, Qt.AscendingOrder)

    def doubleclick_table(self):
        current_row = self.table.currentRow()
        global value
        value = self.table.item(current_row, 1).text()


class DlgAddContactToPhonebookWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(500, 400)

        self.setWindowTitle('Телефонная книга ')

        self.new_text = QLabel(self)
        font = QFont('Times New Roman', 24, 75)
        self.main_text = QLabel(self)
        self.main_text.setText('Новый контакт')
        self.main_text.move(150, 0)
        self.main_text.setFont(font)
        self.main_text.adjustSize()

        self.user_name = QLineEdit(self)
        self.user_name.setPlaceholderText('Имя пользователя')
        self.user_name.move(150, 100)
        self.user_name.resize(200, 30)

        self.phone = QLineEdit(self)
        self.phone.setPlaceholderText('Телефон')
        self.phone.move(150, 150)
        self.phone.resize(200, 30)

        self.birthday_date = QDateEdit(self)
        self.birthday_date.move(150, 200)
        self.birthday_date.resize(200, 30)
        self.birthday_date.setCalendarPopup(True)

        self.btn_ok = QPushButton(self)
        self.btn_ok.move(150, 300)
        self.btn_ok.setFixedWidth(90)
        self.btn_ok.setFixedHeight(50)
        self.btn_ok.setText('Ок')
        self.btn_ok.setStyleSheet("QPushButton { background-color: green }")
        self.btn_ok.clicked.connect(self.evt_btn_ok)

        self.cancel = QPushButton(self)
        self.cancel.move(260, 300)
        self.cancel.setFixedWidth(90)
        self.cancel.setFixedHeight(50)
        self.cancel.setText('Отмена')
        self.cancel.setStyleSheet("QPushButton { background-color: red }")
        self.cancel.clicked.connect(self.evt_btn_cancel)

        self.unique_contact_fault = QLabel(self)
        self.unique_contact_fault.setText(
            'Уже есть пользователь с такими данными. Введите другие.')
        self.unique_contact_fault.move(50, 270)
        self.unique_contact_fault.hide()

    def evt_btn_ok(self):

        try:
            get_or_change_db_data(
                f"""INSERT INTO phone_book (name, phone, birthday_date) 
                VALUES ('{self.user_name.text()}', '{self.phone.text()}', 
                "{self.birthday_date.date().toPyDate()}")""")
            connect_db.commit()
            self.close()
            self.contact_window = DlgContactWindow('')
            self.contact_window.show()
        except IntegrityError:
            self.unique_contact_fault.show()

    def evt_btn_cancel(self):
        self.contact_window = DlgContactWindow('')
        self.contact_window.show()
        self.close()


class DlgReminderWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.resize(500, 400)

        self.setWindowTitle('Телефонная книга ')

        self.new_text = QLabel(self)
        self.main_text = QLabel(self)
        self.main_text.setText('В ближайшую неделю будет День Рождение у: ')
        self.main_text.move(0, 0)

        self.table = QTableWidget(self)
        self.table.move(0, 20)
        self.table.resize(490, 370)
        self.table.setRowCount(15)
        self.table.setColumnCount(3)
        self.table.horizontalHeader().setDefaultSectionSize(160)
        self.table.setHorizontalHeaderLabels(
            ["Имя", "Телефон", "Дата Рождения"])
        self.table.verticalHeader().hide()
        self.get_birthday_contact()

    def get_birthday_contact(self):
        data_for_remind = get_or_change_db_data(
            """SELECT name, phone, birthday_date FROM phone_book
             WHERE MOD(TIMESTAMPDIFF(DAY, birthday_date, CURDATE()), 365.25) 
             BETWEEN 358 AND 365""")
        rows = data_for_remind.fetchall()
        for row_number, row in enumerate(rows):
            for column_number, column in enumerate(row):
                if isinstance(column, datetime.date):
                    self.table.setItem(
                        row_number, column_number,
                        QTableWidgetItem(column.strftime('%d %B %Y')))
                else:
                    self.table.setItem(row_number, column_number,
                                       QTableWidgetItem(str(column)))


def get_or_change_db_data(query_to_db):

    cur = connect_db.cursor()
    cur.execute(query_to_db)
    return cur


def connect_to_db():
    return mariadb.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host="localhost",
        port=3306,
        database=os.getenv("DATABASE")
    )


if __name__ == '__main__':

    load_dotenv()

    connect_db = connect_to_db()

    app = QApplication(sys.argv)

    dlgMain = DlgMain()
    if os.path.exists('login_data.csv'):
        dlgMain = DlgContactWindow('')

    dlgMain.show()
    sys.exit(app.exec_())
