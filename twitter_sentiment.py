import nltk
nltk.download('twitter_samples') # sample tweets to train the model
nltk.download('punkt') # pre-trained model to help tokenize words and understands names may contain a full stop.
nltk.download('wordnet') # used to determine the base word
nltk.download('averaged_perceptron_tagger') # determines the context of a word in a sentence
nltk.download('stopwords') # stop words for various languages including English
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

import re, string, random

class TwitterSentiment:
    def __init__(self, lang = 'english'):
        '''
        Build stopword lists, set train_model flag and accuracy.
        
        Parameters
        ==========
        lang = str: check corpus for available languages
        
        Returns
        =======
        None
        '''
        self._stopwords = set(stopwords.words(lang) + list(string.punctuation))
        self.trained_model = None
        self.model_accuracy = 0
        
    def make_predictions(self, tweet):
        '''
        Calls function to train model if required, cleans and processes the tweets, scores each tweet.
        
        Parameters
        ==========
        tweet = list: tweets to classify
        
        Returns
        =======
        results = list: classified tweets
        '''
        if not self.trained_model:
            self._train_model()
        
        processed_tweet = self.process_tweets(tweet)
        
        tweet_list = []
        for tweet in processed_tweet:
            proc_dict = dict()
            for word in tweet:
                proc_dict[word] = True
            tweet_list.append(proc_dict)
                
        if not tweet_list:
            return 'error with tweets'
        else:
            results = []
            for i, each in enumerate(tweet_list):
                results.append([i, each, self.trained_model.classify(each)])
            return results
        
    def _train_model(self):
        '''
        Trains the classification model using twitter_samples from nltk.corpus.
        
        Parameters
        ==========
        None
        
        Returns
        =======
        None
        '''
        positive_tweets = twitter_samples.strings('positive_tweets.json')
        negative_tweets = twitter_samples.strings('negative_tweets.json')
        
        processed_pos = self.process_tweets(positive_tweets)
        processed_neg = self.process_tweets(negative_tweets)
                
        pos_list = []
        for tweet in processed_pos:
            pos_dict = dict()
            for word in tweet:
                pos_dict[word] = True
            pos_list.append((pos_dict, 'positive'))
         
        neg_list = []
        for tweet in processed_neg:
            neg_dict = dict()
            for word in tweet:
                neg_dict[word] = True
            neg_list.append((neg_dict, 'negative'))       
        
        all_tweets = pos_list + neg_list
        
        random.shuffle(all_tweets)

        train_data = all_tweets[:7000]
        test_data = all_tweets[7000:]

        self.trained_model = NaiveBayesClassifier.train(train_data)
        self.model_accuracy = classify.accuracy(self.trained_model, test_data)
    
    def process_tweets(self, tweets):
        '''
        Process tweets, converting to list if required.
        Cleans tweets and lemmatises them.
        
        Parameters
        ==========
        tweets = list: tweets to process
        
        Returns
        =======
        token_tweets = list: tokenized tweets
        '''
        if not type(tweets) == list:
            try:
                tweets = [tweets]
            except:
                return None
        
        cleansed_tweets = self._clean_tweets(tweets)
        
        token_tweets = self._lemmatise_tweets(cleansed_tweets)
        
        return token_tweets
        
    def _clean_tweets(self, tweets):
        '''
        Remove URLs and @users using regex and return the tweets.
        
        Parameters
        ==========
        tweets = list: tweets to process
        
        Returns
        =======
        processed_tweets = list: tweets with tags removed
        '''
        processed_tweets = []
        
        for tweet in tweets:
            tweet = tweet.lower()
            tweet = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                        r'(?:%[0-9a-f][0-9a-f]))+','', tweet)
            tweet = re.sub(r"@[^\s]+", "", tweet)
            processed_tweets.append(tweet)
        
        return processed_tweets

    def _lemmatise_tweets(self, processed_tweets):
        '''
        Process a list of tweets for lemmatising (return the root word).
        
        Parameters
        ==========
        processed_tweets = list: tweets with tags removed
        
        Returns
        =======
        lem_tweets = list: list of lemmatised tweets.
        '''
        lemm_tweets = []
                
        for tweet in processed_tweets:
            tweet = word_tokenize(tweet)
            lemm_tweets.append(self._lemm_tweet(tweet))
                    
        return lemm_tweets
    
    def _lemm_tweet(self, tweet):
        '''
        Lemmatise the tweets (return the root word), tokenize the tweets.
        Tag as noun verb or adjective and then lemmatise the word to get the root word for easy comparison.
        
        Parameters
        ==========
        tweet = str: single tweet with tags removed
        
        Returns
        =======
        lem_tweets = list: lemmatised tweet.
        '''
        lemmatizer = WordNetLemmatizer()                    
        lemmatized_sentence = []
        
        for word, tag in pos_tag(tweet):
            if tag.startswith('NN'):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'
            lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
        
        lemmatized_sentence = [word for word in lemmatized_sentence if word not in self._stopwords]
        
        return lemmatized_sentence