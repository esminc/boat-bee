# pylint: disable=attribute-defined-outside-init
# pylint: disable=non-ascii-name
# pylint: disable=invalid-name

from moto import mock_dynamodb  # type: ignore

from bee_slack_app.repository.database import create_table
from bee_slack_app.repository.recommend_book_repository import RecommendBookRepository


@mock_dynamodb
class TestRecommendBookRepository:
    def setup_method(self, _):
        self.table = create_table()

    def test_複数のおすすめ本を取得できること(self):
        item = {
            "PK": "book_recommendation#user_id_0#2022-04-01T00:00:00+09:00",
            "GSI_PK": "book_recommendation",
            "GSI_0_SK": "user_id_0",
            "GSI_1_SK": "2022-04-01T00:00:00+09:00",
            "GSI_2_SK": "user_id_0#2022-04-01T00:00:00+09:00",
            "user_id": "user_id_0",
            "created_at": "2022-04-01T00:00:00+09:00",
            "book_recommendations": [
                {"ml_model_name": "ML-a", "isbn": "1234567890123"},
                {"ml_model_name": "ML-b", "isbn": "2345678901234"},
            ],
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book_recommendation#user_id_1#2022-04-01T00:00:00+09:00",
            "GSI_PK": "book_recommendation",
            "GSI_0_SK": "user_id_1",
            "GSI_1_SK": "2022-04-01T00:00:00+09:00",
            "GSI_2_SK": "user_id_1#2022-04-01T00:00:00+09:00",
            "user_id": "user_id_1",
            "created_at": "2022-04-01T00:00:00+09:00",
            "book_recommendations": [
                {"ml_model_name": "ML-a", "isbn": "9876543210987"},
                {"ml_model_name": "ML-b", "isbn": "8765432109876"},
            ],
        }

        self.table.put_item(Item=item)

        recommend_book_repository = RecommendBookRepository()

        result = recommend_book_repository.fetch("user_id_0")

        assert result["created_at"] == "2022-04-01T00:00:00+09:00"
        assert result["book_recommendations"] == [
            {"ml_model_name": "ML-a", "isbn": "1234567890123"},
            {"ml_model_name": "ML-b", "isbn": "2345678901234"},
        ]

    def test_おすすめ本の取得で存在しないユーザIDに対してはNoneを返すこと(self):
        item = {
            "PK": "book_recommendation#user_id_0#2022-04-01T00:00:00+09:00",
            "GSI_PK": "book_recommendation",
            "GSI_0_SK": "user_id_0",
            "GSI_1_SK": "2022-04-01T00:00:00+09:00",
            "GSI_2_SK": "user_id_0#2022-04-01T00:00:00+09:00",
            "user_id": "user_id_0",
            "created_at": "2022-04-01T00:00:00+09:00",
            "book_recommendations": [
                {"ml_model_name": "ML-a", "isbn": "1234567890123"},
                {"ml_model_name": "ML-b", "isbn": "2345678901234"},
            ],
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book_recommendation#user_id_1#2022-04-01T00:00:00+09:00",
            "GSI_PK": "book_recommendation",
            "GSI_0_SK": "user_id_1",
            "GSI_1_SK": "2022-04-01T00:00:00+09:00",
            "GSI_2_SK": "user_id_1#2022-04-01T00:00:00+09:00",
            "user_id": "user_id_1",
            "created_at": "2022-04-01T00:00:00+09:00",
            "book_recommendations": [
                {"ml_model_name": "ML-a", "isbn": "9876543210987"},
                {"ml_model_name": "ML-b", "isbn": "8765432109876"},
            ],
        }

        self.table.put_item(Item=item)

        recommend_book_repository = RecommendBookRepository()

        recommend_book_isbn = recommend_book_repository.fetch("user_id_not_exist")

        assert recommend_book_isbn is None

    def test_ひとつのMLがNoneでもおすすめ本を取得できること(self):
        item = {
            "PK": "book_recommendation#user_id_0#2022-04-01T00:00:00+09:00",
            "GSI_PK": "book_recommendation",
            "GSI_0_SK": "user_id_0",
            "GSI_1_SK": "2022-04-01T00:00:00+09:00",
            "GSI_2_SK": "user_id_0#2022-04-01T00:00:00+09:00",
            "user_id": "user_id_0",
            "created_at": "2022-04-01T00:00:00+09:00",
            "book_recommendations": [
                # ML-aのデータが存在しない
                {"ml_model_name": "ML-b", "isbn": "2345678901234"},
            ],
        }

        self.table.put_item(Item=item)

        item = {
            "PK": "book_recommendation#user_id_1#2022-04-01T00:00:00+09:00",
            "GSI_PK": "book_recommendation",
            "GSI_0_SK": "user_id_1",
            "GSI_1_SK": "2022-04-01T00:00:00+09:00",
            "GSI_2_SK": "user_id_1#2022-04-01T00:00:00+09:00",
            "user_id": "user_id_1",
            "created_at": "2022-04-01T00:00:00+09:00",
            "book_recommendations": [
                {"ml_model_name": "ML-a", "isbn": "9876543210987"},
                {"ml_model_name": "ML-b", "isbn": "8765432109876"},
            ],
        }

        self.table.put_item(Item=item)

        recommend_book_repository = RecommendBookRepository()

        result = recommend_book_repository.fetch("user_id_0")

        assert result["created_at"] == "2022-04-01T00:00:00+09:00"
        assert result["book_recommendations"] == [
            {"ml_model_name": "ML-b", "isbn": "2345678901234"},
        ]
