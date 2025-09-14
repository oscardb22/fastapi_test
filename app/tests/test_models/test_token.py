from app.tests.test_factories.test_token import TokenFactory


class TestToken:
    token = None
    tokens = []

    def test_single_token(self, db_session):
        self.token = TokenFactory()
        assert bool(self.token)

    def test_bach_of_token(self, db_session):
        batch_size = 3
        self.tokens = TokenFactory.create_batch(batch_size)
        assert batch_size == len(self.tokens)
