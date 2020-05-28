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
        ''' '''
        self._stopwords = set(stopwords.words(lang) + list(string.punctuation))
        self.trained_model = None
        self.model_accuracy = 0
        
    def make_predictions(self, tweet):
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
            for each in tweet_list:
                results.append([each, self.trained_model.classify(each)])
            return results
        
    def _train_model(self):
        '''TRAINING SET NEEDS TO BE tuple({'word':True, 'word2': True}, 'Positive')'''
        global all_tweets
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
        if not type(tweets) == list:
            try:
                tweets = [tweets]
            except:
                return None
        
        cleansed_tweets = self._clean_tweets(tweets)
        
        token_tweets = self._lemmatise_tweets(cleansed_tweets)
        
        return token_tweets
        
    def _clean_tweets(self, tweets):
        processed_tweets = []
        
        for tweet in tweets:
            tweet = tweet.lower()
            tweet = re.sub(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                        r'(?:%[0-9a-f][0-9a-f]))+','', tweet)
            tweet = re.sub(r"@[^\s]+", "", tweet)
            processed_tweets.append(tweet)
        
        return processed_tweets

    def _lemmatise_tweets(self, processed_tweets):
        lemm_tweets = []
                
        for tweet in processed_tweets:
            tweet = word_tokenize(tweet)
            lemm_tweets.append(self._lemm_tweet(tweet))
                    
        return lemm_tweets
    
    def _lemm_tweet(self, tweet):
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


t = TwitterSentiment()
t._train_model()



#        freq_dist_pos = FreqDist(all_pos_words)
#        print(freq_dist_pos.most_common(10))
#
#        print(classifier.show_most_informative_features(10))