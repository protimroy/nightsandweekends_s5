"""
Created by Protim R. 2024
"""
import config as C;

class Load():
    """
    Load class for loading data to a database.

    Args:
        None

    Returns:
        None

    Attributes:

        self.df (pd.DataFrame): The dataframe to load.

        self._check_table_exists (function): Check if a table exists.
        self._load_df (function): Load a dataframe to a table.
        

    Raises:
        None
    """
    def __init__( self ):
        """
        Constructor for the Load class.

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
    
    def _check_table_exists( self, table_name: str ) -> bool:
        """
        Checks if a table exists in the database

        Args:
            table_name (str): The table name to check.

        Returns:
            bool: True if the table exists, False otherwise.
        
        Attributes:
            engine (sqlalchemy.engine.base.Connection): The sql engine.

        Raises:
            None
        """
        engine = C.get_engine();
        with engine.connect() as conn:
            query = f"SELECT * FROM {table_name}";
            try:
                conn.execute( query );
                return True;
            except:
                return False;

    def _load_df( self, df, table_name: str ):
        """
        Loads a df to sql table

        Args:
            df (pd.DataFrame): The dataframe to load.
            table_name (str): The table name to load the dataframe to.

        Returns:
            None

        Attributes:
            engine (sqlalchemy.engine.base.Connection): The sql engine.

        Raises:
            ValueError: Error loading to the table.
        """
        self.df = df;
        engine = C.get_engine();
        with engine.connect() as conn:
            if self._check_table_exists( table_name ):
                try:
                    self.df.to_sql( table_name, conn, if_exists="append" );
                except:
                    raise ValueError( f"Error loading {table_name} to database." );
            else:
                try:
                    self.df.to_sql( table_name, conn, if_exists="replace" );
                except:
                    raise ValueError( f"Error loading {table_name} to database." );