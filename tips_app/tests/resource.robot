*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}  127.0.0.1:5000
${BROWSER}  headlesschrome
${HOME URL}  http://${SERVER}
${REGISTER URL}  http://${SERVER}/register
${SIGNIN URL}  http://${SERVER}/signin
${ADD URL}  http://${SERVER}/add
${USER URL}  http://${SERVER}/user

*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}
    Maximize Browser Window

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

Go To Add Tips Page
    Go To  ${ADD URL}

Go To User Page
    Go to  ${USER URL}

User Page Should Be Open
    Title Should Be  user page

Log Out
    Click Link  Log out