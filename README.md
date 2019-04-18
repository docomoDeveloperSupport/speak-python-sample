# SpeakSDK for Python サンプルアプリケーション
本ソースコードは株式会社NTTドコモが提供するドコモAIエージェントAPI [SpeakSDK](https://github.com/docomoDeveloperSupport/speak-python-sdk)のサンプルコードです。


## 動作条件
1. Python3
1. Speak SDK(1.3.0以上)
1. pyuv(pipでインストール)

## GetDeviceToken.pyの使用
対話サービスを利用するにはデバイスIDの登録とデバイストークンの取得が必要です。  
GetDeviceToken.pyを実行すると以下の様にデバイスID登録用のURLを表示して登録の完了を待機します。

```
$ python3 GetDeviceToken.py
Success to get Device ID :xxxxxxxxxx
Please register above ID as your device on User Dashboard. https://users.sebastien.ai
デバイスIDの取得に成功しました。
下記リンク（↓）を使ってブラウザ等でデバイスIDを自分のアカウントに登録して下さい。
https://users.sebastien.ai/dashboard/device_registration?confirm=yes&device_id=xxxxxxxxxx

Press any key AFTER registration >>> 
```

ブラウザでURLにアクセスしてデバイスID登録を完了させて下さい。  
登録にはGoogleアカウントまたはdアカウントによる認証が必要です。  
登録が完了したらEnterを入力して下さい。

```
{
    "device_token": "xxxxxxx-xxx-xxx-xxxx-xxxxxxxxxxx", 
    "refresh_token": "ooooooo-ooo-ooo-oooo-ooooooooooo", 
    "status": "valid"
}
SAVE device_token : xxxxxxx-xxx-xxx-xxxx-xxxxxxxxxxx
SAVE refresh_token : ooooooo-ooo-ooo-oooo-ooooooooooo
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
{"speaker": "satoru", "systemText": {"utterance": "こんにちは。対話開発のトライアルをお楽しみください。", "expression": "こんにちは。対話開発のトライアルをお楽しみください。"}, "version": "sebastien-0.1.0", "type": "nlu_result", "option": {"switchAgent": {"agentType": "1", "agentId": "spftalk"}}}
```

テキスト入力による対話が可能です。以下の例では「しりとりお願い」と入力しています。

```
$ python3 TrialApp.py 
start
しりとりお願い
{"speaker": "satoru", "systemText": {"utterance": "しりとりに繋ぎます。", "expression": "しりとりに繋ぎます。"}, "version": "sebastien-0.1.0", "type": "nlu_result", "option": {"postback": {"payload": "#PB"}, "switchAgent": {"agentType": "1", "agentId": "spftalk"}}}
{"speaker": "rin", "systemText": {"utterance": "前回は29回続いたね。じゃあ、ぼくからいくよ！しりとりの「り」から始めるね。それじゃあ、「領主」。次は、「ユ」から始まる言葉を言ってね。", "expression": "前回は29回続いたね。じゃあ、ぼくからいくよ！しりとりの「り」から始めるね。それじゃあ、「領主」。次は、「ユ」から始まる言葉を言ってね。"}, "version": "sebastien-0.1.0", "type": "nlu_result", "option": {"switchAgent": {"agentType": "2", "agentId": "Shiritori"}}}
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



