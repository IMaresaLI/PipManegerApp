################################################
################################################
################################################
#########*******###*******####**********########
########**#####**#**#####**###**######**########
########**#####**#**#####**###**######**########
########**#####**#**#####**###**********########
########**#####**#**#####**###**################
########**#####**#**#####**###**################
########**######***######**###**################
########**###############**###**################
########**###############**###**################
################################################
########Copyright © Maresal Programming#########
################################################

from PyQt5 import QtWidgets,QtCore,QtGui
import os,sys,requests,json,subprocess,time
from pipManagerDesign import Ui_MainWindow
from bs4 import BeautifulSoup


class pipMnApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(pipMnApp,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pipGetList()
        self.label()
        self.webWorker()


        self.ui.update_Btn.clicked.connect(self.updateVersion)
        self.ui.surum_Btn.clicked.connect(self.checkVersion)

    def pipGetList(self):
        self.btnStatus(False)
        self.ui.treeWidget.clear()
        tuple = ("Package","Version","Last Version")
        self.ui.treeWidget.setHeaderLabels(tuple)
        self.ui.treeWidget.setColumnWidth(0,170)
        self.ui.treeWidget.setColumnWidth(1,100)
        os.system("pip list > piplist.txt")
        pipList = open("piplist.txt","r")
        piplistTxt = pipList.read().split("\n")
        try:
            with open("Version.json","r") as file :
                version = json.load(file)
        except :
            pass
        n=0
        for i in piplistTxt:        
            x = i.split(" ")
            a = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
            a.setText(0,x[0])
            a.setText(1,x[-1])
            if os.path.exists("Version.json"):
                if x[0] == "Package" or x[0] == "Version" or x[0] == "----------------------" or x[0] == "------------" or x == ['']:
                    pass
                else :
                    a.setText(2,version[n][x[0]])
                    n+=1
            else :
                a.setText(2,"Updating")
                
        self.ui.treeWidget.takeTopLevelItem(0).removeChild(a)
        self.ui.treeWidget.takeTopLevelItem(0).removeChild(a)
        self.btnStatus(True)

    def updateVersion(self):
        global ProcessText
        currentData = self.ui.treeWidget.currentItem()
        result = QtWidgets.QMessageBox.question(self,"Güncelleme",f"{currentData.data(0,0)} adlı kütüphaneyi güncellemek istiyor musunuz?",QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        if result == QtWidgets.QMessageBox.Ok:
            if currentData.data(1,0) == currentData.data(2,0):
                QtWidgets.QMessageBox.information(self,"Güncelleme Bilgisi",f"Bu kütüphane zaten güncel.[{currentData.data(2,0)}]")
            else :
                self.btnStatus(False)
                ProcessText = f"pip install {currentData.data(0,0)} --upgrade"
                self.processWorker()

    def webWorker(self):
        self.btnStatus(False)
        self.worker = WebWorker()
        self.worker.start()
        self.worker.finished.connect(self.webWorkerStop)

    def processWorker(self):
        self.worker = ProcessWorker()
        self.worker.start()
        self.worker.finished.connect(self.processWorkerStop)


    def webWorkerStop(self):
        try:
            if self.ui.treeWidget.currentItem().data(2,0) == "Updating":
                self.pipGetList()
            else :
                QtWidgets.QMessageBox.information(self,"Versiyon Kontrol","Tüm Kütüphanelerin son sürüm bilgileri güncellendi.")
                self.pipGetList()
        except Exception as err:
            pass
        finally :
            self.pipGetList()
            self.btnStatus(True)


    def processWorkerStop(self):
        QtWidgets.QMessageBox.information(self,"Bildirim",f"{ProcessText} - İşleminiz Tamamlandı.\n")
        self.btnStatus(True)
        time.sleep(5)
        self.pipGetList()
        


    def label(self):
        self.movie = QtGui.QMovie("PythonLogo.gif")
        self.ui.LogoPython.setMovie(self.movie)
        self.movie.start()

    def btnStatus(self,Status):
        self.ui.update_Btn.setEnabled(Status)
        self.ui.surum_Btn.setEnabled(Status)


    def checkVersion(self):
        self.btnStatus(False)
        self.webWorker()
        self.pipGetList()


class WebWorker(QtCore.QThread):
    def run(self):
        list = []
        pipList = open("piplist.txt","r")
        piplistTxt = pipList.read().split("\n")
        for i in piplistTxt:        
            x = i.split(" ")
            try:
                print(x[0])
                if x[0] == "Package" or x[0] == "Version" or x[0] == "----------------------" or x[0] == [" "]:
                    pass
                else :
                    url = "https://pypi.org/project/"+x[0]+"/"
                    html = requests.get(url).content
                    soup = BeautifulSoup(html,"html.parser")
                    version = soup.find("h1",{"class":"package-header__name"})
                    text = version.text
                    splText = text.strip().split(" ")
                    list.append({x[0]:splText[1]})
                    print("Çalıştı")
            except :
                print("Hata")
        with open("Version.json","w+") as file :
            json.dump(list,file)


class ProcessWorker(QtCore.QThread):
    def run(self):
        for i in range(1):
            subprocess.Popen(ProcessText)
        






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = pipMnApp()
    main.show()
    app.setStyle("Fusion")
    app.exit(app.exec_())
