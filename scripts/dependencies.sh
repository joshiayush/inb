#!/bin/bash

function installDependencies() {
    # Function to install the program dependencies like selenium module, webdriver-manager, urllib module.
    echo "Installing dependencies..."
    echo "Installing Selenium"
    pip3 install selenium
    echo "Installing WebDriver Manager"
    pip3 install webdriver-manager
}
