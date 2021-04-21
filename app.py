#!/usr/bin/env python
# coding: utf-8
'''
Written by Aravind
python3.6 and above
start date 10/03/2021
end date -------
'''
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
from plotly import tools
import plotly.offline as py
import plotly.express as px
from bokeh.models.widgets import Div


DistrictAPI = "https://api.covid19india.org/state_district_wise.json"
StateAPI= "https://api.covid19india.org/data.json"

StateResponse = requests.request("GET", StateAPI)
data1 =json.loads(StateResponse.text)
DistrictResponse = requests.request("GET", DistrictAPI)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
            content:'Made by Aravind'; 
            visibility: visible;
            display: block;
            position: relative;
            #background-color: red;
            padding: 5px;
            top: 2px;
        }
                    </style>
        """

def totalactive():
    active=[]
    date=[]
    data = (data1["cases_time_series"])
    for india in data:
        date_element=str((india["date"]))
        d = datetime.strptime(date_element, '%d %B %Y')
        date.append(d.strftime('%Y-%m-%d'))
        active.append((int(india["totalconfirmed"])-int(india["totaldeceased"])-int(india["totalrecovered"])))
    np_date = np.array(date) 
    np_active = np.array(active) 
    df = pd.DataFrame({'date':np_date, 'active':np_active})
    for_graph = df = pd.DataFrame({'date':np_date, 'active':np_active})
    df['date'] = pd.to_datetime(df['date'])
    firstdate=(pd.to_datetime(df['date']).dt.date.iloc[0])
    lastdate=(pd.to_datetime(df['date']).dt.date.iloc[-1])
    st.title('COVID_19 Analysis - INDIA')
    st.write("DATE VS ACTIVE CASES")
    date_range = st.slider(
        "Select date range to view:",
        value=(datetime.strptime(str(firstdate), "%Y-%m-%d"),datetime.strptime(str(lastdate), "%Y-%m-%d")))
    dates = list(date_range)
    from_date=(dates[0].strftime('%Y-%m-%d'))
    to_date=(dates[1].strftime('%Y-%m-%d'))
    mask = df['date'].between(from_date, to_date, inclusive=False)
    df=df.loc[mask]
    df = df.rename(columns={'date':'index'}).set_index('index')
    st.bar_chart(df)
    for_graph
    deaths()

def deaths():
    data = (data1["cases_time_series"])
    date=[]
    confirm_cases=[]
    for india in data:
        date_element=str((india["date"]))
        d = datetime.strptime(date_element, '%d %B %Y')
        date.append(d.strftime('%Y-%m-%d'))
        confirm_cases.append(int(india["dailydeceased"]))
    np_date = np.array(date) 
    np_cases = np.array(confirm_cases) 
    df = pd.DataFrame({'date':np_date, 'dailydeceased':np_cases})
    df['date'] = pd.to_datetime(df['date'])
    firstdate=(pd.to_datetime(df['date']).dt.date.iloc[0])
    lastdate=(pd.to_datetime(df['date']).dt.date.iloc[-1])
    st.write("DATE VS DEATH RATE")
    date_range = st.slider(
        "Select range to view:",
        value=(datetime.strptime(str(firstdate), "%Y-%m-%d"),datetime.strptime(str(lastdate), "%Y-%m-%d")))
    dates = list(date_range)
    from_date=(dates[0].strftime('%Y-%m-%d'))
    to_date=(dates[1].strftime('%Y-%m-%d'))
    mask = df['date'].between(from_date, to_date, inclusive=False)
    df=df.loc[mask]
    df = df.rename(columns={'date':'index'}).set_index('index')
    st.bar_chart(df)
    deaths_vs_totalcases()


def deaths_vs_totalcases():
    data = (data1["cases_time_series"])
    date=[]
    active=[]
    death=[]
    recovered=[]
    for india in data:
        date_element=str((india["date"]))
        d = datetime.strptime(date_element, '%d %B %Y')
        date.append(d.strftime('%Y-%m-%d'))
        active.append((int(india["totalconfirmed"])-int(india["totaldeceased"])-int(india["totalrecovered"])))
        recovered.append(int(india["totalrecovered"]))
        death.append(int(india["dailydeceased"]))
    np_date = np.array(date) 
    np_cases = np.array(active) 
    np_death = np.array(death)
    np_recovered = np.array(recovered)
    df = pd.DataFrame({'date':np_date ,'recovered':np_recovered,'active':np_cases,'deceased':np_death })
    df
    df['date'] = pd.to_datetime(df['date'])
    firstdate=(pd.to_datetime(df['date']).dt.date.iloc[0])
    lastdate=(pd.to_datetime(df['date']).dt.date.iloc[-1])
    st.write("DEATH VS ACTIVE CASES")
    date_range = st.slider(
        "Select a date of interest:",
        value=(datetime.strptime(str(firstdate), "%Y-%m-%d"),datetime.strptime(str(lastdate), "%Y-%m-%d")))
    dates = list(date_range)
    from_date=(dates[0].strftime('%Y-%m-%d'))
    to_date=(dates[1].strftime('%Y-%m-%d'))
    mask = df['date'].between(from_date, to_date, inclusive=False)
    df=df.loc[mask]
    df = df.rename(columns={'date':'index'}).set_index('index')
    st.line_chart(df)
    statewise()


def statewise():
    State=[]
    district=[]
    StateDate =json.loads(DistrictResponse.text)
    for s in StateDate:
        if "State Unassigned" not in s:
            State.append(s)
    option = st.selectbox(
        'Select a State to view data',
        State)
    allstate = data1["statewise"]
    for states in allstate:
        data=["active","confirmed","recovered","death"]
        total=[]
        disdata=["active","confirmed","death","recovered"]
        distotal=[]
        if (states["state"]==option):
            date_str2=states["lastupdatedtime"]
            date_dt2 = datetime.strptime(date_str2, '%d/%m/%Y %H:%M:%S').date()
            state={}
            state["state"]=states["state"]
            total.append(states["active"])
            total.append(states["confirmed"])
            total.append(states["recovered"])
            total.append(states["deaths"])
            state["lastupdatedtime"]=date_dt2
            df = pd.DataFrame({'date':data ,'total':total})
            df = df.rename(columns={'date':'index'}).set_index('index')
            fig = px.pie(df, values='total', names=df.index, title="Data of"+" "+states["state"]+","+"Last updated on" +" "+str(date_dt2))
            fig.show()
            st.plotly_chart(fig)
            india = (data1["cases_time_series"][-1])
            data =json.loads(DistrictResponse.text)
            for da in data[option]["districtData"]:
                Districts=data[option]["districtData"]
                for d in Districts:
                    district.append(d)
            option1 = st.selectbox(
                'Select a District to view data',
                district)
            alldata=(data[option]["districtData"])
            for d in alldata:
                if d == option1:
                    currentdistrict=d
                    distotal.append(alldata[d]["active"])
                    distotal.append(alldata[d]["confirmed"])
                    distotal.append(alldata[d]["deceased"])
                    distotal.append(alldata[d]["recovered"])
            df = pd.DataFrame({'date':disdata ,'total':distotal})
            df = df.rename(columns={'date':'index'}).set_index('index')
            fig = px.pie(df, values='total', names=df.index, title="Data of"+" "+currentdistrict+","+"Last updated on" +" "+str(date_dt2))
            fig.show()
            st.plotly_chart(fig)
            sourcecode()

def sourcecode():
    st.title('Contribution and other projects')
    if st.button('Open Source code'):
        js = "window.open('https://github.com/aravind-tronix/Covid19_Analysis')"  
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
        st.write('Other projects')
    if st.button('Other projects'):
        js = "window.open('https://jestronics.ml/')"
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)

def totalcases():
    data = (data1["cases_time_series"])
    date=[]
    confirm_cases=[]
    for india in data:
        date_element=str((india["date"]))
        d = datetime.strptime(date_element, '%d %B %Y')
        date.append(d.strftime('%Y-%m-%d'))
        confirm_cases.append(int(india["totalconfirmed"]))
    np_date = np.array(date) 
    np_cases = np.array(confirm_cases) 
    df = pd.DataFrame({'date':np_date, 'totalconfirmed':np_cases})
    df['date'] = pd.to_datetime(df['date'])
    date_range = st.slider(
        "Select a date of interest to view:",
        value=(datetime.strptime("15-03-2020", "%d-%m-%Y"),datetime.strptime("18-04-2021", "%d-%m-%Y")))
    dates = list(date_range)
    from_date=(dates[0].strftime('%Y-%m-%d'))
    to_date=(dates[1].strftime('%Y-%m-%d'))
    mask = df['date'].between(from_date, to_date, inclusive=False)
    df=df.loc[mask]
    df = df.rename(columns={'date':'index'}).set_index('index')
    st.bar_chart(df)
    deaths_vs_totalcases()

totalactive()