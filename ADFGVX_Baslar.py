# -*- coding: utf-8 -*-

"""
Created: 27.10.2021
Author: Jan Baslar
Python Version: 3.9.7
"""


# Matrix Class #
#--------------#
from typing import List
from random import randint


def newMatrix(lenght: int) -> List[List[str]]:
	"""
	Assistant function for creating empty matrix in class Matrix.
	"""
	matrix = []
	for i in range(lenght):
		line = ['' for i in range(lenght)]
		matrix.append(line)
	return matrix


class Matrix:
	"""
	Class for saving data about type of cipher, matrix state and remaining letters.
	"""
	def __init__(self, name: str, alphabet: str, length: int) -> None:
		self.name = name
		self.alphabet = alphabet
		self.matrix = newMatrix(length)
		self.remains = alphabet

	def empty(self) -> None:
		self.matrix = newMatrix(len(self.matrix))
		self.remains = self.alphabet

	def fill(self) -> None:
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[0])):
				if self.matrix[i][j] == '':
					index = randint(0, len(self.remains) - 1)
					self.matrix[i][j] = self.remains[index]
					self.remains = self.remains[:index] + self.remains[index + 1:]

	def find(self, letter: str) -> List[int]:
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[0])):
				if self.matrix[i][j] == letter:
					return [i, j]

	def change(self, letter: str, x: int, y: int) -> None:
		pos = self.find(letter)
		if pos != None:
			self.matrix[pos[0]][pos[1]] = ''

		self.matrix[x][y] = letter
		self.analyze()
		
	def analyze(self) -> None:
		self.remains = self.alphabet
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[0])):
				if self.matrix[i][j] != '':
					self.remains = self.remains.replace(self.matrix[i][j], '')


# Global Variables #
#------------------#
matrixENG = Matrix("ENG", "ABCDEFGHIJKLMNOPRSTUVWXYZ", 5)
matrixCZE = Matrix("CZE", "ABCDEFGHIJKLMNOPQRSTUVXYZ", 5)
matrixV = Matrix("V", "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 6)
matrix = matrixENG


# Changing Settings
def changeSettings(settings: str) -> None:
	"""
	Changes current matrix.
	"""
	global matrix
	if settings == "ENG":
		matrix = matrixENG
	elif settings == "CZE":
		matrix = matrixCZE
	elif settings == "V":
		matrix = matrixV


# Application Logic #
#-------------------#
def filterPunction(text: str) -> str:
	"""
	Removes punction from text.
	"""
	text = text.upper()
	punction = {'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Ě': 'E', 'Í': 'I', 'Ň': 'N', 
	'Ó': 'O', 'Ř':'R', 'Š': 'S','Ť': 'T', 'Ú': 'U', 'Ů': 'U', 'Ý': 'Y', 'Ž': 'Z'}

	for i in range(len(text)):
		if text[i] in punction:
			text = text.replace(text[i], punction[text[i]])

	return text


def replaceNumbers(text: str) -> str:
	"""
	Returns upper text without numbers.
	"""
	text = text.upper()

	text = text.replace('0', "XNULAX")
	text = text.replace('1', "XJEDNAX")
	text = text.replace('2', "XDVAX")
	text = text.replace('3', "XTRIX")
	text = text.replace('4', "XCTYRIX")
	text = text.replace('5', "XPETX")
	text = text.replace('6', "XSESTX")
	text = text.replace('7', "XSEDMX")
	text = text.replace('8', "XOSMX")
	text = text.replace('9', "XDEVETX")

	return text


def restoreNumbers(text: str) -> str:
    """
    Restores digits from special form to normal form.
    """
    text = text.replace("XNULAX", '0')
    text = text.replace("XJEDNAX", '1')
    text = text.replace("XDVAX", '2' )
    text = text.replace("XTRIX", '3')
    text = text.replace("XCTYRIX", '4')
    text = text.replace("XPETX", '5')
    text = text.replace("XSESTX", '6')
    text = text.replace("XSEDMX", '7')
    text = text.replace("XOSMX", '8')
    text = text.replace("XDEVETX", '9')

    return text


def filterInvalid(text: str, valid: str) -> str:
	"""
	Deletes all invalid symbols which are not in parametr valid.
	"""
	if text == '':
		return text
	text = text.upper()

	i = 0
	while i < len(text) - 1:
		if text[i] not in valid:
			text = text[ :i] + text[i + 1: ]
			i -= 1
		i += 1
	if text[-1] not in valid:
		text = text[ :-1]

	return text


def encrypt(text: str, key: str) -> str:
	"""
	Encrypts text and transposes it using key word. 
	"""
	line = "ADFGX"
	if matrix.name == 'V':
		line = "ADFGVX"

	enText = ''
	for i in range(len(text)):
		pos = matrix.find(text[i])
		enText += line[pos[0]] + line[pos[1]]

	transList = []
	for i in range(len(key)):
		index = ord(key[i]) - ord('A')
		transList.append([index, ''])

	for i in range(len(enText)):
		transList[i % len(transList)][1] += enText[i]

	transList.sort(key=lambda x: x[0])

	enText = ''
	for item in transList:
		if item[1] != '':
			enText += item[1] + ' '

	return enText[:-1]


def decrypt(text: str, key: str) -> str:
	"""
	Decrypts text and detransposes it using key word.
	"""
	superTransList = []
	for i in range(len(key)):
		index = ord(key[i]) - ord('A')
		superTransList.append([i, index, ''])
	
	superTransList.sort(key=lambda x: x[1])

	text += ' '
	column = ''
	i = 0
	j = 0
	while i < len(text) and j < len(superTransList):
		if text[i] != ' ':
			column += text[i]
		else:
			superTransList[j][2] = column
			column = ''
			j += 1
		i += 1

	superTransList.sort(key=lambda x: x[0])
	
	newText = ''
	length = len(superTransList)
	
	loops = len(text.replace(' ', ''))
	if loops < length:
		loops = length

	for i in range(loops):
		if i // length < len(superTransList[i % length][2]):
			newText += superTransList[i % length][2][i // length]

	if len(newText) % 2 == 1:
		newText = newText[:-1]

	line = "ADFGX"
	if matrix.name == 'V':
		line = "ADFGVX"

	deText = ''
	for i in range(0, len(newText), 2):
		p0 = line.index(newText[i])
		p1 = line.index(newText[i + 1])
		deText += matrix.matrix[p0][p1]

	return deText


# GUI #
#-----#
# Form implementation generated from reading ui file 'ui3.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1001, 751)
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		MainWindow.setFont(font)
		MainWindow.setStyleSheet("color: rgb(255, 255, 255)")
		MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.labelMain = QtWidgets.QLabel(self.centralwidget)
		self.labelMain.setGeometry(QtCore.QRect(0, 0, 1001, 751))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		self.labelMain.setFont(font)
		self.labelMain.setStyleSheet("background-color: rgba(65, 65, 95, 255);\n"
"padding-top: 3px;\n"
"padding-left: 10px;\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px")
		self.labelMain.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
		self.labelMain.setObjectName("labelMain")
		self.pushButtonX = QtWidgets.QPushButton(self.centralwidget)
		self.pushButtonX.setGeometry(QtCore.QRect(960, 10, 31, 31))
		font = QtGui.QFont()
		font.setFamily("Segoe UI Semibold")
		font.setPointSize(10)
		font.setBold(False)
		font.setWeight(50)
		self.pushButtonX.setFont(font)
		self.pushButtonX.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}")
		self.pushButtonX.setObjectName("pushButtonX")
		font = QtGui.QFont()
		font.setFamily("Segoe UI Semibold")
		font.setPointSize(14)
		font.setBold(False)
		font.setWeight(50)
		self.labelType = QtWidgets.QLabel(self.centralwidget)
		self.labelType.setGeometry(QtCore.QRect(20, 70, 91, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		self.labelType.setFont(font)
		self.labelType.setObjectName("labelType")
		self.labelLang = QtWidgets.QLabel(self.centralwidget)
		self.labelLang.setGeometry(QtCore.QRect(20, 120, 71, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		self.labelLang.setFont(font)
		self.labelLang.setObjectName("labelLang")
		self.labelKey = QtWidgets.QLabel(self.centralwidget)
		self.labelKey.setGeometry(QtCore.QRect(20, 170, 131, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		self.labelKey.setFont(font)
		self.labelKey.setObjectName("labelKey")
		self.pushButtonADFGX = QtWidgets.QPushButton(self.centralwidget)
		self.pushButtonADFGX.setGeometry(QtCore.QRect(110, 70, 91, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		font.setBold(False)
		font.setWeight(50)
		self.pushButtonADFGX.setFont(font)
		self.pushButtonADFGX.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border: 2px solid;\n"
"border-color: rgb(227, 184, 27);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}")
		self.pushButtonADFGX.setObjectName("pushButtonADFGX")
		self.pushButtonADFGVX = QtWidgets.QPushButton(self.centralwidget)
		self.pushButtonADFGVX.setGeometry(QtCore.QRect(210, 70, 101, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		font.setBold(False)
		font.setWeight(50)
		self.pushButtonADFGVX.setFont(font)
		self.pushButtonADFGVX.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}")
		self.pushButtonADFGVX.setObjectName("pushButtonADFGVX")
		self.pushButtonENG = QtWidgets.QPushButton(self.centralwidget)
		self.pushButtonENG.setGeometry(QtCore.QRect(90, 120, 61, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		font.setBold(False)
		font.setWeight(50)
		self.pushButtonENG.setFont(font)
		self.pushButtonENG.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border: 2px solid;\n"
"border-color: rgb(227, 184, 27);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}")
		self.pushButtonENG.setObjectName("pushButtonENG")
		self.pushButtonCZE = QtWidgets.QPushButton(self.centralwidget)
		self.pushButtonCZE.setGeometry(QtCore.QRect(160, 120, 61, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		font.setBold(False)
		font.setWeight(50)
		self.pushButtonCZE.setFont(font)
		self.pushButtonCZE.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}")
		self.pushButtonCZE.setObjectName("pushButtonCZE")
		self.textEditKey = QtWidgets.QTextEdit(self.centralwidget)
		self.textEditKey.setEnabled(True)
		self.textEditKey.setGeometry(QtCore.QRect(150, 170, 161, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEditKey.setFont(font)
		self.textEditKey.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px")
		self.textEditKey.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEditKey.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEditKey.setObjectName("textEditKey")
		self.labelKeyMarks = QtWidgets.QLabel(self.centralwidget)
		self.labelKeyMarks.setGeometry(QtCore.QRect(20, 250, 151, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		self.labelKeyMarks.setFont(font)
		self.labelKeyMarks.setObjectName("labelKeyMarks")
		self.labelKeyRemainings = QtWidgets.QLabel(self.centralwidget)
		self.labelKeyRemainings.setGeometry(QtCore.QRect(20, 280, 421, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		self.labelKeyRemainings.setFont(font)
		self.labelKeyRemainings.setObjectName("labelKeyRemainings")
		self.labelKeyFrame2 = QtWidgets.QLabel(self.centralwidget)
		self.labelKeyFrame2.setGeometry(QtCore.QRect(20, 330, 351, 341))
		self.labelKeyFrame2.setVisible(False)
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelKeyFrame2.setFont(font)
		self.labelKeyFrame2.setStyleSheet("border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px")
		self.labelKeyFrame2.setText("")
		self.labelKeyFrame2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
		self.labelKeyFrame2.setObjectName("labelKeyFrame2")
		self.labelAr = QtWidgets.QLabel(self.centralwidget)
		self.labelAr.setGeometry(QtCore.QRect(70, 330, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelAr.setFont(font)
		self.labelAr.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelAr.setAlignment(QtCore.Qt.AlignCenter)
		self.labelAr.setObjectName("labelAr")
		self.labelVorXr = QtWidgets.QLabel(self.centralwidget)
		self.labelVorXr.setGeometry(QtCore.QRect(270, 330, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelVorXr.setFont(font)
		self.labelVorXr.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelVorXr.setAlignment(QtCore.Qt.AlignCenter)
		self.labelVorXr.setObjectName("labelVorXr")
		self.labelGr = QtWidgets.QLabel(self.centralwidget)
		self.labelGr.setGeometry(QtCore.QRect(220, 330, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelGr.setFont(font)
		self.labelGr.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelGr.setAlignment(QtCore.Qt.AlignCenter)
		self.labelGr.setObjectName("labelGr")
		self.labelFr = QtWidgets.QLabel(self.centralwidget)
		self.labelFr.setGeometry(QtCore.QRect(170, 330, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelFr.setFont(font)
		self.labelFr.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelFr.setAlignment(QtCore.Qt.AlignCenter)
		self.labelFr.setObjectName("labelFr")
		self.labelDr = QtWidgets.QLabel(self.centralwidget)
		self.labelDr.setGeometry(QtCore.QRect(120, 330, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelDr.setFont(font)
		self.labelDr.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelDr.setAlignment(QtCore.Qt.AlignCenter)
		self.labelDr.setObjectName("labelDr")
		self.labelKeyFrame1 = QtWidgets.QLabel(self.centralwidget)
		self.labelKeyFrame1.setGeometry(QtCore.QRect(20, 330, 301, 291))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelKeyFrame1.setFont(font)
		self.labelKeyFrame1.setStyleSheet("border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px")
		self.labelKeyFrame1.setText("")
		self.labelKeyFrame1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
		self.labelKeyFrame1.setObjectName("labelKeyFrame1")
		self.labelXr = QtWidgets.QLabel(self.centralwidget)
		self.labelXr.setGeometry(QtCore.QRect(320, 330, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelXr.setFont(font)
		self.labelXr.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelXr.setAlignment(QtCore.Qt.AlignCenter)
		self.labelXr.setObjectName("labelXr")
		self.labelXr.setVisible(False)
		self.labelAc = QtWidgets.QLabel(self.centralwidget)
		self.labelAc.setGeometry(QtCore.QRect(30, 370, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelAc.setFont(font)
		self.labelAc.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelAc.setAlignment(QtCore.Qt.AlignCenter)
		self.labelAc.setObjectName("labelAc")
		self.labelDc = QtWidgets.QLabel(self.centralwidget)
		self.labelDc.setGeometry(QtCore.QRect(30, 420, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelDc.setFont(font)
		self.labelDc.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelDc.setAlignment(QtCore.Qt.AlignCenter)
		self.labelDc.setObjectName("labelDc")
		self.textEdit10 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit10.setEnabled(True)
		self.textEdit10.setGeometry(QtCore.QRect(70, 420, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit00 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit00.setEnabled(True)
		self.textEdit00.setGeometry(QtCore.QRect(70, 370, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit00.setFont(font)
		self.textEdit00.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit00.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit00.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit00.setObjectName("textEdit00")
		self.textEdit10.setFont(font)
		self.textEdit10.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit10.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit10.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit10.setObjectName("textEdit10")
		self.labelFc = QtWidgets.QLabel(self.centralwidget)
		self.labelFc.setGeometry(QtCore.QRect(30, 470, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelFc.setFont(font)
		self.labelFc.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelFc.setAlignment(QtCore.Qt.AlignCenter)
		self.labelFc.setObjectName("labelFc")
		self.labelGc = QtWidgets.QLabel(self.centralwidget)
		self.labelGc.setGeometry(QtCore.QRect(30, 520, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelGc.setFont(font)
		self.labelGc.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelGc.setAlignment(QtCore.Qt.AlignCenter)
		self.labelGc.setObjectName("labelGc")
		self.labelVorXc = QtWidgets.QLabel(self.centralwidget)
		self.labelVorXc.setGeometry(QtCore.QRect(30, 570, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelVorXc.setFont(font)
		self.labelVorXc.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelVorXc.setAlignment(QtCore.Qt.AlignCenter)
		self.labelVorXc.setObjectName("labelVorXc")
		self.labelXc = QtWidgets.QLabel(self.centralwidget)
		self.labelXc.setGeometry(QtCore.QRect(30, 620, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.labelXc.setFont(font)
		self.labelXc.setStyleSheet("color: rgb(227, 184, 27)")
		self.labelXc.setAlignment(QtCore.Qt.AlignCenter)
		self.labelXc.setObjectName("labelXc")
		self.labelXc.setVisible(False)
		self.textEdit01 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit01.setEnabled(True)
		self.textEdit01.setGeometry(QtCore.QRect(120, 370, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit01.setFont(font)
		self.textEdit01.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit01.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit01.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit01.setObjectName("textEdit01")
		self.textEdit02 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit02.setEnabled(True)
		self.textEdit02.setGeometry(QtCore.QRect(170, 370, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit02.setFont(font)
		self.textEdit02.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit02.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit02.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit02.setObjectName("textEdit02")
		self.textEdit03 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit03.setEnabled(True)
		self.textEdit03.setGeometry(QtCore.QRect(220, 370, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit03.setFont(font)
		self.textEdit03.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit03.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit03.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit03.setObjectName("textEdit03")
		self.textEdit04 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit04.setEnabled(True)
		self.textEdit04.setGeometry(QtCore.QRect(270, 370, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit04.setFont(font)
		self.textEdit04.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit04.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit04.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit04.setObjectName("textEdit04")
		self.textEdit05 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit05.setEnabled(True)
		self.textEdit05.setGeometry(QtCore.QRect(320, 370, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit05.setFont(font)
		self.textEdit05.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit05.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit05.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit05.setObjectName("textEdit05")
		self.textEdit05.setVisible(False)
		self.textEdit11 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit11.setEnabled(True)
		self.textEdit11.setGeometry(QtCore.QRect(120, 420, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit11.setFont(font)
		self.textEdit11.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit11.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit11.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit11.setObjectName("textEdit11")
		self.textEdit12 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit12.setEnabled(True)
		self.textEdit12.setGeometry(QtCore.QRect(170, 420, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit12.setFont(font)
		self.textEdit12.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit12.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit12.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit12.setObjectName("textEdit12")
		self.textEdit13 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit13.setEnabled(True)
		self.textEdit13.setGeometry(QtCore.QRect(220, 420, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit13.setFont(font)
		self.textEdit13.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit13.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit13.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit13.setObjectName("textEdit13")
		self.textEdit14 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit14.setEnabled(True)
		self.textEdit14.setGeometry(QtCore.QRect(270, 420, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit14.setFont(font)
		self.textEdit14.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit14.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit14.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit14.setObjectName("textEdit14")
		self.textEdit15 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit15.setEnabled(True)
		self.textEdit15.setGeometry(QtCore.QRect(320, 420, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit15.setFont(font)
		self.textEdit15.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit15.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit15.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit15.setObjectName("textEdit15")
		self.textEdit15.setVisible(False)
		self.textEdit20 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit20.setEnabled(True)
		self.textEdit20.setGeometry(QtCore.QRect(70, 470, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit20.setFont(font)
		self.textEdit20.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit20.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit20.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit20.setObjectName("textEdit20")
		self.textEdit21 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit21.setEnabled(True)
		self.textEdit21.setGeometry(QtCore.QRect(120, 470, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit21.setFont(font)
		self.textEdit21.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit21.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit21.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit21.setObjectName("textEdit21")
		self.textEdit22 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit22.setEnabled(True)
		self.textEdit22.setGeometry(QtCore.QRect(170, 470, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit22.setFont(font)
		self.textEdit22.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit22.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit22.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit22.setObjectName("textEdit22")
		self.textEdit23 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit23.setEnabled(True)
		self.textEdit23.setGeometry(QtCore.QRect(220, 470, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit23.setFont(font)
		self.textEdit23.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit23.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit23.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit23.setObjectName("textEdit23")
		self.textEdit24 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit24.setEnabled(True)
		self.textEdit24.setGeometry(QtCore.QRect(270, 470, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit24.setFont(font)
		self.textEdit24.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit24.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit24.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit24.setObjectName("textEdit24")
		self.textEdit25 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit25.setEnabled(True)
		self.textEdit25.setGeometry(QtCore.QRect(320, 470, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit25.setFont(font)
		self.textEdit25.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit25.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit25.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit25.setObjectName("textEdit25")
		self.textEdit25.setVisible(False)
		self.textEdit30 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit30.setEnabled(True)
		self.textEdit30.setGeometry(QtCore.QRect(70, 520, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit30.setFont(font)
		self.textEdit30.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit30.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit30.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit30.setObjectName("textEdit30")
		self.textEdit31 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit31.setEnabled(True)
		self.textEdit31.setGeometry(QtCore.QRect(120, 520, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit31.setFont(font)
		self.textEdit31.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit31.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit31.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit31.setObjectName("textEdit31")
		self.textEdit32 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit32.setEnabled(True)
		self.textEdit32.setGeometry(QtCore.QRect(170, 520, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit32.setFont(font)
		self.textEdit32.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit32.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit32.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit32.setObjectName("textEdit32")
		self.textEdit33 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit33.setEnabled(True)
		self.textEdit33.setGeometry(QtCore.QRect(220, 520, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit33.setFont(font)
		self.textEdit33.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit33.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit33.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit33.setObjectName("textEdit33")
		self.textEdit34 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit34.setEnabled(True)
		self.textEdit34.setGeometry(QtCore.QRect(270, 520, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit34.setFont(font)
		self.textEdit34.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit34.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit34.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit34.setObjectName("textEdit34")
		self.textEdit35 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit35.setEnabled(True)
		self.textEdit35.setGeometry(QtCore.QRect(320, 520, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit35.setFont(font)
		self.textEdit35.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit35.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit35.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit35.setObjectName("textEdit35")
		self.textEdit35.setVisible(False)
		self.textEdit40 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit40.setEnabled(True)
		self.textEdit40.setGeometry(QtCore.QRect(70, 570, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit40.setFont(font)
		self.textEdit40.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit40.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit40.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit40.setObjectName("textEdit40")
		self.textEdit41 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit41.setEnabled(True)
		self.textEdit41.setGeometry(QtCore.QRect(120, 570, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit41.setFont(font)
		self.textEdit41.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit41.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit41.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit41.setObjectName("textEdit41")
		self.textEdit42 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit42.setEnabled(True)
		self.textEdit42.setGeometry(QtCore.QRect(170, 570, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit42.setFont(font)
		self.textEdit42.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit42.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit42.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit42.setObjectName("textEdit42")
		self.textEdit43 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit43.setEnabled(True)
		self.textEdit43.setGeometry(QtCore.QRect(220, 570, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit43.setFont(font)
		self.textEdit43.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit43.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit43.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit43.setObjectName("textEdit43")
		self.textEdit44 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit44.setEnabled(True)
		self.textEdit44.setGeometry(QtCore.QRect(270, 570, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit44.setFont(font)
		self.textEdit44.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit44.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit44.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit44.setObjectName("textEdit44")
		self.textEdit45 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit45.setEnabled(True)
		self.textEdit45.setGeometry(QtCore.QRect(320, 570, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit45.setFont(font)
		self.textEdit45.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit45.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit45.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit45.setObjectName("textEdit45")
		self.textEdit45.setVisible(False)
		self.textEdit50 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit50.setEnabled(True)
		self.textEdit50.setGeometry(QtCore.QRect(70, 620, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit50.setFont(font)
		self.textEdit50.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit50.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit50.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit50.setObjectName("textEdit50")
		self.textEdit50.setVisible(False)
		self.textEdit51 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit51.setEnabled(True)
		self.textEdit51.setGeometry(QtCore.QRect(120, 620, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit51.setFont(font)
		self.textEdit51.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit51.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit51.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit51.setObjectName("textEdit51")
		self.textEdit51.setVisible(False)
		self.textEdit52 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit52.setEnabled(True)
		self.textEdit52.setGeometry(QtCore.QRect(170, 620, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit52.setFont(font)
		self.textEdit52.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit52.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit52.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit52.setObjectName("textEdit52")
		self.textEdit52.setVisible(False)
		self.textEdit53 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit53.setEnabled(True)
		self.textEdit53.setGeometry(QtCore.QRect(220, 620, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit53.setFont(font)
		self.textEdit53.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit53.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit53.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit53.setObjectName("textEdit53")
		self.textEdit53.setVisible(False)
		self.textEdit54 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit54.setEnabled(True)
		self.textEdit54.setGeometry(QtCore.QRect(270, 620, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit54.setFont(font)
		self.textEdit54.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit54.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit54.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit54.setObjectName("textEdit54")
		self.textEdit54.setVisible(False)
		self.textEdit55 = QtWidgets.QTextEdit(self.centralwidget)
		self.textEdit55.setEnabled(True)
		self.textEdit55.setGeometry(QtCore.QRect(320, 620, 31, 41))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEdit55.setFont(font)
		self.textEdit55.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border-radius: 10px")
		self.textEdit55.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit55.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEdit55.setObjectName("textEdit55")
		self.textEdit55.setVisible(False)
		self.pushButtonFill = QtWidgets.QPushButton(self.centralwidget)
		self.pushButtonFill.setGeometry(QtCore.QRect(20, 690, 161, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		font.setBold(False)
		font.setWeight(50)
		self.pushButtonFill.setFont(font)
		self.pushButtonFill.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}")
		self.pushButtonFill.setObjectName("pushButtonFill")
		self.pushButtonEmpty = QtWidgets.QPushButton(self.centralwidget)
		self.pushButtonEmpty.setGeometry(QtCore.QRect(200, 690, 171, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		font.setBold(False)
		font.setWeight(50)
		self.pushButtonEmpty.setFont(font)
		self.pushButtonEmpty.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}")
		self.pushButtonEmpty.setObjectName("pushButtonEmpty")
		self.textEditOT = QtWidgets.QTextEdit(self.centralwidget)
		self.textEditOT.setEnabled(True)
		self.textEditOT.setGeometry(QtCore.QRect(460, 110, 521, 241))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEditOT.setFont(font)
		self.textEditOT.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px")
		self.textEditOT.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEditOT.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEditOT.setObjectName("textEditOT")
		self.labelOT = QtWidgets.QLabel(self.centralwidget)
		self.labelOT.setGeometry(QtCore.QRect(460, 70, 281, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		self.labelOT.setFont(font)
		self.labelOT.setObjectName("labelOT")
		self.labelST = QtWidgets.QLabel(self.centralwidget)
		self.labelST.setGeometry(QtCore.QRect(460, 380, 281, 41))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(14)
		self.labelST.setFont(font)
		self.labelST.setObjectName("labelST")
		self.textEditST = QtWidgets.QTextEdit(self.centralwidget)
		self.textEditST.setEnabled(True)
		self.textEditST.setGeometry(QtCore.QRect(460, 420, 521, 241))
		font = QtGui.QFont()
		font.setFamily("Consolas")
		font.setPointSize(14)
		self.textEditST.setFont(font)
		self.textEditST.setStyleSheet("background-color: rgb(50, 50, 70);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px")
		self.textEditST.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEditST.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.textEditST.setObjectName("textEditST")
		self.pushButtonEncrypt = QtWidgets.QPushButton(self.centralwidget)
		self.pushButtonEncrypt.setGeometry(QtCore.QRect(460, 680, 251, 51))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(16)
		font.setBold(False)
		font.setWeight(50)
		self.pushButtonEncrypt.setFont(font)
		self.pushButtonEncrypt.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}")
		self.pushButtonEncrypt.setObjectName("pushButtonEncrypt")
		self.pushButtonDecrypt = QtWidgets.QPushButton(self.centralwidget)
		self.pushButtonDecrypt.setGeometry(QtCore.QRect(730, 680, 251, 51))
		font = QtGui.QFont()
		font.setFamily("Bahnschrift")
		font.setPointSize(16)
		font.setBold(False)
		font.setWeight(50)
		self.pushButtonDecrypt.setFont(font)
		self.pushButtonDecrypt.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}")
		self.pushButtonDecrypt.setObjectName("pushButtonDecrypt")
		
		MainWindow.setCentralWidget(self.centralwidget)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		# Binding #
		#---------#
		self.pushButtonX.clicked.connect(QtCore.QCoreApplication.instance().quit)
		self.pushButtonADFGX.clicked.connect(self.toADFGX)
		self.pushButtonADFGVX.clicked.connect(self.toADFGVX)
		self.pushButtonENG.clicked.connect(self.toENG)
		self.pushButtonCZE.clicked.connect(self.toCZE)
		self.pushButtonFill.clicked.connect(self.fill)
		self.pushButtonEmpty.clicked.connect(self.empty)
		self.pushButtonEncrypt.clicked.connect(self.encryptGUI)
		self.pushButtonDecrypt.clicked.connect(self.decryptGUI)

		table = [[self.textEdit00, self.textEdit01, self.textEdit02, self.textEdit03, self.textEdit04, self.textEdit05],
				[self.textEdit10, self.textEdit11, self.textEdit12, self.textEdit13, self.textEdit14, self.textEdit15],
				[self.textEdit20, self.textEdit21, self.textEdit22, self.textEdit23, self.textEdit24, self.textEdit25],
				[self.textEdit30, self.textEdit31, self.textEdit32, self.textEdit33, self.textEdit34, self.textEdit35],
				[self.textEdit40, self.textEdit41, self.textEdit42, self.textEdit43, self.textEdit44, self.textEdit45],
				[self.textEdit50, self.textEdit51, self.textEdit52, self.textEdit53, self.textEdit54, self.textEdit55]]

		for line in table:
			for cell in line:
				cell.textChanged.connect(self.changeMatrix)

	buttonNormal = ["QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}"]

	buttonSelected = ["QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border: 2px solid;\n"
"border-color: rgb(227, 184, 27);\n"
"border-radius: 10px}\n"
"\n"
"QPushButton:hover{\n"
"color: rgb(227, 184, 27);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border-color: rgb(227, 184, 27);}\n"
"\n"
"QPushButton:pressed{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(227, 184, 27);\n"
"border-color: rgb(227, 184, 27)}"]


	# GUI Functions #
	#---------------#
	def toADFGX(self) -> None:
		self.pushButtonADFGX.setStyleSheet(self.buttonSelected[0])
		self.pushButtonADFGVX.setStyleSheet(self.buttonNormal[0])

		self.labelLang.setVisible(True)
		self.pushButtonENG.setVisible(True)
		self.pushButtonCZE.setVisible(True)

		self.labelKeyFrame1.setVisible(True)
		self.labelKeyFrame2.setVisible(False)

		self.labelVorXr.setText('X')
		self.labelVorXc.setText('X')

		self.labelXr.setVisible(False)
		self.labelXc.setVisible(False)

		self.textEdit05.setVisible(False)
		self.textEdit15.setVisible(False)
		self.textEdit25.setVisible(False)
		self.textEdit35.setVisible(False)
		self.textEdit45.setVisible(False)
		self.textEdit50.setVisible(False)
		self.textEdit51.setVisible(False)
		self.textEdit52.setVisible(False)
		self.textEdit53.setVisible(False)
		self.textEdit54.setVisible(False)
		self.textEdit55.setVisible(False)

		self.toENG()


	def toADFGVX(self) -> None:
		self.pushButtonADFGVX.setStyleSheet(self.buttonSelected[0])
		self.pushButtonADFGX.setStyleSheet(self.buttonNormal[0])

		self.labelLang.setVisible(False)
		self.pushButtonENG.setVisible(False)
		self.pushButtonCZE.setVisible(False)

		self.labelKeyFrame1.setVisible(False)
		self.labelKeyFrame2.setVisible(True)

		self.labelVorXr.setText('V')
		self.labelVorXc.setText('V')

		self.labelXr.setVisible(True)
		self.labelXc.setVisible(True)

		self.textEdit05.setVisible(True)
		self.textEdit15.setVisible(True)
		self.textEdit25.setVisible(True)
		self.textEdit35.setVisible(True)
		self.textEdit45.setVisible(True)
		self.textEdit50.setVisible(True)
		self.textEdit51.setVisible(True)
		self.textEdit52.setVisible(True)
		self.textEdit53.setVisible(True)
		self.textEdit54.setVisible(True)
		self.textEdit55.setVisible(True)

		changeSettings("V")
		self.updateMatrix()


	def toENG(self) -> None:
		self.pushButtonENG.setStyleSheet(self.buttonSelected[0])
		self.pushButtonCZE.setStyleSheet(self.buttonNormal[0])

		changeSettings("ENG")
		self.updateMatrix()


	def toCZE(self) -> None:
		self.pushButtonCZE.setStyleSheet(self.buttonSelected[0])
		self.pushButtonENG.setStyleSheet(self.buttonNormal[0])

		changeSettings("CZE")
		self.updateMatrix()


	def fill(self) -> None:
		matrix.fill()
		self.labelKeyRemainings.setText(matrix.remains)

		self.updateMatrix()


	def empty(self) -> None:
		matrix.empty()
		self.labelKeyRemainings.setText(matrix.remains)

		self.updateMatrix()


	def encryptGUI(self) -> None:
		self.fill()

		key = self.textEditKey.toPlainText()
		alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		key = filterInvalid(filterPunction(key), alphabet)
		self.textEditKey.setText(key)
		if key == '': key = 'A'

		text = self.textEditOT.toPlainText()
		text = filterPunction(text)
		if matrix.name != 'V': 
			text = replaceNumbers(text)
		text = filterInvalid(text.replace(' ', "XMEZERAX"), matrix.alphabet)

		self.textEditST.setText(encrypt(text, key))


	def decryptGUI(self) -> None:
		self.fill()

		key = self.textEditKey.toPlainText()
		alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		key = filterInvalid(filterPunction(key), alphabet)
		self.textEditKey.setText(key)
		if key == '': key = 'A'

		text = self.textEditST.toPlainText()
		valid = 'ADFGX '
		if matrix.name == 'V':
			valid = 'ADFGVX '
		text = filterInvalid(filterPunction(text), valid)
		self.textEditST.setText(text)

		deText = decrypt(text, key)
		if matrix.name != 'V': 
			deText = restoreNumbers(deText)
		deText = deText.replace("XMEZERAX", ' ')

		self.textEditOT.setText(deText)


	def updateMatrix(self) -> None:
		table = [[self.textEdit00, self.textEdit01, self.textEdit02, self.textEdit03, self.textEdit04, self.textEdit05],
			[self.textEdit10, self.textEdit11, self.textEdit12, self.textEdit13, self.textEdit14, self.textEdit15],
			[self.textEdit20, self.textEdit21, self.textEdit22, self.textEdit23, self.textEdit24, self.textEdit25],
			[self.textEdit30, self.textEdit31, self.textEdit32, self.textEdit33, self.textEdit34, self.textEdit35],
			[self.textEdit40, self.textEdit41, self.textEdit42, self.textEdit43, self.textEdit44, self.textEdit45],
			[self.textEdit50, self.textEdit51, self.textEdit52, self.textEdit53, self.textEdit54, self.textEdit55]]
		
		for i in range(len(matrix.matrix)):
			for j in range(len(matrix.matrix[0])):
				if table[i][j].toPlainText() != matrix.matrix[i][j]:
					table[i][j].blockSignals(True)
					table[i][j].setText(matrix.matrix[i][j])
					table[i][j].setAlignment(QtCore.Qt.AlignCenter)
					table[i][j].blockSignals(False)

			self.labelKeyRemainings.setText(matrix.remains)

	
	def changeMatrix(self) -> None:
		table = [[self.textEdit00, self.textEdit01, self.textEdit02, self.textEdit03, self.textEdit04, self.textEdit05],
			[self.textEdit10, self.textEdit11, self.textEdit12, self.textEdit13, self.textEdit14, self.textEdit15],
			[self.textEdit20, self.textEdit21, self.textEdit22, self.textEdit23, self.textEdit24, self.textEdit25],
			[self.textEdit30, self.textEdit31, self.textEdit32, self.textEdit33, self.textEdit34, self.textEdit35],
			[self.textEdit40, self.textEdit41, self.textEdit42, self.textEdit43, self.textEdit44, self.textEdit45],
			[self.textEdit50, self.textEdit51, self.textEdit52, self.textEdit53, self.textEdit54, self.textEdit55]]

		lenght = 5
		if matrix.name == 'V':
			lenght = 6

		for i in range(lenght):
			for j in range(lenght):
				letter = table[i][j].toPlainText()
				if letter != matrix.matrix[i][j]:
					if letter != '':
						letter = filterInvalid(filterPunction(letter[0]), matrix.alphabet)
					matrix.change(letter, i, j)
					self.updateMatrix()
					return


	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.labelMain.setText(_translate("MainWindow", "ADFG(V)X"))
		self.pushButtonX.setText(_translate("MainWindow", "X"))
		self.labelType.setText(_translate("MainWindow", "Typ Šifry:"))
		self.labelLang.setText(_translate("MainWindow", "Jazyk:"))
		self.labelKey.setText(_translate("MainWindow", "Klíčové slovo:"))
		self.pushButtonADFGX.setText(_translate("MainWindow", "ADFGX"))
		self.pushButtonADFGVX.setText(_translate("MainWindow", "ADFGVX"))
		self.pushButtonENG.setText(_translate("MainWindow", "ENG"))
		self.pushButtonCZE.setText(_translate("MainWindow", "CZE"))
		self.textEditKey.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">MARK</p></body></html>"))
		self.labelKeyMarks.setText(_translate("MainWindow", "Zbývající znaky:"))
		self.labelKeyRemainings.setText(_translate("MainWindow", "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"))
		self.textEdit00.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.labelAr.setText(_translate("MainWindow", "A"))
		self.labelVorXr.setText(_translate("MainWindow", "X"))
		self.labelGr.setText(_translate("MainWindow", "G"))
		self.labelFr.setText(_translate("MainWindow", "F"))
		self.labelDr.setText(_translate("MainWindow", "D"))
		self.labelXr.setText(_translate("MainWindow", "X"))
		self.labelAc.setText(_translate("MainWindow", "A"))
		self.labelDc.setText(_translate("MainWindow", "D"))
		self.textEdit10.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.labelFc.setText(_translate("MainWindow", "F"))
		self.labelGc.setText(_translate("MainWindow", "G"))
		self.labelVorXc.setText(_translate("MainWindow", "X"))
		self.labelXc.setText(_translate("MainWindow", "X"))
		self.textEdit01.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit02.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit03.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit04.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit05.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit11.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit12.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit13.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit14.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit15.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit20.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit21.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit22.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit23.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit24.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit25.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit30.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit31.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit32.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit33.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit34.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit35.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit40.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit41.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit42.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit43.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit44.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit45.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit50.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit51.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit52.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit53.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit54.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.textEdit55.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.pushButtonFill.setText(_translate("MainWindow", "Doplnit matici"))
		self.pushButtonEmpty.setText(_translate("MainWindow", "Vymazat matici"))
		self.textEditOT.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.labelOT.setText(_translate("MainWindow", "Otevřený text:"))
		self.labelST.setText(_translate("MainWindow", "Šifrovaný text:"))
		self.textEditST.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Consolas\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.pushButtonEncrypt.setText(_translate("MainWindow", "ZAŠIFROVAT"))
		self.pushButtonDecrypt.setText(_translate("MainWindow", "DEŠIFROVAT"))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
