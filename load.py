import config as C;
import pandas as pd;

class Load():
    def __init__( self ):
        """

        """
        super().__init__();

    def df( self, df, table_name: str ):
        """
        Loads a df to sql table
        """
        engine = C.get_engine();
        with engine.connect() as conn:
            df.to_sql( table_name, conn, if_exists="replace" );