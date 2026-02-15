import os
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
JSON_FILE = os.path.join("utils", "pl-yt-stats.json")


# Official Channel IDs for the Premier League Big Six
BIG_SIX_CHANNELS = {
    "Arsenal": "UCpryVRk_VDudG8SHXgWcG0w",
    "Chelsea": "UCU2PacFf99vhb3hNiYDmxww",
    "Liverpool": "UC9LQwHZoucFT94I2h6JOcjw",
    "Manchester City": "UCkzCjdRMrW2vXLx8mvPVLdQ",
    "Manchester United": "UC6yW44UGJJBvYTlfC7CRg2Q",
    "Tottenham": "UCEg25rdRZXg32iwai6N6l0w",
}


def get_channel_stats(api_key, channel_dict):
    youtube = build("youtube", "v3", developerKey=api_key)
    results = []

    # Get stats in a single request for efficiency
    channel_ids = list(channel_dict.values())
    request = youtube.channels().list(
        part="snippet,statistics", id=",".join(channel_ids)
    )
    response = request.execute()

    for item in response.get("items", []):
        stats = item["statistics"]
        name = item["snippet"]["title"]
        if name == "Tottenham Hotspur":
            color = "#132257"
        if name == "Chelsea Football Club":
            color = "#034694"
        if name == "Arsenal":
            color = "#EF0107"
        if name == "Liverpool FC":
            color = "#D00027"
        if name == "Manchester United":
            color = "#DA291C"
        if name == "Man City":
            color = "#6CABDD"

        subs = int(stats["subscriberCount"])
        views = int(stats["viewCount"])
        vids = int(stats["videoCount"])

        results.append(
            {
                "club": name,
                "subscribers": subs,
                "total_views": views,
                "video_count": vids,
                "color": color,
            }
        )

    return results


if __name__ == "__main__":
    data = get_channel_stats(API_KEY, BIG_SIX_CHANNELS)
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("Data successfully pulled and saved to pl_stats.json")
