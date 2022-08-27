# bee

## プロダクトビジョン

**永和社員のフィードバックをもらいながらみんなで育てていくプロダクト**

## サービス名

**Bee(Book Erabu Eiwa)**

## 環境構築

[VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)を利用してください。

### 環境変数の設定方法

1. .env.sample をコピーして .env ファイルを作成してください。
2. .env ファイルを編集し、適切な環境変数を設定してください。
3. 開発コンテナをビルドすると環境変数がコンテナ内に設定されます。

### 環境変数に設定する項目

- AWS_ACCESS_KEY_ID : AWS アクセスキー ID
- AWS_SECRET_ACCESS_KEY : AWS シークレットアクセスキー
- AWS_DEFAULT_REGION : AWS リージョン(ap-northeast-1 固定)

注 : AWS_ACCESS_KEY_ID などは、デプロイする場合に必要です。ただし、デプロイしない場合でも空の.env ファイルを作成する必要があります。作成しないと、VS Code Remote Development でコンテナを開くときにエラーになります。

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

### 性能測定方法

[こちらを参照](/docs/HOW_TO_MONITOR_PERFORMANCE.md)
