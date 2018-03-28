from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User
from django.test import Client


# Create your tests here.

class GeneralTesting (TestCase):
    def test_basic_addition(self):

        # Test to establish that tests are working

        self.assertEqual(2 + 2, 4)

    def test_static_files(self):
        
        # If using static media correctly the result is not NONE
        
        result = finders.find('images/Picture1.jpg')
        self.assertIsNotNone(result)

    def main_test(self):
        
        # Test main returns an HTTP 200 status code (responds)
        
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        
class TestAboutPage(TestCase):
    def test_about_response(self):

        # Tests whether the about page url responds

        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_using_about_template(self):

        # Test template used to render about page

        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'tvtrail/about.html')


class TestIndexPage(TestCase):
    def test_Index(self):

        # Tests whether index page responds
        
        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)


class TestBuddiesPage(TestCase):
    def test_buddies_response(self):
        
        # Tests if buddies page responds
        
        response = self.client.get(reverse('show_buddies'), follow=True)
        self.assertEqual(response.status_code, 200)

class IndexPageTests(TestCase):

    # Test homepage returns an HTTP 200 status code (responds)
    def test_homepage(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    # Test index returns an HTTP 200 status code (responds)

    def test_indexpage(self):
        response = self.client.get(reverse('index'), follow=True) 
        self.assertEqual(response.status_code, 200)
    # Test that the index page uses login template when not logged in
    
    def test_index_using_login_template(self):
        response = self.client.get(reverse('index'), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html', 'tvtrail/base.html')
        
class LoginView(TestCase):
    
    # Test that the index page uses the index and base templates once logged in
    
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        
    def test_index_using_index_template(self):
        response = self.client.get('/tvtrail/', follow=True)
        self.assertTemplateUsed(response, 'tvtrail/index.html', 'tvtrail/base.html')
    # Test profile returns an HTTP 200 status code
    
    def test_profile(self):
        response = self.client.get(reverse('profile', kwargs={'username':'testuser'}), follow=True)
        self.assertEqual(response.status_code, 200)

    # Test that the profile page uses profile template and base template when logged in

    
    def test_profile_template(self):
        response = self.client.get(reverse('profile', kwargs={'username':'testuser'}), follow=True)
        self.assertTemplateUsed(response, 'tvtrail/profile.html', 'tvtrail/base.html')
