*** Keywords ***

Register With Credentials
    [Arguments]  ${username}  ${password}  ${password_confirmation}
    Input Text  username  ${username}
    Input Password  password  ${password}
    Input Password  password_confirmation  ${password_confirmation}
    Click Button  Register