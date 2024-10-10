import json
import matplotlib.pyplot as plt

# Load the JSON data
with open("repo_analysis_20241009_225856.json") as f:
    data = json.load(f)

# Extract file type distribution from the summary
file_types = data["summary"]["file_types"]

# Generate a pie chart of file types
labels = list(file_types.keys())
sizes = list(file_types.values())

plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("File Type Distribution")
plt.show()
