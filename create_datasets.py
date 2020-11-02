import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

def create_features(row):
    return {
        "length": len(row[3]),
        "body_length": len(row[5]),
        "subscribers": row[6],
        "active_users": row[7],
        "time": round((row[1] % 86400) / 3600, 2),
        "score": row[11]
    }

def save_features(features, name):
    lines = [",".join(features[0].keys()) + "\n"]
    for feature in features:
        lines.append(",".join([str(n) for n in feature.values()]) + "\n")
    with open(name, "w") as f:
        f.writelines(lines)


# Hour dataset
rows = list(c.execute("SELECT * FROM posts WHERE NOT score_hour ISNULL;").fetchall())
features = [create_features(row) for row in rows]
save_features(features, "hour-data.csv")

# Day dataset
rows = list(c.execute("SELECT * FROM posts WHERE NOT score_day ISNULL;").fetchall())
features = [create_features(row) for row in rows]
save_features(features, "day-data.csv")

# Week dataset
rows = list(c.execute("SELECT * FROM posts WHERE NOT score_week ISNULL;").fetchall())
features = [create_features(row) for row in rows]
save_features(features, "week-data.csv")





conn.close()