#!/usr/bin/env python3.5

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import unicodedata
import os.path

header_web = " \\newpage \n \
\\subsubsection{%s \\nobreak\\smallskip\\protect\\includegraphics[width=7pt]{%s-small}}\n \
\\rowcolors{1}{headerblue}{white}\n \
\\begin{table}[H]\n \
\\begin{tabular}{cl}\n \
\\footnotesize{\\textbf{Závažnost:}} & \\footnotesize{\\textbf{OWASP kategorie:}} \\\\ \n \
\\includegraphics[height=12pt]{%s-big} & \\footnotesize{OTG-XXX-000 - Testing for something...}\n \
\\end{tabular}\n \
\\end{table}\n\n\n "


header_infra =" \\newpage \n \
\\subsubsection{%s \\nobreak\\smallskip\\protect\\includegraphics[width=7pt]{%s-small}}\n \
\\rowcolors{1}{headerblue}{white}\n \
\\begin{table}[H]\n \
\\begin{tabular}{cl}\n \
\\footnotesize{\\textbf{Závažnost:}} & \\footnotesize{\\textbf{Ovlivněné systémy:}} \\\\ \n \
\\includegraphics[height=12pt]{%s-big} & \\footnotesize{\n \
\\parbox[c][][c]{8cm}{\n \
\\begin{itemize}[noitemsep]\n \
\\item IP - num\_port/tcp.udp\n \
\\item IP - num\_port/tcp.udp\n \
\\item IP - num\_port/tcp.udp\n \
\\end{itemize}}\n \
}\n \
\\end{tabular}\n \
\\end{table}\n\n\n \
"


nalez_hdr = "\n\n \\paragraph{Nález} \\ \n \
\n \
\\noindent\\rule[1.5ex]{150pt}{3pt} \n \
\n \
"

riziko_hdr = "\n\n \\paragraph{Riziko} \\ \n \
\n \
\\noindent\\rule[1.5ex]{150pt}{3pt} \n \
\n \
"

doporuceni_hdr = "\n\n \\paragraph{Doporučení} \\ \n \
\n \
\\noindent\\rule[1.5ex]{150pt}{3pt} \n \
\n \
"

# def neco():
# 	print("neco")

class win(QWidget):
	def __init__(self, type):
		super().__init__()
		self.initUI(type)



	def initUI(self, type):
		self.type = type

		mainLayout = QVBoxLayout()
		self.setLayout(mainLayout)
		self.setWindowTitle('New issue')

		radioButtonLayout = QHBoxLayout()

		self.criticalRadioButton = QRadioButton("critical")
		self.criticalRadioButton.setText("critical")
		radioButtonLayout.addWidget(self.criticalRadioButton)

		self.highRadioButton = QRadioButton("high")
		self.highRadioButton.setText("high")
		radioButtonLayout.addWidget(self.highRadioButton)

		self.mediumRadioButton = QRadioButton("medium")
		self.mediumRadioButton.setText("medium")
		radioButtonLayout.addWidget(self.mediumRadioButton)

		self.lowRadioButton = QRadioButton("low")
		self.lowRadioButton.setText("low")
		radioButtonLayout.addWidget(self.lowRadioButton)

		self.infoRadioButton = QRadioButton("info")
		self.infoRadioButton.setText("info")
		radioButtonLayout.addWidget(self.infoRadioButton)

		mainLayout.addLayout(radioButtonLayout)




		nameLayout = QHBoxLayout()
		nameLabel = QLabel("Name:")
		nameLayout.addWidget(nameLabel)
		self.nameLineEdit = QLineEdit()
		nameLayout.addWidget(self.nameLineEdit)
		mainLayout.addLayout(nameLayout)


		textLayout = QHBoxLayout()
		textLabel = QLabel("Text:")
		textLayout.addWidget(textLabel)
		self.textTextEdit = QTextEdit()
		textLayout.addWidget(self.textTextEdit)
		mainLayout.addLayout(textLayout)


		riskLayout = QHBoxLayout()
		riskLabel = QLabel("Risk:")
		riskLayout.addWidget(riskLabel)
		self.riskTextEdit = QTextEdit()
		riskLayout.addWidget(self.riskTextEdit)
		mainLayout.addLayout(riskLayout)

		recomLayout = QHBoxLayout()
		recomLabel = QLabel("Reco:")
		recomLayout.addWidget(recomLabel)
		self.recomTextEdit = QTextEdit()
		recomLayout.addWidget(self.recomTextEdit)
		mainLayout.addLayout(recomLayout)


		btnLayout = QHBoxLayout()
		mainLayout.addLayout(btnLayout)
		
		saveBtn = QPushButton("Save")
		saveBtn.clicked.connect(self.saveIssue)
		btnLayout.addWidget(saveBtn)

		clearBtn = QPushButton("Clear")
		clearBtn.clicked.connect(self.clearForm)
		btnLayout.addWidget(clearBtn)

		closeBtn = QPushButton("Close")
		closeBtn.clicked.connect(self.close)
		btnLayout.addWidget(closeBtn)



		self.show()


	def saveIssue(self):
		#print("called saveIssue()")
		name = self.nameLineEdit.text()

		if self.criticalRadioButton.isChecked():
			severity = "critical"
		elif self.highRadioButton.isChecked():
			severity = "high"
		elif self.mediumRadioButton.isChecked():
			severity = "medium"
		elif self.lowRadioButton.isChecked():
			severity = "low"
		elif self.infoRadioButton.isChecked():
			severity = "info"
		else:
			msgBox = QMessageBox()
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText("Chybejici severity")
			msgBox.setStandardButtons(QMessageBox.Cancel)
			msgBox.exec_()
			return

		text = self.textTextEdit.toPlainText()
		risk = self.riskTextEdit.toPlainText()
		recom = self.recomTextEdit.toPlainText()
		
		
		if (self.type == "web"):
			writeIssueWeb(name, severity, text, risk, recom)

		else:
			writeIssueInfra(name, severity, text, risk, recom)



	def clearForm(self):
		pass



def getFileName(name):
	tmp = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
	tmp = tmp.decode('ascii')
	tmp = tmp.replace(" ", "-")
	tmp = tmp.lower()
	return tmp


def writeIssueInfra(name, severity, text, risk, recom):
	path = "./orig/issues-infra.orig/"

	tmpFile = getFileName(name)
	f = os.path.join(path, tmpFile+".tex")


	if os.path.exists(f):
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Soubor jiz existuje")
		msgBox.setStandardButtons(QMessageBox.Cancel)
		msgBox.exec_()
		return


	f = open(f, 'w')


	f.write(header_infra % (name, severity, severity))
	
	f.write(nalez_hdr)
	f.write(text)

	f.write(riziko_hdr)
	f.write(risk)

	f.write(doporuceni_hdr)
	f.write(recom)

	f.write("\n\n")

	f.close()


def writeIssueWeb(name, severity, text, risk, recom):
	path = "./orig/issues-web.orig/"

	tmpFile = getFileName(name)
	f = os.path.join(path, tmpFile+".tex")


	if os.path.exists(f):
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText("Soubor jiz existuje")
		msgBox.setStandardButtons(QMessageBox.Cancel)
		msgBox.exec_()
		return

	#print("writing to %s" % f)

	f = open(f, 'w')


	f.write(header_web % (name, severity, severity))
	
	f.write(nalez_hdr)
	f.write(text)

	f.write(riziko_hdr)
	f.write(risk)

	f.write(doporuceni_hdr)
	f.write(recom)

	f.write("\n\n")

	f.close()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = win()
	sys.exit(app.exec_())


