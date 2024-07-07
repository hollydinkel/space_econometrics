import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

# Example event data
events = [
    {'date': '2024-01-01', 'event': 'New Year'},
    {'date': '2024-02-14', 'event': 'Valentine\'s Day'},
    {'date': '2024-04-01', 'event': 'April Fool\'s Day'},
    {'date': '2024-07-04', 'event': 'Independence Day'},
    {'date': '2024-10-31', 'event': 'Halloween'},
    {'date': '2024-12-25', 'event': 'Christmas'}
]

# Convert to DataFrame and parse dates
df = pd.DataFrame(events)
df['date'] = pd.to_datetime(df['date'])

# Plot the timeline
fig, ax = plt.subplots(figsize=(10, 3))

# Plot the events
ax.plot(df['date'], [1] * len(df), "|", ms=50, color='gray')

# Annotate the events
for idx, row in df.iterrows():
    ax.text(row['date'], 1.1, row['event'], rotation=45, ha='right')

# Format the x-axis
ax.get_yaxis().set_visible(False)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

# Add grid and title
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
# plt.title('Timeline of Events in 2024')

# Adjust layout
plt.tight_layout()
fig.savefig(f"./images/test.png")
