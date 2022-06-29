# 性能測定

## 本ドキュメントの目的

BeeApp の動作性能を測定する方法を説明する

[BeeApp の性能測定をしたい #380](https://github.com/esminc/boat-bee/issues/380) 参照

※AWS 環境/Ngrok 環境の違いによる影響を考慮の上利用してください

## 手順

1. 測定したいファイルで以下のインポートを行う

```py
from bee_slack_app.utils.timer import StopWatch, location
```

2. 測定したい箇所を以下のように変更する

- 変更前

```py
何かの処理
```

- 変更後
  with ブロックで囲む（測定したい処理をインデントする）

```py
with StopWatch(location()):
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
  `say`の処理を with ブロックで囲む

```py
def hello_controller(app):
    @app.message("hello")
    def message_hello(message, say):
        # say() sends a message to the channel where the event was triggered
        with StopWatch(location()):
            say(f"Hey there!! <@{message['user']}>!")
```

- 動作させる
  ![image](https://user-images.githubusercontent.com/44659116/176076510-4da98f46-27bf-409d-a194-78e35c15d1bb.png)

- 測定結果例

```sh
time: 473.593ms         location: ('hello.py', 'message_hello', 11)
```
