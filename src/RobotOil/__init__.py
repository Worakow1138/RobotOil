from RobotOil.Smart_Browser import SmartBrowser
from RobotOil.Smart_Keywords import SmartKeywords

class RobotOil(SmartBrowser, SmartKeywords):

    def __init__(self, loading_elements=None):
        self.loading_elements = loading_elements
        super().__init__()