import requests
import twitter
import json
import pandas as pd
import sys
import csv

# pip install -r requirements.txt

class TwitterAPI:
    '''
    Create an instance of TwitterAPI passing credentials if they have not been hard coded.
    '''
    DOCS = 'https://dev.twitter.com/rest/reference/get/search/tweets'

    _token = ''
    _token_secret = ''
    _consumer_key = ''
    _consumer_secret = ''
    
    resp = ''
    results_df = pd.DataFrame()

    def __init__(self):
        self.check_tokens()

    def __repr__(self):
        '''
        Return a statement specifying if a query has been issued.
        '''
        if self.resp:
            return f'a query has been issued and is stored in the instance of this class'
        else:
            return f'issue a query to hit the TwitterAPI.'

    def check_tokens(self):
        '''
        Check the 4 tokens meet the complexity requirements else request input.
        New tokens can be requested using a Twitter developers account.
        
        Parameters
        ==========
        query = str: twitter search term 
        count = int: number of twitter results, maximum is 100
        
        Returns
        =======
        None - if parameters meet requirements
        AssertionError - if parameters do not meet requirements
        '''
        while not self._token or len(self._token) < 10 or self._token == 'exit':
            self._token = input('Please enter a token, type exit to quit: ')
            if self._token == 'exit':
                break
        while not self._token_secret or len(self._token_secret) < 10 or self._token_secret == 'exit':
            self._token_secret = input('Please enter a token secret: ')
            if self._token_secret == 'exit':
                break
        while not self._consumer_key or len(self._consumer_key) < 10 or self._consumer_key == 'exit':
            self._consumer_key = input('Please enter a consumer key: ')
            if self._consumer_key == 'exit':
                break
        while not self._consumer_secret or len(self._consumer_secret) < 10 or self._consumer_secret == 'exit':
            self._consumer_secret = input('Please enter a consumer secret: ')
            if self._consumer_secret == 'exit':
                break

    def check_query(self, query, count):
        '''
        Check query is not blank and count is within range 0 to 100.
        
        Parameters
        ==========
        query = str: twitter search term 
        count = int: number of twitter results, maximum is 100
        
        Returns
        =======
        None - if parameters meet requirements
        AssertionError - if parameters do not meet requirements
        '''
        assert query != '', 'Please ensure you have entered a query term'
        assert count > 0 and count <= 100, 'Minimum number of results is 0 and maximum number of results is 100'

    def get_columns(self):
        '''
        Get a list of the available columns from the Twitter api response.
        
        Parameters
        ==========
        None
        
        Returns
        =======
        set: top level columns 
        set: second level columns
        '''
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
        '''
        Issue simple query using only a keyword.
        
        Parameters
        ==========
        query = str: twitter search term 
        count = int: number of twitter results, maximum is 100
        
        Returns
        =======
        self.resp = response from Twitter api
        '''
        self.check_query(query, count)
        
        t = twitter.Twitter(auth=twitter.OAuth(self._token, 
                                       self._token_secret, 
                                       self._consumer_key, 
                                       self._consumer_secret)
                                       )

        self.resp = t.search.tweets(q= query, 
                               count = count)
        
        return self.resp

    def issue_geo_query(self, lat = 0, lon = 0, max_range = 1000, query = '', count = 100):
        '''
        Issue geo query using a keyword, latitude and longitude with a maximum range.
        
        Parameters
        ==========
        lat = int: latitude
        lon = int: longitude
        max_range = int: max distance from lat/lon in km
        query = str: twitter search term 
        count = int: number of twitter results, maximum is 100
        
        Returns
        =======
        self.resp = response from Twitter api
        '''
        self.check_query(query, count)
        
        t = twitter.Twitter(auth = twitter.OAuth(self._token, 
                                                self._token_secret, 
                                                self._consumer_key, 
                                                self._consumer_secret)
                                                )

        self.resp = t.search.tweets(q = query, 
                                geocode = f"{lat},{lon},{max_range}km", 
                                count = count
                                )

        return self.resp

    def parse_statuses(self, columns = None):
        '''
        Parses the JSON object into Excel format.
        
        Parameters
        ==========
        columns = list: specify columns to use else default will be used
        
        Returns
        =======
        results_df = pandas dataframe: parsed results
        '''
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
        '''
        Parses the metadata from the Twitter api response.
        
        Parameters
        ==========
        None
        
        Returns
        =======
        meta_string = str: a string containing the metadata from the issued query
        '''
        meta_string = ''
        for each in self.resp['search_metadata']:
            meta_string += f"{each} = {self.resp['search_metadata'][each]}\n"

        return meta_string

    def output_results(self, filename = 'output'):
        '''
        Ouput results from Twitter api query in an Excel workbook.
        
        Parameters
        ==========
        filename = str: output filename without extension
        
        Returns
        =======
        str: string message confirming function has been successful
        '''
        if not filename.endswith('.xlsx'):
            filename = filename + '.xlsx'
        
        if not self.results_df.empty:
            self.results_df.to_excel(filename)
            return f'file output with filename {filename}'
        else:
            return f'results file does not exist, no output created.'