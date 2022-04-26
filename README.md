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
