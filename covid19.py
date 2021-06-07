# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px
from PIL import Image
from datetime import datetime as dt
import streamlit.components.v1 as components
import toml


st.title("COVID-19-Report")
st.write("India has been recovering from the 2nd wave of Covid-19. Access to the enormous amount of data makes it easier to visualize and understand what's really happening! Here is a dashboard that visualises the spread of the pandemic in the country. The data present in this analysis was taken from Kaggle. The data consists information about COVID-19 in India until May 31st. Click '>' on the top left corner to choose the analysis type. ")
image=Image.open("cov19.jpg")
st.image(image,use_column_width=True)
st.sidebar.title("ANALYSIS TYPE")
st.sidebar.markdown("Choose the type of analysis accordingly")
st.markdown("<style>body{background-color:blue;}</style>",unsafe_allow_html=True)





@st.cache(allow_output_mutation=True)


def state():
    statewise=pd.read_csv("archive (8)/StatewiseTestingDetails.csv")
    return statewise
@st.cache(allow_output_mutation=True)
def vaccine():
 vac=pd.read_csv("archive (8)/covid_vaccine_statewise.csv")
 return vac
@st.cache(allow_output_mutation=True)
def covid():
    cov=pd.read_csv("archive (8)/covid_19_india.csv")
    return cov
statewise=state()
vac=vaccine()
cov=covid()




analysis=st.sidebar.selectbox("Select analysis type", ("India-Daily report","Statewise analysis","Vaccination report"))
if analysis=="India-Daily report":
     data1=cov[['Date', 'State/UnionTerritory','Cured','Deaths','Confirmed']]
     data1 = data1.drop(labels=range(15086, 15114), axis=0)
     data1["Active Cases"]=data1["Confirmed"]-(data1["Cured"]+data1["Deaths"])
     daily = cov.groupby(['Date'])['Confirmed', 'Deaths','Cured',].sum().reset_index()
     daily['new_confirmed'] = daily.Confirmed.diff()
     daily['new_deaths'] = daily.Deaths.diff()
     daily['new_cured'] = daily.Cured.diff()

     data1_max=data1[data1["Date"]=="2021-05-31"]

     data1_max["Death rate"]=data1_max["Deaths"]/data1_max["Confirmed"]
     data1_max["Recovery rate"]=data1_max["Cured"]/data1_max["Confirmed"]
     data1_max.rename(columns={'State/UnionTerritory':'State'}, inplace=True)
     z=statewise.groupby("State")["TotalSamples"].last().reset_index()
     data1_max=pd.merge(data1_max,z,how="outer")
     
     data_top=data1_max.sort_values(by="Active Cases", ascending=False)
     data_top.drop(columns=["Date"],inplace=True)
     
     s=z.sort_values(by="TotalSamples",ascending=False)

     st.header("How is India dealing with the pandemic?")
    
     st.write("Here is the latest data that's available")
     st.write((daily[daily["Date"]==daily["Date"].max()]).transpose())
     st.write("Visualising the data to gain more insights📉")
     st.header("Confirmed, Deaths and Recovered")
     fig1 = go.Figure(go.Bar(x= daily.Date, y= daily.Cured, name='Recovered'))
     fig1.add_trace(go.Bar(x=daily.Date, y= daily.Deaths, name='Deaths'))
     fig1.add_trace(go.Bar(x=daily.Date, y= daily.Confirmed, name='Confirmed'))
     fig1.update_layout(barmode='stack',legend_orientation="h",legend=dict(x= 0.3, y=1.1),
                 paper_bgcolor='white',
                 plot_bgcolor = "white",)
    
     st.plotly_chart(fig1)
     st.write("The graph shown above makes it evident that the number of deaths is very less when compared to the daily confirmed cases and the number of people who recovered, so let's analyze the number of deaths separately.")
    
     st.header("Daily Deaths")
    
     fig_deaths=go.Figure(go.Bar(x= daily.Date, y= daily.new_deaths, name='Daily Deaths',marker_color="red" ))
    
  
     st.plotly_chart(fig_deaths)
     st.write("We see a clear downward trend post mid May")
     st.header("Let's now see how the trends have changed over the months this year.")
     data1['Date'] = pd.to_datetime(data1['Date'])
     df21=data1[(data1["Date"]>="2021-01-01") ]
    
    
     df21 = (df21.groupby(df21['Date'].dt.month_name(), sort=False)["Cured","Deaths","Confirmed","Active Cases"]).mean().reset_index()
     df21.drop(labels=range(5,6),axis=0,inplace=True)
     df21.Date.rename("Month",inplace=True)
     active=px.bar(y=df21["Active Cases"],x=df21.Date,labels={"x":"Month","y":"Active Cases"},color=df21["Active Cases"])
     cured=px.bar(y=df21["Cured"],x=df21["Date"],labels={"x":"Month","y":"Cured"},color=df21["Cured"])
     st.header("Monthly Active Cases")
     st.plotly_chart(active)
     st.write("The above graph indicates a clear spike in the number of cases in the month of April")
     st.header("Monthly Cured Cases")
     st.plotly_chart(cured)
     st.write("The number of recoveries is increasing steadily over the months.")
    
if analysis=="Statewise analysis":
    data1=cov[['Date', 'State/UnionTerritory','Cured','Deaths','Confirmed']]
    data1 = data1.drop(labels=range(15086, 15114), axis=0)
    data1["Active Cases"]=data1["Confirmed"]-(data1["Cured"]+data1["Deaths"])
    daily = cov.groupby(['Date'])['Confirmed', 'Deaths','Cured',].sum().reset_index()
    daily['new_confirmed'] = daily.Confirmed.diff()
    daily['new_deaths'] = daily.Deaths.diff()
    daily['new_cured'] = daily.Cured.diff()

    data1_max=data1[data1["Date"]=="2021-05-31"]

    data1_max["Death rate"]=data1_max["Deaths"]/data1_max["Confirmed"]
    data1_max["Recovery rate"]=data1_max["Cured"]/data1_max["Confirmed"]
    data1_max.rename(columns={'State/UnionTerritory':'State'}, inplace=True)
    z=statewise.groupby("State")["TotalSamples"].last().reset_index()
    data1_max=pd.merge(data1_max,z,how="outer")
    data_top=data1_max.sort_values(by="Active Cases", ascending=False)
    data_top.drop(columns=["Date"],inplace=True)
    s=z.sort_values(by="TotalSamples",ascending=False)
   
    
    
    state1=st.selectbox("Select a State or UT:",(data1_max["State"].unique()))
    st.write("Following is the data", state1,"." )
    state_data=data1_max.loc[data1_max["State"]==state1,['Date', 'State', 'Cured', 'Deaths', 'Confirmed',
       'Active Cases', 'Death rate', 'Recovery rate']]
    st.write(state_data)
    fig_state=go.Figure()
    fig_state.add_trace(go.Bar(x=state_data["State"],y=state_data["Confirmed"],text=state_data['Confirmed'],name="Total Confirmed Cases"))  
    fig_state.add_trace(go.Bar(x=state_data['State'],y=state_data['Active Cases'],text=state_data['Active Cases'],name="Active Cases"))
    
    fig_state.add_trace(go.Bar(x=state_data["State"],y=state_data["Deaths"],text=state_data['Deaths'],name="Deaths") )   
    fig_state.update_layout(barmode='group',legend_orientation="h",legend=dict(x= 0.3, y=1.1))
    st.plotly_chart(fig_state)
    st.header("Let us see an overview of how is each state coping with the virus.")
    ste_act=px.line(data1,x='Date',y='Active Cases', color="State/UnionTerritory",width=800,height=400)
  

    st.plotly_chart(ste_act)
    
    st.write("The graph shows how the number of active cases changed ever since the first case was reported. Maharashtra faced a severe surge during both the waves of the pandemic.The surge during the second wave in the months of March-May is very steep and almost double that of the previous one.")
    st.header("Mortality")
    state_deaths=px.line(data1,x='Date',y='Deaths', color="State/UnionTerritory",width=800,height=400)
    st.plotly_chart(state_deaths)
    
    p_rate=px.bar(data1_max,x="State",y="Death rate",color="Death rate",width=1000)
    st.header("Death Rate")
    st.plotly_chart(p_rate)
    st.write("While Maharashtra has the highest number of deaths (94.84K) followed by Karnataka(29.09K), Punjab is seen to have the highest mortality rate.")
    
    st.header("Total Samples taken")
    samples=px.bar(statewise,x=statewise["State"],y="TotalSamples",color="State",width=800,height=400)
    
    st.plotly_chart(samples)

    
    st.write("As of 31st May, UP has done the most number of tests and it can be correlated to it being the most populous state in India. The testing is comparitively low in the union territories, considering the low population.Testing in states like Uttrakhand, Bihar,West Bengal,Orissa can be ramped up even more.")
    st.header("Recovered Cases")
    p1=px.bar(data1_max, x="State",y=data1_max["Cured"], color="Cured", height=500,width=1000)
    
    st.plotly_chart(p1)
    st.header("Active Cases in each state(as of 31/05)")
    p3=px.bar(data1_max,x="State",y="Active Cases",color="Active Cases",width=1000)
    st.plotly_chart(p3)
    st.write("As of 31st May, Karnataka leads the chart with highest number of Active cases, followed by Tamil Nadu and Maharashtra")
    st.header("Recovery Rate")
    
    p2=px.bar(data1_max,x="State",y="Recovery rate",color="Recovery rate",width=1000,height=800, )
    
    st.plotly_chart(p2)
    st.header("States with maximum number of cases:")
    st.write("For better understanding, here are the 10 states with maximum number of active cases (as of 31st May)")
    st.write(data_top.head(10))
    st.write("The choropleth has been plotted on tableau, Move your cursor on any of the states to get an overview")
    html_temp='''<div class='tableauPlaceholder' id='viz1623002119639' style='position: relative'><noscript><a href='#'><img alt='COVID-19 Scenario,(As of 31st May) ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;co&#47;covid-19may31&#47;Sheet1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='covid-19may31&#47;Sheet1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;co&#47;covid-19may31&#47;Sheet1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1623002119639');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''                        
    components.html(html_temp, width=700,height=500)
   
  
if analysis=="Vaccination report":
    vac["Updated On"]=pd.to_datetime(vac["Updated On"])
    vac=vac[vac["Updated On"]<"2021-06-01"]
    vaccine=vac.groupby("State")["Updated On","Total Individuals Vaccinated","Total Sessions Conducted","Total Sites ","First Dose Administered","Second Dose Administered","Male(Individuals Vaccinated)","Female(Individuals Vaccinated)","Transgender(Individuals Vaccinated)",	"Total Covaxin Administered"	,"Total CoviShield Administered","Total Doses Administered"].last().reset_index()
    vaccine["Total Individuals Vaccinated"].sum()
    Indian_population=1392234846.0
    vacs_left=Indian_population-336787050.0
    Percentage_left=(vacs_left/Indian_population)*100
    vac_india=vac[vac["State"]=="India"]
    vaccine.drop(labels=13,inplace=True)
    vaccination=vac.groupby("State")['Total Individuals Vaccinated','Male(Individuals Vaccinated)','Female(Individuals Vaccinated)', 'Transgender(Individuals Vaccinated)','First Dose Administered',	'Second Dose Administered','Total Covaxin Administered', 'Total CoviShield Administered','Total Doses Administered'].last()
    vaccination.reset_index()

    vac2=vac.groupby("State")["Total CoviShield Administered","Total Covaxin Administered"].last().reset_index()

    INDIA_VACS=vac2[vac2["State"]=="India"]
    India_status=vaccination.iloc[13:14]
    l=[90095606.0/168393525.0, 78271582.0/	168393525.0,26337.0/168393525.0]
    y=vac2["Total CoviShield Administered"].sum()
    x=vac2["Total Covaxin Administered"].sum()
    vact=[x,y]

    

    st.header("Let us look at how the vaccination drive is going on in the country")
    st.write("First, we need to make sense out of the numbers. The following data gives a gist of how far we have suceeded with the ongoing drive")
    st.write(India_status.transpose())
    st.write("Numbers do not provide the best picture, So it is always better to visualize to draw necessary conclusions 📊")
    st.header("Individuals vaccinated in each state")
    figx=go.Figure()
    figx.add_trace(go.Bar(x=vaccine["State"],y=vaccine["Male(Individuals Vaccinated)"],name="Male"))
    figx.add_trace(go.Bar(x=vaccine["State"], y= vaccine["Female(Individuals Vaccinated)"], name='Female'))
    figx.add_trace(go.Bar(x=vaccine["State"], y= vaccine["Transgender(Individuals Vaccinated)"], name='Transgender'))
    st.write("The graph shows proportion of genders vaccinated in each state. The male is to female ratio seems balanced whereas the colour representing the transgender or third gender is hardly seen. This might be because of the large disparity in population. In India there are about 490,000 people who identify as the third gender. And about 67% of them live in rural areas. It should be made sure that they are being given access to all the facilities in a safe and secured way. ")
    figx.update_layout(barmode='stack',legend_orientation="h",legend=dict(x= 0.3, y=1.1),
                 paper_bgcolor='white',
                 plot_bgcolor = "white",)
    st.plotly_chart(figx)
    st.header("Gender-wise Distribution")
    gender=px.pie(India_status,names=["Male(Individuals Vaccinated)","Female(Individuals Vaccinated)","Transgender(Individuals Vaccinated)"], values=l,color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(gender)
    st.write("The pie chart shows, the number of transgenders who have been administerd the vaccine account to only 0.0156% of the total. People should be made aware and responsibility should be taken up by higher bodies for a faster, smoother and a fair vaccination drive. ")
    
    st.write("Population of India as on 3rd June is about 1.392 Billion, out of which 336787050.0 have atleatst got their first jab, hence we still have" ,round(Percentage_left,3),"% of poplulation who are yet to receive their ammunition against the virus.")
    st.header("Vaccines")
    
   
    st.write("India has been adminsistering two of its indigenous vaccines to its population, i.e. Covaxin and CoviShield. The following data shows the state-wise consumption of both the vaccines as of 31st May 2021 ")
    st.write(vac2.drop(labels=13))
    type=px.pie(India_status,names=["Total Covaxin Administered","Total CoviShield Administered"], values=vact, color_discrete_sequence=px.colors.sequential.Burg)
    st.plotly_chart(type)
    
    st.header("State-wise Vaccination Summary")
    st.write(vaccination)
    st.write("The following Choropleth shows the progress of the vaccination drive in the country. Move your cursor over any of the states to get a quick summary.")
    vac_temp='''<div class='tableauPlaceholder' id='viz1622789126447' style='position: relative'><noscript><a href='#'><img alt='VACCINATION DATA ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;va&#47;vaccinationdata_16227420602060&#47;Sheet1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='vaccinationdata_16227420602060&#47;Sheet1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;va&#47;vaccinationdata_16227420602060&#47;Sheet1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1622789126447');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''
    components.html(vac_temp, width=700,height=500)
