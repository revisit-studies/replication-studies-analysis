import json
import glob
import pandas as pd

# get the list of files in the folder
files = glob.glob("firebase-dump/participants/*")
print(files)

# create a dictionary to store the event count
event_count = {}

# iterate over the files
for file in files:
    # open the file
    with open(file, "r") as f:
        # read the json data
        data = json.load(f)
        # get the participant id
        participant_id = data["participantId"]
        # initialize the count
        windowEventCount = 0
        provenanceNodeCount = 0
        # Iterate over answers dictionary and count the number of events from
        # windowEvents and provenanceNodes
        print(data["participantId"])
        for key, answer in data["answers"].items():
            windowEventCount += len(answer["windowEvents"])
            if "stimulus" in answer["provenanceGraph"]:
                provenanceNodeCount += len(
                    answer["provenanceGraph"]["stimulus"]["nodes"].keys()
                )
        # store the count in the dictionary
        event_count[participant_id] = {
            "windowEvents": windowEventCount,
            "provenanceNodes": provenanceNodeCount,
        }

# print the event count
print(event_count)

# write the event count to a file
with open("event-count.json", "w") as f:
    json.dump(event_count, f)

# Write the event count to a csv file
df = pd.DataFrame(event_count).T
# rename first column to participantId
df.index.name = "participantId"
df.to_csv("event-count.csv")
