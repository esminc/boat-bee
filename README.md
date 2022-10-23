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
