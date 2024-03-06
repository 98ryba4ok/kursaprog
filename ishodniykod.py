import sqlite3
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QHeaderView, QCheckBox

db = sqlite3.connect("onboarding.db")

class SurveyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Обратная связь')
        self.setGeometry(300, 300, 400, 200)

        self.main_label = QLabel('Если у вас возникли вопросы или появились проблемы, обязательно заполните форму!')
        self.main_label.setStyleSheet("font-family: Arial; font-size: 12pt;")

        self.open_survey_button = QPushButton('Вопросы')
        self.open_survey_button.setStyleSheet("font-family: Arial; font-size: 12pt;")
        self.open_survey_button.clicked.connect(self.show_survey)

        self.new_survey_button = QPushButton('Проблемы')
        self.new_survey_button.setStyleSheet("font-family: Arial; font-size: 12pt;")
        self.new_survey_button.clicked.connect(self.show_new_survey)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.main_label)
        main_layout.addWidget(self.open_survey_button)
        main_layout.addWidget(self.new_survey_button)
        self.setLayout(main_layout)

        self.name_label_survey = QLabel('Ваше ФИО:')
        self.name_label_survey.setStyleSheet("font-family: Arial; font-size: 12pt;")
        self.name_edit_survey = QLineEdit()

        self.question_label_survey = QLabel('Ваш вопрос:')
        self.question_label_survey.setStyleSheet("font-family: Arial; font-size: 12pt;")
        self.question_edit_survey = QLineEdit()

        self.submit_button_survey = QPushButton('Отправить')
        self.submit_button_survey.setStyleSheet("font-family: Arial; font-size: 12pt;")
        self.submit_button_survey.clicked.connect(self.show_survey_results)

        survey_layout = QVBoxLayout()
        survey_layout.addWidget(self.name_label_survey)
        survey_layout.addWidget(self.name_edit_survey)
        survey_layout.addWidget(self.question_label_survey)
        survey_layout.addWidget(self.question_edit_survey)
        survey_layout.addWidget(self.submit_button_survey)

        self.survey_widget = QWidget()
        self.survey_widget.setLayout(survey_layout)
        self.survey_widget.hide()

        self.name_label_new_survey = QLabel('Ваше ФИО:')
        self.name_label_new_survey.setStyleSheet("font-family: Arial; font-size: 12pt;")
        self.name_edit_new_survey = QLineEdit()

        self.checkbox1 = QCheckBox('Проблемы с начальством')
        self.checkbox2 = QCheckBox('Проблемы с коллегами')
        self.checkbox3 = QCheckBox('Нужна психологическая помощь')
        self.checkbox4 = QCheckBox('Другое')

        self.submit_button_mental = QPushButton('Отправить')
        self.submit_button_mental.setStyleSheet("font-family: Arial; font-size: 12pt;")
        self.submit_button_mental.clicked.connect(self.show_mental_results)

        new_survey_layout = QVBoxLayout()
        new_survey_layout.addWidget(self.name_label_new_survey)
        new_survey_layout.addWidget(self.name_edit_new_survey)
        new_survey_layout.addWidget(self.checkbox1)
        new_survey_layout.addWidget(self.checkbox2)
        new_survey_layout.addWidget(self.checkbox3)
        new_survey_layout.addWidget(self.checkbox4)
        new_survey_layout.addWidget(self.submit_button_mental)

        self.new_survey_widget = QWidget()
        self.new_survey_widget.setLayout(new_survey_layout)
        self.new_survey_widget.hide()

    def show_survey(self):
        self.survey_widget.show()

    def show_survey_results(self):
        name = self.name_edit_survey.text()
        question = self.question_edit_survey.text()

        try:
            with sqlite3.connect("onboarding.db") as db:
                cursor = db.cursor()
                cursor.execute("INSERT INTO questions (Full_name, question) VALUES (?, ?)", (name, question))
                db.commit()
        except Exception as e:
            print(f"Ошибка при записи опросных данных в базу данных: {e}")

        self.name_edit_survey.clear()
        self.question_edit_survey.clear()

        self.survey_widget.hide()

    def show_new_survey(self):
        self.new_survey_widget.show()

    def show_mental_results(self):
        name = self.name_edit_new_survey.text()

        problem1 = 1 if self.checkbox1.isChecked() else 0
        problem2 = 1 if self.checkbox2.isChecked() else 0
        problem3 = 1 if self.checkbox3.isChecked() else 0
        other_issue = 1 if self.checkbox4.isChecked() else 0

        try:
            with sqlite3.connect("onboarding.db") as db:
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO Issues (Full_name, problem1, problem2, problem3, other_issue) VALUES (?, ?, ?, ?, ?)",
                    (name, problem1, problem2, problem3, other_issue)
                )
                db.commit()
        except Exception as e:
            print(f"Ошибка при записи данных о проблемах в базу данных: {e}")

        self.name_edit_new_survey.clear()
        self.checkbox1.setChecked(False)
        self.checkbox2.setChecked(False)
        self.checkbox3.setChecked(False)
        self.checkbox4.setChecked(False)

        self.new_survey_widget.hide()

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Введите данные')
        layout = QFormLayout(self)
        self.line_edit1 = QLineEdit(self)  # поле для ввода названия материала
        self.line_edit2 = QLineEdit(self)  # поле для ввода ссылки
        layout.addRow('Введите название материала:', self.line_edit1)
        layout.addRow('Введите ссылку:', self.line_edit2)  # добавление поля для ввода ссылки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)


class Materials(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(['Материал', 'Ссылка'])  # измененное название колонок

        self.populateTable()

        layout.addWidget(self.table)

        button_open_dialog = QPushButton('Добавить материалы', self)
        button_open_dialog.setStyleSheet("background-color: #1E90FF; color: white; padding: 10px; font-family: Arial; font-size: 12pt; border: none; border-radius: 5px;")
        button_open_dialog.clicked.connect(self.showInputDialog)
        layout.addWidget(button_open_dialog)
        self.populateTable()

    def showInputDialog(self):
        dialog = InputDialog(self)
        result = dialog.exec_()

        if result == QDialog.Accepted:
            text1 = dialog.line_edit1.text()
            text2 = dialog.line_edit2.text()

            try:
                with sqlite3.connect("onboarding.db") as db:
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO materials (name, link) VALUES (?, ?)", (text1, text2))
                    db.commit()
            except Exception as e:
                print(f"Ошибка при записи материала в базу данных: {e}")

            self.populateTable()

    def populateTable(self):
        try:
            self.table.clear()
            self.table.setRowCount(0)

            with sqlite3.connect("onboarding.db") as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM materials")
                materials = cursor.fetchall()

                for material in materials:
                    text1 = material[1]
                    text2 = material[2]

                    rowPosition = self.table.rowCount()
                    self.table.insertRow(rowPosition)
                    self.table.setItem(rowPosition, 0, QTableWidgetItem(text1))
                    self.table.setItem(rowPosition, 1, QTableWidgetItem(text2))
        except Exception as e:
            print(f"Ошибка при чтении материалов из базы данных: {e}")

class TabbedProgram(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Сервис онбординга и адаптации сотрудников')
        self.setGeometry(200, 300, 1500, 800)
        tab_widget = QTabWidget(self)
        tab_widget.setGeometry(50, 50, 1340, 700)

        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()
        tab5 = QWidget()

        tab_widget.addTab(tab1, 'Главная страница')
        tab_widget.addTab(tab2, 'Материалы')
        tab_widget.addTab(tab3, 'Инструкции')
        tab_widget.addTab(tab4, 'О компании')
        tab_widget.addTab(tab5, 'Обратная связь')

        tab_widget.setStyleSheet("QTabBar::tab { font-family: Arial; font-size: 14pt; width: 240px; height: 30px;}")
        tab_style = """
                    QTabBar::tab {
                        font-family: Arial; 
                        font-size: 14pt; 
                        width: 200px; 
                        height: 30px; 
                        background-color: 	#6495ED;
                        color: white;
                        border: 1px #1E90FF;
                        border-radius: 8px;
                        margin-right: 10px;
                    }
                    QTabBar::tab:selected {
                        background-color: #1E90FF;
                    
                    }
                    border-color: #1E90FF;
                """
        tab_widget.setStyleSheet(tab_style)

        layout1 = QVBoxLayout()
        label1 = QLabel('Добро пожаловать в наше приложение по онбордингу и адаптации сотрудников! Мы создали это приложение, чтобы помочь вашим новым сотрудникам быстро вливаться в коллектив и ощущать себя комфортно. Наше приложение предлагает удобный гайд по основным процессам и правилам компании, интерактивные курсы по корпоративной культуре, а также возможность задавать вопросы и получать поддержку от опытных сотрудников. Давайте сделаем процесс адаптации вашего персонала максимально эффективным и приятным!')
        label1.setWordWrap(True)
        label1.setAlignment(QtCore.Qt.AlignCenter)
        label1.setAlignment(QtCore.Qt.AlignTop)
        label1.setStyleSheet("font-family: Arial; font-size: 12pt; padding: 20px 100px; border: 2px solid #87CEEB;")
        layout1.addWidget(label1)
        tab1.setLayout(layout1)

        layout2 = QVBoxLayout()
        label2 = QLabel(f'Материалы')
        label2.setAlignment(QtCore.Qt.AlignTop)
        layout2.addWidget(label2)
        label2.setStyleSheet("font-family: Arial; font-size: 12pt;")

        window_with_form = Materials()
        layout2.addWidget(window_with_form)

        tab2.setLayout(layout2)

        layout3 = QVBoxLayout()
        label3 = QLabel('1. Главная страница \n Тут вы найдете описание нашего приложения \n 2. Материалы \n Тут вы сможете найти ссылки на обучающие ресурсы. Также есть возможность добавить свои \n 3. Инструкции \n В этой вкладке вы найдете описание навигации и информацию о пользовании приложением \n 4. О компании \n Тут вы сможете найти адреса офисов и филиалов компании. Немного её истории и описания функций выполняемых этой компанией. \n 5. Обратная связь \n В этой вкладке вы можете найти контактные данные и отправить интересующий вас вопрос. \n')
        label3.setWordWrap(True)
        label3.setAlignment(QtCore.Qt.AlignTop)
        label3.setStyleSheet("font-family: Arial; font-size: 12pt; padding: 20px 100px;")
        layout3.addWidget(label3)
        tab3.setLayout(layout3)

        layout4 = QVBoxLayout()
        label4 = QLabel('Наша компания - это организация, специализирующаяся на предоставлении услуг в области управления человеческими ресурсами. Она помогает компаниям найти, привлечь и удерживать талантливых сотрудников, обеспечивая эффективное управление персоналом и развитие бизнеса. \n\n Наши Услуги включают в себя подбор персонала, оценку и развитие сотрудников, консультирование по вопросам управления персоналом, а также разработку и внедрение HR-стратегий и политик. \n\n Наша организация также занимается анализом и улучшением рабочей среды, созданием программ мотивации и стимулирования сотрудников, а также обучением персонала для повышения профессиональных навыков и компетенций.')
        label4.setWordWrap(True)
        label4.setAlignment(QtCore.Qt.AlignTop)
        label4.setStyleSheet("font-family: Arial; font-size: 12pt; padding: 20px 100px;")
        layout4.addWidget(label4)
        tab4.setLayout(layout4)

        layout5 = QVBoxLayout()
        label5 = QLabel("Контакты наших офисов:\n\nОфис в Москве\nНомер телефона: 777-777-777-777\nПочта: moscow@ofice.com\nОфис в Санкт-Питербурге\nНомер телефона: 777-777-777-777\nПочта: piter@ofice.com\nОфис в Оренбурге\nНомер телефона: 777-777-777-777\nПочта: oren@ofice.com")
        label5.setStyleSheet("font-family: Arial; font-size: 12pt; padding: 20px 100px;")
        label5.setWordWrap(True)
        label5.setAlignment(QtCore.Qt.AlignTop)
        survey_app = SurveyApp()
        layout5.addWidget(label5)
        layout5.addWidget(survey_app)
        tab5.setLayout(layout5)

        self.show()
        try:
            with sqlite3.connect("onboarding.db") as db:
                cursor = db.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  Full_name TEXT,
                                  question TEXT)''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS Issues (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  Full_name TEXT,
                                  problem1 INTEGER,
                                  problem2 INTEGER,
                                  problem3 INTEGER,
                                  other_issue INTEGER)''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS materials (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  name TEXT,
                                  link TEXT)''')

        except Exception as e:
            print(f"Ошибка при создании таблиц в базе данных: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = TabbedProgram()
    sys.exit(app.exec_())

db.close()