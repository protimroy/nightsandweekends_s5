"""
Created by Protim R. 2024
"""
from extract import Extract
from transform import Transform
from load import Load


class Driver():
    """
    Driver class for the ETL process

    args:
        None

    returns:
        Driver object

    attributes:
        self.extract_obj (Extract): The Extract object.
        self.extract_response (dict): The extracted response.
        self.transform_obj (Transform): The Transform object.
        self.transform_response (pd.DataFrame): The transformed response.
        self.load_obj (Load): The Load object.

        self.run_extract (function): Run the extract process.
        self.run_transform (function): Run the transform process.
        self.run_load (function): Run the load process.
        self.main (function): Run the ETL process.

    raises:
        None
    """
    def __init__( self ):
        """
        Constructor for the Driver class.

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

    def run_extract( self ):
        """
        Run the extract process.

        Args:
            None

        Returns:
            None

        Attributes:
            self.extract_obj (Extract): The Extract object.
            self.extract_response (dict): The extracted response.

        Raises:
            None
        """
        # run extract
        self.extract_obj = Extract(wearable="whoop");
        self.extract_response = self.extract_obj.main(api="profile");
        print( self.extract_response );
    
    def run_transform( self ):
        """
        Run the transform process.

        Args:
            None

        Returns:
            None

        Attributes:
            self.transform_obj (Transform): The Transform object.
            self.transform_response (pd.DataFrame): The transformed response

        Raises:
            None
        """
        # run transform
        self.transform_obj = Transform( self.extract_response );
        self.transform_response = self.transform_obj.transform();
        print( self.transform_response );
    
    def run_load( self ):
        """
        Run the load process.

        Args:
            None

        Returns:
            None

        Attributes:
            self.load_obj (Load): The Load object.
        
        Raises:
            None
        """
        # run load
        self.load_obj = Load();
        self.load_obj.df( self.transform_response, "profile" );

    def main( self ):
        """
        Run the ETL process.

        Args:
            None

        Returns:
            None

        Attributes:
            None

        Raises:
            None
        """
        self.run_extract();
        self.run_transform();
        self.run_load();

if __name__ == "__main__":
    driver = Driver();
    driver.main();