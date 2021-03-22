# RobotOil

- [RobotOil](#robotoil)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Importing RobotOil](#importing-robotoil)
    - [Importing into Robot](#importing-into-robot)
    - [Importing into Python](#importing-into-python)
  - [Features and Examples](#features-and-examples)
    - [Persistent Browser](#persistent-browser)
      - [Persistent Browser Example](#persistent-browser-example)
  - [Smart Keywords](#smart-keywords)
    - [Smart Click Example](#smart-click-example)
    - [Text Parsing using JQuery or JavaScript](#text-parsing-using-jquery-or-javascript)
    - [Smart Keywords from Python](#smart-keywords-from-python)
    - [Loading Elements](#loading-elements)
  - [Conclusion](#conclusion)

## Introduction
RobotOil is a library of quality-of-life features for automated test case development with [Robot Framework](https://robotframework.org/) and [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary). 

Enhancements include persistent browser sessions to assist with debugging your scripts and "Smart" versions of common-use SeleniumLibrary Keywords to make navigating your web application even easier. To top it all off, everything within RobotOil may be executed from either a Robot Test Suite OR the execution of a Python file.

Grease the gears of your next automation project with [RobotOil](https://github.com/Worakow1138/RobotOil)!

## Dependencies
Requires RobotFramework, SeleniumLibrary, and [Selenium Tools for Microsoft Edge](https://pypi.org/project/msedge-selenium-tools/). 
Use these pip commands to stay up to date with the latest versions.

    pip install robotframework -U
    pip install robotframework-seleniumlibrary -U
    pip install msedge-selenium-tools -U

## Installation
Recommend using pip to install RobotOil.

    pip install robotframework-RobotOil -U

If using [GitHub](https://github.com/Worakow1138/RobotOil), copy the RobotOil folder from the src folder to anywhere in your PATH. 
Ideally, to the (your Python library)/Lib/site-packages folder.

## Importing RobotOil
RobotOil and all Keywords within may be executed from either a Robot Test Suite, or a Python module.

### Importing into Robot
Simply call RobotOil as Library within your Test Suite or Resource file of choice.

Ensure this is done *after* first calling the SeleniumLibrary Library somewhere prior to calling RobotOil.

    *** Settings ***
    Library    RobotOil

### Importing into Python
Import the RobotOil module and class into a Python file.
All RobotOil Keywords/methods may be called from this class.

    from RobotOil import RobotOil

    oil_class = RobotOil()

## Features and Examples

### Persistent Browser
If you've worked with Selenium, you've likely noticed how every automated test needs to begin with the creation of a new browser session.
Debugging automated test cases with traditional browser sessions can become incredibly time-consuming when needing to, say, correct step 48 of a 50 step test case but having to execute steps 1-47 everytime you try a new fix.

With inspiration from this post by [Tarun Lalwani](https://tarunlalwani.com/post/reusing-existing-browser-session-selenium/), RobotOil's Persistent Browser Sessions ensure you'll never have to start back at the beginning again!

Persistent Browser Sessions not only remain open after a Robot or Python test execution has finished, but will also be reusable for additonal sessions as long as the browser remains open and no new sessions are created.

#### Persistent Browser Example
Create a file named `persistent_test.robot` anywhere on your machine and enter the following code:

    *** Settings ***
    Library           SeleniumLibrary
    Library           RobotOil

    *** Test Cases ***
    Begin Session
        Open Persistent Browser    https://phptravels.com/demo    chrome

In a console, run the command `robot -t "Begin Session" PATH_TO_TEST_SUITE\persistent_test.robot`.
A chrome browser session is started and the test site is navigated to.
Leave this browser *open* before beginning the next step.

In the same `persistent_test.robot` Test Suite, add this Test Case:

    Continue Session
        Use Current Persistent Browser
        Maximize Browser Window

Run this Test Case via `robot -t "Continue Session" PATH_TO_TEST_SUITE\persistent_test.robot`.
If all goes well, you should see the same browser session you opened earlier become maximized.

You may continue to send commands to Persistent Browser Sessions via `Use Current Persistent Browser` until either closing the browser or 
creating a new Persistent Browser.

When it's actually time to close up the browser and any webdrivers that may be hanging around, simply call the `Cleanup Persistent Browser` Keyword.

## Smart Keywords
The [SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary) package features a wide variety of powerful Keywords for interacting with web elements.
Keywords like Click Element, Input Text, and so forth probably make up the bulk of most web automation projects using [Robot Framework](https://robotframework.org/).

However, these Keywords are often limited when dealing with the unpredictability of page load times and elements appearing asynchronously on a given web page.
These limitations cause unexpected failures and sometimes require complex or time-consuming workarounds. 

Smart Keywords offer enhanced versions of these SeleniumLibrary Keywords that account for this unpredictability and provide additonal quality-of-life improvements by:
1. Automatically waiting for targeted elements to be visible before attempting to interact
2. Waiting for "loading elements" to first become non-visible (more on loading elements later)
3. Allowing for the "time to wait" to be established per Keyword call
4. Using JQuery or JavaScript to parse text on the page for easier element lookup, resulting in faster test case writing and more human-readable test cases
5. Being accessible from a Python method as well as a Robot Test Case

### Smart Click Example
In the same `persistent_test.robot` Test Suite from earlier, copy the following code:

    Click Test
        Open Persistent Browser    https://phptravels.com/demo    chrome
        Maximize Browser Window
        Click Element    css:body > header > div > nav > div:nth-child(3) > span
        Click Element    css:body > header > div > nav > div:nth-child(3) > div > a:nth-child(1)
        Click Element    css:#Main > section.is-highlighted > div > div > div.col-md-6.wow.fadeIn.animated > div > div.col-md-4 > a

Run using `robot -t "Click Test" PATH_TO_TEST_SUITE\persistent_test.robot`.

This test ends up failing because the last use of Click Element is targeting the green "Demo" button on the Main Features page.
However, this button has not become completely accessible when the Main Features page finishes loading, causing the Click Element Keywords to fail the Test Case.

![not_yet_loaded](https://github.com/Worakow1138/RobotOil/blob/main/images/not_yet_loaded.png?raw=true)

A typical workaround to this issue might include having to write in a Wait For Page to Contain Element (the element in question) or worse, a call to the dreaded `Sleep` Keyword. Static waits like Sleep and the variability of internet connections and server responses do NOT mix well.

Instead, change the last Click Element to `Smart Click` so the last line looks like this:

    Smart Click    css:#Main > section.is-highlighted > div > div > div.col-md-6.wow.fadeIn.animated > div > div.col-md-4 > a

And run the test again. The test passes due to Smart Click understanding that it has to wait until the Demo button is visible before attempting the interaction.

If you want to ensure that the Demo button, or any element you want to interact with using a Smart Keyword, becomes visible within a known time limit, you may simply give the `timeout` argument a specific parameter like so:

    Smart Click    css:#Main > section.is-highlighted > div > div > div.col-md-6.wow.fadeIn.animated > div > div.col-md-4 > a    timeout=120

This will make Smart Click wait for **up to** 2 minutes for the Demo button to become visible before attempting to click the button.

With this enhancement, you'll never have to explicitly call another Sleep or Wait For... Keyword in your test cases again!

### Text Parsing using JQuery or JavaScript
Most Smart Keywords also include the ability to locate elements based on their element tag and thier inner text.
In our same `Click Test` example from before, let's first change all our Click Elements to Smart Clicks

    Click Test
        Use Current Persistent Browser
        Smart Click    css:body > header > div > nav > div:nth-child(3) > span
        Smart Click    css:body > header > div > nav > div:nth-child(3) > div > a:nth-child(1)
        Smart Click    css:#Main > section.is-highlighted > div > div > div.col-md-6.wow.fadeIn.animated > div > div.col-md-4 > a

The first Smart Click targets the `Features` link in the site banner

![Features](https://github.com/Worakow1138/RobotOil/blob/main/images/top_bar_features.png?raw=true)

We can see that the tag for this element is `span` and the innerText is simply `Features`

With this knowledge, Smart Click can locate this element and click it:

    Smart Click    span    Features

In fact, the rest of the Smart Clicks used in this Test Case can be replaced in the same way, resulting in:

    Click Test
        Use Current Persistent Browser
        Smart Click    span    Features
        Smart Click    a    Main Features
        Smart Click    div.col-md-4 > a    Demo

Note the use of `div.col-md-4 > a` in the last Smart Click. Partial css selectors are also completely viable paramters for Smart Keywords.

With tag and innerText parsing, you are no longer bound to strictly using css selectors or xpaths when targeting elements, resulting in cleaner, more readable, faster to write Test Cases!

### Smart Keywords from Python
One of RobotFramework's greatest advantages is the ease of creating custom Python libraries and methods and being able to execute these directly from a Robot Test Case.
This is especially useful when needing to write out a more complex set of actions from Python where features like nested for loops, while loops, etc, are available.
To further facilitate this capability, Smart Keywords are also accessible from your extended Python libraries and methods.

Create a file named `click_test.py` anywhere on your machine, copy the following example code, and execute the file:

    from RobotOil import RobotOil

    oil_can = RobotOil()

    oil_can.use_current_persistent_browser()
    oil_can.smart_click('span', 'Features')
    oil_can.smart_click('a', 'Main Features')
    oil_can.smart_click('div.col-md-4 > a', 'Demo')

As long as you have left the same browser session open from the previous examples, you should see the same actions performed as in the `Click Test` Test Case.

To move this functionality back into your established Robot Test Cases, simply wrap this code in a method:

    from RobotOil import RobotOil

    oil_can = RobotOil()

    def python_clicking():
        oil_can.use_current_persistent_browser()
        oil_can.smart_click('span', 'Features', timeout=4)
        oil_can.smart_click('a', 'Main Features')
        oil_can.smart_click('div.col-md-4 > a', 'Demo')

And import the file into your `persistent_browser.robot` Test Suite:

    *** Settings ***
    Library           SeleniumLibrary
    Library           RobotOil
    Library           PATH_TO_CLICK_TEXT/click_text.py

From there, simply call `Python Clicking` from a Test Case of your choice:

    *** Test Cases ***
    Python Example
        Python Clicking

You may now leverage the already powerful SeleniumLibrary Keywords, with Smart Keyword enhancements, DIRECTLY from Python, and back into your Robot Test Cases!

### Loading Elements
Often times when testing web applications, asynchronous "loading elements" are implemented by web developers to inform their users that some part of the page is loading.
Common examples include the jQuery Ajax "spinner"

![ajax](https://github.com/Worakow1138/RobotOil/blob/main/images/ajax.jpg?raw=true)

While useful to web developers and site users, these "loading elements" can often obstruct the view of the elements that an automated test case is trying to interact with.
Writing around these loading elements for each expected interaction can be an enormous chore that Smart Keywords handle for us.

In a Robot Test Suite, copy the following example code:

    Ajax Test
        Open Persistent Browser    https://www.jqueryscript.net/demo/Simple-Flexible-Loading-Overlay-Plugin-With-jQuery-loadingoverlay-js/    chrome
        Smart Click    *    Extras "Progress" Test
        Smart Confirm Element    Visible    div    Element 2

This test clicks the `Extras "Progress" Test` button and then attempts to verify that a `div` with the text `Element 2` is visible.
The test, however, fails due to the Ajax spinner being in the way of the target element.

Rather than design our Test Case around this necessary evil of modern web development, create the following list of loading elements in your Test Suite:

    **** Variables ***
    @{loading_elements}    class:loadingoverlay

Then, wherever your call to `RobotOil` exists in your test framework, add this list as an argumen to the class:

    Library    RobotOil    ${loading_elements}

Upon running the same test again, you should find that `Smart Confirm Element` will now appropriately wait for the class:loadingoverlay elements to no longer be visible before attempting to confirm that the `Element 2` element is visible.

RobotOil may take multiple loading elements and will check to make sure each one is not visible before attempting to execute the main function of each Smart Keyword.

Loading elements can just as easily be given to Smart Keywords when called from Python as well, simply include the list of loading elements in the class instance for RobotOil:

    from RobotOil import RobotOil

    oil_can = RobotOil(['class:loadingoverlay'])

## Conclusion
I hope you enjoy the additional capabilities and ease-of-use that RobotOil brings to automated web testing with RobotFramework.

Please don't hesitate to reach out with questions or suggestions on [GitHub](https://github.com/Worakow1138/RobotOil)