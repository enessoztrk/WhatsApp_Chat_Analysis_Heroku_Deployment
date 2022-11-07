import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import preprocessor,helper
from PIL import Image
import plotly


st.sidebar.title('WhatsApp Chat Analysis')
col1, col2,col3,col4= st.sidebar.columns([1,2,2,1])

with col2:
    st.image('icon.png', width=120)

st.title('WhatsApp Chat Analyzer')
with st.expander('See!!.. How it works?'):
    st.subheader('Steps to Analyze:')
    st.markdown(
        '1. Export your WhatsApp chat (Steps to export: Open your WhatsApp in phone>Open Chat> Click on three dots>More>Export '
        'Chat> Without Media>Save anywhere or save on Google Drive.)')
    st.markdown('2. Browse your chat file or drag and drop(if you are using phone then click \' > \' left side, if sidebar not visible)')
    st.markdown('3. Select User: default All, means data will be analyzed for all users/groups')
    st.markdown('4. Click on Show Analysis button')
    st.markdown(
        '5. Turn on Wide mode for better viewing exprience from settings, If you are using phone then close the sidebar for better view')
    st.markdown(
        '6. If you want analyze for single user, just select the name from the dropdown and click on \'Show '
        'Analysis\' button')
    st.markdown(
        '7. If you want to analyze another chat, repeat the same above steps')

# file upload
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat text file:")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode(encoding='utf-8')
    df = preprocessor.preprocess(data)

    # extracting all unique username from df['name'], to show the name list
    user_list = sorted(df['user'].unique())
    # adding 'All' at first position of name list
    user_list.insert(0, "All")
    user_list.remove('group_notification')
    # getting the selected username from dropdown list
    selected_user = st.sidebar.selectbox('Select Username',
                                         user_list)

    if st.sidebar.button("Show Analysis"):
        if selected_user == 'All':
            df1 = df
        else:
            df1 = df[df['user'] == selected_user]

        noOfUsers, noOfmsgs, noOfWords, noOfMedia, noOfLinks = helper.get_msg_stats(df1)
        # displaying stats
        st.subheader(f'Statistics: {selected_user}')

        col1, col2, col3, col4 = st.columns([1, 1.5, 1.5, 1])

        start_dt = str(df['date'].iloc[0])[:10]
        last_dt = str(df['date'].iloc[-1])[:10]
        col2.metric('Chat From:', start_dt)
        col3.metric('Chat To:', last_dt)

        col1, col2, col3, col5 = st.columns(4)
        col1.metric("Total Members", noOfUsers)
        col2.metric("Total Messages", noOfmsgs)
        col3.metric("Total Words Used", noOfWords)
        col5.metric('Total Links Shared', noOfLinks)

 # bar plot of user activity
        with st.expander("Who is the most active members in chat?...click '+' to see details"):
            st.markdown(
                ' In this below graph you will find All the members in the chat. The longest bar shows highest contribution in chat means his/her total number of message has highest in chat then others and the smallest bar shows low contributaion in chat.\n In second graph Red Line shows average messages of all users. You can see how much members chat is above and below the average line.')
#
        user_count = df['user'].value_counts()
        st.bar_chart(user_count)

# plotly bar plot of user activity
        user_count = df['user'].value_counts().reset_index()
        fig = px.bar(user_count, x='index', y='user', labels={'user': 'No of Messages', 'index': 'Members Name '},
                     color='user')
        fig.update_layout(title_text='Members activity in Sorted Order(High to Low)', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        fig.add_hline(y=user_count['user'].mean(), line_width=3, line_color="red")
        st.plotly_chart(fig, use_container_width=True)

        with st.expander(
                "Who has had the most messages in term of %...click '+' to see more details"):
            st.markdown(
                'This graph is known as Donut chart, \n A Donut chart is a circular statistical graphic, which is divided into slices to illustrate numerical proportion. Right side you will names of members with color represents in graph, click on color of name to remove from chart')

# pie chart of user activity percentage
        user_count = df['user'].value_counts().reset_index()
        user_count.columns = ['member', 'message']
        fig = px.pie(user_count, names='member', values='message', hole=0.5)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        #fig.update_layout(title_text='Users Activity in Percentage', title_x=0.5,
        #                   font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

# Top 5 Most and Less active members
        col1, col2, col3 = st.columns([1.5, 0.2, 1.5])
        top5 = df['user'].value_counts().sort_values(ascending=False).reset_index().iloc[0:5]
        top5.columns = ['Member', 'Message']
        with col1:
            st.markdown('Most Active Members')
            st.dataframe(top5)

        last5 = df['user'].value_counts().sort_values().reset_index().iloc[0:5]
        last5.columns = ['Member', 'Message']
        with col3:
            st.markdown('Less Active Members')
            st.dataframe(last5)

        if selected_user == 'All':
            # chat started and ended by members
            with st.expander(f"Who started and ended chat most of time?... Click on '+' to see more details."):
                st.markdown(
                    "Here in below right side chart you will see chat started by member each day in percentage and in right chart you will see chat ended by member.")

            col1, col2 = st.columns(2)
            chat_started, chat_ended = helper.chat_start_end_by(df1)
            fig = px.pie(chat_started, names='Member', values='Count', hole=0.3)
            fig.update_layout(title_text=f'Chat Started by', title_x=0.5,
                              font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update(layout_showlegend=False)
            with col1:

                # st.markdown('Chat Started by members in each day')
                st.plotly_chart(fig, use_container_width=True)

            fig = px.pie(chat_ended, names='Member', values='Count', hole=0.3)
            fig.update_layout(title_text=f'Chat Ended by', title_x=0.5,
                              font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update(layout_showlegend=False)

            with col2:
                # st.markdown('Chat Ended by members in each day')
                st.plotly_chart(fig, use_container_width=True)

        # wordcloud
        with st.expander(f"Which words have occurred most no of times?... click '+' to see more details"):
            st.markdown(
                'This graph is known as Word Map, \n Words in bigger size shows most no of used where smallest size shows less no of used. Also top 10 and list of all words used with their counts shown below.\n There are two word map chart one without stop words and another with stopwords.\n')
        #word_img, word_df = helper.wordMap_without_stopwords(df1)
        #fig, ax = plt.subplots()
        #ax.imshow(word_img)
        #plt.title(f'Most Used Words in Chat by {selected_user}', fontdict={'fontsize': 15}, loc='center', color='r')
        #plt.axis('off')
        #st.markdown('Wordmap without stopwords')
        #st.pyplot(fig)

        col1, col2, col3 = st.columns([2, 0.2, 1.7])

        #with col1:
            # bar chart of most used words
            #fig = px.bar(word_df.sort_values(by='count', ascending=False).head(10), x='count', y='words', color='count')
            #fig.update_layout(title_text=f'10 Most Words Used', title_x=0.5,
                              #font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
            #st.plotly_chart(fig, use_container_width=True)
        
        #with col3:
            #st.markdown(f'List of 30 most used words')
            #st.dataframe(word_df.sort_values(by='count', ascending=False).reset_index(drop=True).head(30))

        word_img, word_df = helper.wordMap_with_stopwords(df1)
        fig, ax = plt.subplots()
        ax.imshow(word_img)
        plt.title(f'Most Used Words in Chat by {selected_user}', fontdict={'fontsize': 15}, loc='center', color='r')
        plt.axis('off')
        st.markdown('Wordmap with stopwords')
        st.pyplot(fig)

        col1, col2, col3 = st.columns([2, 0.2, 1.7])
        with col1:
            # bar chart of most used words
            fig = px.bar(word_df.sort_values(by='count', ascending=False).head(10), x='count', y='words', color='count')
            fig.update_layout(title_text=f'10 Most Words Used', title_x=0.5,
                              font={'family': 'Arial', 'size': 10}, xaxis_showgrid=False, yaxis_showgrid=False)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown(f'List of 30 most used words')
            st.dataframe(word_df.sort_values(by='count', ascending=False).reset_index(drop=True).head(30))


        # Emoji Used
        with st.expander(f"Which were the most used emoji in chat?... click '+' to see more details"):
            st.markdown(
                'This graph is known as Pie Chart.  \nSome emoji which look like box is not recoganised by system...')

        emoji_df = helper.get_emojis(df1)

        col1, col2, col3 = st.columns([2, 0.3, 1])
        with col1:
            # st.markdown('Top 10 Most used Emoji')
            fig = px.pie(emoji_df.head(10), names='emoji', values='counts')
            fig.update_layout(title_text=f'Top 10 Most used Emoji', title_x=0.5,
                              font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update(layout_showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.empty()
        with col3:
            st.markdown(f'List of all used emoji')
            st.dataframe(emoji_df)

        with st.expander(f"Activity Over the periods!... click '+' to see more details"):
            st.markdown(
                'This graph is known as Line Chart.  \nIt shows how activity gradually increasing or decreasing by over period ')

        # line chart daily activity of day and message
        x = df['day_name'].value_counts().sort_index()
        fig = px.line(x=x.index, y=x.values, markers=True, labels={'y': 'Message Count', 'x': 'Day Name'}, height=400,
                      width=400)
        fig.update_layout(title_text='Weekly Chat Behavior by All', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)


        # line chart daily activity of day and message
        x = df['day'].value_counts().sort_index()
        fig = px.line(x=x.index, y=x.values, markers=True, labels={'y': 'Message Count', 'x': 'Day'}, height=400,
                      width=400)
        fig.update_layout(title_text='Daily Chat Behavior by All', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        # Activity of All Users on a single Day of month
        x = df1[['day', 'user']].value_counts().reset_index().sort_values(by='day')
        fig = px.line(x, x='day', y=0, markers=True, labels={'0': 'Message Count', 'day': 'Day'}, color='user')
        fig.update_layout(title_text=f'Daily Activity of {selected_user} ', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        # line chart of month and message
        x = df['month'].value_counts().sort_index()
        fig = px.line(x=x.index, y=x.values, markers=True, labels={'y': 'Message Count', 'x': 'Month'})
        fig.update_layout(title_text=' Monthly Activity of All Users', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        # Activity of All Users on a single month
        x = df1[['month', 'user']].value_counts().reset_index().sort_values(by='month')
        fig = px.line(x, x='month', y=0, markers=True, labels={'0': 'Message Count', 'month': 'Month'}, color='user')
        fig.update_layout(title_text=f'Monthly Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)


        # Activity of All Users on a single Day of month
        x = df1[['year', 'user']].value_counts().reset_index().sort_values(by='year')
        fig = px.line(x, x='year', y=0, markers=True, labels={'0': 'Message Count', 'year': 'Year'}, color='user')
        fig.update_layout(title_text=f'Yearly Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        # line chart of date and message
        x = df['date'].value_counts().sort_index()
        st.write('Line Chart with Date wise Activity of All Users(X-axis: Date, Y-axis: Message Count')
        st.line_chart(x)

        # Activity of All Users on a single Day of month
        x = df1[['date', 'user']].value_counts().reset_index().sort_values(by='date')
        fig = px.line(x, x='date', y=0, markers=True, labels={'0': 'Message Count', 'date': 'Date'}, color='user')
        fig.update_layout(title_text=f'Date wise Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16}, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

        with st.expander(f"{selected_user} Activity ... click '+' to see more details"):
            st.markdown(
                'Below graphs known as Heatmap Chart.  \n Darkest Color shows low possibility where brightest color shows high possibility.\nPls check the color scale and follor the code. If any days name or month name is missing means there is no chat had in that day or month')


        st.plotly_chart(fig, use_container_width=True)

        # heatmap Day and Month Activity
        fig = px.imshow(pd.crosstab(df1['month'], df1['day']))
        fig.update_layout(title_text=f'Daily over Monthly Chat Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        # heatmap weekdays and Month Activity
        fig = px.imshow(pd.crosstab(df1['day_name'], df1['day']),width=700)
        fig.update_layout(title_text=f'Weekly Over Daily  Chat Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        # heatmap Day and hour Activity
        fig = px.imshow(pd.crosstab(df1['hour'], df1['day']),color_continuous_scale=['black', 'red'])
        fig.update_layout(title_text=f'Daily Over Hourly Chat Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        # heatmap weekday and hour Activity
        fig = px.imshow(pd.crosstab(df1['hour'], df1['day_name']))
        fig.update_layout(title_text=f'Weekly Over Hourly Chat Activity of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        # heatmap minute and hour Activity
        fig = px.imshow(pd.crosstab(df1['hour'], df1['minute']))
        fig.update_layout(title_text=f'Minutes Over Hourly Chat Activity    of {selected_user}', title_x=0.5,
                          font={'family': 'Arial', 'size': 16})
        st.plotly_chart(fig, use_container_width=True)

        df1['message_chars'] = df1['message'].apply(lambda z: len(z))
        longest_msg = df1.sort_values(by='message_chars', ascending=False)[
            ['date', 'hour', 'minute', 'user', 'message', 'message_chars']].head(5).reset_index(drop=True)
        longest_msg['date'] = longest_msg['date'].apply(lambda x: str(x)[:10])
        longest_msg['time'] = longest_msg['hour'].apply(lambda x: str(x)) + ":" + longest_msg['minute'].apply(
            lambda x: str(x))
        st.markdown(f"Top 5 longest Message of {selected_user}")
        st.table(longest_msg[['date', 'time', 'user', 'message', 'message_chars']])

        a = df1.groupby(by='date')
        top = a.size().sort_values(ascending=False).index[0]
        top5_msg = a.get_group(top).sort_values(by='message_chars', ascending=False)[
            ['date', 'day_name', 'user', 'message']].head(5).reset_index(drop=True)
        top5_msg['date'] = top5_msg['date'].apply(lambda x: str(x)[:10])
        st.markdown(f'5 Longest message of highest chat happened on a single day by {selected_user}')
        st.table(top5_msg)

        links = helper.get_liks(df1)
        st.markdown('Links Shared')
        st.table(links)
