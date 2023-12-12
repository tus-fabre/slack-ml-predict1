# slack-ml-predict1

## Slack APIによるプログラミング　機械学習への応用編

Slack APIチュートリアル「NodeJSとSlack APIによるいまどきのネットワークプログラミング」の応用編として機械学習向けにアプリを公開する。

### CSVファイルから予測する

タイタニック号の生存者データをCSVファイルから学習し、どのような乗客が生存できるか予測する。

#### 必要なパッケージをインストールする

コマンドライン上で次のコマンドを起動し、依存するPythonパッケージをインストールする。

```bash
pip install -r requirements.txt
```

#### 環境変数を設定する

本アプリを起動するには環境変数の設定が必要である。env.tplファイルをenv.batバッチファイルとしてコピーし、以下の環境変数を定義する。

```bash
copy env.tpl env.bat
```

|  変数名  |  説明  |
| ---- | ---- |
|  SLACK_BOT_TOKEN  | Botユーザーとして関連付けられたトークン。対象Slackワークスペースのアプリ設定 > [OAuth & Permissions] > [Bot User OAuth Token]から取得する。xoxb-で始まる文字列。 |
|  SLACK_APP_TOKEN  | 全ての組織を横断できるアプリレベルトークン。対象Slackワークスペースのアプリ設定 > [Basic Information] > [App-Level Tokens]から取得する。xapp-で始まる文字列。 |
|  SLACK_USER_TOKEN  | アプリをインストールまたは認証したユーザーに成り代わってAPIを呼び出すことができるトークン。対象Slackワークスペースのアプリ設定 > [OAuth & Permissions] > [User OAuth Token]から取得する。xoxp-で始まる文字列。 |
|  LOCAL_FOLDER  | Slackにアップロードしたファイルを暫定的に保存するローカルフォルダーの名前 |

#### 生存者を予測する

- タイタニック号の生存者データを学習し、どのような乗客が生存できるか予測する
- 起動方法

```bash
env.bat
python predict_survivors.py
```

- Slack入力欄の「＋」アイコンで、評価用CSVファイル（DATA/test_survivors.csv）をアップロードする
- Slack画面に予測結果CSVファイルが添付される。生存者番号のとなりに0（死亡と予測）あるいは1（生存と予測）と表記されることを確認する。

### 更新履歴

- 2023-12-12 ファイルアップロードをfiles_upload_v2()に変更
- 2023-02-01 初版
