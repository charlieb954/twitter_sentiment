import twitter_api
import twitter_sentiment

# Create an instance of the twitter class
t_api = twitter_api.TwitterAPI()

# Issue simple or geo query
t_api.issue_simple_query(query = 'Test', count = 10) # t_api.issue_geo_query(query = 'test', lat = 0, lon = 0)

# Get dictionary keys from Twitter dictionary to decide which columns to keep
print(t_api.get_columns())

# Parse metadata
print(t_api.get_metadata())

# Parse the statuses
df = t_api.parse_statuses(columns = None)
tweets_list = list(df['text'])

# Export parsed statuses to Excel
t_api.output_results(filename = 'test')

# Create an instance of the twitter sentiment class
t = twitter_sentiment.TwitterSentiment()

# Use the instance to make predictions, pass a list to return negative/positive
print(t.make_predictions(tweets_list))
