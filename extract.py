"""
Created by Protim R. 2024
"""
import config
import requests
from OAuthSession import OAuthObject

from whoop_api import WhoopAPI

class Extract():
    """
    Extract data from a wearable device.

    Args:
        None

    Returns:
        None

    Attributes:
        wearable (str): The wearable to extract data from.
        conf (configparser.ConfigParser): The configuration settings.
        whoop_request_url (str): The Whoop request URL.
        whoop_auth_url (str): The Whoop authentication URL.
        user (OAuthObject): The OAuth user.

        _get_access_token (function): Get the OAuth access token.
        _make_request (function): Make a request to the API.
        _make_paginated_request (function): Make a paginated request to the API.

    Raises:
        None        
    """
    def __init__( self, wearable: str ):
        """
        Constructor for the Extract class.

        Args:
            wearable (str): The wearable to extract data from.

        Returns:
            None

        Attributes:
            wearable (str): The wearable to extract data from.
            conf (configparser.ConfigParser): The configuration settings.
            whoop_request_url (str): The Whoop request URL.
            whoop_auth_url (str): The Whoop authentication URL.
            user (OAuthObject): The OAuth user.

        Raises:
            None
        """
        self.wearable = wearable;
        if self.wearable == "whoop":
            self.conf = config.get_config("config.ini");

            # parse the configparser object
            auth_dict = dict( self.conf.items( "authentication" ) );
            url_dict = dict( self.conf.items( "urls" ) );

            # get the whoop authentication information
            # whoop is a subword in the key
            whoop_auth = { key: value for key, value in auth_dict.items() if "whoop" in key.lower() };
            whoop_url = { key: value for key, value in url_dict.items() if "whoop" in key.lower() };

            whoop_username = whoop_auth["whoop_username"];
            whoop_password = whoop_auth["whoop_password"];

            self.whoop_request_url = whoop_url["whoop_request_url"];
            self.whoop_auth_url = whoop_url["whoop_auth_url"];

            self.user = OAuthObject().authenticate( self.whoop_auth_url, whoop_username, whoop_password, authenticate = True );
            print( "User Authenticated:", self.user.is_authenticated() );

    def _get_access_token( self ):
        """
        Get the OAuth access token.

        Args:
            None

        Returns:
            str: The OAuth access token.

        Attributes:
            oauth_token (dict): The OAuth token.

        Raises:
            None
        """
        oauth_token = self.user.session.token
        self.access_token = oauth_token['access_token']
        return self.access_token

    def _make_request( self, method: str, url_slug: str, **kwargs ) -> dict[str]:
        """
        Make a request to the API.

        Args:
            method (str): The HTTP method to use for the request.
            url_slug (str): The URL slug for the request.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            dict[str]: The response data from the API.

        Attributes:
            access_token (str): The OAuth access token.
            headers (dict): The request headers.

        Raises:
            requests.exceptions.HTTPError: If the request fails.
        """
        # Get the OAuth token
        access_token = self._get_access_token()

        # Include the OAuth token in the request headers
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {access_token}'

        # Make the request with the OAuth token in the headers
        response = requests.request( method=method, url=self.whoop_request_url + url_slug, headers=headers, **kwargs )
        response.raise_for_status()
        return response.json()
    
    def _make_paginated_request( self, method: str, url_slug: str, **kwargs ) -> list[dict]:
        """
        Make a paginated request to the Whoop API.

        Args:
            method (str): The HTTP method to use for the request.
            url_slug (str): The URL slug for the request.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            list[dict]: The response data from the API.

        Attributes:
            access_token (str): The OAuth access token.
            headers (dict): The request headers.
            params (dict): The request parameters.
            response_data (list[dict]): The response data from the API.

        Raises:
            requests.exceptions.HTTPError: If the request fails.
        """
        # Get the OAuth token
        access_token = self._get_access_token()

        # Include the OAuth token in the request headers
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {access_token}'

        params = kwargs.pop( 'params', {} )
        response_data = list();

        # Make the request with the OAuth token in the headers

        while True:
            response = requests.request( method=method, url=self.whoop_request_url + url_slug, headers=headers, params=params )
            response.raise_for_status()
            response_data += response["records"]

            if next_token := response["next_token"]:
                params["nextToken"] = next_token

            else:
                break

        return response_data
    
    def main( self, api: str ):
        """
        Run the extract process.

        Args:
            api (str): The API to extract data from.

        Returns:
            dict: The extracted response.

        Attributes:
            self.whoop (WhoopAPI): The Whoop API object.

        Raises:
            None
        """
        if self.wearable == "whoop":

            # set the start date to the start of the previous day. i.e 12:01 AM
            # set the end date to the current day
            # dont use now because it will include the current time
        


            self.whoop = WhoopAPI();
            if api == 'cycle':
                # make paginated request
                start, end = self._format_dates( start_date, end_date );
                response = self._make_paginated_request( method="GET", url_slug= self.whoop( api ), params={"start": start, "end": end, "limit": 25} );
            else:
                response = self._make_request( method="GET", url_slug= self.whoop( api ) );
            return response


#if __name__ == "__main__":
    #obj = Extract("whoop");
    #whoop = WhoopAPI();
    
    #response = obj._make_request( method="GET", url_slug= whoop('openapi_schema') );
    #print( response );

    #response = obj._make_request( method="GET", url_slug= whoop('profile') );
    #print( response );