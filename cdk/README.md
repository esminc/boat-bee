# cdk

AWS CDK によるインフラ定義

```sh
# dev環境へのデプロイ
npm run deploy:dev

# prod環境へのデプロイ
npm run deploy:prod
```

# AWS Secrets Manager で設定している環境変数

Lambda で使用する環境変数を、AWS Secrets Manager を用いて設定しています。

- SLACK_APP_TOKEN [Bolt 入門ガイド](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started-http)を参照
- SLACK_BOT_TOKEN [Bolt 入門ガイド](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started-http)を参照
- SLACK_SIGNING_SECRET [Bolt 入門ガイド](https://slack.dev/bolt-python/ja-jp/tutorial/getting-started-http)を参照
- NOTIFY_POST_REVIEW_CHANNEL レビュー投稿通知を流す Slack チャンネル ID
- BEE_OPERATION_BOT_SLACK_WEBHOOK_URL Slack アプリでエラーが発生したときに通知する Slack アプリの Slack Incoming Webhook URL
