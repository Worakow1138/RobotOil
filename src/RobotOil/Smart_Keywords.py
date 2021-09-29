from RobotOil.Web_Utilities import WebUtilities
from robot.api.deco import keyword
from SeleniumLibrary import SeleniumLibrary
from robot.libraries.BuiltIn import (BuiltIn, RobotNotRunningError)
import time

class SmartKeywords(WebUtilities):
    """This class mostly houses calls to SeleniumLibrary Keywords that also behave in a "Smart" fashion, meaning these Keywords will:
       1. Confirm that the element is visible before attempting to interact with the element (unless otherwise specified by the Keyword)
       2. Confirm that any "loading elements" have ceased to be visible before attempting to search for the given elements
       3. With the exception of Smart Input, Smart Input Password, and Smart Get Element Text be able to receive element lookups in the style of "element tag" | "element text"
       4. Fail the Keyword if any of the above actions are not correctly performed within a time limit given at call of the Keyword
       5. Be accessible from a Python file as well as in Robot Framework
    """

    def __init__(self, loading_elements):
        self.loading_elements = loading_elements
    
    # Default time to wait for a desired condition in the Smart Keywords
    global_timeout = 60

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

    # The self.run_robot_keyword() method is used to call Robot methods from either the BuiltIn() class or the SeleniumLibrary() class
    # In order to prevent over-complication of Robot logs, the BuiltIn() class will only be used for the primary function in a the following methods

    # Example: smart_click() checks for the page to be finished loading, the element to be visible, and then performs the click_element() Keyword;
    # Only the click_element() method call will use the BuiltIn() class and therefore appear in the Robot logs. The other two methods will be handeled purely
    # by the SeleniumLibrary() class and will only appear on the Robot log if there is an error.
    def run_robot_keyword(self, keyword, *args):
        if self.env == self.BI:
            return self.BI.run_keyword(keyword, *args)
        elif self.env == self.SEL:
            return self.SEL.run_keyword(keyword, args, {})


    @keyword
    def wait_for_loading_elements(self, timeout=global_timeout):
        """Waits for all given "loading elements" to no longer be visible.
           Typically for use only in the following Smart Keywords.
        """
        if self.loading_elements:
            for element in self.loading_elements:
                self.SEL.run_keyword('wait_until_element_is_not_visible', [element, timeout], {})

    @keyword
    def smart_click(self, *elements, **timeout):
        """Waits for loading elements to no longer be visible.
           Waits for the given element to be visible.
           Attempts to click the element.
           Waits for laoding elements to no longer be visible.

           Argument(s): 
           elements, can include:
           - 'xpath:(xpath locator)' e.g. xpath://span[text()="Some Text"]
           - (xpath locator), starting with '//' e.g. //span[text()="Some Text"]
           - 'css:(css locator)' e.g. css:span
           - 'css:(css locator)' and exact text to search for e.g. css:span | Some Text
           - (css locator) e.g. span
           - (css locator) and exact text to search for e.g. span | Some Text
           - * and exact text to search for e.g. * | Some Text
           If a custom timeout is desired, it may be given in the form of timeout=time_in_seconds; e.g. timeout=30 to set a custom timeout of 30 seconds instead of defaulting to the time set by global_timeout
        """

        if timeout.get('timeout'):
            timeout = int(timeout.get('timeout'))
        else:
            timeout = self.global_timeout
        
        self.wait_for_loading_elements(timeout)

        final_element = self.return_web_element(*elements)

        self.SEL.run_keyword('wait_until_element_is_visible', [final_element, timeout], {})
   
        self.run_robot_keyword('click_element', final_element)

        self.wait_for_loading_elements(timeout)

    @keyword
    def smart_select_from_list(self, *elements, **timeout):
        """Waits for loading elements to no longer be visible.
           Waits until the target_list is visible.
           Attempts to select the item from the target_list according to the item_type.
           Waits for loading elements to no longer be visible.
           
           Examples:
           Smart Select From List | css:#idOfList | index | 0 will select the first item from the list designated by css:#idOfList
           Smart Select From List | css:#idOfList | label | some_text will select a dropdown item with innertext of some_text from the list designated by css:#idOfList
           
           Argument(s):
           - target_list: The list to be selected from
           - item_type: Acceptable values are "index", "value", "label", or the item to be chosen from the list. If "index", "value", or "label" are given, will choose item variable from target_list according to item_type
           - item: The item to be chosen from the target_list. If item_type is given the value of the item to be chosen from the list (instead of index, value, or label), this variable may be left blank
           - timeout: The time to wait for the page to finish loading and for the element to be visible; defaults to global_timeout if not specified
        """

        if timeout.get('timeout'):
            timeout = int(timeout.get('timeout'))
        else:
            timeout = self.global_timeout

        target_list = elements[0]

        item = elements[-1]

        if len(elements) == 3:
            item_type = elements[1]
        else:
            item_type = 'N/A'

        self.wait_for_loading_elements(timeout)

        self.SEL.run_keyword('wait_until_element_is_visible', [target_list, timeout], {})

        item_types = {
            'index':'select_from_list_by_index',
            'value':'select_from_list_by_value',
            'label':'select_from_list_by_label'
        }

        if item_type.lower() in item_types:
            self.run_robot_keyword(item_types[item_type.lower()], target_list, item)
        else:
            self.run_robot_keyword('select_from_list_by_label', target_list, item)

        self.wait_for_loading_elements(timeout)

    @keyword
    def smart_get_element_attribute(self, attribute, *elements, **timeout):
        """Waits for loading elements to no longer be visible.
           Waits until the target element is present on the page (does not need to be visible).
           Retrieves the element's attribute.
           Waits for loading elements to no longer be visible.
           
           Argument(s):
           - attribute: The desired element attribute
           - elements: The element or locator to retrieve the attribute from (see Smart Click for additonal documentation on acceptable values)
           - timeout: The time to wait for the page to finish loading and for the element to be visible; defaults to global_timeout if not specified
        """

        if timeout.get('timeout'):
            timeout = int(timeout.get('timeout'))
        else:
            timeout = self.global_timeout

        self.wait_for_loading_elements(timeout)

        final_element = self.return_web_element(*elements)

        self.SEL.run_keyword('wait_until_page_contains_element', [final_element, timeout], {})

        attribute_value = self.run_robot_keyword('get_element_attribute', final_element, attribute)

        self.wait_for_loading_elements(timeout)

        return attribute_value

    @keyword
    def smart_input(self, element, text, **timeout):
        """Waits for loading elements to no longer be visible.
           Waits until the given element is visible.
           Inputs the text into the given element.
           Waits for loading elements to no longer be visible.
        
            Argument(s):
            - element: The field to enter text in
            - text: The text to be entered
            - timeout: The time to wait for the page to finish loading and for the element to be visible; defaults to global_timeout if not specified
        """

        if timeout.get('timeout'):
            timeout = int(timeout.get('timeout'))
        else:
            timeout = self.global_timeout

        self.wait_for_loading_elements(timeout)

        self.SEL.run_keyword('wait_until_element_is_visible', [element, timeout], {})

        self.run_robot_keyword('input_text', element, text)

        self.wait_for_loading_elements(timeout)

    @keyword
    def smart_confirm_element(self, status_to_confirm, *elements, **timeout):
        """Waits for loading elements to no longer be visible.
           Performs the specific Wait Until Element Is... Keyword(s) based on the status_to_confirm
           Waits for loading elements to no longer be visible.

           Examples:
           Smart Confirm Element | Exists | css:#idOfElement  will pass if the element is detected on the page within the time limit and otherwise fail
           Smart Confirm Element | Not Visible | css:#idOfElement will pass if the element is both detected on the page but is not visible within the time limit 
           
           Argument(s):
           - status_to_confirm: Acceptable statuses to confirm are Visible, Not Visible, Exists, and Not Exists
           - elements: The element or locator to retrieve the attribute from (see Smart Click for additonal documentation on acceptable values)
           - timeout: The time to wait for the page to finish loading and for the element to be at the status indicated by status_to_confirm; defaults to global_timeout if not specified
        """

        if timeout.get('timeout'):
            timeout = int(timeout.get('timeout'))
        else:
            timeout = self.global_timeout

        self.wait_for_loading_elements(timeout)

        statuses = {
            'visible':{
                'status_args':['wait_until_page_contains_element', 'wait_until_element_is_visible'],
                'return_status':'unacceptable'
            },
            'not visible':{
                'status_args':['wait_until_page_contains_element', 'wait_until_element_is_not_visible'],
                'return_status':'unacceptable'
            },
            'exists':{
                'status_args':['wait_until_page_contains_element'],
                'return_status':'unacceptable'
            },
            'not exists':{
                'status_args':['wait_until_page_does_not_contain_element'],
                'return_status':'acceptable'
            },
        }

        status_corrected = status_to_confirm.lower()

        try:
            final_element = self.return_web_element(*elements, return_none=statuses[status_corrected]['return_status'])
            if final_element != None:
                for argument in statuses[status_corrected]['status_args']:
                    self.run_robot_keyword(argument, final_element, timeout)
        except KeyError:
            raise KeyError(f'Argument "{status_to_confirm}" not recognized. Acceptable arguments for smart_confirm_element are Visible, Not Visible, Exists and Not Exists.')           

        self.wait_for_loading_elements(timeout)

    @keyword
    def smart_input_password(self, element, text, **timeout):
        """Waits for loading elements to no longer be visible.
           Waits until the given element is visible.
           Inputs the text into the given element.
           Waits for loading elements to no longer be visible.
           
           Argument(s):
           - element: The field to enter text in
           - text: The text to be entered
           - timeout: The time to wait for the page to finish loading and for the element to be visible; defaults to global_timeout if not specified
        """

        if timeout.get('timeout'):
            timeout = int(timeout.get('timeout'))
        else:
            timeout = self.global_timeout

        self.wait_for_loading_elements(timeout)

        self.SEL.run_keyword('wait_until_element_is_visible', [element, timeout], {})

        try:
            self.run_robot_keyword('input_password', element, text)
        except RobotNotRunningError:
            self.run_robot_keyword('input_text', element, text)

        self.wait_for_loading_elements(timeout)

    @keyword
    def smart_get_element_text(self, element, **timeout):
        """Waits for loading elements to no longer be visible.
           Waits until the given element is visible.
           Retrieves the text of the given element.
           Waits for loading elements to no longer be visible.

           Argument(s):
           - element: The element to retrieve the text from
           - timeout: The time to wait for the page to finish loading and for the element to be visible; defaults to global_timeout if not specified
        """

        if timeout.get('timeout'):
            timeout = int(timeout.get('timeout'))
        else:
            timeout = self.global_timeout

        self.wait_for_loading_elements(timeout)

        self.SEL.run_keyword('wait_until_element_is_visible', [element, timeout], {})

        text = self.SEL.run_keyword('Get WebElement', [element], {}).text

        self.wait_for_loading_elements(timeout)

        return text