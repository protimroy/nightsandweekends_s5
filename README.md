# nightsandweekends_s5
This is the main repo for nights &amp; weekends season5 by Buildspace.

### Bench
![images/nightandweekends_s5.png](images/nws5.png)


This repo contains the following files
# list of files
- README.md
- images/nws5.png
- config.py
    -- This file contains the configuration for the project including the database connection string, the whoop api url, the whoop api token.
- etl_driver.py
    -- This file is the main driver for the ETL process. It calls the extract, transform and load functions.
- extract.py
    -- This file contains the extract function which extracts data from the whoop api.
- transform.py
    -- This file contains the transform function which transforms the data from the whoop api.
- load.py
    -- This file contains the load function which loads the transformed data into the database.
- whoop_api.py
    -- This file contains the whoop api class which is used to make requests to the whoop api.
- OAuthsession.py
    -- This file contains the OAuthSession class which is used to make requests to the whoop api.


# How to run the project
- Clone the repo
- Install Prefect orchestrator
- Start a prefect server by running `prefect server start`
- Run the project by running `python etl_driver.py` which will start a Prefect flow and run the task in the flow.