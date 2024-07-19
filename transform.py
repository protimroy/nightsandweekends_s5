"""
Created by Protim R. 2024
"""
import pandas as pd;

class Transform():
    """
    Transform class for transforming data.

    Args:
        None

    Returns:
        None

    Attributes:
        self.response (dict): The response from the API.
        self.df (pd.DataFrame): The dataframe.

        self._insert_date_column (function): Insert a column for the insert date.
        self._transform (function): Transform the response to a dataframe.

    Raises:
        None
    """
    def __init__( self, response ):
        """
        Constructor for the Transform class.

        Args:
            response (dict): The response from the API.

        Returns:
            None

        Attributes:
            response (dict): The response from the API.
            df (pd.DataFrame): The dataframe.

        Raises:
            None
        """
        super().__init__();
        self.response = response;
    
    def _insert_date_column( self ):
        """
        Insert a column for the insert date

        Args:
            None

        Returns:
            None

        Attributes:
            None

        Raises:
            None
        """
        # add column called insert date
        self.df['insert_date'] = pd.to_datetime('today').strftime("%Y-%m-%d %H:%M:%S");
        

    def _transform( self ):
        """
        Transform the response to a dataframe

        Args:
            None

        Returns:
            pd.DataFrame: The transformed dataframe.

        Attributes:
            None

        Raises:
            None
        """
        # create a dataframe passing an index of 0
        self.df = pd.DataFrame( self.response, index=[0] );
        self._insert_date_column();
        return self.df;