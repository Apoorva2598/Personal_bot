import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credit_key.json"
import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "personalbot-rsropn"

# mongo
from pymongo import MongoClient
db_client = MongoClient("mongodb+srv://test:test@cluster0-x5tqe.mongodb.net/test?retryWrites=true&w=majority")
db = db_client.get_database("data_of_app")
records = db.news_bot

# For news
from gnewsclient import gnewsclient
client = gnewsclient.NewsClient(max_results=3)

def get_news(parameters):
    print (parameters)
    records.insert_one(parameters)
    client.topic = parameters.get('news_type')
    client.language = parameters.get('language')
    client.location = parameters.get('geo-country')
    return client.get_news()
# For news - end


##      AUDIO           - begin
from youtube_api import YouTubeDataAPI
api_key = '<your_youtube_api_key>'
yt = YouTubeDataAPI(api_key)

def get_video(message):
    searches = yt.search(q=message, max_results=1)

    video_link = 'https://www.youtube.com/watch?v='+(searches[0]['video_id'])
    return video_link
###     Audio           - end


## Dictionary
from PyDictionary import PyDictionary
dictionary=PyDictionary()
from language_short_key import lang_list
def get_meaning(parameters):
    print(parameters)
    word = parameters.get('any')
    if parameters.get('diction_type') == 'synonym':
        return dictionary.synonym(word)
    elif parameters.get('diction_type') == 'antonym':
        return dictionary.antonym(word)
    elif parameters.get('diction_type') == 'translate':
        lan = parameters.get('language')
        if lan != '':
            for code, lang in lang_list.items():
                if lan.lower() in lang.lower():
                    break
            return dictionary.translate(word, code)
        else:
            return 'no language provided'
    else:
        return dictionary.meaning(word)
## Dictionary -    End

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result



def fetch_reply(msg, session_id):
    response = detect_intent_from_text(msg, session_id)
    if response.intent.display_name == 'get_news':
        news = get_news(dict(response.parameters))
        news_str = 'Here is your news: '
        for row in news:
            news_str += "\n\n{}\n\n{}\n\n".format(row['title'], row['link'])
            return news_str
    elif response.intent.display_name == 'MusicPlayer':
        video = get_video(msg)
        video = 'Search result : '+ video
        return video
    elif response.intent.display_name == 'Dictionary':
        #print(response)
        meaning = get_meaning(dict(response.parameters))
        return meaning
    else:
        return response.fulfillment_text