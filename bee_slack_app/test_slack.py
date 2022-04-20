import json
import time

from slack_bolt import App
from slack_bolt.request import BoltRequest
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web import WebClient

from bee_slack_app.test_utils.mock_web_api_server import (
    cleanup_mock_web_api_server,
    setup_mock_web_api_server,
)


class TestMessage:

    signing_secret = "secret"
    valid_token = "xoxb-valid"
    signature_verifier = SignatureVerifier(signing_secret)
    mock_api_server_base_url = "http://localhost:8888"

    def setup_method(self):
        setup_mock_web_api_server(self)

    def teardown_method(self):
        cleanup_mock_web_api_server(self)

    def generate_signature(self, body: str, timestamp: str):
        return self.signature_verifier.generate_signature(
            body=body,
            timestamp=timestamp,
        )

    def build_headers(self, timestamp: str, body: str):
        return {
            "content-type": ["application/json"],
            "x-slack-signature": [self.generate_signature(body, timestamp)],
            "x-slack-request-timestamp": [timestamp],
        }

    def build_request_from_body(self, message_body: dict) -> BoltRequest:
        timestamp, body = str(int(time.time())), json.dumps(message_body)
        return BoltRequest(body=body, headers=self.build_headers(timestamp, body))

    def test_sample(self):

        web_client = WebClient(
            token=self.valid_token,
            base_url=self.mock_api_server_base_url,
        )

        app = App(
            client=web_client,
            signing_secret=self.signing_secret,
        )

        @app.message("hello")
        def message_hello(message, say):
            say("What's up?")

        request = self.build_request_from_body(message_body)
        response = app.dispatch(request)

        assert response.status == 200

        # time.sleep(1)  # wait a bit after auto ack()

        # assert self.mock_received_requests["/chat.postMessage"] == 1


message_body = {
    "token": "verification_token",
    "team_id": "T111",
    "enterprise_id": "E111",
    "api_app_id": "A111",
    "event": {
        "client_msg_id": "a8744611-0210-4f85-9f15-5faf7fb225c8",
        "type": "message",
        "text": "hello World!",  # @app.message("hello")より
        "user": "W111",
        "ts": "1596183880.004200",
        "team": "T111",
        "blocks": [
            {
                "type": "rich_text",
                "block_id": "ezJ",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [{"type": "text", "text": "Hello World!"}],
                    }
                ],
            }
        ],
        "channel": "C111",
        "event_ts": "1596183880.004200",
        "channel_type": "channel",
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1596183880,
    "authed_users": ["W111"],
}
message_body2 = {
    "token": "verification_token",
    "team_id": "T111",
    "enterprise_id": "E111",
    "api_app_id": "A111",
    "event": {
        "client_msg_id": "a8744611-0210-4f85-9f15-5faf7fb225c8",
        "type": "message",
        "text": "We've received 103 messages from you!",
        "user": "W111",
        "ts": "1596183880.004200",
        "team": "T111",
        "channel": "C111",
        "event_ts": "1596183880.004200",
        "channel_type": "channel",
    },
    "type": "event_callback",
    "event_id": "Ev111",
    "event_time": 1596183880,
    "authed_users": ["W111"],
}
