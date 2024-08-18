from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Recipe, RecipeLike
from django.contrib.auth.models import User

class RecipeAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(name='Test Recipe', author=self.user)
        self.recipe_list_url = reverse('recipe:recipe-list')
        self.recipe_detail_url = reverse('recipe:recipe-detail', kwargs={'pk': self.recipe.pk})
        self.recipe_like_url = reverse('recipe:recipe-like', kwargs={'pk': self.recipe.pk})
        self.client.login(username='testuser', password='testpass')

    def test_recipe_list(self):
        response = self.client.get(self.recipe_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_recipe_create(self):
        self.client.logout()  # Testing authentication
        response = self.client.post(reverse('recipe:recipe-create'), {
            'name': 'New Recipe',
            'description': 'This is a test recipe'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Authenticated user
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipe:recipe-create'), {
            'name': 'New Recipe',
            'description': 'This is a test recipe'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_recipe_detail(self):
        response = self.client.get(self.recipe_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Recipe')

    def test_recipe_update(self):
        response = self.client.patch(self.recipe_detail_url, {
            'name': 'Updated Recipe'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.name, 'Updated Recipe')

    def test_recipe_delete(self):
        response = self.client.delete(self.recipe_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_recipe_like(self):
        response = self.client.post(self.recipe_like_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(RecipeLike.objects.filter(user=self.user, recipe=self.recipe).exists())

        response = self.client.post(self.recipe_like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.delete(self.recipe_like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(RecipeLike.objects.filter(user=self.user, recipe=self.recipe).exists())

