*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}  library-of-reading-tips.herokuapp.com
${BROWSER}  headlesschrome
${DELAY}  0.3 seconds
${HOME URL}  https://${SERVER}
${REGISTER URL}  https://${SERVER}/register
${SIGNIN URL}  https://${SERVER}/signin

*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}

Go To Main Page
    Go To  ${HOME URL}

Go To Register Page
    Go To  ${REGISTER URL}

Register Page Should Be Open
    Title Should Be  Register

Go To Signin Page
    Go To  ${SIGNIN URL}

Signin Page Should Be Open
    Title Should Be  Signin

Add Tips Page Should Be Open
    Title Should Be  new reading tip

