import twitter_api
import twitter_sentiment
from pprint import pprint
import sys

# Create an instance of the twitter class
t_api = twitter_api.TwitterAPI()
tokens = [t_api._token, 
        t_api._token_secret, 
        t_api._consumer_key, 
        t_api._consumer_secret]

if any([True for a in tokens if a == 'exit']):
    sys.exit()

# Issue simple or geo query
print('Issuing simple query ---->')
t_api.issue_simple_query(query = 'Test', count = 10) # t_api.issue_geo_query(query = 'test', lat = 0, lon = 0)

# Get dictionary keys from Twitter dictionary to decide which columns to keep
print('Get columns function ---->')
pprint(t_api.get_columns())

# Parse metadata
print('Get metadata function ---->')
pprint(t_api.get_metadata())

# Parse the statuses
print('Parsing the statuses ---->')
df = t_api.parse_statuses(columns = None)
tweets_list = list(df['text'])

# Export parsed statuses to Excel
filename = 'test'
print(f'Exporting results as {filename}.xlsx ---->')
t_api.output_results(filename = filename)

# Create an instance of the twitter sentiment class
t = twitter_sentiment.TwitterSentiment()

# Use the instance to make predictions, pass a list to return negative/positive
print('Training model and making predictions ---->')
pprint(t.make_predictions(tweets_list))
