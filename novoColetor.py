import tweepy
import Credenciais
import csv
#import numpy as np
#import pandas as pd
from textblob import TextBlob 
#import matplotlib.pyplot as plt
def autenticar():
        auth = tweepy.OAuthHandler(Credenciais.CONSUMER_KEY,Credenciais.CONSUMER_SECRET)
        auth.set_access_token(Credenciais.ACCESS_TOKEN, Credenciais.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)        
        return api


def csv_to_tweets(ultimo_tweet,api):
        Entrada = open('corona_tweets_45.csv','r', encoding='utf-8')
        csv_r = list(csv.reader(Entrada))
        saida = csv.writer(open('Saida1.csv','a+', encoding= 'utf-8'))
        #tweets= []
        #sentiment_scores =[]
        bol = 0
        for rows in range(0,len(csv_r),100):
                if bol:
                        try:
                                row = csv_r[rows:rows+100]
                                tweets = api.statuses_lookup([i[0] for i in row], tweet_mode="extended")
                                polaridades = {int(i[0]): float(i[1])  for i in row}
                                for tweet in tweets:
                                        texto = tweet.full_text 
                                        if texto[-1] != "…" :
                                                #tweets.append(tweet)
                                                score = TextBlob(texto).sentiment
                                                if score[0]        == polaridades[tweet.id]:
                                                        #sentiment_scores.append(TextBlob(texto).sentiment)
                                                        saida.writerow([texto,tweet.id,len(texto),tweet.created_at,tweet.source,tweet.favorite_count,tweet.retweet_count,score[0],score[1]] )
                                                else:
                                                        print(score[0], polaridades[tweet.id])        
                        except Exception as e:
                                if e.api_code  == 420:        
                                        print(e)
                                        #return tweets, sentiment_scores
                                        return 0
                else:
                        print(ultimo_tweet)
                        if row[0] == ultimo_tweet or ultimo_tweet == '':
                                bol = 1
                #return tweets, sentiment_scores
        return 1
'''
def tweets_to_df(tweets,sentiment_scores):
        df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['Text'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['Tamanho'] = np.array([len(tweet.full_text) for tweet in tweets])
        df['Data'] = np.array([tweet.created_at for tweet in tweets])
        df['Dispositivo utilizado'] = np.array([tweet.source for tweet in tweets])
        df['Curtidas'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['Polaridade'] = np.array([i[0] for i in sentiment_scores])
        df['Subjetividade'] = np.array([i[1] for i in sentiment_scores])        
        return df
'''
def main(args):        
        f = open('Saida1.csv','r',encoding='utf-8')
        csv_r = list(csv.reader(f))
        f.close()
        ultimo_tweet = ''
        # Gambiarra: comentar as duas linhas abaixo ao usar base nova :) confie em mim
        #if len(csv_r) !=0:
        #        ultimo_tweet = csv_r[-2][1]
        
        print(csv_to_tweets(ultimo_tweet,autenticar()))
        #df = tweets_to_df(tweets,sentiment_scores)
        #df.plot(x ='Polaridade', y='Subjetividade', kind = 'scatter')        
        #plt.show()
        #df.to_csv('Final.csv',index=False)
        return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))