*** Keywords ***
Add Tip With Credentials
    [Arguments]  ${title}  ${url}
    Input Text  title  ${title}
    Input Text  url  ${url}
    Click Button  Save