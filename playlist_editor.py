# -*- coding: utf-8 -*-
import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from pathlib import Path

from mainwindow import Ui_MainWindow
from model import Model, Delegate, Item

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = Model(None, Item())
        self.model.insertColumns(0, ['m3u line', 'File path'])
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setItemDelegate(Delegate())

    def check_box_changed(self):

        for r, item in enumerate( self.model.root_item.children() ):

            path = item.data('path')
            anchor = path.anchor
            folderpath = str(path.parent).replace(anchor, '') + '\\'
            filename = str(path.stem)
            suffix = str(path.suffix)

            if not self.ui.checkBox_drive_letter.isChecked():
                anchor = ''

            if not self.ui.checkBox_suffix.isChecked():
                suffix = ''

            if not self.ui.checkBox_folder_path.isChecked():
                folderpath = ''
                
            if not self.ui.checkBox_file_name.isChecked():
                filename = ''
            
            text = (anchor + folderpath + filename + suffix).replace('\\', '/')

            item.set_data('m3u line', text)

            index = self.model.index(r, 0, QtCore.QModelIndex())
            self.model.dataChanged.emit(index, index)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        paths = [Path(url.toLocalFile()) for url in event.mimeData().urls()]
        last_row = self.model.rowCount()
        
        self.model.insertRows(last_row, len(paths))

        children = self.model.root_item.children()

        for r in range(last_row, last_row + len(paths)):
            item = children[r]
            path = paths[r - last_row]
            
            item = self.model.index(r, 0, QtCore.QModelIndex()).internalPointer()
            item.set_data('path', path)
            item.set_data('m3u line', str(path))
            item.set_data('File path', str(path))
        
        self.check_box_changed()

    def save(self):
        p = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + '\\Desktop\\playlist.m3u'
        suffixes = ('m3u (*.m3u)')
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', p, suffixes)
        if not filename[0]:
            return
        
        text = '\n'.join([ item.data('m3u line') for item in self.model.root_item.children() ])

        with open(filename[0], mode='w', encoding='UTF-8') as f:
            f.write(text)

    def clear_list(self):
        self.model.removeRows(0, self.model.rowCount())

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
