*** Settings ***
Resource  resource.robot
Resource  user_resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***
Sign In With Valid Credentials
    Create Tester Account
    Sign In With Testing Credentials
    Page Should Not Contain  Sign-in
    User Page Should Be Open
    Log Out

Sign In With Invalid Username
    Go To Signin Page
    Sign In With Credentials  a  password
    Sign In Should Fail With  Invalid username or password
    Sign In Input Data Should Remain On Page  a  password

Sign In With Incorrect Password
    Go To Signin Page
    Sign In With Credentials  testertester  wrongpassword
    Sign In Should Fail With  Invalid username or password
    Sign In Input Data Should Remain On Page  testertester  wrongpassword

*** Keywords ***

Register With Testing Credentials
    Register With Credentials   testertester  aaaaaaaa   aaaaaaaa

Create Tester Account
    Go To Register Page
    Register With Testing Credentials
    Go To Signin Page

Sign In With Testing Credentials
    Sign In With Credentials  testertester  aaaaaaaa

Sign In Should Fail With
    [Arguments]  ${error}
    Page Should Contain  ${error}
    Signin Page Should Be Open

Sign In Input Data Should Remain On Page
    [Arguments]  ${username}  ${password}
    Input Text  username  ${username}
    Input Text  password  ${password}