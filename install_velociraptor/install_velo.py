#!/usr/bin/python3
# Copyright (C) 2015-2022, Wazuh Inc.
# All rights reserved.

# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.
#
# Modified by sn0b4ll
# Date: 2025-08-15

import sys
import json
import datetime
import urllib.request
import subprocess
from pathlib import PureWindowsPath, PurePosixPath

# Get LOG_FILE from environment variable with fallback to default
LOG_FILE = "C:\\Program Files (x86)\\ossec-agent\\active-response\\active-responses.log"

# Set the link to your custom velo msi here
# Follow https://docs.velociraptor.app/docs/deployment/clients/ for the msi creation
VELO_MSI_URL="<replace with VELO-MSI>"

ADD_COMMAND = 0

OS_SUCCESS = 0
OS_INVALID = -1

class message:
    def __init__(self):
        self.alert = ""
        self.command = 0


def write_debug_file(ar_name, msg):
    with open(LOG_FILE, mode="a") as log_file:
        ar_name_posix = str(PurePosixPath(PureWindowsPath(ar_name[ar_name.find("active-response"):])))
        log_file.write(str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + " " + ar_name_posix + ": " + msg +"\n")


def setup_and_check_message(argv):

    # get alert from stdin
    input_str = ""
    for line in sys.stdin:
        input_str = line
        break

    write_debug_file(argv[0], input_str)

    try:
        data = json.loads(input_str)
    except ValueError:
        write_debug_file(argv[0], 'Decoding JSON has failed, invalid input format')
        message.command = OS_INVALID
        return message

    message.alert = data

    command = data.get("command")

    if command == "add":
        message.command = ADD_COMMAND
    else:
        message.command = OS_INVALID
        write_debug_file(argv[0], 'Not valid command: ' + command)

    return message


def main(argv):

    write_debug_file(argv[0], "Started")

    # validate json and get command
    msg = setup_and_check_message(argv)

    if msg.command < 0:
        sys.exit(OS_INVALID)

    if msg.command == ADD_COMMAND:

        """ Start Custom Key
        At this point, it is necessary to select the keys from the alert and add them into the keys array.
        """

        alert = msg.alert["parameters"]["alert"]
        keys = [alert["rule"]["id"]]

        """ End Custom Key """

        """ Start Custom Action Add """

        # Get the MSI URL from environment variable
        msi_url = VELO_MSI_URL
        
        try:
            # Download the MSI file
            msi_filename = "velo_install.msi"
            urllib.request.urlretrieve(msi_url, msi_filename)

            # Install the MSI using msiexec
            subprocess.run(["msiexec", "/i", msi_filename, "/quiet"], check=True)

            write_debug_file(argv[0], f"Successfully downloaded and installed {msi_filename}")
        except Exception as e:
            write_debug_file(argv[0], f"Failed to download or install MSI: {str(e)}")
        

        with open("ar-test-result.txt", mode="a") as test_file:
            test_file.write("Active response triggered by rule ID: <" + str(keys) + ">\n")

        """ End Custom Action Add """

    write_debug_file(argv[0], "Ended")

    sys.exit(OS_SUCCESS)


if __name__ == "__main__":
    main(sys.argv)
