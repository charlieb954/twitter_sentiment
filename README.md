# twitter_api

<p>A simple TwitterAPI wrapper to issue simple and geo queries.

# How to use
<p>Create a virtual environment using python3 -m venv venv from command line

<p>Install requirements using pip install -r requirements.txt from command line

## Example workflow; 

<p>Create an instance of the twitter class
<p>t_api = TwitterAPI()

<p>Issue simple or geo query
<p>t_api.issue_simple_query(query = 'Test') # t_api.issue_geo_query(query = 'test', lat = 0, lon = 0)

<p>Get dictionary keys from Twitter dictionary to decide which columns to keep
<p>print(t_api.get_columns())

<p>Parse the statuses
<p>print(t_api.parse_statuses(columns = None))

<p>Parse metadata
<p>print(t_api.get_metadata())

<p>Export parsed statuses to Excel
<p>t_api.output_results(filename = 'test')

