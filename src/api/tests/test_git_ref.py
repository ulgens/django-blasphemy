from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status

from core.testcases import TestCase


class GitRefTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = reverse("api:git-ref")

    def test_url(self):
        self.assertEqual(self.url, "/api/git_ref/")

    def test_get(self):
        with CaptureQueriesContext(connection) as db_ctx:
            # Run the request
            resp = self.client.get(self.url)

        # Check the response
        self.assertResponseStatus(resp, status.HTTP_200_OK)
        self.assertEqual(resp["Content-Type"], "application/json")

        # TODO: Check the response data

        # Check the db queries
        self.assertEqual(len(db_ctx), 0)
