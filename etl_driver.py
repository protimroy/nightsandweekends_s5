"""
Created by Protim R. 2024
"""
from prefect import flow, task, get_run_logger, serve;

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
        self.logger (logging.Logger): The (prefect) logger object.

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
        self.logger = get_run_logger();
    
    
    def _pipe(self, func, *args, **kwargs):
        try:
            self = func(self, *args, **kwargs)
        except Exception as e:
            print(f'Piping {func.__name__} failed. Exception: {e.message}')
        finally:
            return self

    def _run_extract( self ):
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
        self.logger.info( "Extract process started." );
        self.extract_obj = Extract(wearable="whoop");
        self.extract_response = self.extract_obj.main(api="profile");
        self.logger.info( "Extract process completed." );
    
    def _run_transform( self ):
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
        self.logger.info( "Transform process started." );
        self.transform_obj = Transform( self.extract_response );
        self.transform_response = self.transform_obj._transform();
        self.logger.info( self.transform_response );
        self.logger.info( "Transform process completed." );
    
    def _run_load( self ):
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
        self.logger.info( "Load process started." );
        self.load_obj = Load();
        self.load_obj._load_df( self.transform_response, "profile" );
        self.logger.info( "Load process completed." );

    def _main( self ):
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
        
        self.logger.info( "ETL process started." );
        self._run_extract();
        self._run_transform();
        self._run_load();
        self.logger.info( "ETL process completed." );

"""
The prefect documentation only uses functions as tasks. There are no examples of class functions as tasks.
The following link provides a solution to this problem:

Prefect : Using task decorators with objects
https://github.com/PrefectHQ/prefect/issues/7198#issuecomment-1910302419

"""

@task
def main( self ):
    print("this is a piped function")
    return Driver._main( self );

@flow( retries=1, retry_delay_seconds=15, log_prints=True )
def whoop():
    driver = Driver();
    driver._pipe( main );
    #driver._main()

if __name__ == "__main__":
    #whoop.serve(name='profile')
    profile_deploy = whoop.deploy(name='profile')
    cycle_deploy = whoop.deploy(name='cycle')
    serve( profile_deploy, cycle_deploy )