# Importing Libraries
import pandas as pd
import streamlit as st
from PIL import Image
import psycopg2
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu


# Setting up page configuration
icon = Image.open("ICN.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by Harish
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")    

# Creating connection with pgAdmin workbench
mydb = psycopg2.connect(host ="localhost",
                        user="postgres",
                        password="Argentina",
                        database="phonepay"
                        )
mydb.autocommit = True

cursor = mydb.cursor()

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
    
    
# MENU 1 - HOME
if selected == "Home":
    st.image("img.png")
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, PgAdmin, pgAdmin-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image("Home.png")    
        
        
# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[States]")
            cursor.execute(f"select states, sum(transaction_count) as Total_Transactions_Count, sum(transaction_amount) as Total from aggregated_transaction where years = {Year} and quarter = {Quarter} group by states order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['states', 'transaction_count','transaction_amount'])
            fig = px.pie(df, values='transaction_amount',
                             names='states',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['transaction_count'],
                             labels={'transaction_count':'transaction_count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[Districts]")
            cursor.execute(f"select districts , sum(Count) as Total_Count, sum(amount) as Total from map_transaction where years = {Year} and quarter = {Quarter} group by districts order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['districts', 'count','amount'])

            fig = px.pie(df, values='amount',
                             names='districts',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['count'],
                             labels={'count':'count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

        with col3:
            st.markdown("### :violet[Pincodes]")
            cursor.execute(f"select pincodes, sum(count) as Total_Transactions_Count, sum(amount) as Total from top_transaction where years = {Year} and quarter = {Quarter} group by pincodes order by Total desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincodes', 'count','amount'])
            fig = px.pie(df, values='amount',
                             names='Pincodes',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['count'],
                             labels={'count':'count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
        
        
 #Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### Sorry No Data to Display for 2023 Qtr 4")
            else:
                cursor.execute(f"select brand, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from aggregated_user where years = {Year} and quarter = {Quarter} group by brand order by Total_Count desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)  
                                      
        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(f"select districts, sum(registereduser) as Total_Users, sum(appopens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} group by districts order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['district', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="district",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)      
            
        with col3:
            st.markdown("### :violet[Pincode]")
            cursor.execute(f"select pincodes, sum(registereduser) as Total_Users from top_user where years = {Year} and quarter = {Quarter} group by pincodes order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['pincodes', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='pincodes',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)   
            
        with col4:
            st.markdown("### :violet[State]")
            cursor.execute(f"select states, sum(registereduser) as Total_Users, sum(appopens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} group by states order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['states', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='states',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)             
                            
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
                                
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            cursor.execute(f"select states, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} group by states order by states")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['states', 'Total_Transactions', 'Total_amount'])
            df1.states.replace({"andaman-&-nicobar-islands":"Andaman & Nicobar","andhra-pradesh":"Andhra Pradesh","arunachal-pradesh":"Arunachal Pradesh","assam":"Assam","bihar":"Bihar","chandigarh":"Chandigarh",
                               "chhattisgarh":"Chhattisgarh","dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu","delhi":"Delhi","goa":"Goa","gujarat":"Gujarat","haryana":"Haryana","himachal-pradesh":"Himachal Pradesh","jammu-&-kashmir":"Jammu & Kashmir","jharkhand":"Jharkhand","karnataka":"Karnataka",
                               "kerala":"Kerala","ladakh":"Ladakh","lakshadweep":"Lakshadweep","madhya-pradesh":"Madhya Pradesh","maharashtra":"Maharashtra","manipur":"Manipur","meghalaya":"Meghalaya","mizoram":"Mizoram","nagaland":"Nagaland","odisha":"Odisha","puducherry":"Puducherry","punjab":"punjab","rajasthan":"Rajasthan","sikkim":"Sikkim","tamil-nadu":"Tamil Nadu",
                               "telangana":"Telangana","tripura":"Tripura","uttar-pradesh":"Uttar Pradesh","uttarakhand":"Uttarakhand","west-bengal":"West Bengal"},inplace = True)
                               
            st.write(df1)
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='states',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True) 
            
# Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            cursor.execute(f"select states, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} group by states order by states")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['states', 'Total_Transactions', 'Total_amount'])
            #df2 = pd.read_csv('Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.states.replace({"andaman-&-nicobar-islands":"Andaman & Nicobar","andhra-pradesh":"Andhra Pradesh","arunachal-pradesh":"Arunachal Pradesh","assam":"Assam","bihar":"Bihar","chandigarh":"Chandigarh",
                               "chhattisgarh":"Chhattisgarh","dadra-&-nagar-haveli-&-daman-&-diu":"Dadra and Nagar Haveli and Daman and Diu","delhi":"Delhi","goa":"Goa","gujarat":"Gujarat","haryana":"Haryana","himachal-pradesh":"Himachal Pradesh","jammu-&-kashmir":"Jammu & Kashmir","jharkhand":"Jharkhand","karnataka":"Karnataka",
                               "kerala":"Kerala","ladakh":"Ladakh","lakshadweep":"Lakshadweep","madhya-pradesh":"Madhya Pradesh","maharashtra":"Maharashtra","manipur":"Manipur","meghalaya":"Meghalaya","mizoram":"Mizoram","nagaland":"Nagaland","odisha":"Odisha","puducherry":"Puducherry","punjab":"punjab","rajasthan":"Rajasthan","sikkim":"Sikkim","tamil-nadu":"Tamil Nadu",
                               "telangana":"Telangana","tripura":"Tripura","uttar-pradesh":"Uttar Pradesh","uttarakhand":"Uttarakhand","west-bengal":"West Bengal"},inplace = True)


            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='states',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        cursor.execute(f"select transaction_type, sum(transaction_count) as Total_Transactions, sum(transaction_amount) as Total_amount from aggregated_transaction where years= {Year} and quarter = {Quarter} group by transaction_type order by transaction_type")
        df = pd.DataFrame(cursor.fetchall(), columns=['transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)   
        
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)

        cursor.execute(f"select states, districts,years,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transaction where years = {Year} and quarter = {Quarter} and states = '{selected_state}' group by states, districts,years,quarter order by states,districts")
        
        df1 = pd.DataFrame(cursor.fetchall(), columns=['states','districts','years','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="districts",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)   
        
# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        cursor.execute(f"select states, sum(registereduser) as Total_Users, sum(appopens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} group by states order by states")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['states', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='states',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)    
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        cursor.execute(f"select states,years,quarter,districts,sum(registereduser) as Total_Users, sum(appopens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} and states = '{selected_state}' group by States, districts,years,quarter order by states,districts")
        
        df = pd.DataFrame(cursor.fetchall(), columns=['states','years', 'quarter', 'districts', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="districts",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)  
        
# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        st.write("**:violet[My Project GitHub link]** ⬇️")
        st.write("https://github.com/Harichan7")
        st.write("**:violet[Image and content source]** ⬇️")
        st.write("https://www.prnewswire.com/in/news-releases/phonepe-launches-the-pulse-of-digital-payments-india-s-first-interactive-geospatial-website-888262738.html")
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("Pulseimg.jpg")                                                                  