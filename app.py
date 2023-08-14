import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
st.sidebar.title("whatsapp chat analyser")
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)

    # fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'overall')
    selected_user=st.sidebar.selectbox('show analysis wrt',user_list)
    if st.sidebar.button('show Analysis'):
        num_messages,words,num_media_messages,links=helper.fetch_stats(selected_user,df)
        st.title('top Statistics')
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)
        with col2:
            st.header('Total words')
            st.title(words)
        with col3:
            st.header('Total media')
            st.title(num_media_messages)
        with col4:
            st.header('Total links')
            st.title(links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig = go.Figure(data=[go.Bar(x=daily_timeline['only_date'], y=daily_timeline['message'])])
        st.plotly_chart(fig)

        # activity heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)






        # finding the busiest users in the group
        if selected_user=='overall':
            st.title('most busy users')
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        # wordcloud
        st.title('word cloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        # most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)
        # emoji analysis
        emojis_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emojis_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emojis_df[1].head(), labels=emojis_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)








