#
# Script to extract interaction data from the bubble chart study's provenance data.
#

import sys
import json
import pandas as pd

sys.setrecursionlimit(3000)

# Download all the participants' data as json from the analysis page:
# https://revisit.dev/replication-studies/analysis/stats/bubblechart-study/table

with open("./bubblechart-study-main.json") as f:
    data = json.load(f)
    all_graphs = []
    for d in data:
        is_search = "bubbleChartWithSearch_4" in d["answers"]
        if "prolificId" not in d["answers"]["introduction_1"]["answer"]:
            print("No Prolific Id")
            continue
        prolificId = d["answers"]["introduction_1"]["answer"]["prolificId"]
        stimulus = (
            "bubbleChartWithSearch_4" if is_search else "bubbleChartWithoutSearch_4"
        )
        graph = d["answers"][stimulus]["provenanceGraph"]
        graph["condition"] = "search" if is_search else "no search"
        graph["prolificId"] = prolificId
        all_graphs.append(graph)

df = pd.DataFrame(
    columns=[
        "ProlificId",
        "Condition",
        "College",
        "Duration",
        "SearchValue",
        "PartOfSearch",
    ]
)


def traverse(prolificId, condition, nodes, current, prev):
    c = nodes[current]
    if len(nodes[current]["children"]) == 0:
        return

    if c["event"] == "hoverItem":
        hoveredItem = nodes[current]["state"]["val"]["all"]["hoveredItem"]
        currentCreatedOn = nodes[current]["createdOn"]
        if hoveredItem is None:
            # get previous hoveredItem and calculate total time
            prevItem = nodes[prev]["state"]["val"]["all"]["hoveredItem"]
            prevSearchValue = nodes[prev]["state"]["val"]["all"]["searchValue"]
            prevCreatedOn = nodes[prev]["createdOn"]
            duration = currentCreatedOn - prevCreatedOn

            # Min time of 500ms
            if duration >= 500:
                contains = False
                if prevSearchValue and prevSearchValue.strip() != "":
                    contains = prevSearchValue.lower() in prevItem["INSTNM"].lower()

                df.loc[len(df)] = [
                    prolificId,
                    condition,
                    prevItem["INSTNM"],
                    currentCreatedOn - prevCreatedOn,
                    prevSearchValue,
                    contains,
                ]

        traverse(prolificId, condition, nodes, nodes[current]["children"][0], current)
    else:
        traverse(prolificId, condition, nodes, nodes[current]["children"][0], prev)


for graph in all_graphs:
    if "stimulus" not in graph:
        print("No Stimulus")
        continue
    stimulus = graph["stimulus"]
    nodes = stimulus["nodes"]
    root = stimulus["root"]
    condition = graph["condition"]
    prolificId = graph["prolificId"]
    print(prolificId)
    traverse(prolificId, condition, nodes, root, None)

df.to_csv("bubble-chart-study-main.csv")
