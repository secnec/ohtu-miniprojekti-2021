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

Add Tip Without Sign In
    Go To Add Tips Page
    Page Should Contain  Please sign in to add a tip.

Add Tip Without URL
    Sign In And Go To Add Tip Page
    Add Tip With Credentials  emptyurl  ${EMPTY}
    Adding Should Fail With  Tip must have an URL and a title at least 3 characters long.
    Log Out

Add Tip With Invalid Title
    Sign In And Go To Add Tip Page
    Add Tip With Credentials  sa  https://en.wikipedia.org/wiki/Sahara
    Adding Should Fail With  Tip must have an URL and a title at least 3 characters long.
    Log Out

Make Too Short Search
    Search With Credentials  a
    Search Should Fail With   Search text must be at least 3 characters long.

Make Unsuccessful Search
    Search With Credentials  thisdoesnotexist
    Search Should Fail With   No tip titles contain: thisdoesnotexist

Added Tips Appear On Home Page
    Sign In And Go To Add Tip Page
    Add Tip With Credentials  sahara  https://en.wikipedia.org/wiki/Sahara
    Go To Main Page
    Page Should Contain  sahara
    Click Link  sahara
    Title Should Be  Sahara - Wikipedia
    Go To Main Page
    Log Out

Make Successful Search
    Sign In And Go To Add Tip Page
    Add Tip With Credentials  sahara  https://en.wikipedia.org/wiki/Sahara
    Go To Main Page
    Search With Credentials  sahara
    Page Should Contain  sahara
    Log Out

User Page Without Sign In
    Go To User Page
    Page Should Contain  Please sign in to view your own tips.

Like Button Visible When Signed In
    Sign In And Go To Add Tip Page
    Add Tip With Credentials  Tip  https://en.wikipedia.org/wiki/Tip
    Log Out
    Click Link  Index
    Page Should Not Contain  Like
    Go To Signin Page
    Sign In With Credentials  username  password1
    Click Link  Index
    Page Should Contain  Like

*** Keywords ***
Search With Credentials
    [Arguments]  ${searchtitle}
    Input Text  searchtitle  ${searchtitle}
    Click Button  Search

Search Should Fail With
    [Arguments]  ${error}
    Page Should Contain  ${error}
    
Adding Should Fail With
    [Arguments]  ${error}
    Page Should Contain  ${error}

Sign In And Go To Add Tip Page
    Go To Register Page
    Register With Credentials  username  password1  password1
    Go To Signin Page
    Sign In With Credentials  username  password1
    Go To Add Tips Page