import requests
import twitter
import json
import pandas as pd
import sys
import csv

# pip install -r requirements.txt

class TwitterAPI:
    '''create an instance of TwitterAPI passing credentials if they have not been hard coded.
    issue_simple_query = required params query string and count of tweets
    issue_geo_query = required params query string, optional lat lon and max range
    parse_statuses = optional param columns.
    parse_metadata = outputs a str with a summary of the metadata
    output_results = outputs parsed statuses in Excel
    '''
    DOCS = 'https://dev.twitter.com/rest/reference/get/search/tweets'

    __token = ''
    __token_secret = ''
    __consumer_key = ''
    __consumer_secret = ''
    
    resp = ''
    results_df = pd.DataFrame()

    def __init__(self):
        '''check tokens are available for querying the API. if not, request them'''
        self.check_tokens()

    def __repr__(self):
        '''function to decide what is returned when the class is printed'''
        if self.resp:
            return f'a query has been issued and is stored in the instance of this class'
        else:
            return f'issue a query to hit the TwitterAPI.'

    def check_tokens(self):
        '''check each of the 4 required tokens are more than 10 in length, request input if not.
        tokens can be requested using a Twitter developers account'''
        while not self.__token or len(self.__token) < 10 or self.__token == 'exit':
            self.__token = input('Please enter a token, type exit to quit: ')
            if self.__token == 'exit':
                break
        while not self.__token_secret or len(self.__token_secret) < 10 or self.__token_secret == 'exit':
            self.__token_secret = input('Please enter a token secret: ')
            if self.__token_secret == 'exit':
                break
        while not self.__consumer_key or len(self.__consumer_key) < 10 or self.__consumer_key == 'exit':
            self.__consumer_key = input('Please enter a consumer key: ')
            if self.__consumer_key == 'exit':
                break
        while not self.__consumer_secret or len(self.__consumer_secret) < 10 or self.__consumer_secret == 'exit':
            self.__consumer_secret = input('Please enter a consumer secret: ')
            if self.__consumer_secret == 'exit':
                break

    def check_query(self, query, count):
        '''check query is not blank and count is within range 0 to 100'''
        assert query != '', 'Please ensure you have entered a query term'
        assert count > 0 and count <= 100, 'Minimum number of results is 0 and maximum number of results is 100'

    def get_columns(self):
        top_level = [key for key in self.resp.keys()]
        second_level = list()

        for key in top_level:
            if type(self.resp[key]) != list:
                for k in self.resp[key].keys():
                    second_level.append(k)
            else:
                for each in self.resp[key]:
                    for k in each.keys():
                        second_level.append(k)

        return set(top_level), set(second_level)

    def issue_simple_query(self, query = 'UK', count = 100):
        '''count = number of twitter results, maximum is 100.
        query = twitter search term'''
        
        self.check_query(query, count)
        
        t = twitter.Twitter(auth=twitter.OAuth(self.__token, 
                                       self.__token_secret, 
                                       self.__consumer_key, 
                                       self.__consumer_secret)
                                       )

        self.resp = t.search.tweets(q= query, 
                               count = count)
        
        return self.resp

    def issue_geo_query(self, lat = 0, lon = 0, max_range = 1000, query = '', count = 100):
        '''lat & lon == geographical centre of search
        max_range == search range in kilometres from centre'''

        self.check_query(query, count)
        
        t = twitter.Twitter(auth = twitter.OAuth(self.__token, 
                                                self.__token_secret, 
                                                self.__consumer_key, 
                                                self.__consumer_secret)
                                                )

        self.resp = t.search.tweets(q = query, 
                                geocode = f"{lat},{lon},{max_range}km", 
                                count = count
                                )

        return self.resp

    def parse_statuses(self, columns = None):
        res = []
        if columns == None:
            columns = ['user', 'id', 'text', 'geo', 'coordinates', 'place']

        for each in self.resp['statuses']:
            row = []
            for col in columns:
                row.append(each[col])
            res.append(row)

        self.results_df = pd.DataFrame(res, columns = columns)

        # user split into name and location to reduce file size
        if 'user' in columns:
            self.results_df['name'] = self.results_df['user'][0]['name']
            self.results_df['location'] = self.results_df['user'][0]['location']
            self.results_df.drop('user', inplace=True, axis = 1)
        
        return self.results_df

    def get_metadata(self):
        meta_string = ''
        for each in self.resp['search_metadata']:
            meta_string += f"{each} = {self.resp['search_metadata'][each]}\n"

        return meta_string

    def output_results(self, filename = 'output'):
        '''optional filename can be provided, do not include extension'''
        if not filename.endswith('.xlsx'):
            filename = filename + '.xlsx'
        
        if not self.results_df.empty:
            self.results_df.to_excel(filename)
            return f'file output with filename {filename}'
        else:
            return f'results file does not exist, no output created.'