*** Settings ***
Resource  resource.robot
Resource  user_resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***
Go To Register Page and Register
    Click Link  Register
    Register With Sample Credentials
    Register Should Succeed

Go To Register Page and Register With Existing Username
    Click Link  Register
    Register With Sample Credentials
    Register Should Fail With  Username is already taken.
    Registration Input Data Should Remain On Page  bookreader  sala54n4!   sala54n4!

Go To Register Page and Register With Too Short Username
    Click Link  Register
    Register With Credentials  u  sala$ana1  sala$ana1
    Register Should Fail With  Username must be at least 3 characters long.
    Registration Input Data Should Remain On Page  u  sala$ana1  sala$ana1

Go To Register Page and Register With Too Short Password
    Click Link  Register
    Register With Credentials  sampleuser  $ala1  $ala1
    Register Should Fail With  Password must be at least 8 characters long.
    Registration Input Data Should Remain On Page  sampleuser  $ala1  $ala1

Go To Register Page and Register With Mismatched Password
    Click Link  Register
    Register With Credentials  sampleuser  $alasana1  $alasana4
    Register Should Fail With  Password and confirmation do not match.
    Registration Input Data Should Remain On Page  sampleuser  $alasana1  $alasana4

*** Keywords ***
Register Should Succeed
    Signin Page Should Be Open

Register Should Fail With
    [Arguments]  ${error}
    Page Should Contain  ${error}
    Register Page Should Be Open

Register With Sample Credentials
    Register With Credentials   bookreader  sala54n4!   sala54n4!

Registration Input Data Should Remain On Page
    [Arguments]  ${username}  ${password}  ${password_confirmation}
    Input Text  username  ${username}
    Input Text  password  ${password}
    Input Text  password_confirmation  ${password_confirmation}