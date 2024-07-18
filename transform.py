import pandas as pd;

class Transform():
    def __init__( self, response ):
        super().__init__();
        self.response = response;

    def transform( self ):
        """
        Transform the response to a dataframe
        """
        # create a dataframe passing an index of 0
        df = pd.DataFrame( self.response, index=[0] );
        return df;