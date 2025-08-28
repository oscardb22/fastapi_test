from apps.authentication.tests.test_factories.test_user import UserFactory


class TestUser:
    user = None
    users = []

    def test_single_user(self, db_session):
        self.user = UserFactory()
        assert bool(self.user)

    def test_bach_of_user(self, db_session):
        batch_size = 3
        self.users = UserFactory.create_batch(batch_size)
        assert batch_size == len(self.users)
