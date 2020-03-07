from texttable import Texttable
from domain.square import Square
from service import *
from ui.ui import UI
from ui.gui import Ui_Dialog
from PyQt5 import QtWidgets 

b = Board()
g = Game(b)

ok = False
while not ok:
    print("Choose UI: \n1 - Console \n2 - GUI")
    try:
        x = int(input("Enter ID: "))
    except Exception as e:
        print(e.args[0])
        continue
    if x != 1 and x != 2:
        print("Incorrect Input!")
        continue
    ok = True

if x == 1:
    ui = UI(g)
    ui.start()
else:
    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog, g) 

        ui.createButtons()

        Dialog.show()
        app.exec_()