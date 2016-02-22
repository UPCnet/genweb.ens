*** Settings ***
Documentation    Test search ens user story
Library          Selenium2Library
Resource         plone/app/robotframework/selenium.robot
Test Setup       Open browser  ${url_search}  ${browser}
Test Teardown    Close browser

*** Variables ***
${selenium_speed}  .5 seconds
${browser}         chrome
${url_login}       ${PLONE_URL}/popup_login_form
${url_search}      ${PLONE_URL}/homepage
${url_create}      ${PLONE_URL}/++add++genweb.ens.ens

*** Test Cases ***
Search without filters
    [Documentation]        The user does not specify search filters and all the
    ...                    ens show up in the results.
    Set selenium speed     ${selenium_speed}
    Given a logged user
    And a set of ens
    When no filters are set
    Then all ens show up in the results

*** Keywords ***
Create ens
    [Arguments]   ${title}  ${acronim}
    Go to         ${url_create}
    Input text    form-widgets-title    ${title}
    Input text    form-widgets-acronim  ${acronim}
    Click button  form-buttons-save

A logged user
    Go to         ${url_login}
    Input text    inputEmail     admin
    Input text    inputPassword  secret
    Click button  submit

A set of ens
    Create ens    Amnistia Internacional  AI
    Create ens    Greenpeace  Gp
    Create ens    United Nations   UN

No filters are set
    Go to  ${url_search}
    Select from list by label    search_input_figura_juridica  Qualsevol
    Select from list by label    search_input_estat  Qualsevol
    Click button                 search_input_button

All ens show up in the results
    Element should contain    results  Amnistia Internacional
    Element should contain    results  Greenpeace
    Element should contain    results  United Nations

