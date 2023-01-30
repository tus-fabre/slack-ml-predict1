# slack-ml-predict1

## Slack APIによるプログラミング　機械学習への応用編

Slack APIチュートリアル「NodeJSとSlack APIによるいまどきのネットワークプログラミング」の応用編として機械学習向けにアプリを公開する。

### CSVファイルから予測する

タイタニック号の生存者データをCSVファイルから学習し、どのような乗客が生存できるか予測する。

#### 必要なライブラリをインストールする

>$ pip install -r requirements.txt

#### 環境変数を設定する

- ファイルenv.tpl内のSLACK_BOT_TOKEN、SLACK_APP_TOKEN、SLACK_USER_TOKENに該当するトークン文字列を設定する
- env.tplをenv.batに名前を変え、バッチを実行する
  >$ ren env.tpl env.bat
  >
  >$ env.bat

#### 生存者を予測する

- タイタニック号の生存者データを学習し、どのような乗客が生存できるか予測する
- 起動方法
  >$ python predict_survivors.py

- 評価用CSVファイル（DATA/test_survivors.csv）をアップロードする
- Slack画面に評価結果CSVファイルが添付される。生存者番号のとなりに0（死亡と予測）あるいは1（生存と予測）と表記されることを確認する。
