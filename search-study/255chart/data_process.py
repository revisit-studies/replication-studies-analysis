import pandas as pd
import json

# Download all the participants' data as json from the analysis page:
# https://revisit.dev/replication-studies/analysis/stats/255chart-study/table
# Initialize an empty DataFrame
df = pd.DataFrame(columns=["ProlificId", "Condition", "Duration", "SearchValue", "chartCode"])
dfs = pd.DataFrame(columns=["ProlificId", "Condition", "Duration", "selectedCharts"])
df_stats = pd.DataFrame(columns=["ParticipantId","ProlificId", "IsSearch", "TotalVisitDuration", "TotalSearchDuration", "VisitCount", "SearchCount"])

# Load JSON data
with open("./255chart-study_main2_all.json") as f:
    data = json.load(f)
    
    records = []  
    searchRecords = []
    stats = {}
    
    for d in data:
        pid = d["participantId"]
        if "introduction_1" not in d["answers"] or "answer" not in d["answers"]["introduction_1"] or "q-short-text" not in d["answers"]["introduction_1"]["answer"]:
            print('Not completed:')
            print(pid)
            continue
        is_search = "255ChartSearch_4" in d["answers"]
        prolificId = d["answers"]["introduction_1"]["answer"]["q-short-text"]
        if prolificId == 'YD':
            continue
        stimulus = "255ChartSearch_4" if is_search else "255ChartControl_4"       
        
        # Extract visits
        visited = [v for v in d["answers"].get(stimulus, {}).get("answer", {}).get('visit', []) if v.get("duration", 0) > 500]
        searched = [s for s in d["answers"].get(stimulus, {}).get("answer", {}).get('search', []) if s.get("duration", 0) > 500]
        
        total_visit_duration = sum(visit.get("duration", 0) for visit in visited)
        total_search_duration = sum(search.get("duration", 0) for search in searched)
        visit_count = len(visited)
        search_count = len(searched)
        
        if visit_count > 0:
            stats[prolificId] = {
                "ProlificId": prolificId,
                "ParticipantId": pid,
                "IsSearch": is_search,
                "TotalVisitDuration": total_visit_duration,
                "TotalSearchDuration": total_search_duration,
                "VisitCount": visit_count,
                "SearchCount": search_count
            }
        
        if visit_count > 0:
            for visit in visited:
                records.append({
                    "ProlificId": prolificId,
                    "Condition": stimulus,
                    "Duration": visit.get("duration", 0),
                    "SearchValue": visit.get("searchId", -1),
                    "chartCode": visit.get("chartCode", "Unknown")
                })

        if visit_count >0:
            for search in searched:
                searchRecords.append({
                    "ProlificId": prolificId,
                    "Condition": stimulus,
                    "Duration": search.get("duration", -1),
                    "selectedCharts": search.get('selectedCharts', -1)
                }) 
        if visit_count == 0:
            print('0 visit')
            print(pid)

# Convert to DataFrame
df = pd.DataFrame(records)
dfs = pd.DataFrame(searchRecords)
df_stats = pd.DataFrame(stats.values())

# Sort df_stats by VisitCount in descending order
df_stats = df_stats.sort_values(by="VisitCount", ascending=False)

# Save to CSV
df.to_csv("output-main2_100p.csv", index=False)
dfs.to_csv("output-main2-search_100p.csv", index=False)
df_stats.to_csv("output-main2-stats_100p.csv", index=False)
