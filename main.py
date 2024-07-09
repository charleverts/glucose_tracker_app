import streamlit as st
import pandas as pd
import warnings
import plotly.express as px
import plotly.graph_objects as go

warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

pd.set_option('display.max_columns', 50)

def cleaned_data(filename):
    
    glucose_df = pd.read_excel(filename, sheet_name = 'main')

    # Drop the first three rows
    glucose_df = glucose_df.iloc[4:]

    # Rename columns using a dictionary
    glucose_df.rename(columns={'Unnamed: 0': 'Date', 
                               'Unnamed: 8': 'Insulin AM', 
                               'Unnamed: 9': 'Insulin PM',
                               'Unnamed: 10': "Sleep"}, 
                                   inplace = True)

    # Drop rows where every column entry is NaN
    glucose_df = glucose_df.dropna(how='all')

    glucose_df = glucose_df[['Date', 'Weight', 'Morning (07:15)', 'Post Breakfast', 'Lunch (12:50)',
           'Post Lunch', 'Dinner (18:30)', 'BedTime (21:45)', 'Insulin AM',
           'Insulin PM', 'Sleep']]

    glucose_df = glucose_df.reset_index(drop=True)

    # Drop rows where NaN exists in the 'Date' column
    glucose_df.dropna(subset=['Date'], inplace=True)

    # Keep only the first 9 characters of the 'Date' column
    glucose_df['Date'] = glucose_df['Date'].astype(str)
    glucose_df['Date'] = glucose_df['Date'].apply(lambda x: x[:10])

    # Dictionary mapping column names to desired data types
    data_type_dict = {
        'Date': str,
        'Weight': float,
        'Morning (07:15)': float,
        'Post Breakfast': float,
        'Lunch (12:50)': float,
        'Post Lunch': float,
        'Dinner (18:30)': float,
        'BedTime (21:45)': float,
        'Insulin AM': float,
        'Insulin PM': float,
        'Sleep': int
    }

    # Convert column data types using the dictionary
    glucose_df = glucose_df.astype(data_type_dict, errors='ignore')
    
    return glucose_df

glucose_df = cleaned_data('DiabetesTracker.xlsx')

# Fig

fig_cols_1 = ['Morning (07:15)', 'Lunch (12:50)',
              'Dinner (18:30)', 'BedTime (21:45)']

# Define specific colors for each line
colors = ['#9BEC00', '#5DEBD7', '#1679AB', '#074173']

fig = px.line(glucose_df, x="Date", y=fig_cols_1, title='Glucose Readings',
              markers=True, color_discrete_sequence=colors)

fig.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to rename legend title
fig.update_layout(
    legend_title_text='Time of Day'  ,
    yaxis_title='Glucose Level'  # New y-axis title
)

# Update layout to change minimum value on y-axis
fig.update_layout(
    yaxis=dict(title='Glucose Levels', range=[0, None])  # Set minimum y-axis value to 50
)

# Update layout to move legend position on x-axis
fig.update_layout(
    legend=dict(
        x=0.9,  # Position the legend horizontally at 50% of the plot width
        y=0.95,
        xanchor='center',  # Center alignment of the legend
        yanchor='top'  # Align legend to the top of the plot
    )
)

# Add transparent green box between y=4 and y=7
fig.add_shape(
    type="rect",
    xref="paper", yref="y",
    x0=0, y0=4, x1=1, y1=7,
    fillcolor="green",
    opacity=0.2,
    layer="below",
    line=dict(
        width=0,
    )
)

# Add dashed horizontal lines at y=4 and y=7
fig.add_shape(
    type="line",
    xref="paper", yref="y",
    x0=0, y0=4, x1=1, y1=4,
    line=dict(color="green", width=1, dash="dash")
)

fig.add_shape(
    type="line",
    xref="paper", yref="y",
    x0=0, y0=7, x1=1, y1=7,
    line=dict(color="green", width=1, dash="dash")
)

# Fig1

fig_cols_1 = ['Insulin AM','Insulin PM']

# Define specific colors for each line
colors = ['#FF7ED4', '#AF47D2']

fig1 = px.line(glucose_df, x="Date", y=fig_cols_1, title='Insulin AM/PM',
              markers=True, color_discrete_sequence=colors)

fig1.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to rename legend title
fig1.update_layout(
    legend_title_text='Time of Day'  ,
    yaxis_title='Dosage'  # New y-axis title
)

# Update layout to change minimum value on y-axis
fig1.update_layout(
    yaxis=dict(title='Dosage', range=[4, 15])  # Set minimum y-axis value to 50
)

# Update layout to move legend position on x-axis
fig1.update_layout(
    legend=dict(
        x=0.1,  # Position the legend horizontally at 50% of the plot width
        y=0.4,
        xanchor='center',  # Center alignment of the legend
        yanchor='top'  # Align legend to the top of the plot
    )
)

# Fig2

# Define specific colors for each line
colors = ['#31363F']

fig2 = px.line(glucose_df, x="Date", y="Weight", title='Weight',
              markers=True, color_discrete_sequence=colors)

fig2.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to rename legend title
fig2.update_layout(
    legend_title_text='Time of Day'  ,
    yaxis_title='Weight (kg)'  # New y-axis title
)

# Update layout to move legend position on x-axis
fig2.update_layout(
    legend=dict(
        x=0.9,  # Position the legend horizontally at 50% of the plot width
        y=0.95,
        xanchor='center',  # Center alignment of the legend
        yanchor='top'  # Align legend to the top of the plot
    )
)

# Fig3

# Define specific colors for each line
colors = ['#540375']

fig3 = px.line(glucose_df, x="Date", y="Sleep", title='Sleep',
              markers=True, color_discrete_sequence=colors)

fig3.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to rename legend title
fig3.update_layout(
    yaxis_title='Sleep'  # New y-axis title
)

# Update layout to change minimum value on y-axis
fig3.update_layout(
    yaxis=dict(title='Sleep Rating', range=[0, 10])  # Set minimum y-axis value to 50
)

# Update layout to move legend position on x-axis
fig3.update_layout(
    legend=dict(
        x=0.9,  # Position the legend horizontally at 50% of the plot width
        y=0.95,
        xanchor='center',  # Center alignment of the legend
        yanchor='top'  # Align legend to the top of the plot
    )
)

### Fig 4

# Convert the DataFrame to long format for Plotly Express
glucose_df_long = glucose_df[['Morning (07:15)','Lunch (12:50)', 
                              'Dinner (18:30)', 'BedTime (21:45)']]\
                              .melt(var_name='Category', value_name='Value')

# Define specific colors for each line
colors = ['#074173']

# Create the box plot
fig4 = px.box(glucose_df_long, x='Category', y='Value', 
             title='Box Plot of All Glucose Readings', points="all",
             color_discrete_sequence=colors)

fig4.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to change minimum value on y-axis
fig4.update_layout(
    yaxis=dict(title='Glucose Levels')  # Set minimum y-axis value to 50
)

### Fig 5

# Calculate mean for each category
means = glucose_df_long.groupby('Category')['Value'].mean().reset_index()

# Create the strip plot
fig5 = px.strip(glucose_df_long, x='Category', y='Value',
               title='All Glucose Readings')

# Add mean points as red dots
fig5.add_trace(go.Scatter(
    x=means['Category'],
    y=means['Value'],
    mode='markers',
    marker=dict(color='red', size=5),
    name='Mean'
))

# Add line connecting mean points
fig5.add_trace(go.Scatter(
    x=means['Category'],
    y=means['Value'],
    mode='lines+markers',
    marker=dict(color='red'),
    line=dict(color='grey', dash='dash'),
    name='Mean Line'
))

fig5.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to change minimum value on y-axis
fig5.update_layout(
    yaxis=dict(title='Glucose Levels')  # Set minimum y-axis value to 50
)

# Update layout to move legend position on x-axis
fig5.update_layout(
    legend=dict(
        x=0.15,  # Position the legend horizontally at 50% of the plot width
        y=0.95,
        xanchor='center',  # Center alignment of the legend
        yanchor='top'  # Align legend to the top of the plot
    )
)

### Fig6

# Create the box plot
fig6 = px.box(glucose_df_long, x='Category', y='Value', 
             title='Box Plot of 7-day Glucose Readings', points="all",
             color_discrete_sequence=colors)

fig6.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to change minimum value on y-axis
fig6.update_layout(
    yaxis=dict(title='Glucose Levels')  # Set minimum y-axis value to 50
)

### Fig7

# Calculate mean for each category
means = glucose_df_long.groupby('Category')['Value'].mean().reset_index()

# Create the strip plot
fig7 = px.strip(glucose_df_long, x='Category', y='Value',
               title='7-day Glucose Readings')

# Add mean points as red dots
fig7.add_trace(go.Scatter(
    x=means['Category'],
    y=means['Value'],
    mode='markers',
    marker=dict(color='red', size=5),
    name='Mean'
))

# Add line connecting mean points
fig7.add_trace(go.Scatter(
    x=means['Category'],
    y=means['Value'],
    mode='lines+markers',
    marker=dict(color='red'),
    line=dict(color='grey', dash='dash'),
    name='Mean Line'
))

fig7.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to change minimum value on y-axis
fig7.update_layout(
    yaxis=dict(title='Glucose Levels')  # Set minimum y-axis value to 50
)

# Update layout to move legend position on x-axis
fig7.update_layout(
    legend=dict(
        x=0.15,  # Position the legend horizontally at 50% of the plot width
        y=0.95,
        xanchor='center',  # Center alignment of the legend
        yanchor='top'  # Align legend to the top of the plot
    )
)

### Set layout

st.set_page_config(page_title = 'Glucose Tracker',  layout = 'wide', 
                   page_icon = ':🩸:')

col1, col2, col3, col4, col5 = st.columns(5)

# with col1:
#     st.image("images/Barkeep-Big.png")
# 
# with col2:
#     st.write('  ')
# 
# with col3:
#     st.write('  ')
# 
# with col4:
#     st.write('  ')
# 
# with col5:
#     st.image("images/HB.png")

with st.sidebar:
    text_0 = st.write("💻 This page displays the metrics relating to Barkeep's usage and data.")
    text_1 = st.write("📊 The graphs are interactive: hover for info, click and drag to zoom, click on legend to add or remove components.")
    # st.metric(label="🍷Barkeep Interactions Today", value = f"{todays_interactions}", delta = f"{difference} vs daily average")
    # st.metric(label="🕵️‍♂️Stock Search Interactions Today", value = f"{SS_today}", delta = f"{SS_difference} vs daily average")
    # st.metric(label="TOTAL Interactions Today", value = f"{todays_interactions+SS_today}")


# Charts

st.plotly_chart(fig)

st.plotly_chart(fig1)

st.plotly_chart(fig2)

st.plotly_chart(fig3)

st.plotly_chart(fig4)

st.plotly_chart(fig5)

st.plotly_chart(fig6)

st.plotly_chart(fig7)

#
#col1, col2 = st.columns(2)
#
#with col1:
#    st.subheader('Session Metrics')
#
#    st.write("Sessions started:", consultants['Sessions'].sum())
#    st.write("Unique interactions:", consultants['Total'].sum())
#
#    st.write("-- Recommendations:", consultants['Search'].sum())
#    st.write("-- SKUs Copied:", consultants['Copy'].sum())
#    st.write("-- Stock Searches:", consultants['Stock Search'].sum())
#    st.write("-- Auto Populate:", consultants['Populate'].sum())
#
#with col2:
#    st.subheader('Averages')
#
#    st.write("Recommendations per session:", round(float(consultants['Search'].sum()/consultants['Sessions'].sum()), 2))
#    st.write("Copies per session:", round(float(consultants['Copy'].sum()/consultants['Sessions'].sum()), 2))
#    st.write("Stock Searches per session:", round(float(consultants['Stock Search'].sum()/consultants['Sessions'].sum()), 2))
#
## Tables
#
#st.subheader('Barkeep Data')
#st.markdown('The following tabs contain data relating to Consultant Interactions, Popular Products, Popular Customers.') 
#
#def convert_df(df):
#    return df.to_csv()
#
#consultants_csv = convert_df(consultants)
## popular_items_csv = convert_df(popular_items)
## max_customers_csv = convert_df(max_customers)
#
#now = datetime.now()
#dt_string = now.strftime("%d_%m_%Y")
#
#tab1, tab2, tab3 = st.tabs(["👩🏽‍💻 Consultants", "🍾 Products", "🥂 Customers"])
#
#with tab1:
#    st.subheader('Consultant Interactions')
#
#    st.download_button(
#        label = "Download as CSV",
#        data = consultants_csv,
#        file_name = str("consultants_" + dt_string + '.csv'),
#        mime = 'text/csv')
#
#    st.dataframe(consultants)
#
#with tab2:
#    st.subheader('Popular Products')
#
#    #st.download_button(
    #    label = "Download as CSV",
    #    data = popular_items_csv,
    #    file_name = str("popular_items_" + dt_string + '.csv'),
    #    mime = 'text/csv')
#
    #st.dataframe(popular_items)

#with tab3:
#    st.subheader('Popular Customers')
#
#    #st.download_button(
#    #    label = "Download as CSV",
#    #    data = max_customers_csv,
#    #    file_name = str("popular_customers_" + dt_string + '.csv'),
#    #    mime = 'text/csv')
##
#    #st.dataframe(max_customers)
#
## Retrieve user feedback to display below data tables
#
#st.subheader('📝 Consultant Feedback')
#
#with st.expander("Expand for Data"):
#
#    feedback = read_items(FEEDBACK_CONTAINER)
#    feedback_df = feedback_item_list_to_df(feedback)
#
#    feedback_df['datetime'] = pd.to_datetime(feedback_df['_ts'] , unit = 's')
#    feedback_df = feedback_df[['user_email', 'datetime', 'feedback_type', 'feedback']]
#    feedback_df = feedback_df.sort_values(by = 'datetime', ascending = False).reset_index(drop = True)
#    
#    st.dataframe(feedback_df)
#
#print('feedback_df loaded')