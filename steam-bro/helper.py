from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()

def fetch_stats(user , df):
    if user != "Overall":
        df = df[df["user"]  == user]
    # shape[0] gives number of rows means no fo messages
    num_messages =  df.shape[0]
    words = []
    for message in df["message"]:
        words.extend(message.split())
    
    # we can able to match if it was ending with (file attached) this will be used in when extracgted with media
    no_of_media_messages = df[df["message"] == "<Media omitted>" ].shape[0]


    # no of links shared
    links = []
    for message in df["message"]:
        links.extend(extract.find_urls(message))

    return (num_messages , len(words) , no_of_media_messages , len(links))

def most_busy_users(df):
    # top 5 users will get here
    # values_count will give user : no of messages by user
    top_users_df = df["user"].value_counts().head()
    # each user messages count / total messages * 100 give a percetage
    # gives the df as [name , percentage]
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns={'index': "name", "user": "percentage"}
    )
    return top_users_df , df


def remove_urls(message):
    for link in extract.find_urls(message):
        message = message.replace(link , "")
    return message


def create_word_cloud(user , df):
    if user != "Overall":
        df = df[df["user"] == user]

    wc = WordCloud(width=500 , height=500 , min_font_size=10 , background_color='white')
    df = df[df["message"] != "<Media omitted>"]
    df["message"] = df["message"].apply(remove_urls)
    # generate() takes a string and split to words 
    df_wc = wc.generate(df["message"].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    # f=open('stop_words_list.txt','r' , encoding="utf-8")
    # stop_words = f.read()
    stop_words = []

    if(selected_user != 'Overall'):
        df= df[df['user'] == selected_user]
    
    temp = df[df['user'] != 'notification']
    temp=temp[temp['message'] != '<Media omitted>']

    words=[]

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    # gives top 20 words
    return_df=pd.DataFrame(Counter(words).most_common(20))
    return return_df

def emoji_helper(selected_user , df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    
    emojis = []
    for message in df["message"]:
        cur = [c for c in message if c in emoji.EMOJI_DATA]
        emojis.extend(cur)
    emojis_counter = Counter(emojis)
    emoji_df = pd.DataFrame(emojis_counter.most_common())
    return emoji_df

def monthly_timeline(selected_user , df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    
    # message : no of messages in that month
    time_line = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    # time : month-year
    for i in range(time_line.shape[0]):
        month_year = time_line["month"][i] + '-' + str(time_line["year"][i])
        time.append(month_year)
    
    time_line["time"] = time
    return time_line

def daily_timeline(selected_user , df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    # return the count messages in each day
    daily_timeline_df = df.groupby('only_date').count()["message"].reset_index()
    return daily_timeline_df

def week_activity_map(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # day : count of messages in each day
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # month : messages count
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # row have the day
    # col have hte period eg "14-15" , "2-3"
    # values are count of messages
    # aggregates with count of messages for each day period
    # if any period have no messages fill with 0
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap