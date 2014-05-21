from django.test import TestCase
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from social.tests.strategy import TestStrategy
from social.utils import module_member
from social.tests.models import TestStorage
from django.test.client import RequestFactory

from auth.forms import AdminUserCreationForm, UserRegistrationForm, LoginForm
from auth.pipeline import get_username, facebook_gender, require_email
from auth.middleware import UpdateProfileMiddleware
from auth.models import CustomerProfile, BusinessProfile

class AdminUserCreationFormTestCase(TestCase):
        
    def test_init(self):
        form = AdminUserCreationForm()
        self.assertTrue(form.fields["email"].required)
        self.assertTrue(form.fields["password1"].required)
        self.assertTrue(form.fields["password2"].required)
        self.assertTrue(form.fields["user_type"].required)
        self.assertTrue(isinstance(form.fields["user_type"].widget, forms.widgets.Select))
        self.assertFalse(form.fields["username"].required)
        self.assertTrue(isinstance(form.fields["username"].widget, forms.widgets.HiddenInput))
    
    def test_clean(self):
        data = {'password1':"123456", 'password2':'123456', 'email':"test@test.com", 'user_type':"C"}
        form = AdminUserCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "C_test@test.com")
        form.save()

        data = {'password1':"123456", 'password2':'123456', 'email':"test@test.com", 'user_type':"C"}
        form2 = AdminUserCreationForm(data=data)
        self.assertFalse(form2.is_valid())
        
        self.assertEqual(form2.errors["username"], ["User with this Username already exists."])

        data = {'password1':"123456", 'password2':'123456', 'email':"test@test.com", 'user_type':"B"}
        form2 = AdminUserCreationForm(data=data)
        self.assertTrue(form2.is_valid())
        form.save()

class UserRegistrationFormTestCase(TestCase):
        
    def test_init(self):
        form = UserRegistrationForm()
        self.assertTrue(form.fields["email"].required)
        self.assertTrue(form.fields["password1"].required)
        self.assertTrue(form.fields["password2"].required)
        self.assertTrue(form.fields["tos"].required)
        self.assertFalse(form.fields["username"].required)
        self.assertTrue(isinstance(form.fields["username"].widget, forms.widgets.HiddenInput))
        

    def test_clean(self):
        data = {'password1':"123456", 'password2':'123456', 'email':"test@test.com", "tos":True}
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())
        if settings.USER_TYPE == "Customer":
            self.assertEqual(form.cleaned_data["username"], "C_test@test.com")
            u = User(username="C_test@test.com", email = "test@test.com").save()
            data = {'password1':"123456", 'password2':'123456', 'email':"test@test.com", "tos":True}
            form = UserRegistrationForm(data=data)
            self.assertFalse(form.is_valid())
        
        else:
            self.assertEqual(form.cleaned_data["username"], "B_test@test.com")
            u = User(username="B_test@test.com", email = "test@test.com").save()
            data = {'password1':"123456", 'password2':'123456', 'email':"test@test.com", "tos":True}
            form = UserRegistrationForm(data=data)
            self.assertFalse(form.is_valid())

class  LoginFormTestCase(TestCase):
    def setUp(self):
        super().setUp()

        u = User(username="C_test@test.com", email = "test@test.com")
        u.set_password("123456")
        u.save()
        
        u = User(username="B_test@test.com", email = "test@test.com")
        u.set_password("123456")
        u.save()
            
    def test_clean(self):
        
        data={"email":"test@test.com", "password":"123456"}
        form = LoginForm(data=data)
        
        self.assertTrue(form.is_valid())
        if settings.USER_TYPE == "Customer":
            self.assertEqual(form.cleaned_data["username"], "C_test@test.com")
            self.assertEqual(form.user_cache.username, "C_test@test.com")
        else:
            self.assertEqual(form.cleaned_data["username"], "B_test@test.com")
            self.assertEqual(form.user_cache.username, "B_test@test.com")



class GetUsernamePipelineTestCase(TestCase):
    def test_get_username(self):
        details = {"email":"test@test.com"}
        result = get_username(object(), details = details, user=None, is_new=True, pipeline_index = 0)
        if settings.USER_TYPE == "Customer":
            self.assertEqual(result["username"], "C_test@test.com")
        else:
            self.assertEqual(result["username"], "B_test@test.com")

        details = {"email":"test@test.com"}
        result = get_username(object(), details = details, user=None, is_new=False, pipeline_index = 0)
        self.assertEqual(result, {})

        details = {}
        result = get_username(object(), details = details, user=None, is_new=True, pipeline_index = 0)
        self.assertEqual(result, {})


class FacebookGenderTestCase(TestCase):
    def test_facebook_gender(self):        
        u = User(username="C_test@test.com", email = "test@test.com")
        u.set_password("123456")
        u.save()

        details = {"gender":"male"}
        
        if settings.USER_TYPE == "Customer":
            result = facebook_gender(object(), details = details, user=u, pipeline_index = 0, is_new=True)
            self.assertEqual(u.customer_profile.gender, "M")
        

class RequireEmailStrategyTestCase(TestCase):
    def test_require_email(self):
        backend = module_member('social.backends.facebook.FacebookOAuth2')
        strategy = TestStrategy(backend=backend, storage=TestStorage)
        details = {}
        #TODO: Test Pending, possible problem on python-social-auth
        #result = require_email(strategy, details = details, user=None, is_new=True, pipeline_index = 1)
        
        
class UpdateProfileMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        if settings.USER_TYPE == "Customer":
            self.user = User.objects.create_user(username='C_test@test.com', email='test@test.com', password='top_secret')
            self.user2 = User.objects.create_user(username='C_test2@test.com', email='test2@test.com', password='top_secret')
            customer_profile = CustomerProfile(user= self.user2, first_name="test", last_name="test", gender="M").save()
        else:
            self.user = User.objects.create_user(username='B_test@test.com', email='test@test.com', password='top_secret')
            self.user2 = User.objects.create_user(username='B_test2@test.com', email='test2@test.com', password='top_secret')
            business_profile = BusinessProfile(user=self.user2, company_name="Company").save()

    def test_process_request(self):
        request = self.factory.get('/')
        request.user = self.user
        response = UpdateProfileMiddleware().process_request(request)
        self.assertEqual(response.url, '/accounts/profile/edit/')
        self.assertEqual(response.status_code, 302)

        request = self.factory.get('/')
        request.user = self.user2
        response = UpdateProfileMiddleware().process_request(request)
        self.assertEqual(response, None)
