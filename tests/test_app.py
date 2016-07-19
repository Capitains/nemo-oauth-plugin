from unittest import TestCase
from flask import Flask
from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from nemo_oauth_plugin import NemoOauthPlugin
import json


class TestPlugin(TestCase):
    def setUp(self):

        app = Flask("Nemo")
        app.secret_key="Test"
        app.debug = True
        self.auth_url = "https://example.org/123/auth"
        self.oauth = NemoOauthPlugin(app,name='perseids',oauth_access_token_url="https://example.org/123/login",
                                     oauth_authorize_url=self.auth_url,
                                     oauth_base_api_url="https://example.org/123/api",
                                     oauth_key='api_key',oauth_scope='read',oauth_secret='api_secret')
        nemo = Nemo(
            app=app,
            base_url="",
            chunker={"default": lambda x, y: level_grouper(x, y, groupby=30)},
            plugins=[self.oauth]
        )
        self.client = app.test_client()

    def test_login_route(self):
        """Ensure login route redirects """
        rv = self.client.get("/oauth/login")
        self.assertEqual(rv.location,
            str(self.auth_url+'?response_type=code&client_id=api_key&redirect_uri=http%3A%2F%2Flocalhost%2Foauth%2Fauthorized&scope=read'))


    def test_authorized_route(self):
        """Ensure authorized route responds """
        rv = self.client.get("/oauth/authorized")
        # TODO FIGURE OUT HOW TO TEST THIS

