# WhatsApp Chat Analysis Heroku Deployment
## About this project:
- The main goal of this project is to analys the whatsapp chat and represents through charts and visuals.
- Project is live now and deployed on heroku. visit at https://wp-analyzer.herokuapp.com/
- This projects can be used for indivisual as well as group chats.
​
## Idea:
1. Created a function that convert WhatsApp chat text file into dataframe with columns name(['date', 'year', 'month', 'day', 'hour', 'minute', 'month_name','day_name', 'user', 'message', 'message_chars'])
​
2. Which Data you will get in this analysis
1. Sum
    - Chat starting date, first entry in chat
    - Chat Ending Date, last entry in chat
    - Total Members in chat, only those who had sent atleat one message
    - Total Messsages, including messages, missed calls, media, links
    - Total Words of Messages, 
    - Total Links Shared
    - Total Missed Calls
2. Bar chart of no messages sent by members
3. Bar chart of no messages sent by members with mean line
4. Pie chart with no if messages sent in %
5. Pie chat of Who started and ended chat most of the time
6. WordMap of most 75 words used in chat with stopwords and without stopwords
7. Box Plot of who sent the longest messages
8. Pie chart of most used emoji
9. Sunburt chart of members and thier weekly messages(and yearly,monthly,weekly)
10. Line chart of Daily chat activity(same monthly, yearly) for all and indivisuals
11. Heatmap represents which has occured more on given to features
12. Table of 5 longest message in entire chat
13. Table of 5 Longest message of highest chat happened on a single day
14. Table of all shared links in chat
    
## Charts used to represents data:
    - Bar, Line, Box, WordMap, Sunburst Heatmap
    
## Librabry used
   - **streamlit** : for web application
   - **matplotlib**: for charts 
   - **plotly** : intrective charts
   - **pandas**: for creation of dataframe
   - **PIL**: opening image file 
   - **re** : regular expression
   - **urlextract**: for extracting URL from chat
   - **collections**: for counting each words
   - **wordcloud**: creating wordmap
   - **emoji**: extracting emoji from chat
   - **warnings**: ignore warnings
​
# Code written in pycharm in three files
- **app.py** : main file
- **preprocessor.py**: for generatig dataset
- **helper.py**: user defined functions as per required
​
# How to use:
1. To use this webapp first you whatapp chat txt file.
    - You can try your whatsapp of any individuals or groups chat this is 100% SAFE and SECURE, I don't have access to this webapp. So, feel free to use.
    - To export your chat: follow the steps given below:
        - Open your whatsapp in mobile only
        - Open any chat
        - click on three vertical dots (upper right corner)
        - click on More
        - click on Export Chat, proceed with Without Media
        - Now save this file anywhere you want.
        
2. Now, vist at https://wp-analyzer.herokuapp.com/
3. Page will look like below
![what2](https://github.com/enessoztrk/WhatsApp_Chat_Analysis_Heroku_Deployment/blob/main/img/1.png?raw=true)
4. To see details how it works click on plus icon '+', click again '-' to close
5. Browse your file or drang and drop in the file box.
6. Once your file has been uploaded all members name will be visible in dropdown menu,default selecte All, if you want to analys for indivisual member then select that member and click on 'Show Analysis'.


# Some Snapshots:
![what3](https://github.com/enessoztrk/WhatsApp_Chat_Analysis_Heroku_Deployment/blob/main/img/2.png?raw=true)
![what3](https://github.com/enessoztrk/WhatsApp_Chat_Analysis_Heroku_Deployment/blob/main/img/3.png?raw=true)
![what3](https://github.com/enessoztrk/WhatsApp_Chat_Analysis_Heroku_Deployment/blob/main/img/4.png?raw=true)
![what3](https://github.com/enessoztrk/WhatsApp_Chat_Analysis_Heroku_Deployment/blob/main/img/5.png?raw=true)
![what3](https://github.com/enessoztrk/WhatsApp_Chat_Analysis_Heroku_Deployment/blob/main/img/6.png?raw=true)
![what3](https://github.com/enessoztrk/WhatsApp_Chat_Analysis_Heroku_Deployment/blob/main/img/7.png?raw=true)
![what3](https://github.com/enessoztrk/WhatsApp_Chat_Analysis_Heroku_Deployment/blob/main/img/8.png?raw=true)
![what3](https://github.com/enessoztrk/WhatsApp_Chat_Analysis_Heroku_Deployment/blob/main/img/9.png?raw=true)

 
