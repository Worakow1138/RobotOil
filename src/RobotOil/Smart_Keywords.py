from robot.api.deco import keyword
from SeleniumLibrary import SeleniumLibrary
from robot.libraries.BuiltIn import (BuiltIn, RobotNotRunningError)

class SmartKeywords:
    """This class mostly houses calls to SeleniumLibrary Keywords that also behave in a "Smart" fashion, meaning these Keywords will:
       1. Confirm that the element is visible before attempting to interact with the element
       2. Confirm that any "loading elements" have ceased to be visible before attempting to search for the given elements
       3. Fail the Keyword if any of the above actions are not correctly performed within a time limit given at call of the Keyword
       4. Be accessible from a Python file as well as in Robot Framework
    """

    def __init__(self, loading_elements, smart_timeout):
        self.loading_elements = loading_elements
        self.smart_timeout = smart_timeout
    
    # Default time to wait for a desired condition in the Smart Keywords
    default_timeout = 60

    # Class instances for BuiltIn, SeleniumLibrary, and Python_Universal_Methods
    BI = BuiltIn()
    SEL = SeleniumLibrary()

    # If any Smart Keywords are called from a Robot execution, the BI.run_keyword() method is used to create more informative Robot logs
    # If any Smart Keywords are called from a Python execution, then the SEL.run_keyword() method needs to be used
    # This is due to the BuiltIn() class being unaccessible from anywhere outside of a Robot execution
    try:
        BuiltIn().get_library_instance('SeleniumLibrary')
        env = BI
    except RobotNotRunningError:
        env = SEL

    def run_robot_keyword(self, keyword, *args):
        """Calls Robot methods from either the BuiltIn() class or the SeleniumLibrary() class"""
        if self.env == self.BI:
            return self.BI.run_keyword(keyword, *args)
        elif self.env == self.SEL:
            return self.SEL.run_keyword(keyword, args, {})

    @keyword
    def smart_keyword(self, robot_keyword, locator, args=None, timeout=None):
        """Performs a SeleniumLibrary ``robot_keyword`` while ensuring that the element represented by ``locator`` is first visible within 
        the time limit in seconds, given by ``timeout``.

        ``args`` represents any information necessary to the SeleniumLibrary keyword, e.g. Input Text requires an element locator and args="Text to Enter"

        Waiting for the element to become visible is not performed if the keyword is defined as one of the ``wait_until`` SeleniumLibrary keywords
        """

        # Timeout for element to be found may come from the timeout given to this method, the smart_timeout set when instantiating the RobotOil class,
        # or the default_timeout.
        if timeout:
            time_to_wait = timeout
        elif self.smart_timeout:
            time_to_wait = self.smart_timeout
        else:
            time_to_wait = self.default_timeout
        time_to_wait = int(time_to_wait)

        # SeleniumLibrary will only accept
        modified_keyword = robot_keyword.replace(" ", "_").lower()

        # ``wait_until_`` keywords do not need to wait until they are visible
        if modified_keyword.startswith("wait_until_"):
            if args:
                return self.run_robot_keyword(modified_keyword, locator, args, time_to_wait)
            else:
                return self.run_robot_keyword(modified_keyword, locator, time_to_wait)

        # Wait until the element is visible before proceeding
        self.run_robot_keyword("wait_until_element_is_visible", locator, time_to_wait)

        # ``Get WebElement`` and ``Get WebElements`` will not work if modified
        if robot_keyword == "Get WebElement" or robot_keyword == "Get WebElements":
            return self.run_robot_keyword(robot_keyword, locator)
        # Convert args to strings as SeleniumLibrary keywords, when executed solely through Python, do not make necessary conversions
        elif type(args) is tuple:
            args = tuple(str(i) for i in args)
            return self.run_robot_keyword(modified_keyword, locator, *args)
        elif args is not None:
            args = str(args)
            return self.run_robot_keyword(modified_keyword, locator, args)
        else:
            return self.run_robot_keyword(modified_keyword, locator)

    @keyword
    def smart_click_element(self, locator, timeout=None):
        """Click the element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        The ``modifier`` argument can be used to pass
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys|Selenium Keys]
        when clicking the element. The `+` can be used as a separator
        for different Selenium Keys. The `CTRL` is internally translated to
        the `CONTROL` key. The ``modifier`` is space and case insensitive, example
        "alt" and " aLt " are supported formats to
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys.ALT|ALT key]
        . If ``modifier`` does not match to Selenium Keys, keyword fails.

        If ``action_chain`` argument is true, see `Boolean arguments` for more
        details on how to set boolean argument, then keyword uses ActionChain
        based click instead of the <web_element>.click() function. If both
        ``action_chain`` and ``modifier`` are defined, the click will be
        performed using ``modifier`` and ``action_chain`` will be ignored.

        Example:
        | Click Element | id:button |                   | # Would click element without any modifiers.               |
        | Click Element | id:button | CTRL              | # Would click element with CTLR key pressed down.          |
        | Click Element | id:button | CTRL+ALT          | # Would click element with CTLR and ALT keys pressed down. |
        | Click Element | id:button | action_chain=True | # Clicks the button using an Selenium  ActionChains        |

        The ``modifier`` argument is new in SeleniumLibrary 3.2
        The ``action_chain`` argument is new in SeleniumLibrary 4.1
        """
        self.smart_keyword("Click Element", locator=locator, timeout=timeout)

    @keyword
    def smart_input_text(self, locator, text, timeout=None):
        """Types the given ``text`` into the text field identified by ``locator``.

        When ``clear`` is true, the input element is cleared before
        the text is typed into the element. When false, the previous text
        is not cleared from the element. Use `Input Password` if you
        do not want the given ``text`` to be logged.

        If [https://github.com/SeleniumHQ/selenium/wiki/Grid2|Selenium Grid]
        is used and the ``text`` argument points to a file in the file system,
        then this keyword prevents the Selenium to transfer the file to the
        Selenium Grid hub. Instead, this keyword will send the ``text`` string
        as is to the element. If a file should be transferred to the hub and
        upload should be performed, please use `Choose File` keyword.

        See the `Locating elements` section for details about the locator
        syntax. See the `Boolean arguments` section how Boolean values are
        handled.

        Disabling the file upload the Selenium Grid node and the `clear`
        argument are new in SeleniumLibrary 4.0
        """
        self.smart_keyword("Input Text", locator=locator, args=text, timeout=timeout)

    @keyword
    def smart_get_web_element(self, locator, timeout=None):
        """Returns the first WebElement matching the given ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        return self.smart_keyword("Get WebElement", locator=locator, timeout=timeout)

    @keyword
    def smart_get_web_elements(self, locator, timeout=None):
        """Returns a list of WebElement objects matching the ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        Starting from SeleniumLibrary 3.0, the keyword returns an empty
        list if there are no matching elements. In previous releases, the
        keyword failed in this case.
        """
        return self.smart_keyword("Get WebElements", locator=locator, timeout=timeout)

    @keyword
    def smart_select_from_list_by_value(self, locator, values, timeout=None):
        """Selects options from selection list ``locator`` by ``values``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.smart_keyword("Select From List By Value", locator=locator, args=values, timeout=timeout)
        
    @keyword
    def smart_select_from_list_by_label(self, locator, labels, timeout=None):
        """Selects options from selection list ``locator`` by ``labels``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.smart_keyword("Select From List By Label", locator=locator, args=labels, timeout=timeout)

    @keyword
    def smart_select_from_list_by_index(self, locator, indexes, timeout=None):
        """Selects options from selection list ``locator`` by ``indexes``.

        Indexes of list options start from 0.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.smart_keyword("Select From List By Index", locator=locator, args=indexes, timeout=timeout)

    @keyword
    def smart_get_text(self, locator, timeout=None):
        """Returns the text value of the element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        return self.smart_keyword("Get Text", locator=locator, timeout=timeout)