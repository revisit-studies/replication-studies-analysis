import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('aggregated_results-final.csv')

# Filter out rows without participantId and exclude specific participant
df_filtered = df[df['participantId'].notna() & 
                 (df['participantId'] != '944e5429-c0c5-4f1e-9483-90dd98f63b88')]

# Create the figure
plt.figure(figsize=(10, 8))

# Plot geometric patterns (blue)
plt.scatter(df_filtered['geo-event-count'], df_filtered['geo-BeauVis'], 
           color='blue', alpha=0.6, label='Geometric Pattern')

# Plot iconic patterns (red)
plt.scatter(df_filtered['icon-event-count'], df_filtered['icon-BeauVis'], 
           color='red', alpha=0.6, label='Iconic Pattern')

# Draw lines connecting each participant's scores
for _, row in df_filtered.iterrows():
    plt.plot([row['geo-event-count'], row['icon-event-count']], 
            [row['geo-BeauVis'], row['icon-BeauVis']], 
            color='gray', alpha=0.3, linestyle='--')

# Customize the plot
plt.xlabel('Event Count')
plt.ylabel('BeauVis Score')
plt.title('Relationship between BeauVis Score and Event Count\nGeometric vs Iconic Patterns')
plt.ylim(0, 7.5)
plt.yticks(range(0, 8))
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Adjust layout
plt.tight_layout()

# Save the plots in both PDF and SVG formats
plt.savefig('combined-pattern-beauvis-events.pdf')
plt.savefig('combined-pattern-beauvis-events.svg')
plt.close() 