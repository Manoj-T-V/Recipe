import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from recipe.models import Recipe, RecipeCategory
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestRecipeViews:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.category = RecipeCategory.objects.create(name='Dessert')
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            desc='Delicious recipe',
            cook_time=30,
            ingredients='sugar, flour',
            procedure='mix ingredients',
            category=self.category,
            author=self.user
        )

    def test_get_recipes(self):
        url = reverse('recipe:recipe-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Test Recipe'

    def test_create_recipe(self):
        url = reverse('recipe:recipe-create')
        data = {
            'title': 'New Recipe',
            'desc': 'A new delicious recipe',
            'cook_time': 20,
            'ingredients': 'eggs, milk',
            'procedure': 'whisk together',
            'category': {'name': 'Main Course'}
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Recipe.objects.count() == 2
        assert Recipe.objects.latest('id').title == 'New Recipe'

    def test_like_recipe(self):
        url = reverse('recipe:recipe-like', kwargs={'pk': self.recipe.id})
        response = self.client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.recipe.likes.count() == 1

    def test_delete_recipe(self):
        url = reverse('recipe:recipe-detail', kwargs={'pk': self.recipe.id})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Recipe.objects.count() == 0
