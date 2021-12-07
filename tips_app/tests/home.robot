*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***
Click Register Link
    Click Link  Register
    Register Page Should Be Open

Click Signin Link
    Click Link  Sign-in
    Signin Page Should Be Open