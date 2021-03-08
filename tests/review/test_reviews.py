from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_review(super_user_client, simple_user_client, api_client, product_factory):
    """Тест создания отзыва"""
    url = reverse('review-list')
    product1 = product_factory()
    review = {
        "product": product1.id,
        "mark": "FV",
        "text": "super puper"
    }
    resp = super_user_client.post(url, review)
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert resp_json
    resp2 = simple_user_client.post(url, review)
    resp3 = api_client.post(url, review)
    assert resp2.status_code == HTTP_201_CREATED
    assert resp3.status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_reviews(api_client, review_factory):
    """Тест получение списка отзывов"""
    url = reverse('review-list')
    review1 = review_factory()
    review2 = review_factory()
    resp = api_client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == 2
    result_ids = {x['id'] for x in resp_json}
    assert {review1.id, review2.id} == result_ids


@pytest.mark.django_db
def test_patch_review(simple_user_client, simple_user_client2, product_factory):
    """Тест обновления отзыва"""
    url = reverse('review-list')
    product1 = product_factory()
    review = {
        "product": product1.id,
        "mark": "FV",
        "text": "super puper"
    }
    resp = simple_user_client.post(url, review)
    resp_json = resp.json()
    rev_id = resp_json['id']
    review2 = {
        "text": "good good"
    }
    url2 = reverse('review-detail', args=[rev_id])
    resp2 = simple_user_client.patch(url2, review2)
    resp3 = simple_user_client2.patch(url2, review2)
    assert resp2.status_code == HTTP_200_OK
    resp_json2 = resp2.json()
    assert resp_json2['text'] == review2['text']
    assert resp3.status_code == HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_review(simple_user_client, simple_user_client2, product_factory):
    """Тест удаление отзыва"""
    url = reverse('review-list')
    product1 = product_factory()
    review = {
        "product": product1.id,
        "mark": "FV",
        "text": "super puper"
    }
    resp = simple_user_client.post(url, review)
    resp_json = resp.json()
    rev_id = resp_json['id']
    url2 = reverse('review-detail', args=[rev_id])
    resp3 = simple_user_client2.delete(url2)
    resp2 = simple_user_client.delete(url2)
    assert resp2.status_code == HTTP_204_NO_CONTENT
    assert resp3.status_code == HTTP_403_FORBIDDEN
