from pyramid.config import Configurator
from pyramid.response import Response
from paste.httpserver import serve
import urllib
import json
import twitter
import tweeter_credentails
import psycopg2

def get_db_connection():
    cur, conn = None, None
    try:
        conn = psycopg2.connect(host="localhost",database="twitter_db", user="postgres", password="postgres321")
        cur = conn.cursor()
        return cur, conn
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        return cur, conn


def api_fetch_user_tweets(request):
     input_data = request.json_body
     in_user_name = input_data['user_name'] 
     in_limit = input_data['limit'] 

     sqlWrapper, conn = get_db_connection() 
     print(sqlWrapper)

     qry = "select tweeter_user_id_pk from twitter_user_tbl where user_nanme  =  '" + in_user_name + "'"
     print('qry is:')
     print(qry) 
     result = sqlWrapper.execute(qry)
     result = sqlWrapper.fetchone()
     print(result)
     if result is None:
         qry = "insert into twitter_user_tbl(user_nanme) values('"+ in_user_name + "')RETURNING tweeter_user_id_pk;"
         print('qry is:')
         print(qry) 
         result = sqlWrapper.execute(qry)
         result = sqlWrapper.fetchone()
         tweeter_user_id = result[0]
         conn.commit()
         print(result)
     else:
          tweeter_user_id = result[0]

     print('tweeter_user_id:  ', tweeter_user_id)


     api_consumer_key = tweeter_credentails.Consumer_API_key
     api_consumer_secrete = tweeter_credentails.API_secret_key 
     api_access_token_key = tweeter_credentails.Access_token
     api_access_token_secrete = tweeter_credentails.Access_token_secret 

     api = twitter.Api(consumer_key=api_consumer_key, consumer_secret=api_consumer_secrete, access_token_key=api_access_token_key, access_token_secret=api_access_token_secrete)


     #res = api.GetUserTimeline(screen_name="ekraje", count=10)
     res = api.GetUserTimeline(screen_name=in_user_name, count=in_limit)
     response_list = []
     for tweet in res:
         tweet = str(tweet)
         print('\n')
         print(type(tweet))
         #print((tweet))
         
         tweet = json.loads(tweet)
         print(type(tweet))
                  

         in_tweet_id = tweet['id']         
         in_tweet_lang = tweet['lang'].encode("utf-8")         
         in_tweet_text = tweet['text'].encode("utf-8")

         print('tweet_id: ', in_tweet_id)
         print('tweet_lang: ', in_tweet_lang)
         print('tweet_text: ', in_tweet_text)
         in_tweet_text = in_tweet_text.replace(',', '').replace("'", '')
         #try:
         if  True:
             qry = "select user_tweet_id_pk from user_tweets_tbl where tweeter_user_id_fk  =  " + str(tweeter_user_id) + " and tweet_id = " +str(in_tweet_id)  
             print('qry is:')
             print(qry) 
             result = sqlWrapper.execute(qry)
             result = sqlWrapper.fetchone()
             print('result')
             print(result)
             if result is None:
                 qry = "insert into user_tweets_tbl(tweeter_user_id_fk, tweet_id, language, tweet_text) values("+ str(tweeter_user_id) + "," + str(in_tweet_id) + ",'" + (in_tweet_lang) + "','" + (in_tweet_text) +"')RETURNING user_tweet_id_pk;"
                 print('qry is:')
                 print(qry) 
                 result = sqlWrapper.execute(qry)
                 result = sqlWrapper.fetchone()
                 user_tweet_id = result[0]
                 conn.commit()
                 print(result)
             else:
                 user_tweet_id = result[0]

             print('user_tweet_id:  ', user_tweet_id)
          
             response_list.append(user_tweet_id)                 
         #except:
         #    pass
     
     final_response = {}
     if len(response_list) > 0: 
         final_response['user_tweet_ids'] = response_list
         final_response['status'] = 'success'
     else:
         final_response['status'] = 'failure'
            
     print(final_response)
     res = json.dumps(final_response)

 
     return Response(res)
     #return Response('success')

#with open('/home/eknath/eknath/twitter/sample_tweeter_op.json', 'w') as f:
#    #json.dumps(res, f)
#     f.write(str(res)) 

   

#print(api.VerifyCredentials())

def api_search_tweets(request):
     input_data = request.json_body
     in_search_str = input_data['search_string'] 

     in_search_str = in_search_str.lower()
     sqlWrapper, conn = get_db_connection() 
     print(sqlWrapper)

     qry = "select * from user_tweets_tbl where lower(tweet_text) like '%" + in_search_str + "%'"
     print('qry is:')
     print(qry) 
     result = sqlWrapper.execute(qry)
     print(result)
     result = sqlWrapper.fetchall()
     print(result)
     response_list = []
     final_response = {}
     
     if result != []:
         for record in result:
             print(record)
             op_dict = {}
             user_tweet_id, tweeter_user_id, tweet_id, lang, tweet_text = record[0], record[1], record[2], record[3], record[4]

             op_dict['user_tweet_id'], op_dict['tweeter_user_id'], op_dict['tweeter_tweet_id'] = user_tweet_id, tweeter_user_id, tweet_id
             op_dict['language'], op_dict['tweet_text'] = lang, tweet_text 
          
             response_list.append(op_dict)                
   
         print(response_list)
 
         final_response['search_result'] = response_list
         final_response['status'] = 'success'
     else:
         final_response['status'] = 'no_result'

     print(final_response)
     res = json.dumps(final_response)
     return Response(res)

if __name__ == '__main__':
    #sqlWrapper, conn = get_db_connection() 
    config = Configurator()
    config.add_view(api_fetch_user_tweets, name = 'fetch_user_tweets')
    config.add_view(api_search_tweets, name = 'search_tweets')
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0')
