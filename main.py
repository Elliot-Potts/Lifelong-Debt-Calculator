# -*- coding: utf-8 -*-

"""
Joke application to check maintenance loan income for students on the following criteria:
    - 2020/21 course start
    - UK student full-time
    - £9,250 tuition fees
    - Living without parents outside of London
    - No extra courses/support

Written by Elliot Potts
(https://elliotpotts.net/)
"""


from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import ctypes
import sys
import re


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(350, 283)
        MainWindow.setMinimumSize(QtCore.QSize(350, 283))
        MainWindow.setMaximumSize(QtCore.QSize(350, 283))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtTitle = QtWidgets.QLabel(self.centralwidget)
        self.txtTitle.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.txtTitle.setObjectName("txtTitle")
        self.verticalLayout.addWidget(self.txtTitle)
        self.incomeEntry = QtWidgets.QLineEdit(self.centralwidget)
        self.incomeEntry.setInputMask("")
        self.incomeEntry.setAlignment(QtCore.Qt.AlignCenter)
        self.incomeEntry.setObjectName("incomeEntry")
        self.verticalLayout.addWidget(self.incomeEntry)
        spacerItem = QtWidgets.QSpacerItem(3, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.btnCalculate = QtWidgets.QPushButton(self.centralwidget)
        self.btnCalculate.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btnCalculate.setObjectName("btnCalculate")
        self.verticalLayout.addWidget(self.btnCalculate)
        spacerItem1 = QtWidgets.QSpacerItem(3, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.txtCalculationAmount = QtWidgets.QLabel(self.centralwidget)
        self.txtCalculationAmount.setObjectName("txtCalculationAmount")
        self.verticalLayout.addWidget(self.txtCalculationAmount)
        spacerItem2 = QtWidgets.QSpacerItem(3, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtYearsAtUni = QtWidgets.QLabel(self.centralwidget)
        self.txtYearsAtUni.setObjectName("txtYearsAtUni")
        self.horizontalLayout.addWidget(self.txtYearsAtUni)
        self.yearEntry = QtWidgets.QSpinBox(self.centralwidget)
        self.yearEntry.setObjectName("yearEntry")
        self.horizontalLayout.addWidget(self.yearEntry)
        self.btnDebtCalculator = QtWidgets.QPushButton(self.centralwidget)
        self.btnDebtCalculator.setObjectName("btnDebtCalculator")
        self.horizontalLayout.addWidget(self.btnDebtCalculator)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(3, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.txtDebtCalculation = QtWidgets.QLabel(self.centralwidget)
        self.txtDebtCalculation.setObjectName("txtDebtCalculation")
        self.verticalLayout.addWidget(self.txtDebtCalculation)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "by Elliot Potts"))
        self.txtTitle.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">How much money me get?<br/></span><span style=\" font-size:12pt;\">Enter your household income below.</span></p></body></html>"))
        self.incomeEntry.setPlaceholderText(_translate("MainWindow", "Enter your household income"))
        self.btnCalculate.setText(_translate("MainWindow", "Calculate"))
        self.txtCalculationAmount.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">You could receieve <span style=\" font-weight:600;\">X AMOUNT </span>in maintenance loans<br/>to be fully repaid until you\'re 105 years old!</p></body></html>"))
        self.txtYearsAtUni.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Years at University:</span></p></body></html>"))
        self.btnDebtCalculator.setText(_translate("MainWindow", "Calculate debt!"))
        self.txtDebtCalculation.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Our generous government will only require<br/>you to repay <span style=\" font-weight:600;\">X AMOUNT </span>for your<br/><span style=\" font-weight:600;\">Y YEARS </span>of study...<br/><span style=\" font-size:6pt;\">assuming £9.2K tuition*</span></p></body></html>"))


class AppLogic(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self.main_url = "https://www.gov.uk/student-finance-calculator/y/2020-2021/uk-full-time/9250.0/away-outside-london/{}.0/no/none-of-the-above"

        self.btnCalculate.setFocus()

        self.txtCalculationAmount.setVisible(False)
        self.txtDebtCalculation.setVisible(False)

        self.btnCalculate.clicked.connect(self.maintenance_calculation)
        self.btnDebtCalculator.clicked.connect(self.debt_calculation)

    def reset_calculate_button(self):
        self.btnCalculate.setText("Calculate")
        self.btnDebtCalculator.setText("Calculate debt!")

    def set_maintenance_loan_text(self, number):
        self.txtCalculationAmount.setText("<html><head/><body><p align=\"center\">You could receieve <span style=\" font-weight:600;\">£{} </span>in maintenance loans<br/>to be fully repaid until you\'re 105 years old!</p></body></html>".format(str(number)))

    def set_debt_calc_text(self, debt_amount, year_amount):
        self.txtDebtCalculation.setText("<html><head/><body><p align=\"center\">Our generous government will only require<br/>you to repay <span style=\" font-weight:600;\">£{} </span>for your<br/><span style=\" font-weight:600;\">{} years </span>of study...<br/><span style=\" font-size:6pt;\">assuming £9.2K tuition*</span></p></body></html>".format(str(debt_amount), str(year_amount)))

    def get_maintenance_loan(self, income_field):
        pass

    def maintenance_calculation(self):
        get_income_field = re.sub('[^0-9]', '', self.incomeEntry.text())

        if len(get_income_field) == 0:
            print(" [-] Calculation on nothing...")
            self.btnCalculate.setText("Enter a valid number then click again.")
        else:
            self.reset_calculate_button()
            print(" [+] Making request to {}.".format(self.main_url.format(get_income_field)))

    def debt_calculation(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AppLogic()
    ui.show()
    sys.exit(app.exec_())

