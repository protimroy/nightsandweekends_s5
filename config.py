"""
This is a configuration file to access config.ini where the authentications information is stored and the urls.
It was made for the nightsandweekends_s5 project.
Protim R 2024
"""
import configparser;
from sqlalchemy import create_engine

def _init_config():
    """
    Initialize the configuration settings.

    Args:
        None

    Returns:
        None

    Attributes:
        _config (configparser.ConfigParser): Configuration

    Raises:
        None
    """
    global _config;
    _config = configparser.ConfigParser();
    return _config.read( "config.ini" );


def get_config( name : str ) -> dict:
    """
    Get the configuration settings.

    Args:
        name (str): Name of the configuration settings to retrieve.

    Returns:
        dict: Configuration settings.

    Attributes:
        _config (configparser.ConfigParser): Configuration settings.

    Raises:
        ValueError: If the configuration setting is not found.
    """
    if name not in _init_config():
        raise ValueError( f"Configuration setting '{name}' not found." );
    return _config;


def get_engine():
    """
    Create and return the sql engine

    Args:
        None

    Returns:
        engine (sqlalchemy.engine.base.Connection): The sql engine.

    Attributes:
        None

    Raises:
        ValueError: Error creating the engine.
    """
    # create a mysql engine
    try:
        return create_engine( _config["database"]["connection_string"] );
    except:
        raise ValueError( "Error creating the engine." );