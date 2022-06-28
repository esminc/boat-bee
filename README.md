# bee

## プロダクトビジョン

**永和社員のフィードバックをもらいながらみんなで育てていくプロダクト**

## サービス名

**Bee(Book Erabu Eiwa)**

## 環境構築

[VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)を利用してください。

デプロイする場合は、下記の環境変数をローカルマシン（コンテナ外）に設定する必要があります。

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

詳しくは、https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html を参照してください。

## 開発

```bash
# 依存パッケージのインストール
make init

# デプロイ
make deploy
```

### 環境変数

AWS 環境で環境変数を設定する場合は、AWS Secrets Manager を介して設定します。

ステージ環境毎に設定できます。

シークレット ID は、slack_secret\_<ステージ環境名>です。(例: slack_secret_dev)

設定できる環境変数

- SLACK_APP_TOKEN [Bolt 入門ガイド](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started-http)を参照
- SLACK_BOT_TOKEN [Bolt 入門ガイド](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started-http)を参照
- SLACK_SIGNING_SECRET [Bolt 入門ガイド](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started-http)を参照
- NOTIFY_POST_REVIEW_CHANNEL レビュー投稿通知を流す Slack チャンネル ID

## 性能測定方法

BeeApp の動作性能を測定する方法です。

[BeeApp の性能測定をしたい #380](https://github.com/esminc/boat-bee/issues/380) 参照

※AWS 環境/Ngrok 環境の違いによる影響を考慮の上利用してください

### 手順

1. 測定したいファイルで以下のインポートを行う

```py
from bee_slack_app.utils.timer import Timer, location
```

2. 測定したい箇所を以下のように変更する

- 変更前

```py
何かの処理
```

- 変更後
  with ブロックで囲む（測定したい処理をインデントする）

```py
with Timer(location()):
    何かの処理
```

3. 測定したい箇所を動作させる
4. ターミナルに以下のように測定結果が表示される

```sh

time: 3.115ms           location: ('home.py', 'update_home_view', 48)
time: 597.583ms         location: ('home.py', 'update_home_view', 65)
time: 2.534ms           location: ('home.py', 'update_home_view', 48)
time: 423.587ms         location: ('home.py', 'update_home_view', 65)
time: 670.071ms         location: ('hello.py', 'show_my_review', 15)
```

### 測定サンプル

- bee_slack_app/view_controller/hello.py

```py
def hello_controller(app):
    @app.message("hello")
    def message_hello(message, say):
        # say() sends a message to the channel where the event was triggered
        with Timer(location()):
            say(f"Hey there!! <@{message['user']}>!")
```

- 動作させる
  ![image](https://user-images.githubusercontent.com/44659116/176076510-4da98f46-27bf-409d-a194-78e35c15d1bb.png)

- 測定結果例

```sh
time: 473.593ms         location: ('hello.py', 'message_hello', 11)
```
