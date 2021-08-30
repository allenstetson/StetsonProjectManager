
from PyQt5 import QtCore, QtGui, QtWidgets

class SnapSplitter(QtWidgets.QSplitter):
    SNAP_BEHAVIORS = ("dynamic", "snapMin", "snapMax")
    def __init__(self, snapBehavior="dynamic", draggable=True, **kwargs):
        super(SnapSplitter, self).__init__(**kwargs)
        self.snapPositions = []
        if snapBehavior not in self.SNAP_BEHAVIORS:
            raise ValueError("Unrecognized snap behavior: {}".format(snapBehavior))
        self.draggable = bool(draggable)
        self.policies = [] # ALLEN?
        self.snapBehavior(snapBehavior)

        
