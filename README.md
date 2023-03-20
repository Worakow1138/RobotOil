# RobotOil

- [RobotOil](#robotoil)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Importing RobotOil](#importing-robotoil)
    - [Importing into Robot](#importing-into-robot)
    - [Importing into Python](#importing-into-python)
  - [Features and Examples](#features-and-examples)
    - [Smart Browser](#smart-browser)
      - [Smart Browser Example](#smart-browser-example)
    - [Smart Keywords](#smart-keywords)
      - [Smart Click Example](#smart-click-example)
      - [Smart Keywords from Python](#smart-keywords-from-python)
  - [Conclusion](#conclusion)

## Introduction
RobotOil is a library of quality-of-life features for automated test case development with [Robot Framework](https://robotframework.org/) and [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary). 

Enhancements include the option of persistent browser sessions to assist with debugging your scripts and "Smart" versions of common-use SeleniumLibrary Keywords to make navigating your web application even easier. Additionally, everything within RobotOil may be executed from either a Robot Test Suite OR the execution of a Python file.

Grease the gears of your next automation project with [RobotOil](https://github.com/Worakow1138/RobotOil)!

## Dependencies
Requires RobotFramework and SeleniumLibrary. 
Use these commands to stay up to date with the latest versions.

    pip install robotframework -U
    pip install robotframework-seleniumlibrary -U

## Installation
Recommend using pip to install RobotOil.

    pip install robotframework-RobotOil -U

If using [GitHub](https://github.com/Worakow1138/RobotOil), copy the RobotOil folder from the src folder to anywhere in your PATH. 
Ideally, to the (your Python library)/Lib/site-packages folder.

## Importing RobotOil
RobotOil and all Keywords within may be executed from either a Robot Test Suite or a Python module.

### Importing into Robot
Simply call RobotOil as Library within your Test Suite or Resource file of choice.

    *** Settings ***
    Library    RobotOil

### Importing into Python
Import the RobotOil module and class into a Python file.
All RobotOil Keywords/methods may be called from this class.

    from RobotOil import RobotOil

    oil_can = RobotOil()

## Features and Examples

### Smart Browser
If you've worked with Selenium, you've likely noticed how every automated test needs to begin with the creation of a new browser session.
Even with debugging tools native to many IDE's, automated test cases with traditional browser sessions can become incredibly time-consuming to maintain when needing to, say, correct step 48 of a 50 step test case but needing to execute steps 1-47 everytime you try a new fix.

By contast, Smart Browser sessions provide the option to remain open after a Robot or Python test execution has finished allowing them to be reusable for additonal sessions as long as the browser remains open and no new sessions are created.

#### Smart Browser Example
Create a file named `oil_test.robot` anywhere on your machine and enter the following code:

    *** Settings ***
    Library           SeleniumLibrary
    Library           RobotOil

    *** Test Cases ***
    Begin Session
        Open Smart Browser    https://phptravels.com/demo    chrome    persist

In a console, run the command `robot -t "Begin Session" PATH_TO_TEST_SUITE\oil_test.robot`.
A chrome browser session is started and the test site is navigated to.
Leave this browser *open* before beginning the next step.

In the same `oil_test.robot` Test Suite, add this Test Case:

    Continue Session
        Use Current Smart Browser
        Maximize Browser Window

Run this Test Case via `robot -t "Continue Session" PATH_TO_TEST_SUITE\oil_test.robot`.
If all goes well, you should see the same browser session you opened earlier become maximized.

You may continue to send commands to Smart Browser Sessions via `Use Current Smart Browser` until either closing the browser or 
creating a new Smart Browser.

When it's actually time to close up the browser and any webdrivers that may be hanging around, simply call the `Cleanup Smart Browser` Keyword.

### Smart Keywords
The [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary) package features a wide variety of powerful Keywords for interacting with web elements.
Keywords like Click Element, Input Text, and so forth probably make up the bulk of most web automation projects using [Robot Framework](https://robotframework.org/).

However, these Keywords are often limited when dealing with the unpredictability of page load times and elements appearing asynchronously on a given web page.
These limitations cause unexpected failures and sometimes require complex or time-consuming workarounds. 

Smart Keywords offer enhanced versions of these SeleniumLibrary Keywords that account for this unpredictability and provide additonal quality-of-life improvements by:
1. Automatically waiting for targeted elements to be visible before attempting to interact
2. Allowing for the "time to wait" to be established per Keyword call
3. Being accessible from a Python method as well as a Robot Test Case

#### Smart Click Example
In the same `oil_test.robot` Test Suite from earlier, copy the following code:

    Text Retrieval Test
        Open Smart Browser    https://the-internet.herokuapp.com/dynamic_loading/2    chrome
        Maximize Browser Window
        Click Element   css:#start > button
        ${hello_text}    Get Text    css:#finish

Run using `robot -t "Text Retrieval Test" PATH_TO_TEST_SUITE\oil_test.robot`.

This test ends up failing because the Get Text keyword gives up looking for the #finish id before this element can become available.

![not_yet_loaded](https://github.com/Worakow1138/RobotOil/blob/main/images/not_yet_loaded.png?raw=true)

A typical workaround to this issue might include having to write in a `Wait For Page to Contain Element` or worse, a call to the dreaded `Sleep` Keyword. Static waits like Sleep and the variability of internet connections and server responses do NOT mix well and having to write out a `Wait For...` Keyword before nearly every test step is a chore.

Instead, simple add the word `Smart` to the `Get Text` keyword so the last line looks like this:

    ${hello_text}    Smart Get Text    css:#finish

And run the test again. The test passes due to `Smart Get Text` understanding that it has to wait until the "finish" element is visible before attempting to retrieve its text.

If you want to ensure that the finish element, or any element you want to interact with using a Smart Keyword, becomes visible within a known time limit, you may simply give the `timeout` parameter a specific argument like so:

    ${hello_text}    Smart Get Text    css:#finish    timeout=120

This will make `Smart Get Text` wait for **up to** 2 minutes for the finish element to become visible before attempting to click the button.

Note: Not all SeleniumLibrary Keywords are available by simply adding `Smart` as a prefix. If a keyword has not been explicitly added to the `Smart Keywords` class, you may add `Smart Keyword` to a SeleniumLibrary keyword and receive the same benefits. For example:

    ${hello_text}    Smart Keyword    Get Text    css:#finish    timeout=120

With this enhancement, you'll never have to explicitly call another `Sleep` or `Wait For...` Keyword in your test cases again!

#### Smart Keywords from Python
One of RobotFramework's greatest advantages is the ease of creating custom Python libraries and methods and being able to execute these directly from a Robot Test Case.
This is especially useful when needing to write out a more complex set of actions from Python where features like nested for loops, while loops, etc, are available.
To further facilitate this capability, Smart Keywords are also accessible from your extended Python libraries and methods.

Create a file named `click_test.py` anywhere on your machine, copy the following example code, and execute the file:

    from RobotOil import RobotOil

    oil_can = RobotOil()

    oil_can.open_smart_browser('https://phptravels.com/', 'chrome', 'persist')
    oil_can.browser.maximize_window()
    oil_can.smart_click_element('link:Features')
    oil_can.smart_click_element('link:Main Features')
    oil_can.smart_click_element('link:Demo')

To move this functionality back into your established Robot Test Cases, simply wrap this code in a method:

    from RobotOil import RobotOil

    oil_can = RobotOil()

    def python_clicking():
        oil_can.open_smart_browser('https://phptravels.com/', 'chrome', 'persist')
        oil_can.browser.maximize_window()
        oil_can.smart_click_element('link:Features')
        oil_can.smart_click_element('link:Main Features')
        oil_can.smart_click_element('link:Demo')

And import the file into your `oil_test.robot` Test Suite:

    *** Settings ***
    Library           SeleniumLibrary
    Library           RobotOil
    Library           PATH_TO_CLICK_TEXT/click_test.py

From there, simply call `Python Clicking` from a Test Case of your choice:

    *** Test Cases ***
    Python Example
        Python Clicking

You may now leverage the already powerful SeleniumLibrary Keywords, with Smart Keyword enhancements, DIRECTLY from Python, and back into your Robot Test Cases!

## Conclusion
I hope you enjoy the additional capabilities and ease-of-use that RobotOil brings to automated web testing with RobotFramework.

Please don't hesitate to reach out with questions or suggestions on [GitHub](https://github.com/Worakow1138/RobotOil)