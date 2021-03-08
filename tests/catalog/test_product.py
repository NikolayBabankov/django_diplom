from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_product(super_user_client, simple_user_client, api_client):
    """Тест создания товара"""
    url = reverse('product-list')
    product = {'title': 'Honor 222',
               'description': 'phone chine',
               'price': 100}
    resp = super_user_client.post(url, product)
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert resp_json
    assert resp_json['title'] == product['title']
    resp2 = simple_user_client.post(url, product)
    resp3 = api_client.post(url, product)
    assert resp2.status_code == HTTP_403_FORBIDDEN
    assert resp3.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_product(api_client, product_factory):
    """Тест получение списка товаров"""
    url = reverse('product-list')
    product1 = product_factory()
    product2 = product_factory()
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == 2
    result_ids = {x['id'] for x in resp_json}
    assert {product1.id, product2.id} == result_ids


@pytest.mark.django_db
def test_patch_product(super_user_client, simple_user_client, api_client, product_factory):
    """Тест обновления товара"""
    product1 = product_factory()
    url = reverse('product-detail', args=[product1.id])
    product = {'title': 'Phone'}
    resp = super_user_client.patch(url, product)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json['title'] == product['title']
    resp2 = simple_user_client.patch(url, product)
    resp3 = api_client.patch(url, product)
    assert resp2.status_code == HTTP_403_FORBIDDEN
    assert resp3.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_product(super_user_client, simple_user_client, api_client, product_factory):
    """Тест удаление товара"""
    product1 = product_factory()
    url = reverse('product-detail', args=[product1.id])
    resp = super_user_client.delete(url)
    resp2 = simple_user_client.delete(url)
    resp3 = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    assert resp2.status_code == HTTP_403_FORBIDDEN
    assert resp3.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_collection(super_user_client, simple_user_client, api_client, product_factory):
    """Тест создания коллекции"""
    url = reverse('collection-list')
    product1 = product_factory()
    product2 = product_factory()
    collection = {
        "title": "Phone",
        "description": "Best Phone",
        "product": [product1.id, product2.id]}
    resp = super_user_client.post(url, collection)
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert resp_json
    resp2 = simple_user_client.post(url, collection)
    resp3 = api_client.post(url, collection)
    assert resp2.status_code == HTTP_403_FORBIDDEN
    assert resp3.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_collection(api_client, collection_factory):
    """Тест получение списка коллекций"""
    url = reverse('collection-list')
    collection1 = collection_factory()
    collection2 = collection_factory()
    resp5 = api_client.get(url)
    assert resp5.status_code == HTTP_200_OK
    resp_json = resp5.json()
    assert len(resp_json) == 2
    result_ids = {x['id'] for x in resp_json}
    assert {collection1.id, collection2.id} == result_ids


@pytest.mark.django_db
def test_patch_collection(super_user_client, simple_user_client, api_client, collection_factory, product_factory):
    """Тест обновления коллекции"""
    collection1 = collection_factory()
    url = reverse('collection-detail', args=[collection1.id])
    product1 = product_factory()
    product2 = product_factory()
    collection = {
        "title": "Phone",
        "description": "Best Phone",
        "product": [product1.id, product2.id]}
    resp = super_user_client.patch(url, collection)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json['title'] == collection['title']
    assert resp_json['product'] == [product1.id, product2.id]
    resp2 = simple_user_client.patch(url, collection)
    resp3 = api_client.patch(url, collection)
    assert resp2.status_code == HTTP_403_FORBIDDEN
    assert resp3.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_delete_collection(super_user_client, simple_user_client, api_client, collection_factory):
    """Тест удаление коллекции"""
    collection1 = collection_factory()
    url = reverse('collection-detail', args=[collection1.id])
    resp = super_user_client.delete(url)
    resp2 = simple_user_client.delete(url)
    resp3 = api_client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    assert resp2.status_code == HTTP_403_FORBIDDEN
    assert resp3.status_code == HTTP_401_UNAUTHORIZED
