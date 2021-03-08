import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from model_bakery import baker


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def super_user_client():
    user = User.objects.create_superuser(
        'myadmin', 'myemail@s.com', 'mypassword')
    token = Token.objects.get_or_create(user_id=user.id)
    list_token = list(token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + list_token[0].key)
    return client


@pytest.fixture
def simple_user_client():
    user = User.objects.create_user('myuser', 'myemail@s.com', 'mypassword')
    token = Token.objects.get_or_create(user_id=user.id)
    list_token = list(token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + list_token[0].key)
    return client


@pytest.fixture
def simple_user_client2():
    user = User.objects.create_user('myuser2', 'myemail@s.com', 'mypassword')
    token = Token.objects.get_or_create(user_id=user.id)
    list_token = list(token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + list_token[0].key)
    return client


@pytest.fixture
def product_factory():
    def factory(**kwargs):
        return baker.make('Product', **kwargs)
    return factory


@pytest.fixture
def collection_factory():
    def factory(**kwargs):
        return baker.make('Collection', **kwargs)
    return factory


@pytest.fixture
def review_factory():
    def factory(**kwargs):
        return baker.make('Review', **kwargs)
    return factory


@pytest.fixture
def order_factory():
    def factory(**kwargs):
        return baker.make('Order', **kwargs)
    return factory
