import random
from random import randint

from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ...factories import SnippetFactory


@tag("api", "snippet")
class SnippetAPITests(APITestCase):
    response_keys = (
        "id",
        "title",
        "code",
        "language",
        "style",
    )

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        # Create sample objects
        cls.instance_number = randint(10, 20)  # noqa: S311
        instances = SnippetFactory.create_batch(cls.instance_number)

        cls.instance = random.choice(instances)  # noqa: S311

    @classmethod
    def get_detail_url(cls, pk):
        return reverse(
            "api:snippet-detail",
            kwargs={"pk": pk},
        )

    @classmethod
    def get_list_url(cls):
        return reverse("api:snippet-list")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.detail_url = cls.get_detail_url(pk=cls.instance.pk)
        cls.list_url = cls.get_list_url()

    def test_detail_url(self):
        self.assertEqual(self.detail_url, f"/api/snippets/{self.instance.pk}/")

    def test_detail(self):
        with self.assertNumQueries(1):
            # Run the request
            resp = self.client.get(self.detail_url)

        # Check the response
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        api_response_keys = data.keys()
        self.assertSetEqual(set(api_response_keys), set(self.response_keys))

    def test_list_url(self):
        self.assertEqual(self.list_url, "/api/snippets/")

    def test_list(self):
        with self.assertNumQueries(1):
            # Run the request
            resp = self.client.get(self.list_url)

        # Check the response
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        # Assumes self.instance_number < settings.REST_FRAMEWORK["PAGE_SIZE"]
        self.assertEqual(len(data["results"]), self.instance_number)

        api_response_keys = data["results"][0].keys()
        self.assertSetEqual(set(api_response_keys), set(self.response_keys))
