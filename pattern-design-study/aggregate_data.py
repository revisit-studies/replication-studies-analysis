import pandas as pd
import json

# Read the CSV file
df = pd.read_csv('pattern-design-study_all_tidy.csv')

# Initialize an empty list to store the aggregated data
aggregated_data = []

# Group by participantId
for participant_id in df['participantId'].unique():
    participant_data = df[df['participantId'] == participant_id]
    
    # Get the values for each column
    goals = participant_data[participant_data['responseId'] == 'design-strategies-goals']['answer'].iloc[0] if not participant_data[participant_data['responseId'] == 'design-strategies-goals']['answer'].empty else None
    iconic = participant_data[participant_data['responseId'] == 'design-strategies-iconic-textures']['answer'].iloc[0] if not participant_data[participant_data['responseId'] == 'design-strategies-iconic-textures']['answer'].empty else None
    geometric = participant_data[participant_data['responseId'] == 'design-strategies-geometric-textures']['answer'].iloc[0] if not participant_data[participant_data['responseId'] == 'design-strategies-geometric-textures']['answer'].empty else None
    compare = participant_data[participant_data['responseId'] == 'compare-texture']['answer'].iloc[0] if not participant_data[participant_data['responseId'] == 'compare-texture']['answer'].empty else None
    diff_geo = participant_data[participant_data['responseId'] == 'different-chart-geo']['answer'].iloc[0] if not participant_data[participant_data['responseId'] == 'different-chart-geo']['answer'].empty else None
    diff_icon = participant_data[participant_data['responseId'] == 'different-chart-icon']['answer'].iloc[0] if not participant_data[participant_data['responseId'] == 'different-chart-icon']['answer'].empty else None
    
    # Get demographic data
    gender = participant_data[participant_data['responseId'] == 'gender']['answer'].iloc[0] if not participant_data[participant_data['responseId'] == 'gender']['answer'].empty else None
    gender_other = participant_data[participant_data['responseId'] == 'gender-other']['answer'].iloc[0] if not participant_data[participant_data['responseId'] == 'gender-other']['answer'].empty else None
    age = participant_data[participant_data['responseId'] == 'age']['answer'].iloc[0] if not participant_data[participant_data['responseId'] == 'age']['answer'].empty else None
    experience = participant_data[participant_data['responseId'] == 'experience']['answer'].iloc[0] if not participant_data[participant_data['responseId'] == 'experience']['answer'].empty else None
    
    # Get condition from the parameters column in the design-strategies-goals row
    condition_row = participant_data[participant_data['responseId'] == 'design-strategies-goals']
    condition = None
    if not condition_row.empty:
        try:
            parameters = json.loads(condition_row['parameters'].iloc[0])
            condition = parameters
        except:
            condition = None
    
    # Add to aggregated data
    aggregated_data.append({
        'participantId': participant_id,
        'gender': gender,
        'gender-other': gender_other,
        'age': age,
        'experience': experience,
        'design-strategies-goals': goals,
        'design-strategies-iconic-textures': iconic,
        'design-strategies-geometric-textures': geometric,
        'compare-texture': compare,
        'different-chart-geo': diff_geo,
        'different-chart-icon': diff_icon,
        'condition': str(condition)
    })

# Create final dataframe
result_df = pd.DataFrame(aggregated_data)

# Save to CSV
result_df.to_csv('aggregated_results.csv', index=False)

print("Data has been aggregated and saved to 'aggregated_results.csv'") 