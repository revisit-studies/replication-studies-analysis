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
        totalProvenanceNodeCount = 0
        barGeoGeoIcon = 0
        barIconGeoIcon = 0
        pieGeoGeoIcon = 0
        pieIconGeoIcon = 0
        mapGeoGeoIcon = 0
        mapIconGeoIcon = 0
        first = ""
        second = ""
        # Iterate over answers dictionary and count the number of events from
        # windowEvents and provenanceNodes
        print(data["participantId"])
        for key, answer in data["answers"].items():
            windowEventCount += len(answer["windowEvents"])
            if "stimulus" in answer["provenanceGraph"]:
                totalProvenanceNodeCount += len(
                    answer["provenanceGraph"]["stimulus"]["nodes"].keys()
                )
                if "bar-geo_geo-icon" in key:
                    barGeoGeoIcon += len(
                        answer["provenanceGraph"]["stimulus"]["nodes"].keys()
                    )
                    second = "bar-geo_geo-icon" if first != "" else ""
                    first = "bar-geo_geo-icon" if first == "" else first
                if "bar-icon_geo-icon" in key:
                    barIconGeoIcon += len(
                        answer["provenanceGraph"]["stimulus"]["nodes"].keys()
                    )
                    second = "bar-icon_geo-icon" if first != "" else ""
                    first = "bar-icon_geo-icon" if first == "" else first
                if "pie-geo_geo-icon" in key:
                    pieGeoGeoIcon += len(
                        answer["provenanceGraph"]["stimulus"]["nodes"].keys()
                    )
                    second = "pie-geo_geo-icon" if first != "" else ""
                    first = "pie-geo_geo-icon" if first == "" else first
                if "pie-icon_geo-icon" in key:
                    pieIconGeoIcon += len(
                        answer["provenanceGraph"]["stimulus"]["nodes"].keys()
                    )
                    second = "pie-icon_geo-icon" if first != "" else ""
                    first = "pie-icon_geo-icon" if first == "" else first
                if "map-geo_geo-icon" in key:
                    mapGeoGeoIcon += len(
                        answer["provenanceGraph"]["stimulus"]["nodes"].keys()
                    )
                    second = "map-geo_geo-icon" if first != "" else ""
                    first = "map-geo_geo-icon" if first == "" else first
                if "map-icon_geo-icon" in key:
                    mapIconGeoIcon += len(
                        answer["provenanceGraph"]["stimulus"]["nodes"].keys()
                    )
                    second = "map-icon_geo-icon" if first != "" else ""
                    first = "map-icon_geo-icon" if first == "" else first

        # store the count in the dictionary
        event_count[participant_id] = {
            "windowEvents": windowEventCount,
            "provenanceNodes": totalProvenanceNodeCount,
            "bar-geo_geo-icon": barGeoGeoIcon,
            "bar-icon_geo-icon": barIconGeoIcon,
            "pie-geo_geo-icon": pieGeoGeoIcon,
            "pie-icon_geo-icon": pieIconGeoIcon,
            "map-geo_geo-icon": mapGeoGeoIcon,
            "map-icon_geo-icon": mapIconGeoIcon,
            "first": first,
            "second": second,
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
