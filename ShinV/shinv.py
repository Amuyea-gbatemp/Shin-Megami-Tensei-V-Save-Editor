# -*- coding: utf-8 -*-
# Shin Megami Tensei V Save Editor
import sys, os
import binascii
import struct
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import functools
from shinVvalues import *
import re
import codecs

class ShinVApp(QMainWindow):

    def __init__(self):
        super().__init__()
        global root
        root = QFileInfo(__file__).absolutePath()
        self.title = "Shin Megami Tensei V Save Editor"
        self.setWindowIcon(QIcon(root + '/img/icon.png'))
        width = 800
        height = 400
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setMinimumSize(width, height)

        self.initUI()

    def initUI(self):
        global root
        root = QFileInfo(__file__).absolutePath()
        self.setWindowTitle(self.title)

        #########################################
        #				MENUBAR					#
        #########################################

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        helpMenu = menubar.addMenu('&Help')

        fileMenu_open = QAction(QIcon(root + '/img/open_file.png'), '&Open', self)
        fileMenu_open.setShortcut('Ctrl+O')
        fileMenu_open.setStatusTip('Open File')
        fileMenu_open.triggered.connect(self.openfile)

        fileMenu_save = QAction(QIcon(root + '/img/save_file.png'), '&Save', self)
        fileMenu_save.setShortcut('Ctrl+S')
        fileMenu_save.setStatusTip('Save File')
        fileMenu_save.triggered.connect(self.savefile)

        fileMenu_exit = QAction(QIcon(root + '/img/exit.png'), '&Exit', self)
        fileMenu_exit.setShortcut('Ctrl+Q')
        fileMenu_exit.setStatusTip('Exit')
        fileMenu_exit.triggered.connect(qApp.quit)

        helpMenu_usage = QAction(QIcon(root + '/img/help.png'), '&How to use', self)
        helpMenu_usage.setShortcut('Ctrl+H')
        helpMenu_usage.setStatusTip('How to use')
        helpMenu_usage.triggered.connect(self.show_howto)

        helpMenu_about = QAction(QIcon(root + '/img/about.png'), '&About', self)
        helpMenu_about.setStatusTip('About')
        helpMenu_about.triggered.connect(self.show_about)

        fileMenu.addAction(fileMenu_open)
        fileMenu.addAction(fileMenu_save)
        fileMenu.addAction(fileMenu_exit)
        helpMenu.addAction(helpMenu_usage)
        helpMenu.addAction(helpMenu_about)

        #########################################
        #				TOOLBAR					#
        #########################################

        toolbar = self.addToolBar("File")
        toolbar.setMovable(False)

        toolbar_openfile = QAction(QIcon(root + "/img/open_file.png"), "Open File", self)
        toolbar_openfile.triggered.connect(self.openfile)

        toolbar_savefile = QAction(QIcon(root + "/img/save_file.png"), "Save File", self)
        toolbar_savefile.triggered.connect(self.savefile)

        toolbar.addAction(toolbar_openfile)
        toolbar.addAction(toolbar_savefile)

        #########################################
        #				TABS					#
        #########################################

        centralWidget = QWidget(self)
        centralWidgetLayout = QVBoxLayout(centralWidget)
        centralWidget.setLayout(centralWidgetLayout)

        tabContainer = QTabWidget(centralWidget)

        tab1 = QWidget(tabContainer)

        tab1layout = QVBoxLayout(tab1)

        tabContainer.setLayout(tab1layout)

        tabContainer.addTab(tab1, "Main Save")

        tabContainer.setCurrentIndex(0)
        centralWidgetLayout.addWidget(tabContainer)
        self.setCentralWidget(centralWidget)

        #########################################
        #               Save 1                  #
        #########################################

        btn_mode = QPushButton('Mode', tab1)
        btn_mode.setToolTip("Game's Mode")
        btn_mode.move(30, 30)
        btn_mode.clicked.connect(lambda: self.show_statwindow("GameMode"))

        btn_name = QPushButton('Names', tab1)
        btn_name.setToolTip('Character Names')
        btn_name.move(200, 30)
        btn_name.clicked.connect(lambda: self.show_statwindow("Names"))

        btn_moneyglory = QPushButton('Money/Glory', tab1)
        btn_moneyglory.setToolTip('Money and Glory')
        btn_moneyglory.move(400, 30)
        btn_moneyglory.clicked.connect(lambda: self.show_statwindow("MoneyGlory"))

        btn_characterdemonstat = QPushButton('HP & MP', tab1)
        btn_characterdemonstat.setToolTip('Character & Demons HP, MP')
        btn_characterdemonstat.move(30, 100)
        btn_characterdemonstat.clicked.connect(lambda: self.show_statwindow("CharacterDemonHPMP"))

        btn_characterdemonstats = QPushButton('Stats', tab1)
        btn_characterdemonstats.setToolTip('Character & Demons Str, Mag, Vit, Agi, Luc')
        btn_characterdemonstats.move(200, 100)
        btn_characterdemonstats.clicked.connect(lambda: self.show_statwindow("CharacterDemonStats"))

        btn_characterdemonskills = QPushButton('Skills', tab1)
        btn_characterdemonskills.setToolTip('Character & Demons Skills')
        btn_characterdemonskills.move(400, 100)
        btn_characterdemonskills.clicked.connect(lambda: self.show_statwindow("CharacterDemonSkill"))

        btn_level = QPushButton('Level', tab1)
        btn_level.setToolTip('Character & Demon Level')
        btn_level.move(30, 170)
        btn_level.clicked.connect(lambda: self.show_statwindow("CharacterDemonLevel"))

        btn_exp = QPushButton('Exp', tab1)
        btn_exp.setToolTip('Character & Demon Level')
        btn_exp.move(200, 170)
        btn_exp.clicked.connect(lambda: self.show_statwindow("CharacterDemonExp"))

        btn_demonid = QPushButton('Demon_ID', tab1)
        btn_demonid.setToolTip('Demon IDs')
        btn_demonid.move(400, 170)
        btn_demonid.clicked.connect(lambda: self.show_statwindow("DemonID"))

        btn_items = QPushButton('Items', tab1)
        btn_items.setToolTip('Items')
        btn_items.move(30, 240)
        btn_items.clicked.connect(lambda: self.show_statwindow("Items_"))

        btn_magatama = QPushButton('Essence', tab1)
        btn_magatama.setToolTip('Essence')
        btn_magatama.move(200, 240)
        btn_magatama.clicked.connect(lambda: self.show_statwindow("Essences"))

        self.show()

    # Open File
    @pyqtSlot()
    def openfile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', 'GameSave0')

        if filename[0] == '':
            return

        if (os.path.getsize(filename[0]) >= 300000):  # Filesize check
            f = open(filename[0], "rb").read()
            i = int.from_bytes(f[:4], byteorder='little', signed=False)

            if i == 1396790855:
                global h
                h = (binascii.hexlify(f))

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Not a valid savefile! \nPlease decrypt the save file and try again!")
                msg.setWindowTitle("Not valid")
                msg.setWindowIcon(QIcon(root + '/img/icon.ico'))
                msg.buttonClicked.connect(self.openfile)
                msg.exec_()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Not a valid savefile!")
            msg.setWindowTitle("Not valid")
            msg.setWindowIcon(QIcon(root + '/img/icon.ico'))
            msg.exec_()

    # Save File
    def savefile(self):
        if self.checkforsave():
            savedir = QFileDialog.getSaveFileName(self, 'Save File', 'GameSave')
            if savedir[0] == '':
                return

            file = open(savedir[0], "wb")
            file.write(binascii.unhexlify(h))
            file.close()

    # Check if a savefile is open
    def checkforsave(self):
        if "h" in globals():
            return True
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Open a <b>Save File</b> first!")
            msg.setWindowTitle("No Save File")
            msg.setWindowIcon(QIcon(root + '/img/icon.ico'))
            msg.exec_()
            return False

    # How to
    def show_howto(self):
        global root
        howto = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        howto.setWindowTitle("How To Use")
        howto.setWindowIcon(QIcon(root + '/img/help.png'))
        width = 400
        height = 200
        howto.resize(width, height)
        howto.setFixedSize(width, height)
        howto.setWindowModality(Qt.ApplicationModal)

        l1 = QLabel()
        l2 = QLabel()

        l1.setText("<center><b>HOW TO USE</b><br><br></center>")
        l2.setText("<ul><li>1. Dump your save with your preferred save manager</li><li>2. Open your save (savedata)</li><li>3. Edit stuff to your liking</li><li>4. Save it (Ctrl + S)</li><li>5. Overwrite your save with the one you just edited</li><li>6. That's it!</li></ul>")

        l1.setAlignment(Qt.AlignLeft)
        l2.setAlignment(Qt.AlignLeft)

        vbox = QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addWidget(l2)
        vbox.addStretch()
        howto.setLayout(vbox)
        howto.exec_()

    # About
    def show_about(self):
        global root
        about = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        about.setWindowTitle("About")
        about.setWindowIcon(QIcon(root + '/img/about.png'))
        width = 450
        height = 350
        about.resize(width, height)
        about.setFixedSize(width, height)
        about.setWindowModality(Qt.ApplicationModal)

        l1 = QLabel()
        l1.setText(
            "<b>THIS SOFTWARE MUST NOT BE SOLD,NEITHER ALONE NOR AS PART OF A BUNDLE. IF YOU PAID FOR THIS SOFTWARE OR RECEIVED IT AS PART OF A BUNDLE FOLLOWING PAYMENT,<br>YOU HAVE BEEN SCAMMED AND SHOULD DEMAND YOUR MONEY BACK IMMEDIATELY.</b>")
        l1.setAlignment(Qt.AlignCenter)
        l1.setWordWrap(True)
        l2 = QLabel()
        l2.setText("Created by: <a href=\"https://github.com/Amuyea-gbatemp\"><b>Amuyea-gbatemp</b></a>")
        l2.setOpenExternalLinks(True)
        l2.setAlignment(Qt.AlignLeft)
        l3 = QLabel()
        l3.setText("Advices/Helpful: Discord Server<br>Reference on Python Save Editor: <a href=\"https://github.com/CapitanRetraso/Ultimate-Smasher\"><b>Capitán Retraso</b></a>")
        l3.setOpenExternalLinks(True)
        l3.setAlignment(Qt.AlignLeft)
        l4 = QLabel()
        l4.setText("<a href=\"https://github.com/Amuyea-gbatemp/Persona-5-Strikers-Scramble-Save-Editor/issues\"><b>Report a problem</b></a>")
        l4.setOpenExternalLinks(True)
        l4.setAlignment(Qt.AlignRight)
        l5 = QLabel()
        l5.setText(
            "<b>DISCLAIMER</b><br> This tool can damage your savegame or cause a ban if not used correctly.<br><b>By using it you are responsible for any data lost or ban.</b><br>Be careful when editing your savegame and always keep a clean backup.")
        l5.setAlignment(Qt.AlignCenter)
        l5.setWordWrap(True)

        vbox = QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addStretch()
        vbox.addWidget(l5)
        vbox.addStretch()
        vbox.addWidget(l2)
        vbox.addWidget(l3)
        vbox.addWidget(l4)
        about.setLayout(vbox)

        about.exec_()

    # Name & Value
    def show_statwindow(self, category):
        if self.checkforsave():
            statwindow = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            statwindow.setWindowTitle("Stats - " + category)
            statwindow.setWindowIcon(QIcon(root + '/img/icon.ico'))
            width = 550
            height = 400
            statwindow.resize(width, height)
            statwindow.setFixedSize(width, height)
            self.layout = QVBoxLayout()

            #########################################
            #             Save  Offsets             #
            #########################################

            if (category == "GameMode"):
                statNames = modedata
                statOffsets = mode_offset

            elif(category == "Names"):
                statNames = characternamesList
                NamestatOffsets = character_names_offsets

            elif(category == "MoneyGlory"):
                statNames = moneygloryList
                statOffsets = money_glory_offsets

            elif(category == "CharacterDemonHPMP"):
                statNames = characterdemonhpmpList
                statOffsets = characterdemon_hpmp_offsets

            elif (category == "CharacterDemonStats"):
                statNames = characterdemonstatsList
                statOffsets = characterdemon_stats_offsets

            elif (category == "CharacterDemonSkill"):
                statNames = characterdemonskillList
                statOffsets = characterdemon_skill_offsets

            elif (category == "CharacterDemonLevel"):
                statNames = levelList
                statOffsets = chardemon_level_offsets

            elif (category == "CharacterDemonExp"):
                statNames = expList
                statOffsets = chardemon_exp_offsets

            elif (category == "DemonID"):
                statNames = demonidlist
                statOffsets = demon_id_offsets

            elif (category == "Items_"):
                statNames = itemList
                statOffsets = item_offsets

            elif (category == "Essences"):
                statNames = essenceList
                statOffsets = essence_offsets

            self.tableWidget = QTableWidget()
            self.tableWidget.setColumnCount(2)

            if (category == "Names"):
                self.tableWidget.setRowCount(len(NamestatOffsets))
                for x in range(len(NamestatOffsets)):
                    self.tableWidget.setItem(x, 0, QTableWidgetItem(statNames[x]))
                    self.tableWidget.setItem(x, 1, QTableWidgetItem(
                        str(self.readFromPositionName(NamestatOffsets[x], NamestatOffsets[x] + 16, ">LL"))))

            elif (category == "MoneyGlory" or category == "CharacterDemonExp"):
                self.tableWidget.setRowCount(len(statNames))
                for x in range(len(statOffsets)):
                    self.tableWidget.setItem(x, 0, QTableWidgetItem(statNames[x]))
                    self.tableWidget.setItem(x, 1, QTableWidgetItem(
                        str(self.readFromPosition(statOffsets[x], statOffsets[x] + 4, "<L"))))

            elif (category == "CharacterDemonHPMP" or category == "CharacterDemonStats" or category == "CharacterDemonSkill" or category == "DemonID"):
                self.tableWidget.setRowCount(len(statNames))
                for x in range(len(statOffsets)):
                    self.tableWidget.setItem(x, 0, QTableWidgetItem(statNames[x]))
                    self.tableWidget.setItem(x, 1, QTableWidgetItem(
                        str(self.readFromPosition2bytes(statOffsets[x], statOffsets[x] + 2, ">L"))))

            elif(category == "GameMode" or category == "Essences" or category == "Items_" or category == "CharacterDemonLevel"):
                self.tableWidget.setRowCount(len(statNames))
                for x in range(len(statOffsets)):
                    self.tableWidget.setItem(x, 0, QTableWidgetItem(statNames[x]))
                    self.tableWidget.setItem(x, 1, QTableWidgetItem(
                        str(self.readFromPositionbyte(statOffsets[x], statOffsets[x] + 1, "<L"))))

            else:
                self.tableWidget.setRowCount(len(statNames))
                for x in range(len(statOffsets)):
                    self.tableWidget.setItem(x, 0, QTableWidgetItem(statNames[x]))
                    self.tableWidget.setItem(x, 1, QTableWidgetItem(
                        str(self.readFromPosition2bytes(statOffsets[x], statOffsets[x] + 2, ">L"))))
            # Name
            def writeStatsName():
                for x in range(len(NamestatOffsets)):
                    value = str(self.tableWidget.item(x, 1).text())
                    newname = value.replace(" ", "")
                    #print(newname)
                    my_string_4 = re.sub("\x00", "", newname)
                    if len(my_string_4) > 8:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("One or more values are too high!")
                        msg.setWindowTitle("Error")
                        msg.exec_()
                        return
                    elif len(my_string_4) <= 8:
                        charperiod = '\x00'.join(my_string_4[i:i + 1] for i in range(0, len(my_string_4), 1))
                        newstring = charperiod.ljust(16, '\x00')
                        #print(newstring)
                        #print("Test: " + newstring, "Hex: " + newstring.encode("utf-8").hex())
                        self.writeToPositionName(newstring, NamestatOffsets[x], NamestatOffsets[x] + 16, ">LL")

            # Money Write (EXP)
            def writeStats():
                for x in range(len(statOffsets)):
                    value = int(self.tableWidget.item(x, 1).text())
                    if (value <= 99999999):
                        self.writeToPosition(value, statOffsets[x], statOffsets[x] + 4, "<L")
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("One or more values are too high!")
                        msg.setWindowTitle("Error")
                        msg.exec_()
                        return

                    if (x == len(statOffsets) - 1):
                        statwindow.done(0)

            def write1b1yteStats1byte():
                for x in range(len(statOffsets)):
                    value = int(self.tableWidget.item(x, 1).text())
                    if (value <= 255):
                        self.writeToPosition(value, statOffsets[x], statOffsets[x] + 1, "<B")
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("One or more values are too high!")
                        msg.setWindowTitle("Error")
                        msg.exec_()
                        return

                    if (x == len(statOffsets) - 1):
                        statwindow.done(0)

            def write2bytesStats2bytes():
                for x in range(len(statOffsets)):
                    value = int(self.tableWidget.item(x, 1).text())
                    if (value <= 65535):
                        self.writeToPosition(value, statOffsets[x], statOffsets[x] + 2, "<H")
                        print(value)
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText("One or more values are too high!")
                        msg.setWindowTitle("Error")
                        msg.exec_()
                        return

                    if (x == len(statOffsets) - 1):
                        statwindow.done(0)

            def give_items_number():

                if (category == "GameMode"):
                    amount, okPressed = QInputDialog.getInt(self, "Items", "Amount:", 0, 0, 0x3, 10)
                    if okPressed:
                        for x in range(len(statOffsets)):
                            value = self.tableWidget.item(x, 1).setText(str(amount))

                elif (category == "Essences"):
                    amount, okPressed = QInputDialog.getInt(self, "Items", "Amount:", 0, 0, 0x1, 10)
                    if okPressed:
                        for x in range(len(statOffsets)):
                            value = self.tableWidget.item(x, 1).setText(str(amount))

                elif(category == "Items_"):
                    amount, okPressed = QInputDialog.getInt(self, "Items", "Amount:", 0, 0, 0x3E7, 10)
                    if okPressed:
                        for x in range(len(statOffsets)):
                            value = self.tableWidget.item(x, 1).setText(str(amount))

            button_save = QPushButton("Save Changes")
            button_give = QPushButton("Give items")

            if (category == "Names"):
                button_save.clicked.connect(writeStatsName)

            elif (category == "MoneyGlory"):
                button_save.clicked.connect(writeStats)

            elif (category == "CharacterDemonSkill" or category == "CharacterDemonStats" or category == "CharacterDemonHPMP"):
                button_save.clicked.connect(write2bytesStats2bytes)

            elif (category == "GameMode" or category =="Essences" or category == "Items_" or category == "CharacterDemonLevel"):
                button_save.clicked.connect(write1b1yteStats1byte)

            else:
                button_save.clicked.connect(write2bytesStats2bytes)

            button_give.clicked.connect(give_items_number)

            button_cancel = QPushButton("Cancel")
            button_cancel.clicked.connect(statwindow.done)
            hbox = QHBoxLayout()
            hbox.addWidget(button_save)
            hbox.addWidget(button_cancel)
            if (category != "Names" and category != "MoneyGlory" and category != "CharacterDemonHPMP" and category != "CharacterDemonStats" and category != "CharacterDemonSkill" and category != "CharacterDemonLevel" and category != "CharacterDemonExp" and category != "DemonID"):
                hbox.addWidget(button_give)

            self.layout.addLayout(hbox)

            self.tableWidget.setHorizontalHeaderLabels(['Name', 'Value'])
            self.tableWidget.verticalHeader().hide()
            self.tableWidget.setColumnWidth(0, 350)
            self.tableWidget.setColumnWidth(1, 150)
            self.layout.addWidget(self.tableWidget)
            statwindow.setLayout(self.layout)
            statwindow.setWindowModality(Qt.ApplicationModal)
            statwindow.exec_()

    # Read Name
    def readFromPositionName(self, startOffset, endOffset, type):
        valueToRead = (binascii.unhexlify(h[startOffset * 2:endOffset * 2]))
        valueToRead1 = binascii.hexlify(valueToRead)
        valueToRead2 = codecs.decode(valueToRead1, "hex").decode('utf-8')
        valueToRead3 = valueToRead2.replace("\x00", "")
        return valueToRead3

    # Read 3-4 bytes
    def readFromPosition(self, startOffset, endOffset, type):
        valueToRead = (binascii.unhexlify(h[startOffset * 2:endOffset * 2]))
        valueToRead1 = struct.unpack(type, valueToRead)
        valueToRead2 = functools.reduce(lambda rst, d: rst * 10 + d, (valueToRead1))
        return valueToRead2

    # Read 2 bytes (00 00)
    def readFromPosition2bytes(self, startOffset, endOffset, type):
        valueToRead = (binascii.unhexlify(h[startOffset * 2:endOffset * 2]))
        reverseval = bytes([c for t in zip(valueToRead[1::2], valueToRead[::2]) for c in t])
        valueToRead1 = binascii.hexlify(reverseval)
        valueToRead2 = int(valueToRead1, 16)
        return valueToRead2

    # Read a byte (00)
    def readFromPositionbyte(self, startOffset, endOffset, type):
        valueToRead = (binascii.unhexlify(h[startOffset * 2:endOffset * 2]))
        valueToRead1 = binascii.hexlify(valueToRead)
        valueToRead2 = int(valueToRead1, 16)
        return valueToRead2

    # Write to Save Values
    def writeToPosition(self, value, startOffset, endOffset, type):
        global h
        valueToWrite = binascii.hexlify(struct.pack(type, value))
        h = h[:startOffset * 2] + valueToWrite + h[endOffset * 2:]

    # Write to Save Name
    def writeToPositionName(self, value, startOffset, endOffset, type):
        global h
        valueToWrite = value.encode("utf-8").hex()
        h = h[:startOffset * 2] + str(valueToWrite).encode('ascii') + h[endOffset * 2:]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    if (sys.platform.startswith('linux')):
        font = app.font()
        font.setPointSize(9)
        app.setFont(font)
    ex = ShinVApp()
    sys.exit(app.exec_())