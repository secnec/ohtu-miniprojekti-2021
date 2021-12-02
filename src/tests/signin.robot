*** Settings ***
Resource  resource.robot
Resource  register_resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***
Sign In With Valid Credentials
    Create Tester Account
    Sign In With Testing Credentials
    Add Tips Page Should Be Open

Sign In With Invalid Username
    Go To Signin Page
    Sign In With Credentials  a  password
    Signin Page Should Be Open

Sign In With Incorrect Password
    Go To Signin Page
    Sign In With Credentials  testertester  wrongpassword
    
*** Keywords ***

Register With Testing Credentials
    Register With Credentials   testertester  aaaaaaaa   aaaaaaaa

Create Tester Account
    Go To Register Page
    Register With Testing Credentials
    Go To Signin Page

Sign In With Credentials
    [Arguments]  ${username}  ${password}
    Input Text  username  ${username}
    Input Password  password  ${password}
    Click Button  Sign in

Sign In With Testing Credentials
    Sign In With Credentials  testertester  aaaaaaaa