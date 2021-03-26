import pandas as pd    
import numpy as np 
import re
import pickle 
from textblob import Word
from nltk.corpus import stopwords

def clean_reviews(input):
    return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ",input.lower()).split())

def remove_stopwords(df):
    stop = stopwords.words('english')
    df['input']=df['input'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    return df

def lemmatization(df):
    df['input']=df['input'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))    
    return df   

def modelpredict(df):
    with open('model','rb') as modelFile:
        model = pickle.load(modelFile)

    return model.predict(df['input'].tolist())
    
def preprocessingnpredictions(userinput):
    data=[]
    df = pd.DataFrame(data, columns=['input'])
    df = df.append({'input': userinput }, ignore_index=True)
    df['input']=df['input'].apply(clean_reviews)
    df=remove_stopwords(df)
    df=lemmatization(df)
    predicted_value=modelpredict(df)
    df = None
    return predicted_value[0]

def etsyprediction():
    df1=pd.read_csv(r'scrappedReviews.csv')
    df1.columns=['reviews']
    df1['predictedvalue']=np.nan

    for i in df1.index:
        df1.iloc[i,1]  = preprocessingnpredictions(df1.iloc[i,0])
    df1.to_csv('etsypredictedreviews.csv') 




