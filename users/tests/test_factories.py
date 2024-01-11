from django.contrib.auth.models import User
from django.test import TestCase

from ..factories import UserFactory
from ..models import Profile


class TestUsersFactory(TestCase):
    def test_create_single_default_user(self):
        user = UserFactory.create()
        db_user = User.objects.last()
        self.assertEqual(user.username, user.username)
        self.assertEqual(user.email, db_user.email)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_create_batch_default_user(self):
        for _ in range(10):
            UserFactory.create()

        self.assertEqual(User.objects.count(), 10)
        self.assertEqual(Profile.objects.count(), 10)
