from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class WebpageTest(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user("temporary", "temp@gmail.com", "temporary")

    def test_01_webpage(self):
        rv = self.client.get("/")
        self.assertEqual(rv.status_code, 200)
        self.assertContains(rv, "IRON-AGE-DANUBE")
        rv = self.client.get("/accounts/login/")
        self.assertContains(rv, "Username")
        form_data = {"username": "temporary", "password": "temporary"}
        rv = self.client.post("/accounts/login/", form_data, follow=True)
        self.assertContains(rv, "temporary")
        rv = self.client.get("/logout", follow=True)
        self.assertContains(rv, "You've logged out")
        form_data = {"username": "non_exist", "password": "temporary"}
        rv = self.client.post("/accounts/login/", form_data, follow=True)
        self.assertContains(rv, "user does not exist")

    def test_02_imprint(self):
        url = reverse("webpage:imprint")
        rv = self.client.get(url)
        self.assertContains(rv, "Media owner")
