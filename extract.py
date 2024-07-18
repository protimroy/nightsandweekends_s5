import json
import config
import requests
from OAuthSession import OAuthObject


import whoop_api
from whoop_api import WhoopAPI

class Extract():
    """
    """
    def __init__( self, wearable: str ):
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
        """
        oauth_token = self.user.session.token
        self.access_token = oauth_token['access_token']
        return self.access_token

    def _make_request( self, method: str, url_slug: str, **kwargs ) -> dict[str]:
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
        if self.wearable == "whoop":
            self.whoop = WhoopAPI();
            response = self._make_request( method="GET", url_slug= self.whoop( api ) );
            return response


#if __name__ == "__main__":
    #obj = Extract("whoop");
    #whoop = WhoopAPI();
    
    #response = obj._make_request( method="GET", url_slug= whoop('openapi_schema') );
    #print( response );

    #response = obj._make_request( method="GET", url_slug= whoop('profile') );
    #print( response );