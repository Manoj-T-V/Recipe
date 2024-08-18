import pytest
from recipe.models import Recipe, RecipeCategory, RecipeLike
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestRecipeModels:
    def setup_method(self):
        self.user = User.objects.create(username='testuser')
        self.category = RecipeCategory.objects.create(name='Dessert')

    def test_recipe_creation(self):
        recipe = Recipe.objects.create(
            title='Test Recipe',
            desc='Delicious recipe',
            cook_time=30,
            ingredients='sugar, flour',
            procedure='mix ingredients',
            category=self.category,
            author=self.user
        )
        assert recipe.title == 'Test Recipe'
        assert recipe.category == self.category
        assert recipe.author == self.user

    def test_recipe_like_creation(self):
        recipe = Recipe.objects.create(
            title='Another Recipe',
            desc='Yummy recipe',
            cook_time=40,
            ingredients='chocolate, milk',
            procedure='stir well',
            category=self.category,
            author=self.user
        )
        recipe_like = RecipeLike.objects.create(user=self.user, recipe=recipe)
        assert recipe_like.user == self.user
        assert recipe_like.recipe == recipe

    def test_recipe_like_count(self):
        recipe = Recipe.objects.create(
            title='Another Test Recipe',
            desc='Yummy recipe',
            cook_time=40,
            ingredients='chocolate, milk',
            procedure='stir well',
            category=self.category,
            author=self.user
        )
        RecipeLike.objects.create(user=self.user, recipe=recipe)
        assert recipe.likes.count() == 1
