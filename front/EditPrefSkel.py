# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Code\hotspotter\gui\EditPrefSkel.ui'
#
# Created: Fri Apr 05 09:54:57 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_editPrefSkel(object):
    def setupUi(self, editPrefSkel):
        editPrefSkel.setObjectName(_fromUtf8("editPrefSkel"))
        editPrefSkel.resize(668, 530)
        self.verticalLayout = QtGui.QVBoxLayout(editPrefSkel)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.prefTreeView = QtGui.QTreeView(editPrefSkel)
        self.prefTreeView.setObjectName(_fromUtf8("prefTreeView"))
        self.verticalLayout.addWidget(self.prefTreeView)

        self.retranslateUi(editPrefSkel)
        QtCore.QMetaObject.connectSlotsByName(editPrefSkel)

    def retranslateUi(self, editPrefSkel):
        editPrefSkel.setWindowTitle(_translate("editPrefSkel", "Edit Preferences", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    editPrefSkel = QtGui.QWidget()
    ui = Ui_editPrefSkel()
    ui.setupUi(editPrefSkel)
    editPrefSkel.show()
    sys.exit(app.exec_())

