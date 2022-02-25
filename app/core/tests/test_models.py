from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from core import models
from core.models import Tag, Ingredient

def sample_user(email='test@something.dev', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class Modeltest(TestCase):
    
    def test_create_user_email_successful(self):
        """Test creating a new user with email is successful"""
        email = "test@somehing.dev"
        password = "Testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test whether the email for a new user is normalized"""
        email = 'test@SOMETHING.DEV'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_invalid_user_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@something.dev',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the Recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Chilly Cheese Fries',
            time_minutes = 15,
            price = 5.00,

        )

        self.assertEqual(str(recipe), recipe.title)
    
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'upload/recipe/{uuid}.jpg'

        self.assertEqual(file_path,exp_path)

