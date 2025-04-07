import pandas as pd

# Read the CSV files
event_df = pd.read_csv('event-count.csv')
results_df = pd.read_csv('aggregated_results-coded.csv')

# Function to extract condition values
def get_condition_values(condition_str):
    try:
        # Convert string representation of dictionary to actual dictionary
        condition_dict = eval(condition_str)
        return condition_dict.get('condition_chart', None), condition_dict.get('condition_texture', None)
    except:
        return None, None

# Add condition values as separate columns
results_df[['condition_chart', 'condition_texture']] = results_df['condition'].apply(
    lambda x: pd.Series(get_condition_values(x))
)

# Function to get event counts based on condition
def get_event_counts(row, event_data):
    participant_events = event_data[event_data['participantId'] == row['participantId']]
    
    if participant_events.empty:
        return 0, 0
        
    chart_condition = row['condition_chart']
    
    if chart_condition == 0:  # bar chart
        geo_count = participant_events['bar-geo_geo-icon'].iloc[0]
        icon_count = participant_events['bar-icon_geo-icon'].iloc[0]
    elif chart_condition == 1:  # pie chart
        geo_count = participant_events['pie-geo_geo-icon'].iloc[0]
        icon_count = participant_events['pie-icon_geo-icon'].iloc[0]
    elif chart_condition == 2:  # map chart
        geo_count = participant_events['map-geo_geo-icon'].iloc[0]
        icon_count = participant_events['map-icon_geo-icon'].iloc[0]
    else:
        return 0, 0
        
    return geo_count, icon_count

# Apply the function to each row
results_df[['geo-event-count', 'icon-event-count']] = results_df.apply(
    lambda row: pd.Series(get_event_counts(row, event_df)), 
    axis=1
)

# Save the updated results
results_df.to_csv('aggregated_results-coded-updated.csv', index=False) 