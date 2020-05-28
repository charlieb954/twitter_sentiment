# twitter_api.py

A simple TwitterAPI wrapper to issue simple and geo queries.

## How to use
- Create a virtual environment using "python3 -m venv venv" from command line
- Install requirements using "pip install -r requirements.txt" from command line

## Example workflow; 

<p><b>Create an instance of the twitter class</b></p>

- t_api = TwitterAPI()

<p><b>Issue simple or geo query</b></p>

- t_api.issue_simple_query(query = 'Test') # t_api.issue_geo_query(query = 'test', lat = 0, lon = 0)

<p><b>Get dictionary keys from Twitter dictionary to decide which columns to keep</b></p>

- print(t_api.get_columns())

<p><b>Parse the statuses</b></p>

- print(t_api.parse_statuses(columns = None))

<p><b>Parse metadata</b></p>

- print(t_api.get_metadata())

<p><b>Export parsed statuses to Excel</b></p>

- t_api.output_results(filename = 'test')



## twitter_sentiment.py

Builds and trains a NLTK model to mark Tweets positive or negative

- t = TwitterSentiment()
- t.make_predictions(['tweets to classify'])

## app.py

Uses twitter_api.py to pull tweets from the Twitter API, then makes predictions using twitter_sentiment.py
