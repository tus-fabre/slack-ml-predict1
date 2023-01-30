#!/usr/bin/env python
# coding: utf-8
#
# [FILE] predict_survivors.py
#
# [DESCRIPTION]
#  タイタニック号の生存者を予測するSlackアプリトップファイル
#
# [NOTES]
#

import os, sys
import time
from pathlib import Path
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# BOTトークンからアプリを初期化する
slack_token=os.environ.get("SLACK_BOT_TOKEN")
if slack_token == None:
    print("環境変数が設定されていません")
    sys.exit()
app = App(token=slack_token)

# ここのパッケージは重いので、ここでロードする
from titanic_model import createModel, predictSurvivors

# アプリトークン
app_token = os.environ["SLACK_APP_TOKEN"]
# ユーザートークン：ファイルの内容を取得するため用いる
user_token = os.environ.get("SLACK_USER_TOKEN")
# ローカルフォルダー
csv_folder = os.environ.get("LOCAL_FOLDER")
# タイタニック生存者モデルを作成する
model = createModel("DATA/titanic_survivors.csv")

#
# [EVENT] message
#
# [DESCRIPTION]
#  次のメッセージを受信したときのリスナー関数
#   Unhandled request ({'type': 'event_callback', 'event': {'type': 'message', 'subtype': 'file_share'}})
#
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

#
# [EVENT] file_shared
#
# [DESCRIPTION]
#  ファイルを共有したときに起動するリスナー関数
#
# [NOTES]
#  対応可能なファイルタイプ：csv
#
@app.event("file_shared")
def file_shared(payload, client, ack, say):
    ack()

    # アップロードしたファイルのIDを取得する
    file_id = payload.get('file').get('id')
    
    # ファイル情報を取得する
    file_info = client.files_info(file = file_id).get('file')
    url = file_info.get('url_private')
    file_name = csv_folder + "/" + file_info.get('title')
    file_type = file_info.get('filetype')

    csv_file = None
    if file_type == 'csv':
        csv_file = file_name
    else:
        say(f"サポートしていないファイル形式です： {file_type}")
        return

    # ファイルの内容を取得する
    resp = requests.get(url, headers={'Authorization': 'Bearer %s' % user_token})
    
    # 一時的にファイルをローカルフォルダーに保存する
    save_file = Path(file_name)
    save_file.write_bytes(resp.content)

    # 予測結果用ファイルに生存者の予測を出力する
    epoch_time = time.time()
    output_file = csv_folder + "/Predicted-" + str(epoch_time) + ".csv"
    predictSurvivors(model, csv_file, output_file)

    # 予測結果ファイルをアップロードする
    channel_id = payload.get('channel_id')
    try:
        client.files_upload(
            channels=channel_id,
            title=output_file,
            file=output_file,
            initial_comment="予測結果ファイルを添付します",
        )
        os.remove(output_file)
    except Exception as e:
        print(e)

    os.remove(csv_file) 
   
#
# Start the Slack app
#
if __name__ == "__main__":
    print('⚡️Prediction App starts...')
    SocketModeHandler(app, app_token).start()

#
# END OF FILE
#