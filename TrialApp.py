# coding: utf-8
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
from speak import Speak, NluMetaData
import pyuv
import signal
import json

postbackAfterUtt=None

def on_started():
    print ("start")

def on_failed(ecode, failstr):
    print ("error occurred : %s(%d)" % (failstr, ecode))
    stop()

def on_meta_out(meta):
    meta_dict = json.loads(meta)
    if meta_dict["type"] != "nlu_result":
        return
    print(meta.strip())
    option = meta_dict["option"]
    if "postback" in option:
        postback = option["postback"]
        if "afterUtt" in postback and postback["afterUtt"]:
            global postbackAfterUtt
            postbackAfterUtt = postback
        else:
            put_postback(postback)

def on_play_end(data):
    global postbackAfterUtt
    if postbackAfterUtt is not None:
        put_postback(postbackAfterUtt)
        postbackAfterUtt = None

def put_postback(postback):
    if "clientData" in postback:
        put_meta(postback["payload"],postback["clientData"])
    else:
        put_meta(postback["payload"])

def put_meta(voiceText, clientData=None):
    meta = NluMetaData()
    meta.voiceText = voiceText
    if clientData is not None:
        meta.clientData = clientData
    meta.clientData["deviceInfo"] = dict(playTTS="on")
    sdk.put_meta(meta)

def poll(timer_handle):
    sdk.poll()

def on_stdin(handle, data, error):
    input = data.decode().strip()
    if input == "-q":
        stop()
    elif input == "-m":
        sdk.mute()
    elif input == "-u":
        sdk.unmute()
    else:
        put_meta(data.decode().strip())

def signal_cb(handle, signum):
    stop()

def stop():
    poll_timer.close()
    stdin_pipe.close()
    signal_h.close()

def fileread(filename):
    f = open("./." + filename, "r")
    output = f.read()
    print("READ " + filename + " : " + output)
    f.close()
    return output

# SDK初期化
sdk = Speak()
sdk.init()
sdk.set_url("wss://spf-v2.sebastien.ai/talk")
sdk.set_device_token(fileread("trial_device_token"))
sdk.set_on_play_end(on_play_end)
sdk.set_on_meta_out(on_meta_out)
# SDK開始
sdk.start(on_started, on_failed, False)
# pollingタイマ
loop = pyuv.Loop.default_loop()
poll_timer = pyuv.Timer(loop)
poll_timer.start(poll, 0, 0.2)
# 標準入力パイプ
stdin_pipe = pyuv.Pipe(loop)
stdin_pipe.open(sys.stdin.fileno())
stdin_pipe.start_read(on_stdin)
# SIGNALハンドラ
signal_h = pyuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)
# イベントループ開始
loop.run()
print ("\nstop")
