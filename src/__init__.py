from RobotOil.Persistent_Browser import PersistentBrowser
from RobotOil.Smart_Keywords import SmartKeywords

class RobotOil(PersistentBrowser, SmartKeywords):

    def __init__(self, loading_elements=None):
        self.loading_elements = loading_elements
        super().__init__()