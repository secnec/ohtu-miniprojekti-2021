*** Settings ***
Resource  resource.robot
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

Go To Register Page and Register With Too Short Username
    Click Link  Register
    Register With Credentials  u  sala$ana1  sala$ana1
    Register Should Fail With  Username must be at least 3 characters long.
    
Go To Register Page and Register With Too Short Password
    Click Link  Register
    Register With Credentials  sampleuser  $ala1  $ala1
    Register Should Fail With  Password must be at least 8 characters long.

Go To Register Page and Register With Mismatched Password
    Click Link  Register
    Register With Credentials  sampleuser  $alasana1  $alasana4
    Register Should Fail With  Password and confirmation do not match.

    
*** Keywords ***
Register Should Succeed
    Signin Page Should Be Open
    # Ei mitään hajua miten voisi tarkastaa tietokannan herokusta, mutta
    # kirjatumistestit tietenkin varmistavat, että käyttäjä oikeasti luotiin.

Register Should Fail With
    [Arguments]  ${error}
    Page Should Contain  ${error}
    Register Page Should Be Open

Register With Sample Credentials
    Register With Credentials   bookreader  sala54n4!   sala54n4!

Register With Credentials
    [Arguments]  ${username}  ${password}  ${password_confirmation}
    Input Text  username  ${username}
    Input Password  password  ${password}
    Input Password  password_confirmation  ${password_confirmation}
    Click Button  Register