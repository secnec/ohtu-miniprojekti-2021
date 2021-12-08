*** Settings ***
Resource  resource.robot
Resource  user_resource.robot
Resource  add_tip_resource.robot
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

Make Too Short Search
    Search With Credentials  a
    Search Should Fail With   Search text must be at least 3 characters long.

Make Unsuccessful Search
    Search With Credentials  thisdoesnotexist
    Search Should Fail With   No tip titles contain: thisdoesnotexist

Added Tips Appear On Home Page
    Go To Register Page
    Register With Credentials  username  password1  password1
    Go To Signin Page
    Sign In With Credentials  username  password1
    Add Tip With Credentials  sahara  https://en.wikipedia.org/wiki/Sahara
    Go To Main Page
    Page Should Contain  sahara


*** Keywords ***
Search With Credentials
    [Arguments]  ${searchtitle}
    Input Text  searchtitle  ${searchtitle}
    Click Button  Search

Search Should Fail With
    [Arguments]  ${error}
    Page Should Contain  ${error}

