*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlesschrome
${DELAY}  0.3 seconds
${HOME URL}  http://${SERVER}
${REGISTER URL}  http://${SERVER}/register
${SIGNIN URL}  http://${SERVER}/signin

*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}

Go To Main Page
    Go To  ${HOME URL}

Register Page Should Be Open
    Title Should Be  Register

Go To Signin Page
    Go To  ${SIGNIN URL}

Signin Page Should Be Open
    Title Should Be  Signin
