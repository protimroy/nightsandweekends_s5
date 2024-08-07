"""
Created by Protim R. 2024
"""
import requests;
import config;

class WhoopAPI():
    def __init__(self) -> None:
        super().__init__();
        self.conf = config.get_config( "config.ini" );
        self.url_dict = dict( self.conf.items( "urls" ) );

        self.schema = self._get_schema();

    def _get_schema( self ):
        """
        Get the OpenAPI schema.

        Args:
            None

        Returns:
            dict: The OpenAPI schema.

        Attributes:
            url (str): The URL to the OpenAPI schema.
            response (requests.models.Response): The response object.

        Raises:
            requests.exceptions.HTTPError: If the request fails.
        """

        url = self.url_dict['whoop_openapi_url'];
        
        response = requests.get( url );
        response.raise_for_status();
        return response.json(); 

    def _get_paths_object_endpoints( self ):
        """
        Get the paths object endpoints in a list. Each element is a relative path to an individual endpoint.
        The field name MUST begin with a slash. The path is appended to the basePath in order to construct the full URL.

        https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md#paths-object

        Args:
            None

        Returns:
            list : object endpoints.

        Attributes:
            None

        Raises: 
            ValueError: If the schema is empty.

        """
        if self.schema:
            if len( self.schema['paths'].keys() ) != 0:
                return self.schema['paths'].keys();
            else:
                raise ValueError( "Path keys are empty.")
        else:
            raise ValueError( "Schema is empty." );

    def _get_paths_item_object( self, key: str ):
        """
        Get the paths object item.

        Args:
            key (str): The key to the paths object.

        Returns:
            dict: The paths object item.

        Attributes:
            None

        Raises:
        """
        value_dict = self.schema['paths'][key];
        
        #print( key, value_dict )
        #print( value_dict['get']['tags'] );
        #print( value_dict['get']['description'] );
        #print( value_dict['get']['operationId'] );
        #print( value_dict['get']['parameters'] );
        #print( value_dict['get']['responses'] );
        #print( value_dict['get']['security'] );

        return value_dict
    
    
    def __call__( self, endpoint: str ):
        """
        Get the endpoint.

        Args:
            endpoint (str): The endpoint.

        Returns:
            dict: The endpoint.

        Attributes:
            self.keys (list): The object endpoints.

        Raises:
            None
        """
        self.keys = self._get_paths_object_endpoints();

        if endpoint == "profile":
            return self._get_profile();
    
        elif endpoint == 'cycle':
            return self._get_cycle_collection();
    
        elif endpoint == 'recovery':
            return self._get_recovery();
    
        elif endpoint == 'sleep':
            return self._get_sleep();
    
        elif endpoint == 'workout':
            return self._get_workout();

        elif endpoint == 'measurements':
            return self._get_measurements();

        elif endpoint == 'openapi_schema':
            #print( self.schema );
            #return self.get_paths_item_object();
            return self._get_schema();

    ### API Endpoints
    def _get_profile( self ) -> dict[str]:
        """
        Get the user profile.

        Args:
            None

        Returns:
            dict[str]: Response JSON data loaded into an object. Example:
                {
                    "user_id": 10129,
                    "email": "jsmith123@whoop.com",
                    "first_name": "John",
                    "last_name": "Smith"
                }

        Attributes:
            None

        Raises:
            None
        """
        # get the element in self.keys() with profile in the subword and id is not
        key = [ key for key in self.keys if "profile" in key and "Id" not in key ][0];
        return key

    def _get_body_measurement( self ) -> dict[str]:
        """
        Get the user's body measurements.

        Args:
            None

        Returns:
            dict[str]: Response JSON data loaded into an object. Example:
                {
                    "height_meter": 1.8288,
                    "weight_kilogram": 90.7185,
                    "max_heart_rate": 200
                }
        
        Attributes:
            None

        Raises:
            None
        """
        # get the element in self.keys() with profile in the subword and id is not
        key = [ key for key in self.keys if "measurement" in key and "Id" not in key ][0];
        return key
    
    def _get_cycle_collection( self ) -> dict[str]:
        """
        Make request to Get Cycle Collection endpoint.

        Get all physiological cycles for a user. Results are sorted by start time in
        descending order.

        Args:


        Returns:
            list[dict[str]]: Response JSON data loaded into an object. Example:
                [
                    {
                        "id": 93845,
                        "user_id": 10129,
                        "created_at": "2022-04-24T11:25:44.774Z",
                        "updated_at": "2022-04-24T14:25:44.774Z",
                        "start": "2022-04-24T02:25:44.774Z",
                        "end": "2022-04-24T10:25:44.774Z",
                        "timezone_offset": "-05:00",
                        "score_state": "SCORED",
                        "score": {
                            "strain": 5.2951527,
                            "kilojoule": 8288.297,
                            "average_heart_rate": 68,
                            "max_heart_rate": 141
                        }
                    },
                    ...
                ]
        
        Attributes:

        Raises:
            ValueError: If `start_date` is after `end_date
        """
        

        #return self._make_paginated_request(
            #method="GET",
            #url_slug="v1/cycle",
            #params={"start": start, "end": end, "limit": 25},
        #)
        key = [ key for key in self.keys if "cycle" in key and "Id" not in key ][0];
        return key

    

#if __name__ == "__main__":
    #obj = WhoopAPI();
    #print( obj.schema );
    
    #keys = obj.get_paths_object_endpoints();
    #print( keys )
    #obj.get_paths_item_object( '/v1/cycle/{cycleId}' );
    #for key in keys:
        #obj.get_paths_item_object( key );
        #break;
