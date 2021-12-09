*** Settings ***
Resource  resource.robot
Resource  user_resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Main Page

*** Test Cases ***
Tip Added By Others Does Not Show On User Page
    Sign In As User1
    Go To Add Tips Page
    Add Tip With Credentials  google  https://google.com
    Log Out
    Sign In As User2
    Go To User Page
    Page Should Not Contain  google

Tip Added By User Shows Up On User Page
    Sign In As User1
    Go To Add Tips Page
    Add Tip With Credentials  google  https://google.com
    Go To User Page
    Click Link  google
    Title Should Be  Google


*** Keywords ***
Sign In As User1
    Go To Register Page
    Register With Credentials  user1 aaaaaaaa  aaaaaaaa
    Go To Signin Page
    Sign In With Credentials  user1  aaaaaaaa

Sign In As User2
    Go To Register Page
    Register With Credentials  user2 bbbbbbbb  bbbbbbbb
    Go To Signin Page
    Sign In With Credentials  user2  bbbbbbbb