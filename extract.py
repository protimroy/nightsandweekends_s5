"""
This module contains functions to extract data from various wearable APIs.
The APIs include:
- Whoop
- Oura
- Apple Watch/Health


"""
import json;
from typing import Any;
from authlib.common.urls import extract_params;
from authlib.integrations.requests_client import OAuth2Session;
from datetime import datetime, time, timedelta;


class ExtractBase( object ):
    """
    Base class for extracting data from various wearable APIs.
    """
    def __init__( self ):
        pass;

    def authenticate( self ):
        """
        Authenticate with the API.
        """
        raise NotImplementedError( "This method must be implemented in a derived class." );
    
    def get( self, url: str, params: dict = None ) -> Any:
        """
        Send a GET request to the API.

        Attributes:
            url (str): URL to send the request to.
            params (dict, optional): Parameters to include in the request.
        
        Returns:
            Any: Data returned from the request.

        Raises:
            ValueError: If the request is unsuccessful.
        """
        raise NotImplementedError( "This method must be implemented in a derived class." );


class Extract( ExtractBase ):
    """
    Class for extracting data from the Whoop API.

    Attributes:
        session (authlib.OAuth2Session): Requests session for accessing the API.
        user_id (str): User ID of the owner of the session. Will default to an empty
            string before the session is authenticated and then replaced by the correct
            user ID once a token is fetched.

    Raises:
        ValueError: If `start_date` is after `end_date`.
    """
    def __init__( self ):
        super().__init__();
        self.auth_url = ;

    def _auth_password_json( self, _client, _method, uri, headers, body ):
        body = json.dumps( dict( extract_params( body ) ) );
        headers["Content-Type"] = "application/json";

        return uri, headers, body


    def authenticate( self, authenticate : bool ) -> None:
        """Authenticate OAuth2Session by fetching token.

        If `user_id` is `None`, it will be set according to the `user_id` returned with
        the token.

        Args:
            kwargs (dict[str, Any], optional): Additional arguments for `fetch_token()`.
        """
        TOKEN_ENDPOINT_AUTH_METHOD = "password_json"  # noqa

        self._username = username
        self._password = password

        self.session = OAuth2Session(
            token_endpont=f"{self.auth_url}/oauth/token",
            token_endpoint_auth_method=self.TOKEN_ENDPOINT_AUTH_METHOD,
        )

        self.session.register_client_auth_method( ( self.TOKEN_ENDPOINT_AUTH_METHOD, self._auth_password_json ) );

        self.user_id = "";

        if authenticate:
            self.authenticate();
        

    def get( self, url: str, params: dict = None ) -> Any:
        pass;