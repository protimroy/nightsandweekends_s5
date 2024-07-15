"""
"""
import requests;
import json;
import config;


class BaseAPI( object ):
    """
    Base class for any wearable API such as Whoop, Fitbit, etc.
    """
    def __init__( self ):
        self.conf = config.get_config( "config.ini" );
        self.url_dict = dict( self.conf.items( "urls" ) );

    def get_schema( self ):
        raise NotImplementedError( "This method must be implemented in a derived class." );



class WhoopAPI( BaseAPI ):
    def __init__(self) -> None:
        super().__init__();
        self.schema = self.get_schema();


    def get_schema( self ):
        url = self.url_dict['whoop_openapi_url'];

        response = requests.get( url );
        response.raise_for_status();
        return response.json(); 

    def get_paths_object_endpoints( self ):
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

    def get_paths_item_object( self, key: str ):
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
        
        print( value_dict['get']['tags'] );
        print( value_dict['get']['description'] );
        print( value_dict['get']['operationId'] );
        print( value_dict['get']['parameters'] );
        print( value_dict['get']['responses'] );
        print( value_dict['get']['security'] );
    
    def __call__( self, endpoint: str ):
        if endpoint == "profile":
            keys = obj.get_paths_object_endpoints();
            return self.get_profile( );

    ### API Endpoints
    def get_profile( self, key ) -> dict[str]:
        """
        Get the user profile.

        Args:
            None

        Returns:
            dict : The user profile.

        Attributes:
            None

        Raises:
            None
        """
        pass
            

if __name__ == "__main__":
    obj = WhoopAPI();
    #print( obj.schema );
    
    keys = obj.get_paths_object_endpoints();
    obj.get_paths_item_object( '/v1/cycle/{cycleId}' );