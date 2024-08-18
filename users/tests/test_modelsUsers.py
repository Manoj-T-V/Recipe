import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from recipe.models import Recipe
from users.models import CustomUser, Profile

User = get_user_model()

@pytest.mark.django_db
class TestCustomUserModel:
    def test_create_user_with_email(self):
        user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')
        assert user.email == 'testuser@example.com'
        assert user.username == 'testuser'
        assert user.check_password('testpass')
        assert str(user) == 'testuser@example.com'

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='admin@example.com', username='admin', password='adminpass')
        assert superuser.email == 'admin@example.com'
        assert superuser.is_superuser
        assert superuser.is_staff
        assert str(superuser) == 'admin@example.com'

    def test_str_method(self):
        user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')
        assert str(user) == 'testuser@example.com'

@pytest.mark.django_db
class TestProfileModel:
    def setup_method(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            desc='Delicious recipe',
            cook_time=30,
            ingredients='sugar, flour',
            procedure='mix ingredients',
            category=None,  # Adjust if you have a default category
            author=self.user
        )
        self.profile = Profile.objects.create(user=self.user)
    
    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        assert profile.user == self.user
        assert profile.bookmarks.count() == 0
        assert profile.avatar is None
        assert profile.bio == ''

    def test_profile_str_method(self):
        profile = Profile.objects.get(user=self.user)
        assert str(profile) == 'testuser'

    def test_profile_bookmarks(self):
        self.profile.bookmarks.add(self.recipe)
        assert self.profile.bookmarks.count() == 1
        assert self.recipe in self.profile.bookmarks.all()
    
    def test_profile_avatar(self):
        self.profile.avatar = 'avatar/test_image.png'
        self.profile.save()
        assert self.profile.avatar.name == 'avatar/test_image.png'
