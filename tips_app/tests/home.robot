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

Add Valid Tip Redirects To Own Page
    Sign In And Go To Add Tip Page
    Add Tip With Credentials  amazon  https://en.wikipedia.org/wiki/Amazon_rainforest
    Page Should Contain  Your own tips
    Log Out

Add Tip Without URL
    Sign In And Go To Add Tip Page
    Add Tip With Credentials  emptyurl  ${EMPTY}
    Adding Should Fail With  Tip must have an URL and a title at least 3 characters long.
    Tip Input Data Should Remain On Page  emptyurl  ${EMPTY}
    Log Out

Add Tip With Invalid Title
    Sign In And Go To Add Tip Page
    Add Tip With Credentials  sa  https://en.wikipedia.org/wiki/Sahara
    Adding Should Fail With  Tip must have an URL and a title at least 3 characters long.
    Tip Input Data Should Remain On Page  sa  https://en.wikipedia.org/wiki/Sahara
    Log Out

Make Too Short Search
    Search With Credentials  ?#
    Search Should Fail With   Search text must be at least 3 characters long.
    Search Input Data Should Remain  ?#

Make Unsuccessful Search
    Search With Credentials  thisdoesnotexist
    Search Should Fail With   No tip titles contain: thisdoesnotexist
    Search Input Data Should Remain  thisdoesnotexist

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

Unliking Reduces Like Count And Changes Button
    Go To Main Page

    Like Button For Specific Tip Should Be  amazon  Like
    Like Button For Specific Tip Should Be  sahara  Like

    Click Like Button On Tip  amazon
    Click Like Button On Tip  sahara

    Like Button For Specific Tip Should Be  amazon  Unlike
    Like Button For Specific Tip Should Be  sahara  Unlike

    Log Out
    Go To Register Page
    Register With Credentials  liker  liker12345  liker12345
    Go To Signin Page
    Sign In With Credentials  liker  liker12345
    Go To Main Page

    Click Like Button On Tip  amazon

    Log Out
    Go To Signin Page
    Sign In With Credentials  username  password1
    Go To Main Page

    Page Should Contain  2 likes
    Page Should Contain  1 likes

    Click Like Button On Tip  sahara
    Page Should Not Contain  1 likes

    Click Like Button On Tip  amazon
    Page Should Not Contain  2 likes
    Page Should Contain  1 likes

    Log Out
    Go To Signin Page
    Sign In With Credentials  liker  liker12345
    Go To Main Page

    Click Like Button On Tip  amazon
    Like Button For Specific Tip Should Be  amazon  Like
    Like Button For Specific Tip Should Be  sahara  Like
    Page Should Not Contain  1 likes
    Page Should Not Contain  Unlike

Deleted Tips Do Not Appear On Home Page
    Sign In And Go To Add Tip Page
    Add Tip With Credentials  sahara  https://en.wikipedia.org/wiki/Sahara
    Go To User Page
    Delete Tip
    Go To User Page
    Page Should Not Contain  sahara

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

Search Input Data Should Remain
    [Arguments]  ${searchtitle}
    Input Text  searchtitle  ${searchtitle}

Tip Input Data Should Remain On Page
    [Arguments]  ${title}  ${url}
    Input Text  title  ${title}
    Input Text  url  ${url}

Click Like Button On Tip
    [Arguments]  ${tip_title}
    Click Button  xpath://a[text()[contains(.,"${tip_title}")]]/following-sibling::button[1]

Like Button For Specific Tip Should Be
    [Arguments]  ${tip_title}  ${button_text}
    Page Should Contain Button  //a[text()[contains(.,"${tip_title}")]]/following-sibling::button[contains(text(),"${button_text}")]