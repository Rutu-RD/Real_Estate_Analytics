import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import ast
from wordcloud import WordCloud
import pickle
import mplcursors

def data_files():
    df = pd.read_csv('gurgaon_properties_missing_value_imputation.csv')
    latlong = pd.read_csv('latlong.csv')
    latlong['latitude'] = latlong['coordinates'].str.split(',').str.get(0).str.split('°').str.get(0).astype('float')
    latlong['longitude'] = latlong['coordinates'].str.split(',').str.get(1).str.split('°').str.get(0).astype('float')
    new_df = df.merge(latlong, on='sector')
    return new_df

def display_graph():
    new_df=data_files()
    group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'Built_up_area', 'latitude', 'longitude']].mean()
    #group_df['price_per_sqft']=group_df['price_per_sqft']/1000

    fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft",size=group_df['price_per_sqft'],size_max=35,
                            color_continuous_scale=px.colors.cyclical.IceFire, zoom=11,
                            mapbox_style="open-street-map", text=group_df.index,width=1200,height=800)
    st.plotly_chart(fig)


def graph_setor():
    new_df=data_files()
    group_df = new_df.groupby('sector')[
        ['price', 'price_per_sqft', 'Built_up_area', 'latitude', 'longitude']].mean().sort_values(by='price_per_sqft',
                                                                                                  ascending=False)

    n=group_df.head(10)
    figure=plt.figure()
    figs,ax=plt.subplots(figsize=(90,50))

    figs=px.bar(n,x=n.index,y=n['price_per_sqft'],title='Sector Vs price/sqft')
    st.plotly_chart(figs)
def graph_builtuparea():
    # Set font size for tick labels on both axes
    new_df = data_files()
    group_df = new_df.groupby('sector')[
        ['price', 'price_per_sqft', 'Built_up_area', 'latitude', 'longitude']].mean().sort_values(by='price_per_sqft',
                                                                                                  ascending=False)

    n = group_df
    figure = plt.figure(figsize=(90,50))
    fig = px.scatter(n, x=n.index, y='Built_up_area', size=n['price_per_sqft'],color='price_per_sqft',
                     labels={'Built_up_area': 'Built-up Area'},
                     title='Sector vs Area and Price',
                     hover_data={'price_per_sqft': ':.2f'},color_continuous_scale='viridis',width=900,height=800)
    st.plotly_chart(fig)

def display_sunbursts():
    import plotly.express as px
    import pandas as pd

    new_df = data_files()
    n = new_df[['property_type', 'bedRoom', 'price_per_sqft','agePossession']]
    n['bedRoom'] = n['bedRoom'].astype('object')


    # Set multi-index using 'property_type' and 'bedroom'
    df_multiindex = n.set_index(['property_type', 'bedRoom'])

    # Reset the index to convert multi-index to columns
    df_multiindex = df_multiindex.reset_index()

    # Create a Sunburst chart using Plotly Express
    fig = px.sunburst(
        df_multiindex,
        path=['property_type','bedRoom'],
        values='price_per_sqft',
        title="Sunburst Chart: Property Type and Bedroom",
        color='price_per_sqft',
        color_continuous_scale='viridis',
        hover_data=['price_per_sqft'],
        labels={'price_per_sqft': 'Price per sqft'},
        width=600,
        height=600
    )

    # Display the Sunburst chart
    st.plotly_chart(fig)

def area_vs_price():
    df=data_files()
    fig = px.scatter(df, x="Built_up_area", y="price", color="bedRoom",color_continuous_scale='viridis', title="Area Vs Price")
    # Show the plot
    st.plotly_chart(fig)

def display_wordcloud():
    df1 = pd.read_csv('gurgaon_properties.csv')
    df = pd.read_csv('gurgaon_properties_missing_value_imputation.csv')
    wordcloud_df = df1.merge(df, left_index=True, right_index=True)[['features', 'sector']]

    main = []
    for item in wordcloud_df['features'].dropna().apply(ast.literal_eval):
        main.extend(item)
    feature_text = ' '.join(main)
    pickle.dump(feature_text, open('feature_text.pkl', 'wb'))
    plt.rcParams["font.family"] = "Arial"

    wordcloud = WordCloud(width=2000, height=800,
                          background_color='white',
                          stopwords=set(['s']),  # Any stopwords you'd like to exclude
                          min_font_size=10).generate(feature_text)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.image(wordcloud.to_image())  # st.pyplot()


st.set_page_config(page_title="Insights")
st.title('Analytics Module  ')
# button=st.button("click me")
tab1, tab2, tab3 = st.tabs(["Sector Graph", "other graph","Flat Vs House"])
with tab1:
    #col1,col2=st.columns(2)
    #with col1:
    st.subheader("Top 10  Sectors price_per_sqft")
    st.write(graph_setor())
    st.subheader("Built up area")
    st.write(graph_builtuparea())
    #with col2 :
    st.subheader("area Vs Price")
    st.write(area_vs_price())
    st.subheader("wordcloud of facilities")
    st.write(display_wordcloud())
with tab2:
        st.subheader("sector wise distribution ")
        st.write(display_graph())
        with st.expander("See Explaination"):
            st.write("this graph shows the sectors ")

with tab3:
        st.subheader("Flat Vs House comparison  with bedroom showing distribution with price per sq ft ")
        st.write(display_sunbursts())

        # Create a Sunburst chart using Plotly Express
