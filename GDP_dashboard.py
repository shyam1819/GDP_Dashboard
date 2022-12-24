import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
#import seaborn as sns
import matplotlib.pyplot as plt

from numerize import numerize

st.set_page_config(page_title="World GDP Dashboard",page_icon=":globe_with_meridians:",layout="wide")

@st.cache # For short time memory to avoid data read during rerun
def get_data():
    df=pd.read_csv("World_gdp.csv")
    #df.columns=cols
    #df=df.drop(["Indicator Code","Indicator Name"],axis=1)
    return df

df=get_data()

# --- Dashbaord title ---
st.title(":bar_chart: World GDP Dashboard")
st.markdown("##")

st.markdown("---")

# --- Filter ---
def sum_gdp(df,center):
    total_gdp=df[center].sum()
    h=df.nlargest(3,[center])
    return total_gdp,h


center=st.selectbox("Select year:",("2019","2020","2021"))

if center=="2019":
    total_gdp,h=sum_gdp(df,center)
    h1=h.iloc[0]
    h2=h.iloc[1]
    h3=h.iloc[2]
elif center=="2020":
    total_gdp,h=sum_gdp(df,center)
    h1=h.iloc[0]
    h2=h.iloc[1]
    h3=h.iloc[2]
elif center=="2021":
    total_gdp,h=sum_gdp(df,center)
    h1=h.iloc[0]
    h2=h.iloc[1]
    h3=h.iloc[2]

l_column, r_column=st.columns([1,3])
with l_column:
    st.subheader("")
with r_column:
    st.subheader("Top three nations in the world: ")

L1_column,L2_column,R2_column,R1_column= st.columns(4)

with L1_column:
    st.subheader("Net GDP in {}".format(center))
    st.subheader(f"US $ {numerize.numerize(total_gdp)}")

with L2_column:
    st.header("1. {}".format(h1["Country Name"]))
    st.subheader(f"US $ {numerize.numerize(h1[center],2)}")

with R2_column:
    st.header("2. {}".format(h2["Country Name"]))
    st.subheader(f"US $ {numerize.numerize(h2[center],2)}")

with R1_column:
    st.header("3. {}".format(h3["Country Name"]))
    st.subheader(f"US $ {numerize.numerize(h3[center],2)}")    
st.markdown("---")

L_column, M_column,R_column=st.columns([2,4,3])

with L_column:
    st.subheader("GDP of top ten nations in {}".format(center))
    t10=df.nlargest(10,[center])
    t10.style.hide_index()
    st.write(t10[["Country Name",center]])
with M_column:
    st.subheader("Continent wise contribution to net GDP")
    C=df.groupby(["Continent"])[center].sum().reset_index(name="Total")
    fig=px.pie(C,names="Continent",values="Total")
    #plt.figure(figsize=(4,4))
    st.plotly_chart(fig)
with R_column:
    st.subheader("Top 3 nations in every continent")
    G=df.groupby(["Continent"])[center].nlargest(3).reset_index(name="Values")
    g=pd.DataFrame()
    g=g.append([df.loc[i] for i in G["level_1"].unique()])
    continent=st.multiselect("Select Continents",options=g["Continent"].unique(),default=["Asia","Europe","North America"])
    #g=g[g["Continent"] not in ["Africa","Oceania"]]
    g_selection=g.query("Continent==@continent")
    fig=px.bar(g_selection,x="Continent",y=center,color="Country Name",barmode="group")
    fig.update_traces(width=0.25)
    st.plotly_chart(fig)

st.markdown("---")

st.subheader("GDP value of nations from the year 1960-2021")
code=st.multiselect("Select countries codes:",options=["IND","CHN","JPN","USA","FRA","CAN","GBR"],default=["IND"])
df_selection=df.query("Code==@code")
df_selection=df_selection.T
df_selection=df_selection.drop(["Unnamed: 0","Country Name","Country","Continent"])
df_selection.columns=df_selection.iloc[0]
df_selection=df_selection.drop(["Code"])
#df_selection=df_selection.rename(columns={"Code":"Year"})
#st.write(df_selection)
y=df_selection["IND"].to_numpy()
fig=px.line(df_selection,x=df_selection.index,y=code)
#plt.xlabel("Year")
#plt.ylabel("GDP Value")
st.plotly_chart(fig,use_container_width=True)
        

    
# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 2rem;
                    padding-bottom: 10rem;
                    padding-left: 2rem;
                    padding-right: 2rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
