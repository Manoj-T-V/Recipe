import pytest
from rest_framework import serializers
from recipe.serializers import RecipeCategorySerializer, RecipeSerializer, RecipeLikeSerializer
from recipe.models import Recipe, RecipeCategory, RecipeLike
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestRecipeCategorySerializer:
    def test_category_serializer(self):
        category = RecipeCategory.objects.create(name='Dessert')
        serializer = RecipeCategorySerializer(instance=category)
        expected_data = {'id': category.id, 'name': category.name}
        assert serializer.data == expected_data

@pytest.mark.django_db
class TestRecipeSerializer:
    def setup_method(self):
        self.user = User.objects.create(username='test_user')
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

    def test_recipe_serializer_data(self):
        serializer = RecipeSerializer(instance=self.recipe)
        expected_data = {
            'id': self.recipe.id,
            'category': {'id': self.category.id, 'name': self.category.name},
            'category_name': self.recipe.category.name,
            'picture': None,
            'title': self.recipe.title,
            'desc': self.recipe.desc,
            'cook_time': self.recipe.cook_time,
            'ingredients': self.recipe.ingredients,
            'procedure': self.recipe.procedure,
            'author': self.recipe.author.id,
            'username': self.recipe.author.username,
            'total_number_of_likes': self.recipe.get_total_number_of_likes(),
            'total_number_of_bookmarks': self.recipe.get_total_number_of_bookmarks()
        }
        assert serializer.data == expected_data

    def test_recipe_serializer_create(self):
        data = {
            'title': 'New Recipe',
            'desc': 'This is a new recipe',
            'cook_time': 45,
            'ingredients': 'eggs, milk',
            'procedure': 'mix ingredients',
            'category': {'name': 'Main Course'}
        }
        serializer = RecipeSerializer(data=data)
        assert serializer.is_valid()
        recipe = serializer.save(author=self.user)
        assert Recipe.objects.count() == 2
        assert recipe.title == 'New Recipe'
        assert recipe.category.name == 'Main Course'

    def test_recipe_serializer_update(self):
        data = {'title': 'Updated Recipe', 'category': {'name': 'Snacks'}}
        serializer = RecipeSerializer(instance=self.recipe, data=data, partial=True)
        assert serializer.is_valid()
        updated_recipe = serializer.save()
        assert updated_recipe.title == 'Updated Recipe'
        assert updated_recipe.category.name == 'Snacks'

@pytest.mark.django_db
class TestRecipeLikeSerializer:
    def setup_method(self):
        self.user = User.objects.create(username='test_user')
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
        self.recipe_like = RecipeLike.objects.create(user=self.user, recipe=self.recipe)

    def test_recipe_like_serializer_data(self):
        serializer = RecipeLikeSerializer(instance=self.recipe_like)
        expected_data = {'id': self.recipe_like.id, 'user': self.recipe_like.user.id, 'recipe': self.recipe_like.recipe.id}
        assert serializer.data == expected_data

    def test_recipe_like_serializer_create(self):
        data = {'user': self.user.id, 'recipe': self.recipe.id}
        serializer = RecipeLikeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        recipe_like = serializer.save()
        assert RecipeLike.objects.count() == 2
        assert recipe_like.recipe == self.recipe
        assert recipe_like.user == self.user
