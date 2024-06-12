import json
import boto3
import tweepy

def lambda_handler(event, context):
    # Log the Tweepy version
    print(f"Tweepy version: {tweepy.__version__}")

    # Twitter API credentials
    consumer_key = 'yF2vQp2dKX9avygbn72Sw5ZWx'
    consumer_secret = 'XxUv1t5lM1puaG7b3AO0lc1kgwYNmMg3x7f0PAYnXDujRDnnY5'
    access_token = '3688691909-EH91DmEu3szAcmZKrByvL8EUzsAGiQymfT30eN6'
    access_token_secret = 'YscfW7ViWCgNVr0iM5jiLVn59eVgCkJqFqzgtArP2bhnB'
    
    # Set up Tweepy authorization
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    
    # Fetch tweets
    username = event['username']
    tweets = api.user_timeline(screen_name=username, count=10, tweet_mode='extended')
    
    comprehend = boto3.client('comprehend')
    
    sentiment_results = []
    for tweet in tweets:
        text = tweet.full_text
        sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        sentiment_results.append({
            'tweet_id': str(tweet.id),
            'text': text,
            'sentiment': sentiment['Sentiment']
        })
    
    # Store results in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SentimentAnalysisResults')
    for result in sentiment_results:
        table.put_item(Item=result)
    
    return {
        'statusCode': 200,
        'body': json.dumps(sentiment_results)
    }
