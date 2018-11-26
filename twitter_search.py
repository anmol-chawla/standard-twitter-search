import requests
import yaml
import base64


with open('cred.yml', 'r') as cred_file:
    values = yaml.load(cred_file)


def get_auth():
    # Obtain the OAuth2 access token
    token_creds = values['credentials']['consumer_api_key'] + \
        ':' + values['credentials']['consumer_api_secret_key']
    encoded_token = base64.b64encode(token_creds.encode()).decode()
    request_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'charset': 'UTF-8',
        'Authorization': 'Basic ' + encoded_token
    }
    request_body = {'grant_type': 'client_credentials'}
    request_url = 'https://api.twitter.com/oauth2/token'
    response = requests.post(
        request_url, headers=request_headers, data=request_body)
    return response.json()['access_token']


def search_tweets(query, geocode=None, lang='en', result_type='mixed', count='15', until=None):
    '''
    Searches Twiiter for tweets related to the query
    geocode : optional to allow for localisation of results, foramt - lat,long, radius (eg. "40.712776,-74.005974,1km")
    lang : desired language for the result
    result_tyep : mixed, recent or popular
    count : number of tweets returned
    until : returns the tweets created before the given date
    '''
    request_url = 'https://api.twitter.com/1.1/search/tweets.json'
    request_headers = {
        'Authorization': 'Bearer {}'.format(get_auth())
    }
    request_params = {
        'q': query,
        'lang': lang,
        'result_type': result_type,
        'count': count,
    }
    if geocode:
        request_params['geocode'] = geocode
    if until:
        request_params['until'] = until
    response = requests.get(
        request_url, headers=request_headers, params=request_params)
    return response.json()


def get_format_tweets(response_json):
    data = []
    for dic in response_json['statuses']:
        tweet = {}
        tweet['text'] = dic['text']
        try:
            tweet['link'] = 'https://www.twitter.com/' + \
                dic['user']['screen_name'] + '/status/' + str(dic['id'])
        except Exception:
            tweet['link'] = None
        tweet['image'] = dic['user']['profile_image_url_https']
        tweet['type'] = 'tweet'
        data.append(tweet)
    return data
