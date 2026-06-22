import pandas as pd
import sqlite3

conn = sqlite3.connect("food_wastage.db")

providers = pd.read_csv("C:/Users/Bhagyashree/OneDrive/Desktop/food_waste_management/data/providers_data.csv")
receivers = pd.read_csv("C:/Users/Bhagyashree/OneDrive/Desktop/food_waste_management/data/receivers_data.csv")
food = pd.read_csv("C:/Users/Bhagyashree/OneDrive/Desktop/food_waste_management/data/food_listings_data.csv")
claims = pd.read_csv("C:/Users/Bhagyashree/OneDrive/Desktop/food_waste_management/data/claims_data.csv")

providers.to_sql("providers", conn, if_exists="replace", index=False)
receivers.to_sql("receivers", conn, if_exists="replace", index=False)
food.to_sql("food_listings", conn, if_exists="replace", index=False)
claims.to_sql("claims", conn, if_exists="replace", index=False)

print("Database Created Successfully")