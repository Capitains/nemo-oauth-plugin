# -*- coding: utf-8 -*-

from flask import redirect, url_for, session, request, jsonify
from flask_nemo.plugin import PluginPrototype
from pkg_resources import resource_filename
from flask_oauthlib.client import OAuth


class NemoOauthPlugin(PluginPrototype):
    """
    OAuth2 Client Plugin For Nemo

    :param app an instance of the parent flask app
           (must have sessions enabled via the secret_key)
    :type Flask
    :param oauth_name
    :type str
    :param oauth_key
    :type str
    :param oauth_secret
    :type str
    :param oauth_scope
    :type str
    :param oauth_access_token_url
    :type str
    :param oauth_authorize_url
    :type str
    :param oauth_request_token_url
    :type str
    :param oauth_base_api_url
    :type str
    :param oauth_callback_url
    :type str

    :ivar authobj the initialized OAuth Client Object
    :ivar authcallback the url for the oauth callback
    :cvar HAS_AUGMENT_RENDER: (False) Does not add a stack of render
    :cvar TEMPLATES the added templates
    :cvar CSS the added CSS
    :cvar ROUTES the added routes
    """

    HAS_AUGMENT_RENDER = False
    TEMPLATES = { "nemo_oauth_plugin": resource_filename("nemo_oauth_plugin","data/templates") }
    CSS = [resource_filename("nemo_oauth_plugin","data/assets/css/nemo_oauth_plugin.css")]
    ROUTES = [
        ("/oauth/login","r_oauth_login",["GET"]),
        ("/oauth/authorized","r_oauth_authorized",["GET"])
    ]

    def __init__(self,app,oauth_name=None,oauth_key=None,oauth_secret=None,oauth_scope=None,oauth_access_token_url=None,
                 oauth_authorize_url=None,oauth_request_token_url=None,oauth_base_api_url=None,oauth_callback_url=None,
                 *args,**kwargs):
        super(NemoOauthPlugin, self).__init__(*args,**kwargs)
        oauth = OAuth(app)
        self.authobj = oauth.remote_app(
            oauth_name,
            consumer_key=oauth_key,
            consumer_secret=oauth_secret,
            request_token_params={'scope':oauth_scope},
            base_url=oauth_base_api_url,
            request_token_url=oauth_request_token_url,
            access_token_method='POST',
            access_token_url=oauth_access_token_url,
            authorize_url=oauth_authorize_url
        )
        self.authobj.tokengetter(self.oauth_token)
        self.authcallback = oauth_callback_url

    def r_oauth_login(self):
        """
        Route for OAuth2 Login

        :return: Redirects to OAuth Provider Login URL
        """
        #return self.authobj.authorize(callback=url_for('.r_oauth_authorized', _external=True))
        callback_url = self.authcallback
        if callback_url is None:
            callback_url = url_for('.r_oauth_authorized', _external=True)
        return self.authobj.authorize(callback=callback_url)


    def r_oauth_authorized(self):
        """
        Route for OAuth2 Authorization callback
        :return: {"template"}
        """
        resp = self.authobj.authorized_response()
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error'],
                request.args['error_description']
            )
        session['oauth_token'] = (resp['access_token'], '')
        user = self.authobj.get('user')
        ## TODO this is too specific to Perseids' api model. We should externalize.
        session['oauth_user_uri'] = user.data['user']['uri']
        session['oauth_user_name'] = user.data['user']['full_name']
        return {
            "template": "nemo_oauth_plugin::authorized.html",
            "username": session['oauth_user_name']
        }

    def oauth_token(token=None):
        """
        tokengetter function
        :return: the current access token
        :rtype str
        """
        return session.get('oauth_token')
