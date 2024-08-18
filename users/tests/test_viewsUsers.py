import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from recipe.models import Recipe
from users.models import Profile
from users.serializers import CustomUserSerializer, UserRegisterationSerializer, UserLoginSerializer, ProfileSerializer, ProfileAvatarSerializer, PasswordChangeSerializer

User = get_user_model()

@pytest.mark.django_db
class TestUserRegisterationAPIView:
    def setup_method(self):
        self.client = APIClient()

    def test_register_user(self):
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'tokens' in response.data
        assert User.objects.filter(email='newuser@example.com').exists()

@pytest.mark.django_db
class TestUserLoginAPIView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')

    def test_login_user(self):
        url = reverse('user-login')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpass'
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'tokens' in response.data

@pytest.mark.django_db
class TestUserLogoutAPIView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.refresh_token = RefreshToken.for_user(self.user).refresh_token

    def test_logout_user(self):
        url = reverse('user-logout')
        data = {'refresh': str(self.refresh_token)}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_205_RESET_CONTENT

@pytest.mark.django_db
class TestUserAPIView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_get_user(self):
        url = reverse('user-detail')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'testuser@example.com'

    def test_update_user(self):
        url = reverse('user-detail')
        data = {'username': 'updateduser'}
        response = self.client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'updateduser'

@pytest.mark.django_db
class TestUserProfileAPIView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, bio='Bio information')
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['bio'] == 'Bio information'

    def test_update_profile(self):
        url = reverse('user-profile')
        data = {'bio': 'Updated bio'}
        response = self.client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['bio'] == 'Updated bio'

@pytest.mark.django_db
class TestUserAvatarAPIView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user, avatar='avatar/test_image.png')
        self.client.force_authenticate(user=self.user)

    def test_get_avatar(self):
        url = reverse('user-avatar')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['avatar'] == 'avatar/test_image.png'

    def test_update_avatar(self):
        url = reverse('user-avatar')
        data = {'avatar': 'avatar/new_image.png'}
        response = self.client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['avatar'] == 'avatar/new_image.png'

@pytest.mark.django_db
class TestUserBookmarkAPIView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user)
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            desc='Delicious recipe',
            cook_time=30,
            ingredients='sugar, flour',
            procedure='mix ingredients',
            category=None,
            author=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_add_bookmark(self):
        url = reverse('user-bookmark', kwargs={'pk': self.user.id})
        data = {'id': self.recipe.id}
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert self.profile.bookmarks.count() == 1

    def test_remove_bookmark(self):
        self.profile.bookmarks.add(self.recipe)
        url = reverse('user-bookmark', kwargs={'pk': self.user.id})
        data = {'id': self.recipe.id}
        response = self.client.delete(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert self.profile.bookmarks.count() == 0

@pytest.mark.django_db
class TestPasswordChangeAPIView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='oldpassword123')
        self.client.force_authenticate(user=self.user)

    def test_change_password(self):
        url = reverse('user-password-change')
        data = {
            'old_password': 'oldpassword123',
            'new_password': 'newpassword123'
        }
        response = self.client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.user.refresh_from_db()
        assert self.user.check_password('newpassword123')

    def test_invalid_old_password(self):
        url = reverse('user-password-change')
        data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword123'
        }
        response = self.client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
