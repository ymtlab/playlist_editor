# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui

class Model(QtCore.QAbstractItemModel):
    def __init__(self, parent_=None, root_item=None):
        super(Model, self).__init__(parent_)
        self.parent_object = parent_
        self.root_item = root_item
        self.root_index = QtCore.QModelIndex()
        self._columns = []

    def columns(self):
        return self._columns

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._columns)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.EditRole:
            item = index.internalPointer()
            return item.data( self._columns[index.column()] )
        if role == QtCore.Qt.DisplayRole:
            item = index.internalPointer()
            data = item.data( self._columns[index.column()] )
            return data
        return QtCore.QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, i, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._columns[i]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return i + 1
 
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QtCore.QModelIndex()
 
    def insertColumn(self, column, column_text, parent=QtCore.QModelIndex()):
        return self.insertColumns(column, [column_text], parent)

    def insertColumns(self, column, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns( parent, column, column + len(columns) - 1 )
        self._columns[ column : column + len(columns) - 1 ] = columns
        self.endInsertColumns()
        return True

    def insertRow(self, row, parent=QtCore.QModelIndex()):
        return self.insertRows(row, 1, parent)

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        if parent == QtCore.QModelIndex():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        self.beginInsertRows(parent, row, row + count - 1)
        parent_item.insert_children(row, count)
        self.endInsertRows()
        return True

    def moveRow(self, sourceParent, sourceRow, destinationParent, destinationChild):
        return self.moveRows(sourceParent, sourceRow, 1, destinationParent, destinationChild)

    def moveRows(self, sourceParent, sourceRow, count, destinationParent, destinationChild):
        sourceRowEnd = sourceRow + count - 1
        self.beginMoveRows(sourceParent, sourceRow, sourceRowEnd, destinationParent, destinationChild)

        # source item
        if sourceParent == QtCore.QModelIndex():
            item = self.root_item
        else:
            item = sourceParent.internalPointer()
        
        # move children
        children = item.move_send(sourceRow, sourceRowEnd + 1)

        # insert item
        if destinationParent == QtCore.QModelIndex():
            item = self.root_item
        else:
            item = destinationParent.internalPointer()

        # insert row
        if sourceParent == destinationChild:
            if sourceRow > destinationChild:
                row = destinationChild
            else:
                row = sourceRow  + 1
        else:
            row = destinationChild
        
        # insert to children
        item.move_receive(children, row)

        self.endMoveRows()
        return True

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        child_item = index.internalPointer()
        parent_item = child_item.parent()
        if parent_item == self.root_item:
            return QtCore.QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)
        
    def removeColumn(self, column, parent=QtCore.QModelIndex()):
        return self.removeColumns(column, 1, parent)

    def removeColumns(self, column, count, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, column, column + count - 1)
        del self._columns[column : column + count]
        self.endRemoveColumns()
        return True

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        return self.removeRows(row, 1, parent)
 
    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        self.beginRemoveRows(parent, row, row + count - 1)
        parent_item.remove_children(row, count)
        self.endRemoveRows()
        return True
 
    def rowCount(self, parent=QtCore.QModelIndex()):
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        return parent_item.child_count()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not self.hasIndex(index.row(), index.column(), index.parent()):
            return False
        if role == QtCore.Qt.EditRole:
            if value == 'None':
                index.internalPointer().clear(self._columns[index.column()])
            else:
                index.internalPointer().set_data( self._columns[index.column()], value )
            return True
        return False

class Item(object):
    def __init__(self, parent_item=None, dictionary={}):
        self._dict = dictionary
        self._parent_item = parent_item
        self._children = []

    def child(self, row):
        if row > len(self._children):
            return None
        return self._children[row]

    def child_count(self):
        return len(self._children)

    def children(self):
        return self._children

    def clear(self, column=None):
        if column is None:
            self._dict = {}
            return
        if column in set(self._dict.keys()):
            del self._dict[column]

    def data(self, column):
        if column in self._dict:
            return self._dict[column]
        return None

    def extend_dict(self, _dict):
        for key in _dict:
            self._dict[key] = _dict[key]
        
    def insert_children(self, row, count):
        self._children[row:row+count-1] = [ Item(self, {}) for i in range(count) ]

    def move_send(self, start, end):
        c0 = self._children[0:start]
        c1 = self._children[start:end]
        c2 = self._children[end:len(self._children)]
        self._children = c0 + c2
        return c1

    def move_receive(self, children, row):
        c0 = self._children[0:row]
        c1 = self._children[row:len(self._children)]
        self._children = c0 + children + c1

    def parent(self):
        return self._parent_item
        
    def remove_children(self, row, count):
        del self._children[row:row+count]

    def row(self):
        if self._parent_item:
            return self._parent_item._children.index(self)
        return 0

    def set_data(self, column, data):
        self._dict[column] = data

    def set_dict(self, _dict):
        self._dict = _dict

    def to_dict(self):
        return self._dict

class Delegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None, setModelDataEvent=None):
        super(Delegate, self).__init__(parent)
        self.setModelDataEvent = setModelDataEvent
 
    def createEditor(self, parent, option, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        if value is None:
            return QtWidgets.QLineEdit(parent)
        if type(value) in [ str, int, float ]:
            return QtWidgets.QLineEdit(parent)
        return
 
    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        if value is None:
            editor.setText(str(value))
            return
        if type(value) in [ str, int, float ]:
            editor.setText(str(value))
            return
        return
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.text().strip())
        if not self.setModelDataEvent is None:
            self.setModelDataEvent()
        
    def paint(self, painter, option, index):
        data = index.model().data(index)
        if type(data) is QtGui.QPixmap:
            # cell size
            r = option.rect
            x, y, w, h = r.x(), r.y(), r.width(), r.height()
            
            # image size
            w2, h2 = data.size().width(), data.size().height()
            
            # aspect rasio
            r1, r2 = w / h, w2 / h2
            
            if r1 < r2:
                h = w / r2
            else:
                w = h * r2
            
            pixmap2 = data.scaled(w, h, QtCore.Qt.KeepAspectRatio)
            rect = QtCore.QRect(x, y, w, h)
            painter.drawPixmap(rect, pixmap2)
        super(Delegate, self).paint(painter, option, index)
