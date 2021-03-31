import os, subprocess
from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from robot.api.deco import keyword
from RobotOil.Utility_Webdriver_Setup import UtilityWebdriverSetup as UWS
try:
    from RobotOil.session_info import session_info
except ImportError:
    pass



class PersistentBrowser:

    def __init__(self):
        self.browser_options = {
        'edge': {
            'options': EdgeOptions(),
            'webdriver_create': Edge
        },
        'chrome': {
            'options': webdriver.ChromeOptions(),
            'webdriver_create': webdriver.Chrome
        },
        'firefox': {
            'options': webdriver.FirefoxOptions(),
            'webdriver_create': webdriver.Remote
        },
        'ie': {
            'options': webdriver.IeOptions(),
            'webdriver_create': webdriver.Ie
        },
        }

    @keyword
    def open_persistent_browser(self, url, browser, *browser_options, **port):
        """Creates a Persistent Browser, a selenium-generated browser session that can be interacted with via Robot Keywords and Python methods, interchangeably. 
           Persistent Browsers and the accompanying webdriver exe file (chromedriver.exe, geckodriver.exe, etc.) do not automatically close after a test execution.
           Arguments:
           - url: The starting url for the Persistent Browser to navigate to
           - browser: The desired browser to open (currently supports Chrome, Firefox, Edge, and IE)
           - browser_options: Additional arguments for the browser session, e.g. --headless to launch in headless mode
           - port: Only needed for Persistent Browsers using Firefox, all other browsers will automatically select unused ports
        """ 

        global initial_browser

        browser = browser.lower()

        self.options = self.browser_options[browser]['options']

        if browser == 'edge':
            self.options.use_chromium = True

        for arg in browser_options:
            self.options.add_argument(arg)

        if browser == 'firefox':
            if port.get('port'):
                port = int(port.get('port'))
            else:
                port = 4444
            subprocess.Popen(f'geckodriver.exe -p {port}')
            service = webdriver.firefox.service.Service('geckodriver.exe', port=port)
            initial_browser = self.browser_options[browser]['webdriver_create'](options=self.options, command_executor=service.service_url)
        else:
            initial_browser = self.browser_options[browser]['webdriver_create'](options=self.options)

        session_info = [initial_browser.command_executor._url, initial_browser.session_id]

        UWS.create_utility_webdrivers(session_info[0], session_info[1])

        UWS.browser.get(url)

    @keyword
    def use_current_persistent_browser(self):
        """Allows for test executions to begin on the last opened Persistent Browser
        """
        UWS.create_utility_webdrivers(session_info[0], session_info[1])


    @keyword
    def cleanup_persistent_browser(self):
        """Attempts to tear down most recent persistent browser.
           Kills all geckodriver.exe and chromedriver.exe processes.
        """
        try:
            UWS.browser.quit()
        except:
            pass
        os.system('taskkill /f /im geckodriver.exe')
        os.system('taskkill /f /im chromedriver.exe')




