# 05/05/2021, 20:39 - Balaji: Emo ra nenu Inka cheyaledu avi
# example message format

import re
import pandas as pd
def preprocess(data , pattern=24):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    if pattern == 12:
        pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({
        "user_message": messages,
        "message_date": dates,
    })
    # Parsing date time
    old_timestamp_pattern = r"\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s-\s"
    new_timestamp_pattern = r"\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s-\s"
    if re.match(old_timestamp_pattern, df["message_date"][0]):
        df["date"] = pd.to_datetime(df["message_date"], format="%d/%m/%Y, %H:%M - ")
    elif re.match(new_timestamp_pattern, df["message_date"][0]):
        df["date"] = pd.to_datetime(df["message_date"], format="%m/%d/%y, %H:%M - ")
    else:
        raise ValueError("Invalid format!")

    users = []
    messages = []
    for message in df["user_message"]:
        # split by : and split to user , message
        entry = re.split("([\w\W]+?):\s",message)
        if entry[1:]: # if it is user message (uname : message)
            users.append(entry[1])
            msg = entry[2]
        else: # if it is notification chat without user name
            users.append("notification")
            msg = entry[0]
        msg = msg.replace("\n", " ").strip() # \n removal
        msg = msg.replace("This message was deleted","")
        msg = msg.replace("<This message was edited>","")
        messages.append(msg)
    df["user"] = users
    df["message"] = messages
    df.drop(columns=["user_message"] , inplace=True)

    df["only_date"] = df["date"].dt.date
    df["year"] = df['date'].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] =  df['date'].dt.month_name()
    df["day"]=  df['date'].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    
    return df