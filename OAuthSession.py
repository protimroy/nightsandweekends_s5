"""
This module contains functions to authenticate a user with the Whoop API.
Created by Protim R. 2024

ref:
[1] https://github.com/patrickloeber/whoop-analyzer/tree/main
"""
import os;
import sys;
import json;
from typing import Any;
from datetime import datetime, time, timedelta;

from authlib.common.urls import extract_params;
from authlib.integrations.requests_client import OAuth2Session;

import config;

#import prefect
#from prefect import task
#from prefect.engine.signals import SKIP
#from prefect.tasks.shell import ShellTask


class OAuthObjectBase( object ):
    """
    Base class for extracting data from various wearable APIs.
    """
    def __init__( self ):
        pass;

    def authenticate( self ):
        """
        Authenticate with the API.

        Args:
            None

        Returns:
            None
        
        Attributes:
            None
        
        Raises:
            NotImplementedError: If the method is not implemented in a derived class.
        """
        raise NotImplementedError( "This method must be implemented in a derived class." );
    
    def is_authenticated( self ):
        """
        Check if the session is authenticated.

        Args:
            None

        Returns:
            bool: Whether the session is authenticated.

        Attributes:
            None

        Raises: 
            NotImplementedError: If the method is not implemented in a derived class.
        """
        raise NotImplementedError( "This method must be implemented in a derived class." );


class OAuthObject( OAuthObjectBase ):
    """
    Class for extracting data from the Whoop API.

    Args:
        ExtractBase (ExtractBase): Base class for extracting data from various wearable APIs.
    
    Returns:
        None

    Attributes:
        session (authlib.OAuth2Session): Requests session for accessing the API.
        user_id (str): User ID of the owner of the session. Will default to an empty
            string before the session is authenticated and then replaced by the correct
            user ID once a token is fetched.
        auth_url (str): URL for the authentication endpoint.
        url (str): URL for the API.
        username (str): Username for the API.
        password (str): Password for the API.

        TOKEN_ENDPOINT_AUTH_METHOD (str): Authentication method for the token endpoint.

    Raises:
        ValueError: If `start_date` is after `end_date`.
    """
    def __init__( self ):
        """
        Constructor for the Extract class.

        Args:
            None
        
        Returns:
            None

        Attributes:
            None

        Raises:
            None
        """
        super().__init__();


    def _auth_password_json( self, _client, _method, uri, headers, body ):
        """
        Authenticate the OAuth2Session with the password JSON method.

        Args:
            _client (authlib.OAuth2Session): OAuth2Session client.
            _method (str): HTTP method.
            uri (str): URI for the request.
            headers (dict): Headers for the request.
            body (dict): Body for the request.

        Returns:
            tuple: URI, headers, and body for the request.

        Attributes:
            body (str): JSON string of the body.
            headers (dict): Headers for the request.

        Raises:
            None
        """
        body = json.dumps( dict( extract_params( body ) ) );
        headers["Content-Type"] = "application/json";

        return uri, headers, body


    def authenticate( self, url: str, username: str, password: str, authenticate: bool ) -> None:
        """Authenticate OAuth2Session by fetching token.

        If `user_id` is `None`, it will be set according to the `user_id` returned with
        the token.

        Args:
            username (str): Username for the API.
            password (str): Password for the API.
            url (str): URL for the API.
            authenticate (bool): Whether or not to authenticate the session.
        
        Returns:
            None
        
        Attributes:
            session (authlib.OAuth2Session): Requests session for accessing the API.
            user_id (str): User ID of the owner of the session. Will default to an empty
                string before the session is authenticated and then replaced by the correct
                user ID once a token is fetched.
            auth_url (str): URL for the authentication endpoint.
            
            TOKEN_ENDPOINT_AUTH_METHOD (str): Authentication method for the token endpoint.
        
        Raises:
            ValueError: If the request is unsuccessful.
        """
        if authenticate:
            self.TOKEN_ENDPOINT_AUTH_METHOD = "password_json"  # noqa

            self._username = str(username)
            self._password = str(password)

            self._auth_url = url

            self.session = OAuth2Session(
                token_endpont=f"{self._auth_url}/oauth/token",
                token_endpoint_auth_method=self.TOKEN_ENDPOINT_AUTH_METHOD,
            )

            self.session.register_client_auth_method( ( self.TOKEN_ENDPOINT_AUTH_METHOD, self._auth_password_json ) );

            self.user_id = "";

            self.session.fetch_token(
                url=f"{self._auth_url}/oauth/token",
                username=self._username,
                password=self._password,
                grant_type="password",
            )

            if not self.user_id:
                self.user_id = str(self.session.token.get("user", {}).get("id", ""))
            
            return self;

    def is_authenticated( self ) -> bool:
        """
        Check if the OAuth2Session is authenticated.

        Args:
            None

        Returns:
            bool: Whether the OAuth2Session has a token and is therefore authenticated.
        
        Attributes:
            None

        Raises:
            None
        """
        return self.session.token is not None
    
    def __enter__( self ):
        """
        Enter the OAuth2 Session.

        Args:
            None

        Returns:
            self (OAuthObject): OAuth2 Session.
        
        Attributes:
            None

        Raises:
            None
        """
        return self;

    def __exit__( self, exc_type, exc_value, traceback ):
        """
        Close the OAuth2 Session.

        Args:
            exc_type (type): Exception type.
            exc_value (Exception): Exception value.
            traceback (traceback): Traceback.

        Returns:
            None

        Attributes:
            None

        Raises:
            None
        """
        self.close();
    
    def close(self) -> None:
        """
        Close the OAuth2 Session.

        Args:
            None

        Returns:
            None

        Attributes:
            None

        Raises:
            None
        """
        self.session.close()


#if __name__ == "__main__":
    #conf = config.get_config("config.ini");

    # parse the configparser object
    #auth_dict = dict( conf.items( "authentication" ) );
    #url_dict = dict( conf.items( "urls" ) );
    
    # get the whoop authentication information
    # whoop is a subword in the key
    #whoop_auth = { key: value for key, value in auth_dict.items() if "whoop" in key.lower() };
    #whoop_url = { key: value for key, value in url_dict.items() if "whoop" in key.lower() };

    #whoop_username = whoop_auth["whoop_username"];
    #whoop_password = whoop_auth["whoop_password"];

    #whoop_request_url = whoop_url["whoop_request_url"];
    #whoop_auth_url = whoop_url["whoop_auth_url"];

    #user = OAuthObject().authenticate( whoop_auth_url, whoop_username, whoop_password, authenticate = True );
    #print( "User Authenticated:", user.is_authenticated() );
    #print( user.session.token );