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
    
    glucose_df['7_day Average'] = round(glucose_df['Weight'].rolling(window=7).mean(), 1)
    
    return glucose_df

glucose_df = cleaned_data('DiabetesTracker.xlsx')

mean_all_time = round(glucose_df[['Morning (07:15)', 'Lunch (12:50)', 'Dinner (18:30)', 'BedTime (21:45)']].mean().mean(), 1)
mean_last_30 = round(glucose_df.tail(30)[['Morning (07:15)', 'Lunch (12:50)', 'Dinner (18:30)', 'BedTime (21:45)']].mean().mean(), 1)
mean_last_7 = round(glucose_df.tail(7)[['Morning (07:15)', 'Lunch (12:50)', 'Dinner (18:30)', 'BedTime (21:45)']].mean().mean(), 1)

diff_all = round(mean_last_30 - mean_all_time, 1)
diff_30 = round(mean_last_7 - mean_last_30, 1)

# Convert the DataFrame to long format for Plotly Express
glucose_df_long = glucose_df[['Morning (07:15)','Lunch (12:50)', 
                              'Dinner (18:30)', 'BedTime (21:45)']]\
                              .melt(var_name='Category', value_name='Value')
                              
def value_to_rank(value):
    if value < 3:
        return 'very low'
    elif 3 <= value < 4:
        return 'low'
    elif 4 <= value < 7:
        return 'good'
    elif 7 <= value < 10:
        return 'elevated'
    elif 10 <= value < 15:
        return 'high'
    elif value >= 15:
        return 'extremely high'
    
glucose_df_long['Rank'] = glucose_df_long['Value'].apply(value_to_rank)

glucose_df_long = glucose_df_long.dropna()

num_readings = glucose_df.shape[0]*4
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
        x=0.8,  # Position the legend horizontally at 50% of the plot width
        y=0.9,
        xanchor='center',  # Center alignment of the legend
        yanchor='top'  # Align legend to the top of the plot
    )
)

# Fig2

# Define specific colors for each line
# Define specific colors for each line
colors = ['#758694']

fig2 = px.line(glucose_df, x="Date", y=["Weight"], title='Weight',
              markers=True, color_discrete_sequence=colors)

# Add the 7_day Weight line as a dotted line
fig2.add_scatter(x=glucose_df["Date"], y=glucose_df["7_day Average"],
                 mode='lines', name='7_day Average', line=dict(dash='dot', color='#758694'))

fig2.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to rename legend title
fig2.update_layout(
    yaxis_title='Weight (kg)'  # New y-axis title
)

# Update layout to move legend position on x-axis
fig2.update_layout(
    legend=dict(
        x=0.8,  # Position the legend horizontally at 50% of the plot width
        y=0.6,
        xanchor='center',  # Center alignment of the legend
        yanchor='top'  # Align legend to the top of the plot
    )
)

# Fig3

# Define specific colors for each line
colors = ['#FFC7ED']

# fig3 = px.line(glucose_df, x="Date", y="Sleep", title='Sleep',
#               markers=True, color_discrete_sequence=colors)
# 
# fig3.update_layout(
#     title = {'y':0.85,
#              'x':0.5,
#              'xanchor': 'center',
#              'yanchor': 'top'})
# 
# # Update layout to rename legend title
# fig3.update_layout(
#     yaxis_title='Sleep'  # New y-axis title
# )
# 
# # Update layout to change minimum value on y-axis
# fig3.update_layout(
#     yaxis=dict(title='Sleep Rating', range=[0, 10])  # Set minimum y-axis value to 50
# )
# 
# # Update layout to move legend position on x-axis
# fig3.update_layout(
#     legend=dict(
#         x=0.9,  # Position the legend horizontally at 50% of the plot width
#         y=0.95,
#         xanchor='center',  # Center alignment of the legend
#         yanchor='top'  # Align legend to the top of the plot
#     )
# )

### Fig 4

# Convert the DataFrame to long format for Plotly Express
glucose_df_long = glucose_df[['Morning (07:15)','Lunch (12:50)', 
                              'Dinner (18:30)', 'BedTime (21:45)']]\
                              .melt(var_name='Category', value_name='Value')

# Define specific colors for each line
colors = ['#074173']

# Create the box plot
fig4 = px.box(glucose_df_long, x='Category', y='Value', 
             title='All Glucose Readings', points="all",
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

### Fig8

glucose_df_last_week = glucose_df.tail(7)
glucose_df_last_week = glucose_df_last_week.reset_index(drop=True)

# Convert the DataFrame to long format for Plotly Express
glucose_df_last_week_long = glucose_df_last_week[['Morning (07:15)','Lunch (12:50)', 
                              'Dinner (18:30)', 'BedTime (21:45)']]\
                              .melt(var_name='Category', value_name='Value')

# Define specific colors for each line
colors = ['#074173']

# Create the box plot
fig8 = px.box(glucose_df_last_week_long, x='Category', y='Value', 
             title='Last 7 days Glucose Readings', points="all",
             color_discrete_sequence=colors)

fig8.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to change minimum value on y-axis
fig8.update_layout(
    yaxis=dict(title='Glucose Levels')  # Set minimum y-axis value to 50
)

### Fig9

# Calculate mean for each category
means = glucose_df_last_week_long.groupby('Category')['Value'].mean().reset_index()

# Create the strip plot
fig9 = px.strip(glucose_df_last_week_long, x='Category', y='Value',
               title='Last 7 days Glucose Readings')

# Add mean points as red dots
fig9.add_trace(go.Scatter(
    x=means['Category'],
    y=means['Value'],
    mode='markers',
    marker=dict(color='red', size=5),
    name='Mean'
))

# Add line connecting mean points
fig9.add_trace(go.Scatter(
    x=means['Category'],
    y=means['Value'],
    mode='lines+markers',
    marker=dict(color='red'),
    line=dict(color='grey', dash='dash'),
    name='Mean Line'
))

fig9.update_layout(
    title = {'y':0.85,
             'x':0.5,
             'xanchor': 'center',
             'yanchor': 'top'})

# Update layout to change minimum value on y-axis
fig9.update_layout(
    yaxis=dict(title='Glucose Levels')  # Set minimum y-axis value to 50
)

# Update layout to move legend position on x-axis
fig9.update_layout(
    legend=dict(
        x=0.15,  # Position the legend horizontally at 50% of the plot width
        y=0.95,
        xanchor='center',  # Center alignment of the legend
        yanchor='top'  # Align legend to the top of the plot
    )
)

# Add transparent green box between y=4 and y=7
fig9.add_shape(
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
fig9.add_shape(
    type="line",
    xref="paper", yref="y",
    x0=0, y0=4, x1=1, y1=4,
    line=dict(color="green", width=1, dash="dash")
)

fig9.add_shape(
    type="line",
    xref="paper", yref="y",
    x0=0, y0=7, x1=1, y1=7,
    line=dict(color="green", width=1, dash="dash")
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
    text_0 = st.write("💻 This page displays the metrics relating to my Blood Glucose levels.")
    text_1 = st.write("📊 The graphs are interactive: hover for info, click and drag to zoom, click on legend to add or remove components.")

    st.image('images/cpe1.png')
    
    st.metric(label="Average of All Readings", value = f"{mean_all_time} mmol/L", delta_color="inverse")
   
    st.metric(label="Average of last 30 days Readings", value = f"{mean_last_30} mmol/L", delta = f"{diff_all} vs All Time", delta_color="inverse")

    st.metric(label="Average of last 7 days Readings", value = f"{mean_last_7} mmol/L", delta = f"{diff_30} vs last 30 days", delta_color="inverse")
    
# Charts

# Set y-axis range for both figures
fig.update_yaxes(range=[0, 20])

# Layout the Streamlit app with two columns
# Create columns with specified proportions
col1, col2, col3 = st.columns([4, 1, 2])

with col1:
    st.success(f'{num_readings} Blood Glucose readings have been recorded since 19 June 2024.', icon="🎯")

with col3:
    st.markdown("**Select the pie chart's time horizon:**")
    time_horizon = st.radio("",
                           ["All Readings", "Last 30 days", "Last 7 days"],
                           label_visibility="collapsed")

### Fig10

# Perform actions based on selection
if time_horizon == "All Readings":
    time_horizon_value = glucose_df.shape[0]
    # Add any specific calculation or action for comedy here
elif time_horizon == "Last 30 days":
    time_horizon_value = 30
    # Add any specific calculation or action for drama here
else: #"Last 7 days"
    time_horizon_value = 7

glucose_df_long = glucose_df.tail(time_horizon_value)[['Morning (07:15)','Lunch (12:50)', 
                              'Dinner (18:30)', 'BedTime (21:45)']]\
                              .melt(var_name='Category', value_name='Value')
                              
def value_to_rank(value):
    if value < 3:
        return 'very low'
    elif 3 <= value < 4:
        return 'low'
    elif 4 <= value < 7:
        return 'good'
    elif 7 <= value < 10:
        return 'elevated'
    elif 10 <= value < 15:
        return 'high'
    elif value >= 15:
        return 'extremely high'
    
glucose_df_long['Rank'] = glucose_df_long['Value'].apply(value_to_rank)

glucose_df_long = glucose_df_long.dropna()

pie_df = pd.DataFrame(glucose_df_long['Rank'].value_counts()).reset_index()

# Rename columns using a dictionary
pie_df.rename(columns={'index': 'Reading_Type',
                       'Rank': 'Count'}, 
                       inplace = True)

# Define the desired order
Reading_Type_order = ['low', 'good', 'elevated', 'high', 'extremely high']

# Convert the 'Category' column to a categorical type with the specified order
pie_df['Reading_Type'] = pd.Categorical(pie_df['Reading_Type'], categories=Reading_Type_order, ordered=True)

# Sort the DataFrame by the 'Category' column
pie_df = pie_df.sort_values('Reading_Type')

### Fig10
labels = pie_df['Reading_Type']
values = pie_df['Count']

# Define specific colors for each category
color_map = {
    'low': '#ffffa1',
    'good': '#3CCF4E',
    'elevated': '#FF8E00',
    'high': '#E4003A',
    'extremely high': '#6C0345'
}

fig10 = px.pie(pie_df, values=values, names=labels,color='Reading_Type',
               color_discrete_map=color_map,
               category_orders={'Reading_Type': Reading_Type_order})

fig10.update_layout(
    title={
        'text': 'Counts by Category',
        'x': 0.5,  # Horizontal position of the title (0: left, 0.5: center, 1: right)
        'xanchor': 'center'  # Anchor point of the title text
    },
    legend=dict(
        x=0.7,  # Position it horizontally (0: left, 1: right)
        y=0.95,  # Position it vertically (0: bottom, 1: top)
        xanchor='left',  # Use 'left', 'center', or 'right' for horizontal alignment
        yanchor='middle',  # Use 'top', 'middle', or 'bottom' for vertical alignment
        bordercolor='Black',  # Border color
        borderwidth=1  # Border width
    )
)

col1, col2 = st.columns([3, 2])
with col1:
    st.plotly_chart(fig, use_container_width=True) 

with col2:
    st.plotly_chart(fig10, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

# Set y-axis range for both figures
fig4.update_yaxes(range=[0, 20])
fig8.update_yaxes(range=[0, 20])

# Layout the Streamlit app with two columns
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.plotly_chart(fig8, use_container_width=True)

# Set y-axis range for both figures
fig5.update_yaxes(range=[0, 20])
fig9.update_yaxes(range=[0, 20])

# Layout the Streamlit app with two columns
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.plotly_chart(fig9, use_container_width=True)
    