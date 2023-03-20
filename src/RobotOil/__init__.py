from RobotOil.Smart_Browser import SmartBrowser
from RobotOil.Utility_Webdriver_Setup import UtilityWebdriverSetup
from RobotOil.Smart_Keywords import SmartKeywords

class RobotOil(SmartBrowser, SmartKeywords, UtilityWebdriverSetup):
    """
    RobotOil is a library of quality-of-life features for automated test case development with Robot Framework and SeleniumLibrary.
    Enhancements include the option of persistent browser sessions to assist with debugging your scripts and "Smart" versions of common-use SeleniumLibrary Keywords to make navigating your web application even easier. 
    Additionally, everything within RobotOil may be executed from either a Robot Test Suite OR the execution of a Python file.
    Grease the gears of your next automation project with RobotOil!
    """

    def __init__(self, smart_timeout = None):
        self.smart_timeout = smart_timeout
        super().__init__()