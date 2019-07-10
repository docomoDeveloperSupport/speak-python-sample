#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2019, NTT DOCOMO, INC.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#  Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#  Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#  Neither the name of the NTT DOCOMO, INC. nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL NTT DOCOMO, INC. BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import json
import urllib.request
import os
import subprocess
import webbrowser
from time import sleep

TARGET = "trial"
CONFIG = {
    "trial":{
        "uds":"https://users-v2.sebastien.ai"
    }
}

def get_response(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode()
    print(html)
    return html


def fileoutput(filename, output):
    f = open("./." + TARGET + "_" + filename, "wb")
    f.write(output.encode())
    f.close()
    print("SAVE " + filename + " : " + output)


def fileexist(filename):
    return os.path.exists("./." + TARGET + "_" + filename)


def fileread(filename):
    f = open("./." + TARGET + "_" + filename, "r")
    output = f.read()
    print("READ " + filename + " : " + output)
    f.close()
    return output

if __name__ == '__main__':
    args = sys.argv
    if 1 < len(args):
        TARGET = args[1]
    if TARGET in CONFIG:
        uds = CONFIG[TARGET]["uds"]
    else:
        print(TARGET + " is illegal argument.")
        exit()
    if not fileexist("device_id"):
        device_id = input("AgentCraftで発行したデバイスIDを入力して下さい。>>> ")
        url = uds + "/dashboard/device_registration?confirm=yes&device_id=" + device_id
        fileoutput("device_id", device_id)
        print("UDSに自動接続します。SSH接続の場合は下記リンク（↓）を使ってブラウザ等でデバイスIDを自分のアカウントに登録して下さい。\n",url)
        webbrowser.open(url)
        sleep(8)
        i = input('Press any key AFTER registration >>> ')

    else:
        device_id = fileread("device_id")

    if not fileexist("device_token"):
        device_token_json = get_response(uds + "/api/req_device_token?device_id=" + device_id)
        try:
            device_token = json.loads(device_token_json)["device_token"]
        except:
            print("Failed to get Device Token. Check User Dashboard to make sure the Device ID is registered properly.")
            print("If the Device ID has been registered, please remove and register the Device ID again on User Dashboard.")
            print("Device Tokenの取得に失敗しました。Device IDがUser Dashboardで正しく登録されているのか確認して下さい。")
            os.remove("./." + TARGET + "_device_id")
            exit()
        fileoutput("device_token", device_token)
        refresh_token = json.loads(device_token_json)["refresh_token"]
        fileoutput("refresh_token", refresh_token)
    else:
        device_token = fileread("device_token")
        refresh_token = fileread("refresh_token")

        # DeviceToken validation
        validate_result = get_response(uds + "/api/validate_device_token?device_token=" + device_token)
        status = json.loads(validate_result)["status"]
        if status != "valid":
            # Update DeviceToken by RefreshToken
            device_token_json = get_response(uds + "/api/update_device_token?refresh_token=" + refresh_token)
            device_token = json.loads(device_token_json)["device_token"]
            if device_token == "" or device_token is None:
                os.remove("./." + TARGET + "_device_id")
                os.remove("./." + TARGET + "_device_token")
                os.remove("./." + TARGET + "_refresh_token")
                print("Failed to update Device Token by Refresh Token. Check User Dashboard to make sure the Device ID is registered properly.")
                print("If the Device ID has been registered, please remove and register the Device ID again on User Dashboard.")
                print("Device Tokenの更新に失敗しました。Device IDがUser Dashboardで正しく登録されているのか確認して下さい。")
            else:
                fileoutput("device_token", device_token)
                refresh_token = json.loads(device_token_json)["refresh_token"]
                fileoutput("refresh_token", refresh_token)
