# SpeakSDK for Python サンプルアプリケーション
本ソースコードは株式会社NTTドコモが提供するドコモAIエージェントAPI [SpeakSDK](https://github.com/docomoDeveloperSupport/speak-python-sdk)のサンプルコードです。


## 動作条件
1. Raspberry Pi 3 Model B (OS: Raspbian 4.19.57)
1. Speak SDK(1.8.0以上)
1. Python3
1. pyuv(pipでインストール)

## GetDeviceToken.pyの使用
対話サービスを利用するにはデバイスIDの登録とデバイストークンの取得が必要です。  
スクリプト中における `client_secret` はダミー値であるため、ご自身で取得した値に書き換えて実行してください。

GetDeviceToken.pyを実行すると以下の様にデバイスID登録用のURLを表示して登録の完了を待機します。

```
$ python3 GetDeviceToken.py
Success to get DeviceID :xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
デバイスIDの取得に成功しました。
Please register DeviceID as your device on User Dashboard.
下記リンク（↓）を使ってブラウザ等でデバイスIDを自分のアカウントに登録して下さい。
https://doufr.aiplat.jp/device/regist?directAccess=true&deviceId=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Press any key AFTER registration >>> 
```

ブラウザでURLにアクセスしてデバイスID登録を完了させて下さい。  
登録にはGoogleアカウントまたはdアカウントによる認証が必要です。  
登録が完了したらEnterを入力して下さい。

```
Success to get DeviceToken : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
デバイストークンの取得に成功しました。
Success to get RefreshToken : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
リフレッシュトークンの取得に成功しました。
```

GetDeviceToken.pyはデバイストークンとリフレッシュトークンを取得して標準出力に表示します。

> リフレッシュトークンはデバイストークンの更新に使用します。  
GetDeviceToken.pyは取得したリフレッシュトークンを隠しファイルに保存しています。
デバイストークンの使用期限が切れた時はGetDeviceToken.pyを再び実行して下さい。
保存したリフレッシュトークンでデバイストークンを更新します。

## TrialApp.pyの使用
TrialApp.pyの以下の行に取得したデバイストークンを記述します。

```
102行目 sdk.set_device_token("PUT_YOUR_DEVICE_TOKEN")

```
TrialApp.pyを実行します。"start"が表示されると対話可能となります。

```
$ python3 TrialApp.py 
start

```

## TrialApp.pyの機能
マイクを使用した音声入力による対話が可能です。NLUから送信されたメタデータは標準出力に表示します。以下の例では「こんにちは」と発話しています。

```
$ python3 TrialApp.py 
start
{"systemText": {"utterance": "こんにちは。対話開発のトライアルをお楽しみください。", "expression": "こんにちは。対話開発のトライアルをお楽しみください。"}, "version": "sebastien-1.0.0", "type": "nlu_result", "option": {"switchAgent": {"agentType": "1", "agentId": "21_12_main"}}, "speaker_params": {"style_id": "jpn_JP-N-S0001-T001-E01", "voice_type": 1.0, "pitch": 12, "intonation": 10, "power_rate": 2.0, "speaker_id": "jpn_JP-N-S0001-T001-E01-SR0"}}
```

テキスト入力による対話が可能です。以下の例では「こんにちは」と入力しています。

```
$ python3 TrialApp.py 
start
こんにちは
{"systemText": {"utterance": "こんにちは。対話開発のトライアルをお楽しみください。", "expression": "こんにちは。対話開発のトライアルをお楽しみください。"}, "version": "sebastien-1.0.0", "type": "nlu_result", "option": {"switchAgent": {"agentType": "1", "agentId": "21_12_main"}}, "speaker_params": {"style_id": "jpn_JP-N-S0001-T001-E01", "voice_type": 1.0, "pitch": 12, "intonation": 10, "power_rate": 2.0, "speaker_id": "jpn_JP-N-S0001-T001-E01-SR0"}}
```

対話中は以下のコマンドが使用可能です。

| コマンド | 機能 |
| :----- | :--- |
| -m | 音声入力をOFFにします。 | 
| -u | 音声入力をONにします。 | 
| -q | 対話を終了します。 | 

## License
本サンプルコードは以下の修正BSDライセンスが適用されます。

[LICENSE.txt](/LICENSE.txt)

また本サンプルアプリケーションの動作に必要となる[SpeakSDK](https://github.com/docomoDeveloperSupport/speak-python-sdk)の利用にあたっては下記ソフトウェア開発キットの利用に関する規約が適用されます。規約をご確認のうえ利用をお願いいたします。

[ソフトウェア開発キットの利用に関する規約](https://github.com/docomoDeveloperSupport/speak-python-sdk/blob/master/LICENSE.md)

## Acknowledgments
This product includes software developed by the OpenSSL Project for use in the OpenSSL Toolkit. (http://www.openssl.org/)  
This product includes cryptographic software written by Eric Young (eay@cryptsoft.com)

## Author
[NTT DOCOMO, INC.](https://docs.sebastien.ai/)



