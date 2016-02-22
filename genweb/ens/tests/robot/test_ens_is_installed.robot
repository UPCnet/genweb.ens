*** Settings ***
Documentation    Basic tests to check whether the ens package is installed
Library          Selenium2Library
Resource         plone/app/robotframework/selenium.robot

*** Variables ***
${browser}         chrome
${url_homepage}    ${PLONE_URL}/homepage

*** Test Cases ***
Homepage is shown
    Open browser           ${url_homepage}  ${browser}
    Page should contain    Inici
    Close browser

