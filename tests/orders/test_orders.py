from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_order(super_user_client, simple_user_client, api_client, product_factory):
    """Тест создания товара
        в создании товаров все получаеться, а вот в тестах постоянно ошибка 400. Не могу понять в чем дело
        пишет ожидался в debug видел , что пишет ожидался dict , а на вход отправили datatypes 
    """
    url = reverse('order-list')
    product1 = product_factory()
    product2 = product_factory()
    order = {
        "item": [
            {"product": product1.id, "quantity": 1},
            {"product": product2.id, "quantity": 1},
        ]
    }
    resp = super_user_client.post(url, order)
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert resp_json
    resp2 = simple_user_client.post(url, order)
    resp3 = api_client.post(url, order)
    assert resp2.status_code == HTTP_403_FORBIDDEN
    assert resp3.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_order(super_user_client, order_factory, simple_user_client):
    """Тест получение списка товаров"""
    url = reverse('order-list')
    order1 = order_factory()
    order2 = order_factory()
    resp = super_user_client.get(url)
    resp2 = simple_user_client.get(url)
    assert resp.status_code == HTTP_200_OK
    assert resp2.status_code == HTTP_200_OK
    resp_json = resp.json()
    resp2_json = resp.json()
    assert len(resp_json) == 2
    result_ids = {x['id'] for x in resp_json}
    result_ids2 = {x['id'] for x in resp2_json}
    assert {order1.id, order2.id} == result_ids
    assert {order1.id, order2.id} == result_ids2
