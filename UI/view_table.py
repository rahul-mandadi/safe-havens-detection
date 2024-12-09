import sys
import streamlit as st
import os
import sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Queries.query import Queries
from Queries.connection import Connection
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import joblib


conn_obj = sqlite3.connect('../safe-haven-detection.db')

conn = Connection(conn_obj).connect()
conn.execute("PRAGMA foreign_keys = ON;")
query = Queries(conn)



# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Queries", "Visualization", "ML Model", "Insert", "Update"],  key="sidebar_menu")

# Conditional rendering based on the selected menu option
if menu == "Dashboard":
    st.title("Safe Haven Dashboard")
    st.write("The Safe Haven Risk Detection system is a comprehensive data analytics platform designed to assess community safety metrics and classify which counties and cities are safe across the U.S.")


elif menu == "Queries":
    st.title("Fetch Data")
    # Tabs for the Queries section
    tabs = st.tabs(["Fire Emergency", "Food Banks", "Hospitals", "Law Enforcement"])  # Add appropriate tab names

    # Fire emergency services query
    with tabs[0]:
        st.subheader("Fire Emergency")

        city_id = st.number_input('Enter the county fips', min_value=1, value=1840008960, key="fire_emergency_fips")

        tab, df = query.query_by_city(city_id, 'fire_emergency_services')
        if not df.empty:
            st.subheader("Query Results")
            st.dataframe(df)  # Display the DataFrame in an interactive table
        else:
            st.warning("No data available for the given cities code.")

    # Food banks services query
    with tabs[1]:
        st.subheader("Food Banks")

        city_id = st.number_input('Enter the city fips', min_value=1, value=1840008960, key="food_banks_city_id")

        # Food banks query
        tab, df = query.query_by_city(city_id, 'food_banks')
        if not df.empty:
            st.subheader("Query Results")
            st.dataframe(df)  # Display the DataFrame in an interactive table
        else:
            st.warning("No data available for the given cities code.")

    # Hospitals services query
    with tabs[2]:
        st.subheader("Hospitals")

        city_id = st.number_input('Enter the city fips', min_value=1, value=1840008960, key="hospitals_city_id")

        # Hospitals query
        tab, df = query.query_by_city(city_id, 'hospitals')
        if not df.empty:
            st.subheader("Query Results")
            st.dataframe(df)
        else:
            st.warning("No data available for the given cities code.")

    # Law enforcement services query
    with tabs[3]:
        st.subheader("Law Enforcement")

        city_id = st.number_input('Enter the city fips', min_value=1, value=1840008960, key="law_enforcement_city_id")

        # Law enforcement query
        tab, df = query.query_by_city(city_id, 'local_law_enforcement')
        if not df.empty:
            st.subheader("Query Results")
            st.dataframe(df)
        else:
            st.warning("No data available for the given cities code.")
elif menu == "Visualization":
    st.title("Visualization")
    # st.write("This section will contain data visualization plots.")

    # Visualization for the top N counties based on crime rate
    st.subheader("Crime")
    top_n = st.number_input('Enter the number of top counties to display based on crime rate', min_value=1, max_value=100, value=20, key="top_n_input")

    tab, df = query.get_highest_top_n_crime_rate(top_n)

    if not df.empty: 
        counties = df['county_name'] 
        crime_rates = df['crime_rate_per_100000']  

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(counties, crime_rates, color='skyblue')

        ax.set_title(f'Top {top_n} Counties by Crime Rate', fontsize=16)
        ax.set_xlabel('Counties', fontsize=12)
        ax.set_ylabel('Crime Rate', fontsize=12)
        ax.tick_params(axis='x', rotation=45)

        st.pyplot(fig)

    plt.bar(df['county_name'], df['crime_rate_per_100000'], color='skyblue')


    # Visualization for the top N counties based on unemployment rate
    st.subheader("Unemployment")
    top_n_unemp_rates = st.number_input('Enter the number of top counties to display based on unemployment rate', min_value=1, max_value=100, value=20, key="top_n_unemp_rates")
    
    tab, df = query.get_highest_top_n_unemployment(top_n_unemp_rates)

    if not df.empty: 
        counties = df['county_name'] 
        unemployment_rates = df['unemployment_rate_2022']  

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(counties, unemployment_rates, color='skyblue')

        ax.set_title(f'Top {top_n_unemp_rates} Counties by Unemployment Rate', fontsize=16)
        ax.set_xlabel('Counties', fontsize=12)
        ax.set_ylabel('Unemployment Rate', fontsize=12)
        ax.tick_params(axis='x', rotation=45)

        st.pyplot(fig)

    plt.bar(df['county_name'], df['unemployment_rate_2022'], color='skyblue')

    # Visualization for the top N counties based on poverty rate
    st.subheader("Poverty")
    top_n_poverty_rates = st.number_input('Enter the number of top counties to display based on poverty rate', min_value=1, max_value=100, value=20, key="top_n_poverty_rates")
    
    tab, df = query.get_highest_top_n_poverty(top_n_poverty_rates)

    if not df.empty: 
        counties = df['county_name'] 
        poverty_rates = df['poverty_percentage']  

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(counties, poverty_rates, color='skyblue')

        ax.set_title(f'Top {top_n_poverty_rates} Counties by Poverty Rate', fontsize=16)
        ax.set_xlabel('Counties', fontsize=12)
        ax.set_ylabel('Poverty Rate', fontsize=12)
        ax.tick_params(axis='x', rotation=45)

        st.pyplot(fig)

    plt.bar(df['county_name'], df['poverty_percentage'], color='skyblue')

    # Visualization for the top N counties based on safety score
    st.subheader("Safety")
    top_n_safety_scores= st.number_input('Enter the number of top counties to display based on  rate', min_value=1, max_value=100, value=20, key="top_n_safety_scores")
    
    safety_df = query.get_safety_data()
    print(safety_df)
    top_safe = safety_df.sort_values(by='safety_index', ascending=False).tail(top_n_safety_scores).copy()

    top_safe['county_label'] = top_safe['county_name'] + ", " + top_safe['state_name']
    # if not df.empty: 
   # Create the plot
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.hlines(y=top_safe['county_label'], xmin=0, xmax=top_safe['safety_index'], color='#90CAF9', alpha=0.8, linewidth=2)
    ax.scatter(top_safe['safety_index'], top_safe['county_label'], color='#1E88E5', s=100, label='Safety Index')

    # Add title and labels
    ax.set_title(f'Top {top_n_safety_scores} Safest Counties', fontsize=16)
    ax.set_xlabel('Safety Index', fontsize=14)
    ax.set_ylabel('County Name, State', fontsize=14)

    # Add gridlines
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Adjust layout
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)


    # Visualization for the top N counties based on at-risk score
    st.subheader("At-Risk counties")
    top_n_risk= st.number_input('Enter the number of top counties to display based on risk', min_value=1, max_value=100, value=20, key="top_n_risk")
    
    risk_df = query.get_safety_data()
    print(risk_df)
    top_risk = risk_df.sort_values(by='safety_index', ascending=False).head(top_n_risk).copy()

    top_risk['county_label'] = top_risk['county_name'] + ", " + top_risk['state_name']
    # if not df.empty: 
   # Create the plot
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.hlines(y=top_risk['county_label'], xmin=0, xmax=top_risk['safety_index'], color='#90CAF9', alpha=0.8, linewidth=2)
    ax.scatter(top_risk['safety_index'], top_risk['county_label'], color='#1E88E5', s=100, label='Risk Index')

    # Add title and labels
    ax.set_title(f'Top {top_n_risk} Risky Counties', fontsize=16)
    ax.set_xlabel('Risk Index', fontsize=14)
    ax.set_ylabel('County Name, State', fontsize=14)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)


    # Visualization for the top N counties based on crime rate donut chart
    st.subheader("Crime Types Distribution")
    crime_data = query.get_crime_types_distribution()  
    crime_labels = ['Murder', 'Rape', 'Robbery', 'Burglary']
    crime_values = [
        crime_data['total_murder'],
        crime_data['total_rape'],
        crime_data['total_robbery'],
        crime_data['total_burglary']
    ]

    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    fig, ax = plt.subplots(figsize=(8, 8))

    wedges, texts = ax.pie(
        crime_values,
        labels=None,  # No labels directly on pie chart
        autopct=None,  
        colors=colors,
        startangle=90,
        wedgeprops=dict(width=0.3)  # Donut chart effect
    )
    total = sum(crime_values)
    legend_labels = [
        f"{label}: {value} ({value / total * 100:.1f}%)"
        for label, value in zip(crime_labels, crime_values)
    ]
    ax.legend(
        wedges,
        legend_labels,
        title="Crime Types",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    plt.tight_layout()
    st.pyplot(fig)


    # Visualization for the top N counties based on Population Growth and Safety Analysis
    st.subheader("Population Growth: Percentage and Absolute Trends (2020-2023)")
    top_n_pop= st.number_input('Enter the number of top counties to display based on risk', min_value=1, max_value=100, value=20, key="top_n_pop")
    
    growth_data = query.get_counties_with_highest_pop_growth(top_n_pop, "2020", "2023")  
    _, growth_df = growth_data  

    # Create the figure and first axis
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Population Growth Percentage as a bar chart
    ax1.bar(
        growth_df["county_name"], 
        growth_df["growth_percentage"], 
        color="skyblue", 
        alpha=0.7, 
        label="Population Growth (%)"
    )
    ax1.set_ylabel("Population Growth (%)", fontsize=12, color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")
    ax1.set_xlabel("County Name", fontsize=12)
    ax1.set_xticks(range(len(growth_df["county_name"])))
    ax1.set_xticklabels(growth_df["county_name"], rotation=45, ha="right")

    # Create a twin axis for Absolute Growth
    ax2 = ax1.twinx()
    ax2.plot(
        growth_df["county_name"], 
        growth_df["growth"], 
        color="green", 
        marker="o", 
        label="Population Growth (Absolute)"
    )
    ax2.set_ylabel("Population Growth (Absolute)", fontsize=12, color="green")
    ax2.tick_params(axis="y", labelcolor="green")

    # Set the overall title and layout
    # fig.suptitle("Population Growth: Percentage and Absolute Trends (2020-2023)", fontsize=14)
    fig.tight_layout()

    # Add legend and display the plot in Streamlit
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.95))
    st.pyplot(fig)




   # Visualization for the top N counties based on hospital count and crime rate
    st.subheader("Number of Hospitals in Counties with Crime Rate")

    # User input for the number of top counties to display
    crime_threshold = st.number_input(
        'Enter the number of top counties to display based on risk',
        min_value=1, max_value=100, value=10, key="crime_threshold"
    )

    # Fetch hospital data based on crime threshold
    _, hospital_df = query.get_hospital_with_percent_crime_rate(crime_threshold)

    # Group and count hospitals per county
    hospital_counts = (
        hospital_df.groupby(['county_name', 'crime_rate_per_100000'])
        .size()
        .reset_index(name='hospital_count')
    )

    # Sort the hospital data by crime rate
    hospital_counts = hospital_counts.sort_values(by='crime_rate_per_100000', ascending=False)

    # Adjust the number of counties displayed based on user input
    top_n = min(len(hospital_counts), crime_threshold)  # Limit to the number of available counties
    hospital_counts = hospital_counts.head(top_n)

    # Create a figure for the horizontal bar chart
    fig, ax = plt.subplots(figsize=(12, top_n * 0.6))  # Dynamically adjust the height
    bars = ax.barh(
        hospital_counts['county_name'], 
        hospital_counts['hospital_count'], 
        color="#FFA07A"
    )

    # Annotate each bar with the crime rate
    for bar, crime_rate in zip(bars, hospital_counts['crime_rate_per_100000']):
        ax.text(
            bar.get_width() + 0.5, 
            bar.get_y() + bar.get_height() / 2,
            f"{crime_rate:.1f}",
            va='center'
        )

    # Set chart titles and labels
    ax.set_title(f"Number of Hospitals in Top {top_n} Counties with Highest Crime Rate", fontsize=16)
    ax.set_xlabel("Number of Hospitals", fontsize=12)
    ax.set_ylabel("County Name", fontsize=12)

    # Adjust y-ticks for readability
    ax.tick_params(axis='y', labelsize=10)  # Decrease y-tick label font size
    ax.invert_yaxis()  # Invert y-axis to display the largest bar at the top

    # Adjust layout
    fig.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)





    # Visualization for the top N counties based on hospital count and crime rate
    st.subheader("Food Banks in High Poverty Areas")

   # Example threshold for poverty percentage
    threshold = st.slider("Select the poverty threshold (%)", min_value=20, max_value=30, value=20)


   # Query function
    _, food_bank_df = query.get_food_banks_with_percent_poverty(threshold)

    # Group by county and count the number of food banks
    food_bank_counts = food_bank_df.groupby('county_name')['food_bank_name'].count().reset_index()
    food_bank_counts = food_bank_counts.sort_values(by='food_bank_name', ascending=False)

    # Plot the data
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(food_bank_counts['county_name'], food_bank_counts['food_bank_name'], color="#66B3FF")
    ax.set_title(f"Number of Food Banks in Counties with Poverty > {threshold}%", fontsize=16)
    ax.set_xlabel("Number of Food Banks", fontsize=12)
    ax.set_ylabel("County Name", fontsize=12)
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)
elif menu == "ML Model":
    st.title("Machine Learning Model")
    st.write("This section will contain the machine learning model implementation.")

    scaler_X = joblib.load('../Machine Learning/scaler_X.joblib')
    best_rf = joblib.load('../Machine Learning/best_random_forest_model.joblib') 
    

    # Input fields for user to enter values
    murder = st.number_input("Number of murders", min_value=0.0, step=1.0)
    rape = st.number_input("Number of rapes", min_value=0.0, step=1.0)
    robbery = st.number_input("Number of robberies", min_value=0.0, step=1.0)
    burglary = st.number_input("Number of burglaries", min_value=0.0, step=1.0)
    unemployment_rate_2022 = st.number_input("Unemployment rate in 2022 (%)", min_value=0.0, max_value=100.0, step=0.1)
    population_estimate_2022 = st.number_input("Population estimate in 2022", min_value=0)
    poverty_index = st.number_input("Poverty index (sum of poverty percentages)", min_value=0.0, step=0.1)
    education_improvement = st.number_input("Education improvement (difference in no HS degree percentages)", min_value=0.0, step=0.1)

    if st.button("Predict"):

        input_data = pd.DataFrame({
            'murder': [murder],
            'rape': [rape],
            'robbery': [robbery],
            'burglary': [burglary],
            'unemployment_rate_2022': [unemployment_rate_2022],
            'population_estimate_2022': [population_estimate_2022],
            'poverty_index': [poverty_index],
            'education_improvement': [education_improvement]
        })

        # Ensure the features are in the correct order
        required_columns = [
            'murder', 'rape', 'robbery', 'burglary',
            'unemployment_rate_2022', 'population_estimate_2022',
            'poverty_index', 'education_improvement'
        ]

        input_data = input_data[required_columns]

        # Apply log1p transformation to skewed features (as done in preprocessing)
        skewed_features = [
            'murder', 'rape', 'robbery', 'burglary',
            'unemployment_rate_2022', 'population_estimate_2022'
        ]
        for feature in skewed_features:
            input_data[feature] = np.log1p(input_data[feature])

        # Apply the scaler
        input_data_scaled = scaler_X.transform(input_data)

        # Predict crime rates in log-transformed space
        predicted_crime_rates_log = best_rf.predict(input_data_scaled)

        # Inverse transform to get crime rates in original scale
        predicted_crime_rates = np.expm1(predicted_crime_rates_log)

        crime_rate_median_original = 176.4591

        # Classify safety levels using the median in original scale
        safety_levels = ['Safe' if rate <= crime_rate_median_original else 'High-Risk' for rate in predicted_crime_rates]

        # Prepare the results DataFrame
        results = input_data.copy()
        # results['Predicted_Crime_Rate'] = predicted_crime_rates
        results['Predicted_Crime_Rate'] = predicted_crime_rates
        results['Safety_Level'] = safety_levels

        # print(results)
        predicted_value  = results['Safety_Level']
        
        st.write(f"The predicted crime rate is: {predicted_crime_rates[0]} which is considered {predicted_value[0]}")
        # st.write(results)

elif menu == "Insert":
    st.title("Insert Operations")
    st.write("This section will contain Insert operations on the database.")

    city_id_options = query.get_all_city_ids()
    fips_code_list = query.get_all_fips_codes()


    # Create operation Populations
    st.subheader("Insert population data")

    fips_code_list_population = query.get_all_fips_codes_in_population()
    fipscode_pop = st.selectbox("Select Fipscode", fips_code_list_population, key="fipscode_pop")
    population_estimate_2020 = st.number_input("population_estimate_2020")
    population_estimate_2021 = st.number_input("population_estimate_2021")
    population_estimate_2022 = st.number_input("population_estimate_2022")
    population_estimate_2023 = st.number_input("population_estimate_2023")
    
    if st.button("Add Population Record"):
        query.insert_population(fipscode_pop, population_estimate_2020, population_estimate_2021, population_estimate_2022, population_estimate_2023)
        st.write("Record added successfully!")
        
    # Create operation crime
    st.subheader("Insert crime data")
    fips_code_list_crime = query.get_all_fips_codes_in_crime()
    fipscode_crime = st.selectbox("Select Fipscode", fips_code_list_crime, key="fips_code_crime")
    crime_rate_per_100000 = st.number_input("crime_rate_per_100000")
    crime_id = st.number_input("crime_id")
    murder = st.number_input("murder")
    rape = st.number_input("rape")
    burglary = st.number_input("burglary")
    robbery = st.number_input("robbery")
    
    if st.button("Add Crime Record"):
        msg = query.insert_crime(fipscode_crime, crime_rate_per_100000, crime_id, murder, rape, burglary, robbery)
        
        # query.hello()

        st.write(msg)

    # Create operation education
    st.subheader("Insert education data")   
    fips_code_list_educatoin = query.get_all_fips_codes_in_education()
    fipscode_edu = st.selectbox("Select Fipscode", fips_code_list_educatoin, key="fips_code_edu")
    pct_no_hs_degree_18_22 = st.number_input("pct_no_hs_degree_18_22")
    pct_no_hs_degree_08_12 = st.number_input("pct_no_hs_degree_08_12")
    pct_no_hs_degree_2000 = st.number_input("pct_no_hs_degree_2000")

    if st.button("Add Education Record"):
        msg = query.insert_education(fipscode_edu, pct_no_hs_degree_18_22, pct_no_hs_degree_08_12, pct_no_hs_degree_2000)
        st.write(msg)

    
    # Create operation fire emergency services
    st.subheader("Insert Fire Emergency Services Data")
    city_id_list_fire = query.get_all_city_ids_in_fire_emergency_services()
    city_id_fire = st.selectbox("Select City ID", city_id_list_fire, key="city_id_fire")
    fire_emergency_id = st.number_input("fire_emergency_id")
    name = st.text_input("Name")
    address = st.text_input("Address")
    
    if st.button("Add Fire Emergency Service Record"):
        msg = query.insert_fire_emergency_services(city_id_fire, fire_emergency_id, name, address)
        st.write(msg)

    # Create operation hospitals
    st.subheader("Insert Hospital Data")
    hospital_id = st.number_input("hospital_id")
    city_id_list_hosp = query.get_all_city_ids_in_hospitals()
    city_id_hosp = st.selectbox("Select City ID", city_id_list_hosp, key="city_id_hosp")
    name = st.text_input("Hospital Name")
    address = st.text_input("Hospital Address")
    status = st.text_input("Status")
    ownership_information = st.text_input("Ownership Information")

    if st.button("Add Hospital Record"):
        msg = query.insert_hospital(hospital_id, city_id, name, address, status, ownership_information)
        st.write(msg)

    # Create operation local law enforcement
    st.subheader("Insert Local Law Enforcement Data")
    city_id_list_law = query.get_all_city_ids_in_local_law_enforcement()
    city_id_law = st.selectbox("Select City ID", city_id_list_law, key="city_id_law")
    law_enforcement_id = st.number_input("Law Enforcement ID")
    name = st.text_input("Law Enforcement Name")
    address = st.text_input("Law Enforcement Address")
    type_of_law_enforcement = st.text_input("Type of Law Enforcement")

    if st.button("Add Law Enforcement Record"):
        msg = query.insert_local_law_enforcement(law_enforcement_id, name, city_id_law, address, type_of_law_enforcement)
        st.write(msg)

    
    # Create operation poverty
    st.subheader("Insert Poverty Data")
    fips_code_list_pov = query.get_all_fips_codes_in_poverty()
    fipscode_poverty = st.selectbox("Select Fipscode", fips_code_list_pov, key="fips_code_poverty")
    poverty_percentage = st.number_input("Poverty Percentage")
    poverty_percentage_18 = st.number_input("Poverty Percentage 18")
    poverty_percentage_5_17 = st.number_input("Poverty Percentage 5-17")

    year = st.number_input("Year", min_value=2000, max_value=2023, step=1)

    if st.button("Add Poverty Record"):
        msg = query.insert_poverty(fipscode_poverty, poverty_percentage, poverty_percentage_18, poverty_percentage_5_17)
        st.write(msg)

    # Create operation unemployment
    st.subheader("Insert Unemployment Data")
    fipscode_unemployment = st.selectbox("Select Fipscode", fips_code_list, key="fips_code_unemployment")
    unemployment_rate_2020 = st.number_input("Unemployment Rate 2020")
    unemployment_rate_2021 = st.number_input("Unemployment Rate 2021")
    unemployment_rate_2022 = st.number_input("Unemployment Rate 2022")

    if st.button("Add Unemployment Record"):
        msg = query.insert_unemployment(fipscode_unemployment, unemployment_rate_2020, unemployment_rate_2021, unemployment_rate_2022)
        st.write(msg)

    # Create operation US cities
    st.subheader("Insert US Cities Data")
    city_id_counties = st.text_input("City Id")
    fipscode_cities = st.selectbox("Select Fipscode", fips_code_list, key="fipscode_cities")
    city_name = st.text_input("City Name")

    if st.button("Add US County Record"):
        msg = query.insert_us_cities(city_id_counties, fipscode_cities, city_name)
        st.write(msg)

    # Create operation US counties
    st.subheader("Insert US Counties Data")
    fipscode = st.number_input("Fipscode")
    state_id = st.number_input("State ID")
    county_name = st.text_input("County Name")
    state_name = st.text_input("State Name")

    if st.button("Add US City Record"):
        msg = query.insert_us_counties(fipscode, state_id, county_name, state_name)
        st.write(msg)

elif menu == "Update":
    st.title("Update Operations")
    st.write("This section will contain update operations on the database.")

    city_id_options = query.get_all_city_ids()
    fips_code_list = query.get_all_fips_codes()

    # Update operation for population data
    st.subheader("Update Population Data")
    fips_code_list_population = query.get_all_fips_codes_in_population()
    fipscode_pop_update = st.selectbox("Select Fipscode to Update", fips_code_list_population, key="fips_code_pop_update")
    population_estimate_2020_update = st.number_input("Update population_estimate_2020", key="pop_2020_update")
    population_estimate_2021_update = st.number_input("Update population_estimate_2021", key="pop_2021_update")
    population_estimate_2022_update = st.number_input("Update population_estimate_2022", key="pop_2022_update")
    population_estimate_2023_update = st.number_input("Update population_estimate_2023", key="pop_2023_update")

    if st.button("Update Population Record"):
        if population_estimate_2020_update > 0 and population_estimate_2021_update > 0 and population_estimate_2022_update > 0 and population_estimate_2023_update > 0:
            query.update_population(fipscode_pop_update, population_estimate_2020_update, population_estimate_2021_update, population_estimate_2022_update, population_estimate_2023_update)
            st.write("Population record updated successfully!")
        else:
            st.warning("Please enter values greater than 0 for all fields.")

    # Update operation for crime data
    st.subheader("Update Crime Data")
    fips_code_list_crime = query.get_all_fips_codes_in_crime()
    fipscode_crime_update = st.selectbox("Select Fipscode to Update", fips_code_list_crime, key="fips_code_crime_update")
    crime_rate_per_100000_update = st.number_input("Update crime_rate_per_100000", key="crime_rate_update")
    crime_id_update = st.number_input("Update crime_id", key="crime_id_update")
    murder_update = st.number_input("Update murder", key="murder_update")
    rape_update = st.number_input("Update rape", key="rape_update")
    burglary_update = st.number_input("Update burglary", key="burglary_update")
    robbery_update = st.number_input("Update robbery", key="robbery_update")

    if st.button("Update Crime Record"):
        if crime_rate_per_100000_update > 0 and crime_id_update > 0 and murder_update > 0 and rape_update > 0 and burglary_update > 0 and robbery_update > 0:
            query.update_crime_table(fipscode_crime_update, crime_rate_per_100000_update, crime_id_update, murder_update, rape_update, burglary_update, robbery_update)
            st.write("Crime record updated successfully!")
        else:
            st.warning("Please enter values greater than 0 for all fields.")

    # Update operation for education data
    st.subheader("Update Education Data")
    fips_code_list_educatoin = query.get_all_fips_codes_in_education()
    fipscode_edu_update = st.selectbox("Select Fipscode to Update", fips_code_list_educatoin, key="fips_code_edu_update")
    pct_no_hs_degree_18_22_update = st.number_input("Update pct_no_hs_degree_18_22", key="edu_18_22_update")
    pct_no_hs_degree_08_12_update = st.number_input("Update pct_no_hs_degree_08_12", key="edu_08_12_update")
    pct_no_hs_degree_2000_update = st.number_input("Update pct_no_hs_degree_2000", key="edu_2000_update")

    if st.button("Update Education Record"):
        if pct_no_hs_degree_18_22_update > 0 and pct_no_hs_degree_08_12_update > 0 and pct_no_hs_degree_2000_update > 0:
            query.update_education(fipscode_edu_update, pct_no_hs_degree_18_22_update, pct_no_hs_degree_08_12_update, pct_no_hs_degree_2000_update)
            st.write("Education record updated successfully!")
        else:
            st.warning("Please enter values greater than 0 for all fields.")

    # Update operation for fire emergency services data
    st.subheader("Update Fire Emergency Services Data")
    city_id_list_fire = query.get_all_city_ids_in_fire_emergency_services()
    city_id_fire_update = st.selectbox("Select City ID to Update", city_id_list_fire, key="city_id_fire_update")
    fire_emergency_id_update = st.number_input("Update fire_emergency_id", key="fire_emergency_id_update")
    name_update = st.text_input("Update Name", key="name_update")
    address_update = st.text_input("Update Address", key="address_update")

    if st.button("Update Fire Emergency Service Record"):
        if fire_emergency_id_update > 0 and name_update and address_update:
            query.update_fire_emergency_services(city_id_fire_update, fire_emergency_id_update, name_update, address_update)
            st.write("Fire emergency service record updated successfully!")
        else:
            st.warning("Please enter valid values for all fields.")

    # Update operation for hospital data
    st.subheader("Update Hospital Data")
    hospital_id_update = st.number_input("Update hospital_id", key="hospital_id_update")
    city_id_list_hosp = query.get_all_city_ids_in_hospitals()
    city_id_update = st.selectbox("Select City ID to Update", city_id_list_hosp, key="city_id_hospital_update")
    name_update = st.text_input("Update Hospital Name", key="hospital_name_update")
    address_update = st.text_input("Update Hospital Address", key="hospital_address_update")
    status_update = st.text_input("Update Status", key="status_update")
    ownership_information_update = st.text_input("Update Ownership Information", key="ownership_information_update")

    if st.button("Update Hospital Record"):
        if hospital_id_update > 0 and name_update and address_update and status_update and ownership_information_update:
            query.update_hospitals(hospital_id_update, city_id_update, name_update, address_update, status_update, ownership_information_update)
            st.write("Hospital record updated successfully!")
        else:
            st.warning("Please enter valid values for all fields.")

    # Update operation for local law enforcement data
    st.subheader("Update Local Law Enforcement Data")
    city_id_list_law = query.get_all_city_ids_in_local_law_enforcement()
    city_id_law_update = st.selectbox("Select City ID to Update", city_id_list_law, key="city_id_law_update")
    law_enforcement_id_update = st.number_input("Update Law Enforcement ID", key="law_enforcement_id_update")
    name_update = st.text_input("Update Law Enforcement Name", key="law_enforcement_name_update")
    address_update = st.text_input("Update Law Enforcement Address", key="law_enforcement_address_update")
    type_of_law_enforcement_update = st.text_input("Update Type of Law Enforcement", key="type_of_law_enforcement_update")

    if st.button("Update Law Enforcement Record"):
        if law_enforcement_id_update > 0 and name_update and address_update and type_of_law_enforcement_update:
            query.update_local_law_enforcement(law_enforcement_id_update, name_update, city_id_law_update, address_update, type_of_law_enforcement_update)
            st.write("Law enforcement record updated successfully!")
        else:
            st.warning("Please enter valid values for all fields.")

    # Update operation for poverty data
    st.subheader("Update Poverty Data")
    fips_code_list_pov = query.get_all_fips_codes_in_poverty()
    fipscode_poverty_update = st.selectbox("Select Fipscode to Update", fips_code_list_pov, key="fips_code_poverty_update")
    poverty_percentage_update = st.number_input("Update Poverty Percentage", key="poverty_percentage_update")
    poverty_percentage_18_update = st.number_input("Update Poverty Percentage 18", key="poverty_percentage_18_update")
    poverty_percentage_5_17_update = st.number_input("Update Poverty Percentage 5-17", key="poverty_percentage_5_17_update")

    if st.button("Update Poverty Record"):
        if poverty_percentage_update > 0 and poverty_percentage_18_update > 0 and poverty_percentage_5_17_update > 0:
            query.update_poverty(fipscode_poverty_update, poverty_percentage_update, poverty_percentage_18_update, poverty_percentage_5_17_update)
            st.write("Poverty record updated successfully!")
        else:
            st.warning("Please enter values greater than 0 for all fields.")

    # Update operation for unemployment data
    st.subheader("Update Unemployment Data")
    fipscode_unemployment_update = st.selectbox("Select Fipscode to Update", fips_code_list, key="fips_code_unemployment_update")
    unemployment_rate_2020_update = st.number_input("Update Unemployment Rate 2020", key="unemployment_rate_2020_update")
    unemployment_rate_2021_update = st.number_input("Update Unemployment Rate 2021", key="unemployment_rate_2021_update")
    unemployment_rate_2022_update = st.number_input("Update Unemployment Rate 2022", key="unemployment_rate_2022_update")

    if st.button("Update Unemployment Record"):
        if unemployment_rate_2020_update > 0 and unemployment_rate_2021_update > 0 and unemployment_rate_2022_update > 0:
            query.update_unemployment(fipscode_unemployment_update, unemployment_rate_2020_update, unemployment_rate_2021_update, unemployment_rate_2022_update)
            st.write("Unemployment record updated successfully!")
        else:
            st.warning("Please enter values greater than 0 for all fields.")

    # Update operation for US cities data
    st.subheader("Update US Cities Data")
    city_id_counties_update = st.text_input("Update City Id", key="city_id_counties_update")
    fipscode_cities_update = st.selectbox("Select Fipscode to Update", fips_code_list, key="fipscode_cities_update")
    city_name_update = st.text_input("Update City Name", key="city_name_update")

    if st.button("Update US County Record"):
        if city_id_counties_update and city_name_update:
            query.update_us_cities(city_id_counties_update, fipscode_cities_update, city_name_update)
            st.write("US county record updated successfully!")
        else:
            st.warning("Please enter valid values for all fields.")

    # Update operation for US counties data
    st.subheader("Update US Counties Data")
    fipscode_update = st.number_input("Update Fipscode", key="fipscode_update")
    state_id_update = st.number_input("Update State ID", key="state_id_update")
    county_name_update = st.text_input("Update County Name", key="county_name_update")
    state_name_update = st.text_input("Update State Name", key="state_name_update")

    if st.button("Update US City Record"):
        if fipscode_update > 0 and state_id_update > 0 and county_name_update and state_name_update:
            query.update_us_counties(fipscode_update, state_id_update, county_name_update, state_name_update)
            st.write("US city record updated successfully!")
        else:
            st.warning("Please enter valid values for all fields.")