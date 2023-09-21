#
# Milan Bartos <milan@bartos.se>
# (C) 2018
#
import sys
import re
import os
import os.path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import shutil
import random
import string
import create

import xml.etree.ElementTree as ET
import os


import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class issuePool ():
    """
    Contains all issues of type oneIssue
    """
    def __init__(self, poolLocation):
        self.pool = {}
        self.readAllFromDir(poolLocation)

    def readAllFromDir(self, dir):
        for item in os.listdir(dir):
            #logger.info("reading issue "+item)
            itemId = item[:-4]
            newIssue = oneIssue(itemId)
            newIssue.readFromFile(os.path.join(dir, item), "cz")
            self.pool[itemId] = newIssue

    def getIssue(self, _id):
        return self.pool[_id]



class oneIssue ():
    """
    Contains one particular issue and it's functionality.

    - supports writing it out as Latex issue
    - possible to extend to support more formats
    """
    def __init__(self, _id):
        self._id = _id

    def readFromFile(self, filename, lang):
        logger.debug("reading "+filename+" "+lang)
        
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        self.lang = lang

        self.name = self.root.findall("name/"+self.lang)[0].text
        self.category = self.root.findall("category")[0].text
        self.risk = self.root.findall("risk")[0].text
        self.likelihood = self.root.findall("likelihood")[0].text
        self.impact = self.root.findall("impact")[0].text
        self.references = self.root.findall("references")[0].text
        self.tfinding = self.root.findall("tfinding/"+self.lang)[0].text
        self.trisk = self.root.findall("trisk/"+self.lang)[0].text
        self.trecommendation = self.root.findall("trecommendation/"+self.lang)[0].text
        self.tsteps = self.root.findall("tsteps/"+self.lang)[0].text
        self.whocanexploit = self.root.findall("whocanexploit")[0].text


    def getWebLatex(self):
        if self.lang == "cz":
            return self.getWebLatexCZ()


# XXX tady by slo jeste, aby 'tsteps' bylo splitnuty podle newlines (nebo napriklad '#')
# a na zaklade toho by kazda newline byl dalsi bod postupu
    def getWebLatexCZ(self):
        logger.debug("running "+self.name)
        return """
\\newpage
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%
%%%%%%%%%     FINDING
%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\\subsubsection{"""+self.name+""" \\nobreak\\smallskip\\protect\\includegraphics[width=7pt]{"""+self.risk+"""small}}
\\rowcolors{1}{headerblue}{white}
\\begin{table}[H]
\\begin{tabular}{cl}
\\footnotesize{\\textbf{Závažnost:}} \\\\
\\includegraphics[height=12pt]{"""+self.risk+"""big}
\\end{tabular}
\\end{table}

\\paragraph{Nález} \\

\\noindent\\rule[1.5ex]{150pt}{3pt}

"""+self.tfinding+"""

\\paragraph{Postup exploitace / ověření zranitelnosti} \\

\\noindent\\rule[1.5ex]{150pt}{3pt}

\\begin{enumerate}[noitemsep]
\\item XXX
\\end{enumerate}

"""+self.tsteps+"""

\\paragraph{Riziko} \\

\\noindent\\rule[1.5ex]{150pt}{3pt}

"""+self.trisk+"""

\\paragraph{Doporučení} \\

\\noindent\\rule[1.5ex]{150pt}{3pt}

"""+self.trecommendation+"""

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        """



class report():
    """
    This class should actually contain whole report in the form that is
    independent of everything else like format etc.
    """
    def __init__(self):

        self.projectname = ""
        self.customer = ""
        self.target = ""
        self.authorcompany = "APPSEC s.r.o."
        self.lang = "cz"

        self.type = "" # web / infra / webscan / infrascan

        self.ip = issuePool("./issues/")
        self.issues = []

    def addIssue(self, issueId):
        self.issues.append(self.ip.getIssue(issueId))

    def setProjectName(self, projectname):
        self.projectname = projectname

    def setCustomer(self, customer):
        self.customer = customer

    def setTarget(self, target):
        self.target = target

    def setType(self, type):
        self.type = type

    def getLatex(self):
        ret = """This is a report with following issues:
        """
        for item in self.issues:
            ret += item.getWebLatex()+"\n"

        return ret









class issueXml():
    """
        Contains xml representation of issue. We can afford
        to use [0] there as we assume all issue xml files are
        well formed
    """
    def __init__(self, f, lang):
        self.tree = ET.parse(f)
        self.root = self.tree.getroot()
        self.lang = lang

    def getName(self):
        return self.root.findall("name/"+self.lang)[0].text

    def getCategory(self):
        return self.root.findall("category")[0].text

    def getRisk(self):
        return self.root.findall("risk")[0].text

    def getLikelihood(self):
        return self.root.findall("likelihood")[0].text

    def getImpact(self):
        return self.root.findall("impact")[0].text

    def getReferences(self):
        return self.root.findall("references")[0].text

    def getTfinding(self):
        return self.root.findall("tfinding/"+self.lang)[0].text

    def getTrisk(self):
        return self.root.findall("trisk/"+self.lang)[0].text

    def getTrecommendation(self):
        return self.root.findall("trecommendation/"+self.lang)[0].text

    def getTsteps(self):
        return self.root.findall("tsteps/"+self.lang)[0].text

    def getWhocanexploit(self):
        return self.root.findall("whocanexploit")[0].text



class Config(object):
    issuesLocation = "issues"
    target = None
    lang = "cz"
    company = None

    allissues = {}



def writeConfigFile():

    company = ""
    logobig = ""
    logo = ""

    if Config.company == "appsec":
        company = "APPSEC s.r.o."
        logobig = "logobig-appsec"
        logo = "logo-appsec"
        autor = "Milan Bartoš <milan@appsec.cz>"
    elif Config.company == "defendio":
        company = "DEFENDIO s.r.o."
        logobig = "logobig-defendio"
        logo = "logo-defendio"
        autor = "Milan Bartoš <milan@defendio.net>"


    print("writeConfigFile start")
    text = "\\newcommand{\\ip}{"+Config.target+"}\n \
\\newcommand{\\projectname}{"+Config.project+" \\ip}\n \
\\newcommand{\\spolecnost}{Example Company}\n \
\\newcommand{\\autor}{"+autor+"}\n \
\\newcommand{\\defendio}{"+company+"}\n \
\\newcommand{\\logo}{"+logo+"}\n \
\\newcommand{\\logobig}{"+logobig+"}\n"

    f = open("inc/config.tex", 'w')
    f.write(text)
    f.close()

    print("writeConfigFile end")




class myQCheckBox(QCheckBox):
    """
        Vytvoreni vlastniho QCheckBoxu, aby obsahoval nektere potrebne informace
    """
    def __init__(self, n, w):
        super().__init__(n, w)

    def initUI(self):
        super().initUI()

        self.severity = ""
        self.url = ""


def usage():
    print("usage: python3.5 sablona.py -c config_file -t report_type target appsec/defendio")


def createLabel(text, colour):
    """
        Vytvori label pro jednotlive sloupce s nalezama
        text a colour definuji text na labelu a barvu pozadi
    """
    ret = QLabel()
    ret.setText(text)
    ret.setStyleSheet("background-color: %s; padding: 2; border: 1px solid gray" % colour)
    return ret


def createButton(text, run):
    """
        Vytvori tlacitko
        text a run definuji text na tlacitku a co spustit pri stisknuti
    """
    ret = QPushButton(text)
    ret.clicked.connect(run)
    return ret


def getFilesInDirectory(url):
    files = [f[:-4] for f in os.listdir(url) if os.path.isfile(os.path.join(url, f))]
    files = [x for x in files if not x.startswith('.')]
    files = [x for x in files if not x.endswith('.')]
    return files


def randomword(len):
    """
        generate random string of length 'len'
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))


def createInst (type, configFile):
    writeConfigFile();


    # create the issue pool
    ip = issuePool("./issues/")


    if Config.reportTypeGeneric == "web":
        print("Copying web.latex...")
        shutil.copy("orig/web.latex.orig", Config.target+".latex")

    if Config.reportTypeGeneric == "webscan":
        print("Copying webscan.latex...")
        shutil.copy("orig/webscan.latex.orig", Config.target+".latex")

    if Config.reportTypeGeneric == "infra":
        print("Copying infra.latex...")
        shutil.copy("orig/infra.latex.orig", Config.target+".latex")

    if Config.reportTypeGeneric == "infrascan":
        print("Copying infrascan.latex...")
        shutil.copy("orig/infrascan.latex.orig", Config.target+".latex")

    # modify the appropriate file with the information from issue-config file
    print("Adding know issues from config file...")

    if os.path.isfile(configFile):

        # read whole latex file for further changes
        latexFileHandle = open(Config.target+".latex", 'r')
        latexFileContent = latexFileHandle.read()

        confFileHandle = open(configFile, 'r')

        for linetmp in confFileHandle:
            line = linetmp.rstrip()
            logger.debug("issue from config is "+line)

            # nacist vzor
            #vzorFile = "vzor_"+Config.lang+".tex"
            #vzorFileHandle = open(vzorFile, 'r')
            #vzorText = vzorFileHandle.read()

            # nahradit informace v nem
            #issue = issueXml("issues/"+line+".xml", Config.lang)


            #vzorText = vzorText.replace("%%%NAME%%%", issue.getName())
            #vzorText = vzorText.replace("%%%RISK%%%", issue.getRisk())
            #vzorText = vzorText.replace("%%%TFINDING%%%", issue.getTfinding())
            #vzorText = vzorText.replace("%%%TSTEPS%%%", issue.getTsteps())
            #vzorText = vzorText.replace("%%%TRISK%%%", issue.getTrisk())
            #vzorText = vzorText.replace("%%%TRECOMMENDATION%%%", issue.getTrecommendation())


            vzorText = ip.getIssue(line).getWebLatex()
            vzorText = vzorText+"\n"+"%%%P%%%"

            #newLine = "\\input{"+issuesLocation+"/"+line+"} %%%NL%%%"+"\\n \\\\ \\n"+"%%%P%%%"
            newLine = vzorText


            latexFileContent = latexFileContent.replace('%%%P%%%', newLine)

        print("Finishing...")
        latexFileContent = latexFileContent.replace('%%%NL%%%', '\n')
        latexFileContent = latexFileContent.replace('%%%P%%%', '\n')

        latexFileHandle.close()

        # write the modified stuff back
        latexFileHandleWrite = open(Config.target+".latex", 'w')
        latexFileHandleWrite.write(latexFileContent)

    print("Success")
    exit(0)

class win(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def addIssue(self):
        self.addWin = create.win(Config.reportTypeGeneric)

        self.addWin.show()


    def clearLayouts(self):
        for layout in self.layouts.values():
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i)
                if type(widget) == QWidgetItem:
                    widget.widget().setParent(None)

        for l in self.layouts.values():
            l.removeWidget(l.takeAt(0).widget())


    def loadNewItems(self):
        self.clearLayouts()
        self.fillLayouts()


    def fillLayouts(self):

        issuesLocation = Config.issuesLocation

        files = getFilesInDirectory(issuesLocation)

        # aby byly nalezy vzdycky abecedne serazene
        files.sort()


        for f in files:

            print("XXX",f)

            severity = self.getSeverityFromFile(f, issuesLocation)
            text = self.getTextFromFile(f, issuesLocation)

            item = myQCheckBox(text, self)

            # nastaveni url
            item.url = f
            item.severity = severity

            # pokud je nalez v configu, tak ho zaskrtnout
            if f in self.configList:
                item.setChecked(1)


            self.items.append(item)

            try:
                self.layouts[item.severity].addWidget(item)
            except IndexError:
                print ("problem, neexistujici severity: %s" % item.url)


        # add stretch to all scroll layouts
        for l in self.layouts.values():
            l.addStretch(1)


    def preExit(self):
        print("creating Instance...")
        createInst(self.reportType, self.configFile)
        pass

    def initUI(self):
        self.items = []

        self.configList = []
        if len(sys.argv) > 6 and sys.argv[1] == "-c" and sys.argv[3] == "-t":
            self.config = True
            self.configFile = sys.argv[2]
            self.readConfigItems(self.configFile)
            self.reportType = sys.argv[4]
            Config.target = sys.argv[5]
            Config.company = sys.argv[6]

            # setup Config class for that particular type of scan
            if self.reportType == "web":
                Config.reportTypeGeneric = "web"
                Config.project = "Penetrační test webové aplikace"
            elif self.reportType == "webscan":
                Config.reportTypeGeneric = "webscan"
                Config.project = "Vulnerability scan webové aplikace"
            elif self.reportType == "infra":
                Config.reportTypeGeneric = "infra"
                Config.project = "Infrastrukturní penetrační test"
            elif self.reportType == "infrascan":
                Config.reportTypeGeneric = "infrascan"
                Config.project = "Infrastrukturní scan"
            else:
                print ("Error, -t must be either web or infra or webscan or infrascan")
                usage()
                exit(1)

        else:
            print("Error, must state -c file -t type")
            usage()
            exit(1)


        # main layout
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        self.layout1 = QHBoxLayout()
        mainLayout.addLayout(self.layout1)

        self.layout2 = QHBoxLayout()
        mainLayout.addLayout(self.layout2)


        # tlacitko pro generovani configu a ukonceni programu
        generateBtn = createButton("Generate", self.generate)
        quitBtn = createButton("Ready", self.preExit)
        newBtn = createButton("New issue", self.addIssue)
        clearBtn = createButton("Load new items", self.loadNewItems)

        # layouty pro jednotlivy issues podle severity
        self.criticalLayout, self.criticalLayoutScroll = self.newLayoutFat('Critical', 'violet')
        self.highLayout, self.highLayoutScroll = self.newLayoutFat('High', 'red')
        self.mediumLayout, self.mediumLayoutScroll = self.newLayoutFat('Medium', 'yellow')
        self.lowLayout, self.lowLayoutScroll = self.newLayoutFat('Low', 'lightgreen')
        self.infoLayout, self.infoLayoutScroll = self.newLayoutFat('Info', 'lightblue')

        # layouty adresovatelny pomoci severity
        self.layouts = {
            "critical": self.criticalLayoutScroll,
            "high": self.highLayoutScroll,
            "medium": self.mediumLayoutScroll,
            "low": self.lowLayoutScroll,
            "info": self.infoLayoutScroll
            }

        # pridani issues layoutu
        self.layout1.addLayout(self.criticalLayout)
        self.layout1.addLayout(self.highLayout)
        self.layout1.addLayout(self.mediumLayout)
        self.layout2.addLayout(self.lowLayout)
        self.layout2.addLayout(self.infoLayout)


        # layout pro buttony
        btnLayout = QVBoxLayout()
        btnLayout.addWidget(generateBtn)
        btnLayout.addWidget(newBtn)
        btnLayout.addWidget(clearBtn)
        #btnLayout.addWidget(fillBtn)
        btnLayout.addStretch(1)
        btnLayout.addWidget(quitBtn)
        self.layout2.addLayout(btnLayout)


        # naplni layouty datama
        self.fillLayouts()


        self.setWindowTitle('Web issue config generator')
        self.showMaximized()


    def newLayoutFat (self, text, colour):
        """
            Vytvori scrollovaci layout a vsechno co s nim souvisi
        """
        ScrollArea = QScrollArea(self)
        ScrollArea.setWidgetResizable(True)
        ScrollAreaWidget = QWidget(ScrollArea)
        ScrollArea.setWidget(ScrollAreaWidget)
        Layout = QVBoxLayout()
        Label = createLabel(text, colour)
        Layout.addWidget(Label)
        Layout.addWidget(ScrollArea)
        LayoutScroll = QVBoxLayout(ScrollAreaWidget)
        return (Layout, LayoutScroll)


    def getSeverityFromFile(self, f, directory):
        """
            Vraci zavaznost nalezu prectenou ze souboru
        """
        path = os.path.join(directory, f+".xml")
        f = open (path, 'r')

        for line in f:
            m = re.search('<risk>(.*)</risk>', line)
            if m and m.group(1):
                return m.group(1)
        f.close()


    def getTextFromFile(self, f, directory):
        """
            Vraci identifikaci nalezu
        """
        return f


    def generate(self):
        """
            Generuje vystupni config soubor podle zaskrtnutych nalezu
            na vystupu jsou nalezy serazeny podle zavaznosti
        """
        print("generating...")
        criticalList = []
        highList = []
        mediumList = []
        lowList = []
        infoList = []

        urlLists = {
            "critical": criticalList,
            "high": highList,
            "medium": mediumList,
            "low": lowList,
            "info": infoList
            }

        f = open(sys.argv[2], 'w+')
        for i in self.items:
            if i.isChecked() == True:
                urlLists[i.severity].append(i.url)

        # vypsat jednotlivy nalezy do konfiguraky podle zavaznosti
        for i in ["critical", "high", "medium", "low", "info"]:
            for x in urlLists[i]:
                f.write(x+"\n")

        f.close()
        print("end generating...")


    def readConfigItems(self, configFile):
        """
            Cte config soubor a uklada jednotlive nalezy v nem uvedene
            do seznamu existujicich nalezu
        """
        try:
            if self.config == True:
                with open(configFile) as f:
                    self.configList = f.readlines()
                self.configList = [x.strip() for x in self.configList]
        except FileNotFoundError:
            pass # it's ok, just file doesn't have any issues yet


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = win()
    sys.exit(app.exec_())
