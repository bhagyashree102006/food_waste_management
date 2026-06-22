import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("food_wastage.db", check_same_thread=False)

st.set_page_config(
    page_title="Food Wastage Management System",
    layout="wide"
)

st.title("🍲 Food Wastage Management System")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Providers",
        "Receivers",
        "Claims",
        "Food Listings",
        "CRUD Operations",
        "SQL Analysis",
        "EDA Dashboard"
    ]
)

# ================= DASHBOARD =================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    # YAHAN SE NAYA KPI CODE START

    total_providers = pd.read_sql(
        "SELECT COUNT(*) total FROM providers", conn
    ).iloc[0,0]

    total_receivers = pd.read_sql(
        "SELECT COUNT(*) total FROM receivers", conn
    ).iloc[0,0]

    total_food_listings = pd.read_sql(
        "SELECT COUNT(*) total FROM food_listings", conn
    ).iloc[0,0]

    total_claims = pd.read_sql(
        "SELECT COUNT(*) total FROM claims", conn
    ).iloc[0,0]

    total_quantity = pd.read_sql(
        "SELECT SUM(Quantity) total FROM food_listings", conn
    ).iloc[0,0]

    completed_claims = pd.read_sql(
        "SELECT COUNT(*) total FROM claims WHERE Status='Completed'", conn
    ).iloc[0,0]

    pending_claims = pd.read_sql(
        "SELECT COUNT(*) total FROM claims WHERE Status='Pending'", conn
    ).iloc[0,0]

    cancelled_claims = pd.read_sql(
        "SELECT COUNT(*) total FROM claims WHERE Status='Cancelled'", conn
    ).iloc[0,0]

    total_cities = pd.read_sql(
        "SELECT COUNT(DISTINCT City) total FROM providers", conn
    ).iloc[0,0]

    food_types = pd.read_sql(
        "SELECT COUNT(DISTINCT Food_Type) total FROM food_listings", conn
    ).iloc[0,0]

    meal_types = pd.read_sql(
        "SELECT COUNT(DISTINCT Meal_Type) total FROM food_listings", conn
    ).iloc[0,0]

    provider_types = pd.read_sql(
        "SELECT COUNT(DISTINCT Provider_Type) total FROM food_listings", conn
    ).iloc[0,0]

    # KPI CARDS

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Providers", total_providers)
    c2.metric("Receivers", total_receivers)
    c3.metric("Food Listings", total_food_listings)
    c4.metric("Claims", total_claims)

    c5,c6,c7,c8 = st.columns(4)

    c5.metric("Food Quantity", total_quantity)
    c6.metric("Completed", completed_claims)
    c7.metric("Pending", pending_claims)
    c8.metric("Cancelled", cancelled_claims)

    c9,c10,c11,c12 = st.columns(4)

    c9.metric("Cities", total_cities)
    c10.metric("Food Types", food_types)
    c11.metric("Meal Types", meal_types)
    c12.metric("Provider Types", provider_types)

    st.subheader("Top 10 Cities By Providers")

    q = """
    SELECT City,
    COUNT(*) Total_Providers
    FROM providers
    GROUP BY City
    ORDER BY Total_Providers DESC
    LIMIT 10
    """

    df = pd.read_sql(q, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["City"], df["Total_Providers"])

    plt.xticks(rotation=45)

    st.pyplot(fig)

# ================= PROVIDERS =================

elif menu == "Providers":

    st.header("Providers")

    df = pd.read_sql(
        "SELECT * FROM providers",
        conn
    )

    st.dataframe(df)

# ================= RECEIVERS =================

elif menu == "Receivers":

    st.header("Receivers")

    df = pd.read_sql(
        "SELECT * FROM receivers",
        conn
    )

    st.dataframe(df)

# ================= CLAIMS =================

elif menu == "Claims":

    st.header("Claims")

    df = pd.read_sql(
        "SELECT * FROM claims",
        conn
    )

    st.dataframe(df)
    # ================= FOOD LISTINGS =================

#elif menu == "Food Listings":

   # st.header("Food Listings")

    #city = st.selectbox(
        ##"Select City",
        #["All"] +
        #list(
           # pd.read_sql(
               # "SELECT DISTINCT Location FROM food_listings",
             #   conn
            #)["Location"]
       # )
    #)
elif menu == "Food Listings":

    st.header("🍲 Food Listings")

    df = pd.read_sql(
        "SELECT * FROM food_listings",
        conn
    )

    # Search Box
    search = st.text_input("🔍 Search Food Name")

    if search:
        df = df[
            df["Food_Name"].astype(str)
            .str.contains(search, case=False)
        ]

    # Location Filter
    locations = ["All"] + list(df["Location"].dropna().unique())

    selected_location = st.selectbox(
        "📍 Select Location",
        locations
    )

    if selected_location != "All":
        df = df[
            df["Location"] == selected_location
        ]

    # Show Data
    st.dataframe(df)

    # Download CSV
    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="food_listings.csv",
        mime="text/csv"
    )

    food_type = st.selectbox(
        "Food Type",
        ["All"] +
        list(
            pd.read_sql(
                "SELECT DISTINCT Food_Type FROM food_listings",
                conn
            )["Food_Type"]
        )
    )

    meal_type = st.selectbox(
        "Meal Type",
        ["All"] +
        list(
            pd.read_sql(
                "SELECT DISTINCT Meal_Type FROM food_listings",
                conn
            )["Meal_Type"]
        )
    )

    query = "SELECT * FROM food_listings WHERE 1=1"

    if selected_location != "All":
        df = df[df["Location"] == selected_location]
        #query += f" AND Location='{city}'"

    if food_type != "All":
        query += f" AND Food_Type='{food_type}'"

    if meal_type != "All":
        query += f" AND Meal_Type='{meal_type}'"

    df = pd.read_sql(query, conn)

    st.dataframe(df)

    st.subheader("Provider Contact Details")

    providers_df = pd.read_sql("""
    SELECT
    Provider_ID,
    Name,
    Type,
    City,
    Contact
    FROM providers
    """, conn)

    st.dataframe(providers_df)

    st.subheader("Receiver Contact Details")

    receivers_df = pd.read_sql("""
    SELECT
    Receiver_ID,
    Name,
    Type,
    City,
    Contact
    FROM receivers
    """, conn)

    st.dataframe(receivers_df)
elif menu == "CRUD Operations":

    st.header("✏️ CRUD Operations")

    crud_option = st.selectbox(
        "Select Operation",
        ["Add Food", "Update Food", "Delete Food"]
    )

    # ADD FOOD
    if crud_option == "Add Food":

        st.subheader("Add Food Listing")

        food_name = st.text_input("Food Name")
        quantity = st.number_input("Quantity", min_value=1)

        expiry = st.text_input("Expiry Date")

        provider_id = st.number_input(
            "Provider ID",
            min_value=1
        )

        provider_type = st.text_input(
            "Provider Type"
        )

        location = st.text_input("Location")

        food_type = st.text_input("Food Type")

        meal_type = st.text_input("Meal Type")

        if st.button("Add Food"):

            conn.execute("""
            INSERT INTO food_listings
            (
            Food_Name,
            Quantity,
            Expiry_Date,
            Provider_ID,
            Provider_Type,
            Location,
            Food_Type,
            Meal_Type
            )
            VALUES (?,?,?,?,?,?,?,?)
            """,
            (
            food_name,
            quantity,
            expiry,
            provider_id,
            provider_type,
            location,
            food_type,
            meal_type
            ))

            conn.commit()

            st.success("Food Added Successfully")

    # UPDATE

    elif crud_option == "Update Food":

        st.subheader("Update Quantity")

        food_id = st.number_input(
            "Food ID",
            min_value=1
        )

        new_qty = st.number_input(
            "New Quantity",
            min_value=1
        )

        if st.button("Update"):

            conn.execute("""
            UPDATE food_listings
            SET Quantity=?
            WHERE Food_ID=?
            """,
            (new_qty, food_id))

            conn.commit()

            st.success("Updated Successfully")

    # DELETE

    elif crud_option == "Delete Food":

        st.subheader("Delete Food")

        food_id = st.number_input(
            "Food ID",
            min_value=1
        )

        if st.button("Delete"):

            conn.execute("""
            DELETE FROM food_listings
            WHERE Food_ID=?
            """,
            (food_id,))

            conn.commit()

          # ================= SQL ANALYSIS =================

elif menu == "SQL Analysis":

    st.header("📈 SQL Analysis")

    queries = {

    "Q1 Providers Per City":
    """
    SELECT City,
    COUNT(*) AS Total_Providers
    FROM providers
    GROUP BY City
    ORDER BY Total_Providers DESC
    """,

    "Q2 Receivers Per City":
    """
    SELECT City,
    COUNT(*) AS Total_Receivers
    FROM receivers
    GROUP BY City
    ORDER BY Total_Receivers DESC
    """,

    "Q3 Provider Type Contribution":
    """
    SELECT Provider_Type,
    SUM(Quantity) AS Total_Food
    FROM food_listings
    GROUP BY Provider_Type
    ORDER BY Total_Food DESC
    """,

    "Q4 Total Food Quantity":
    """
    SELECT SUM(Quantity) AS Total_Food
    FROM food_listings
    """,

    "Q5 Listings By Location":
    """
    SELECT Location,
    COUNT(*) AS Listings
    FROM food_listings
    GROUP BY Location
    ORDER BY Listings DESC
    """,

    "Q6 Food Type Distribution":
    """
    SELECT Food_Type,
    COUNT(*) AS Total
    FROM food_listings
    GROUP BY Food_Type
    """,

    "Q7 Claim Status":
    """
    SELECT Status,
    COUNT(*) AS Total
    FROM claims
    GROUP BY Status
    """,

    "Q8 Meal Type":
    """
    SELECT Meal_Type,
    COUNT(*) AS Total
    FROM food_listings
    GROUP BY Meal_Type
    """,

    "Q9 Top Donors":
    """
    SELECT Provider_ID,
    SUM(Quantity) AS Total_Donated
    FROM food_listings
    GROUP BY Provider_ID
    ORDER BY Total_Donated DESC
    LIMIT 10
    """,

    "Q10 Top Receivers":
    """
    SELECT Receiver_ID,
    COUNT(*) AS Total_Claims
    FROM claims
    GROUP BY Receiver_ID
    ORDER BY Total_Claims DESC
    LIMIT 10
    """
    }

    selected_query = st.selectbox(
        "Select Query",
        list(queries.keys())
    )

    result = pd.read_sql(
        queries[selected_query],
        conn
    )

    st.dataframe(result)

# ================= EDA DASHBOARD =================

elif menu == "EDA Dashboard":

    st.header("📊 EDA Dashboard")

    q1 = """
    SELECT City,
    COUNT(*) AS Total_Providers
    FROM providers
    GROUP BY City
    ORDER BY Total_Providers DESC
    LIMIT 10
    """

    df = pd.read_sql(q1, conn)

    fig, ax = plt.subplots(figsize=(8,4))

    ax.bar(
        df["City"],
        df["Total_Providers"]
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)
elif menu == "EDA Dashboard":

    st.header("📊 EDA Dashboard")

    # Graph 1
    st.subheader("Top 10 Cities By Providers")

    df = pd.read_sql("""
    SELECT City,
    COUNT(*) AS Total
    FROM providers
    GROUP BY City
    ORDER BY Total DESC
    LIMIT 10
    """, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["City"], df["Total"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Graph 2
    st.subheader("Food Type Distribution")

    df = pd.read_sql("""
    SELECT Food_Type,
    COUNT(*) AS Total
    FROM food_listings
    GROUP BY Food_Type
    """, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["Food_Type"], df["Total"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Graph 3
    st.subheader("Claim Status")

    df = pd.read_sql("""
    SELECT Status,
    COUNT(*) AS Total
    FROM claims
    GROUP BY Status
    """, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["Status"], df["Total"])
    st.pyplot(fig)

    # Graph 4
    st.subheader("Provider Type Contribution")

    df = pd.read_sql("""
    SELECT Provider_Type,
    SUM(Quantity) AS Total
    FROM food_listings
    GROUP BY Provider_Type
    """, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["Provider_Type"], df["Total"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Graph 5
    st.subheader("Top 10 Locations")

    df = pd.read_sql("""
    SELECT Location,
    SUM(Quantity) AS Total
    FROM food_listings
    GROUP BY Location
    ORDER BY Total DESC
    LIMIT 10
    """, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["Location"], df["Total"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Graph 6
    st.subheader("Meal Type Distribution")

    df = pd.read_sql("""
    SELECT Meal_Type,
    COUNT(*) AS Total
    FROM food_listings
    GROUP BY Meal_Type
    """, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["Meal_Type"], df["Total"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Graph 7
    st.subheader("Top 10 Donors")

    df = pd.read_sql("""
    SELECT Provider_ID,
    SUM(Quantity) AS Total
    FROM food_listings
    GROUP BY Provider_ID
    ORDER BY Total DESC
    LIMIT 10
    """, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["Provider_ID"].astype(str), df["Total"])
    st.pyplot(fig)

    # Graph 8
    st.subheader("Top 10 Receivers")

    df = pd.read_sql("""
    SELECT Receiver_ID,
    COUNT(*) AS Total
    FROM claims
    GROUP BY Receiver_ID
    ORDER BY Total DESC
    LIMIT 10
    """, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["Receiver_ID"].astype(str), df["Total"])
    st.pyplot(fig)

    # Graph 9
    st.subheader("Food Quantity By Food Type")

    df = pd.read_sql("""
    SELECT Food_Type,
    SUM(Quantity) AS Total
    FROM food_listings
    GROUP BY Food_Type
    """, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["Food_Type"], df["Total"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Graph 10
    st.subheader("Listings By Provider Type")

    df = pd.read_sql("""
    SELECT Provider_Type,
    COUNT(*) AS Total
    FROM food_listings
    GROUP BY Provider_Type
    """, conn)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.bar(df["Provider_Type"], df["Total"])
    plt.xticks(rotation=45)
    st.pyplot(fig)