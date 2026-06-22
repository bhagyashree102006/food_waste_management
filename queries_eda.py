import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("food_wastage.db")

# ---------------- GRAPH 1 ----------------
q1 = """
SELECT City,
COUNT(*) AS Total_Providers
FROM providers
GROUP BY City
ORDER BY Total_Providers DESC
LIMIT 10
"""

df = pd.read_sql(q1, conn)

plt.figure(figsize=(10,5))
plt.bar(df["City"], df["Total_Providers"])
plt.title("Top 10 Cities by Providers")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ---------------- GRAPH 2 ----------------
q2 = """
SELECT City,
COUNT(*) AS Total_Receivers
FROM receivers
GROUP BY City
ORDER BY Total_Receivers DESC
LIMIT 10
"""

df = pd.read_sql(q2, conn)

plt.figure(figsize=(10,5))
plt.bar(df["City"], df["Total_Receivers"])
plt.title("Top 10 Cities by Receivers")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ---------------- GRAPH 3 ----------------
q3 = """
SELECT Food_Type,
COUNT(*) AS Total_Items
FROM food_listings
GROUP BY Food_Type
ORDER BY Total_Items DESC
LIMIT 10
"""

df = pd.read_sql(q3, conn)

plt.figure(figsize=(8,8))
plt.pie(df["Total_Items"],
        labels=df["Food_Type"],
        autopct="%1.1f%%")
plt.title("Food Type Distribution")
plt.show()


# ---------------- GRAPH 4 ----------------
q4 = """
SELECT Provider_Type,
SUM(Quantity) AS Total_Food
FROM food_listings
GROUP BY Provider_Type
ORDER BY Total_Food DESC
LIMIT 10
"""

df = pd.read_sql(q4, conn)

plt.figure(figsize=(10,5))
plt.bar(df["Provider_Type"], df["Total_Food"])
plt.title("Provider Contribution")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ---------------- GRAPH 5 ----------------
q5 = """
SELECT Status,
COUNT(*) AS Total
FROM claims
GROUP BY Status
"""

df = pd.read_sql(q5, conn)

plt.figure(figsize=(8,8))
plt.pie(df["Total"],
        labels=df["Status"],
        autopct="%1.1f%%")
plt.title("Claim Status")
plt.show()


# ---------------- GRAPH 6 ----------------
q6 = """
SELECT Location,
COUNT(*) AS Listings
FROM food_listings
GROUP BY Location
ORDER BY Listings DESC
LIMIT 10
"""

df = pd.read_sql(q6, conn)

plt.figure(figsize=(10,5))
plt.bar(df["Location"], df["Listings"])
plt.title("Top 10 Locations")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ---------------- GRAPH 7 ----------------
q7 = """
SELECT Meal_Type,
COUNT(*) AS Total
FROM food_listings
GROUP BY Meal_Type
ORDER BY Total DESC
LIMIT 10
"""

df = pd.read_sql(q7, conn)

plt.figure(figsize=(10,5))
plt.bar(df["Meal_Type"], df["Total"])
plt.title("Meal Type Distribution")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ---------------- GRAPH 8 ----------------
q8 = """
SELECT Food_Name,
COUNT(*) AS Total
FROM food_listings
GROUP BY Food_Name
ORDER BY Total DESC
LIMIT 10
"""

df = pd.read_sql(q8, conn)

df["Food_Name"] = df["Food_Name"].astype(str).str[:12]

plt.figure(figsize=(12,5))
plt.bar(df["Food_Name"], df["Total"])
plt.title("Top 10 Food Items")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ---------------- GRAPH 9 ----------------
q9 = """
SELECT Provider_ID,
SUM(Quantity) AS Total_Donated
FROM food_listings
GROUP BY Provider_ID
ORDER BY Total_Donated DESC
LIMIT 10
"""

df = pd.read_sql(q9, conn)

plt.figure(figsize=(10,5))
plt.bar(df["Provider_ID"].astype(str),
        df["Total_Donated"])

plt.title("Top 10 Donors")
plt.tight_layout()
plt.show()


# ---------------- GRAPH 10 ----------------
q10 = """
SELECT Receiver_ID,
COUNT(*) AS Total_Claims
FROM claims
GROUP BY Receiver_ID
ORDER BY Total_Claims DESC
LIMIT 10
"""

df = pd.read_sql(q10, conn)

plt.figure(figsize=(10,5))
plt.bar(df["Receiver_ID"].astype(str),
        df["Total_Claims"])

plt.title("Top 10 Receivers")
plt.tight_layout()
plt.show()


# ---------------- GRAPH 11 ----------------
q11 = """
SELECT Food_Type,
AVG(Quantity) AS Avg_Qty
FROM food_listings
GROUP BY Food_Type
ORDER BY Avg_Qty DESC
LIMIT 10
"""

df = pd.read_sql(q11, conn)

plt.figure(figsize=(10,5))
plt.bar(df["Food_Type"],
        df["Avg_Qty"])

plt.title("Average Quantity by Food Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ---------------- GRAPH 12 ----------------
q12 = """
SELECT Provider_Type,
COUNT(*) AS Listings
FROM food_listings
GROUP BY Provider_Type
ORDER BY Listings DESC
LIMIT 10
"""

df = pd.read_sql(q12, conn)

plt.figure(figsize=(10,5))
plt.bar(df["Provider_Type"],
        df["Listings"])

plt.title("Listings by Provider Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ---------------- GRAPH 13 ----------------
q13 = """
SELECT Location,
SUM(Quantity) AS Total_Qty
FROM food_listings
GROUP BY Location
ORDER BY Total_Qty DESC
LIMIT 10
"""

df = pd.read_sql(q13, conn)

plt.figure(figsize=(10,5))
plt.bar(df["Location"],
        df["Total_Qty"])

plt.title("Top 10 Cities by Quantity")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ---------------- GRAPH 14 ----------------
q14 = """
SELECT Food_Name,
Quantity
FROM food_listings
ORDER BY Quantity DESC
LIMIT 10
"""

df = pd.read_sql(q14, conn)

df["Food_Name"] = df["Food_Name"].astype(str).str[:12]

plt.figure(figsize=(12,5))
plt.bar(df["Food_Name"],
        df["Quantity"])

plt.title("Top 10 Food Quantities")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ---------------- GRAPH 15 ----------------
q15 = """
SELECT Provider_ID,
COUNT(*) AS Listings
FROM food_listings
GROUP BY Provider_ID
ORDER BY Listings DESC
LIMIT 10
"""

df = pd.read_sql(q15, conn)

plt.figure(figsize=(10,5))
plt.bar(df["Provider_ID"].astype(str),
        df["Listings"])

plt.title("Top 10 Providers by Listings")
plt.tight_layout()
plt.show()

conn.close()




