from RobotOil.Utility_Webdriver_Setup import UtilityWebdriverSetup as UWS
from SeleniumLibrary import SeleniumLibrary

class WebUtilities:

    def __init__(self):
        self.SEL = SeleniumLibrary()

    def return_web_element(self, *elements, **return_none):
        """Returns a Selenium Webelement if given more than one argument.
           If given only one argument, returns the argument assuming it is already a locator or webelement
           Acceptable arguments for elements are:
           - 'xpath:(xpath locator)'
           - (xpath locator), starting with '//'
           - 'css:(css locator)'
           - 'css:(css locator)' and exact text to search for
           - (css locator)
           - (css locator) and exact text to search for
           - '*' and exact text to search for

           - return_none: If set to "acceptable", will allow this method to retun None instead of tripping the AssertionError

           Example: ${final_element}  |  Python Return Element  |  css:#someId  |  InnerText Of Element with id of someId
        """
        # Default is to not allow returning a None final_element
        # This can be overridden by using return_none = 'acceptable'
        default_return = {"return_none": "unacceptable"}
        return_none = {**default_return, **return_none}

        final_element = None

        # If only one argument is given, the argument is returned and assumed to be either a Selenium WebElement or locator
        if len(elements) == 1:
            final_element = elements[0]
        else:
            # If more than one argument is given, either jQuery or JavaScript is used to return a Selenium WebElement.
            # The first argument is taken as the selector to give either the jQuery or JavaScript method
            # The second argument is taken as the exact text of the element to search for
            jQuery_ready = None

            try:
                # jQuery is not enabled on all pages.
                # If this execute_script() method returns an error, the attempt is passed and JavaScript will be used to locate the WebElement
                jQuery_ready = UWS.browser.execute_script('return jQuery.active')

                while jQuery_ready == 1:
                    jQuery_ready = UWS.browser.execute_script('return jQuery.active')
            except:
                pass

            # Allows using the common "css:" prefix for css selectors in Robot
            if elements[0].startswith('css:'):
                selector = elements[0][4:]
            else:
                selector = elements[0]
                
            # When entering strings that begin with "#" in Robot, the "\" is typically used to avoid commenting out the string
            if elements[1].startswith(r'\#'):
                final_text = elements[1][1:]
            else:
                final_text = elements[1]

            if jQuery_ready != None:
                # jQuery method
                final_element = UWS.browser.execute_script("return $('"+selector+"').filter(function() { return $(this).text().trim().replace(/\\n/g, '').replace(/  (?= )/g, '').replace('  ', ' ') === '"+final_text+"'; })[0]")

            else:
                # JavaScript method
                JS = """var selector = document.querySelectorAll('"""+selector+"""');
                        var searchText = '"""+final_text+"""';
                        var found;

                        for (var i = 0; i < selector.length; i++) {
                        if (selector[i].textContent.trim().replace(/\\n/g, '').replace(/  (?= )/g, '').replace('  ', ' ') == searchText) {
                            found = selector[i];
                            break;
                            }
                        }
                        return found
                        """
                final_element = UWS.browser.execute_script(JS)

        if final_element is None and return_none.get('return_none') == 'unacceptable':
            self.SEL.failure_occurred()
            raise AssertionError('Element with tag "' + selector + '" and text "' + final_text + '" was not found.')
        else:
            return final_element