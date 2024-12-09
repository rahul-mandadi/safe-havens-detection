import sqlite3
import pandas as pd
import sys
import os
from tabulate import tabulate


class Queries:
    def __init__(self, conn):
        self.conn = conn
    
    # INSERT QUERIES
    def insert_education(self, fipscode, pct_no_hs_degree_18_22, pct_no_hs_degree_08_12, pct_no_hs_degree_2000):
        try:
            cursor = self.conn.cursor()

            cursor.execute("INSERT INTO education (fips_code, pct_no_hs_degree_18_22, pct_no_hs_degree_08_12, pct_no_hs_degree_2000) VALUES (?, ?, ?, ?)", 
                        (fipscode, pct_no_hs_degree_18_22, pct_no_hs_degree_08_12, pct_no_hs_degree_2000))

            self.conn.commit()
            cursor.close()
            return "Data Added successfully"
        except Exception as e:
            return f"Error while adding data: {e}"
        
    def insert_fire_emergency_services(self, city_id, fire_emergency_id, name, address):
        try:
            cursor = self.conn.cursor()

            cursor.execute("INSERT INTO fire_emergency_services (city_id, fire_emergency_id, name, address) VALUES (?, ?, ?, ?)", 
                           (city_id, fire_emergency_id, name, address))

            self.conn.commit()
            cursor.close()
            return "Data Added successfully"
        except Exception as e:
            return f"Error while adding data: {e}"
        
        
    def insert_hospital(self, hospital_id, city_id, name, address, status, ownership_information):
            try:
                cursor = self.conn.cursor()

                cursor.execute("INSERT INTO hospitals (hospital_id, city_id, name, address, status, ownership_information) VALUES (?, ?, ?, ?, ?, ?)", 
                               (hospital_id, city_id, name, address, status, ownership_information))

                self.conn.commit()
                cursor.close()
                return "Data Added successfully"
            except Exception as e:
                return f"Error while adding data: {e}"
        
    def insert_population(self, fipscode, population_estimate_2020, population_estimate_2021, population_estimate_2022, population_estimate_2023):
        cursor = self.conn.cursor()

        cursor.execute("INSERT INTO population (fips_code, population_estimate_2020, population_estimate_2021, population_estimate_2022, population_estimate_2023) VALUES (?, ?, ?, ?, ?)", (fipscode, population_estimate_2020, population_estimate_2021, population_estimate_2022, population_estimate_2023))

        self.conn.commit()
    
    def insert_crime(self, fipscode, crime_rate_per_100000, crime_id, murder, rape, robbery, burglary):
        try:
            cursor = self.conn.cursor()

            cursor.execute("INSERT INTO crime (fips_code, crime_rate_per_100000, crime_id, murder, rape, robbery, burglary) VALUES (?, ?, ?, ?, ?, ?, ?)", (fipscode, crime_rate_per_100000, crime_id, murder, rape, robbery, burglary))

            self.conn.commit()
            return "Data Added successfully"
        except Exception as e:
            return f"Error while adding data: {e}"
        

    def insert_local_law_enforcement(self, local_law_id, name, city_id, address, type_of_law_enforcement):
        try:
            cursor = self.conn.cursor()

            cursor.execute("INSERT INTO local_law_enforcement (local_law_id, name, city_id, address, type_of_law_enforcement) VALUES (?, ?, ?, ?, ?)", 
                               (local_law_id, name, city_id, address, type_of_law_enforcement))

            self.conn.commit()
            cursor.close()
            return "Data Added successfully"
        except Exception as e:
            return f"Error while adding data: {e}"

    def insert_poverty(self, fipscode, poverty_percentage, poverty_percentage_under_18, poverty_percentage_5_17):
        try:
            cursor = self.conn.cursor()

            cursor.execute("INSERT INTO poverty (fips_code, poverty_percentage, poverty_percentage_under_18, poverty_percentage_5_17) VALUES (?, ?, ?, ?)", 
                           (fipscode, poverty_percentage, poverty_percentage_under_18, poverty_percentage_5_17))

            self.conn.commit()
            cursor.close()
            return "Data Added successfully"
        except Exception as e:
            return f"Error while adding data: {e}"

    def insert_unemployment(self, fipscode, unemployment_rate_2020, unemployment_rate_2021, unemployment_rate_2022):
        try:
            cursor = self.conn.cursor()

            cursor.execute("INSERT INTO unemployment (fips_code, unemployment_rate_2020, unemployment_rate_2021, unemployment_rate_2022) VALUES (?, ?, ?, ?)", 
                           (fipscode, unemployment_rate_2020, unemployment_rate_2021, unemployment_rate_2022))

            self.conn.commit()
            cursor.close()
            return "Data Added successfully"
        except Exception as e:
            return f"Error while adding data: {e}"

    def insert_us_cities(self, city_id, fipscode, city_name):
        try:
            cursor = self.conn.cursor()

            cursor.execute("INSERT INTO us_cities (city_id, fips_code, city_name) VALUES (?, ?, ?)", 
                           (city_id, fipscode, city_name))

            self.conn.commit()
            cursor.close()
            return "Data Added successfully"
        except Exception as e:
            return f"Error while adding data: {e}"

    def insert_us_counties(self, fipscode, state_id, county_name, state_name):
        try:
            cursor = self.conn.cursor()

            cursor.execute("INSERT INTO us_counties (fips_code, state_id, county_name, state_name) VALUES (?, ?, ?, ?)", 
                           (fipscode, state_id, county_name, state_name))

            self.conn.commit()
            cursor.close()
            return "Data Added successfully"
        except Exception as e:
            return f"Error while adding data: {e}"
    def query_data(self):
        cursor = self.conn.cursor()

        # Check if the table contains data
        cursor.execute("SELECT COUNT(*) FROM hospitals")
        count = cursor.fetchone()[0]
        print(f"Rows in 'us_counties': {count}")

    # UPDATE QUERIES
    def update_crime_table(self, fips_code, crime_rate_per_100000, crime_id, murder, rape, robbery, burglary):
        cursor = self.conn.cursor()
        query = '''
            UPDATE crime
            SET crime_rate_per_100000 = ?, crime_id = ?, murder = ?, rape = ?, robbery = ?, burglary = ?
            WHERE fips_code = ?;
        '''
        cursor.execute(query, (crime_rate_per_100000, crime_id, murder, rape, robbery, burglary, fips_code))
        self.conn.commit()
        cursor.close()

    def update_education(self, fips_code, pct_no_hs_degree_18_22, pct_no_hs_degree_08_12, pct_no_hs_degree_2000):
        cursor = self.conn.cursor()
        query = '''
            UPDATE education
            SET pct_no_hs_degree_18_22 = ?, pct_no_hs_degree_08_12 = ?, pct_no_hs_degree_2000 = ?
            WHERE fips_code = ?;
        '''
        cursor.execute(query, (pct_no_hs_degree_18_22, pct_no_hs_degree_08_12, pct_no_hs_degree_2000, fips_code))
        self.conn.commit()
        cursor.close()

    def update_fire_emergency_services(self, city_id, fire_emergency_id, name, address):
        cursor = self.conn.cursor()
        query = '''
            UPDATE fire_emergency_services
            SET name = ?, address = ?
            WHERE city_id = ? AND fire_emergency_id = ?;
        '''
        cursor.execute(query, (name, address, city_id, fire_emergency_id))
        self.conn.commit()
        cursor.close()

    def update_food_banks(self, city_id, food_banks_id, food_bank_name, address, status):
        cursor = self.conn.cursor()
        query = '''
            UPDATE food_banks
            SET food_bank_name = ?, address = ?, status = ?
            WHERE city_id = ? AND food_banks_id = ?;
        '''
        cursor.execute(query, (food_bank_name, address, status, city_id, food_banks_id))
        self.conn.commit()
        cursor.close()

    def update_hospitals(self, hospital_id, city_id, name, address, status, ownership_information):
        cursor = self.conn.cursor()
        query = '''
            UPDATE hospitals
            SET city_id = ?, name = ?, address = ?, status = ?, ownership_information = ?
            WHERE hospital_id = ?;
        '''
        cursor.execute(query, (city_id, name, address, status, ownership_information, hospital_id))
        self.conn.commit()
        cursor.close()

    def update_local_law_enforcement(self, local_law_id, name, city_id, address, type_of_law_enforcement):
        cursor = self.conn.cursor()
        query = '''
            UPDATE local_law_enforcement
            SET name = ?, city_id = ?, address = ?, type_of_law_enforcement = ?
            WHERE local_law_id = ?;
        '''
        cursor.execute(query, (name, city_id, address, type_of_law_enforcement, local_law_id))
        self.conn.commit()
        cursor.close()

    def update_population(self, fips_code, population_estimate_2020, population_estimate_2021, population_estimate_2022, population_estimate_2023):
        cursor = self.conn.cursor()
        query = '''
            UPDATE population
            SET population_estimate_2020 = ?, population_estimate_2021 = ?, population_estimate_2022 = ?, population_estimate_2023 = ?
            WHERE fips_code = ?;
        '''
        cursor.execute(query, (population_estimate_2020, population_estimate_2021, population_estimate_2022, population_estimate_2023, fips_code))
        self.conn.commit()
        cursor.close()

    def update_poverty(self, fips_code, poverty_percentage, poverty_percentage_under_18, poverty_percentage_5_17):
        cursor = self.conn.cursor()
        query = '''
            UPDATE poverty
            SET poverty_percentage = ?, poverty_percentage_under_18 = ?, poverty_percentage_5_17 = ?
            WHERE fips_code = ?;
        '''
        cursor.execute(query, (poverty_percentage, poverty_percentage_under_18, poverty_percentage_5_17, fips_code))
        self.conn.commit()
        cursor.close()

    def update_unemployment(self, fips_code, unemployment_rate_2020, unemployment_rate_2021, unemployment_rate_2022):
        cursor = self.conn.cursor()
        query = '''
            UPDATE unemployment
            SET unemployment_rate_2020 = ?, unemployment_rate_2021 = ?, unemployment_rate_2022 = ?
            WHERE fips_code = ?;
        '''
        cursor.execute(query, (unemployment_rate_2020, unemployment_rate_2021, unemployment_rate_2022, fips_code))
        self.conn.commit()
        cursor.close()

    def update_us_cities(self, city_id, fips_code, city_name):
        cursor = self.conn.cursor()
        query = '''
            UPDATE us_cities
            SET fips_code = ?, city_name = ?
            WHERE city_id = ?;
        '''
        cursor.execute(query, (fips_code, city_name, city_id))
        self.conn.commit()
        cursor.close()

    def update_us_counties(self, fips_code, state_id, county_name, state_name):
        cursor = self.conn.cursor()
        query = '''
            UPDATE us_counties
            SET state_id = ?, county_name = ?, state_name = ?
            WHERE fips_code = ?;
        '''
        cursor.execute(query, (state_id, county_name, state_name, fips_code))
        self.conn.commit()
        cursor.close()

    # INSERT DATA INTO ALL TABLES
    def insert_data(self):
        self.conn.execute("PRAGMA foreign_keys = ON;")

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS us_counties(
            fips_code INTEGER PRIMARY KEY,
            state_id TEXT,
            county_name TEXT,
            state_name TEXT
        );
        ''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS us_cities(
            city_id TEXT PRIMARY KEY,
            fips_code INTEGER,
            city_name TEXT,
            FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        ''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS education(
            fips_code INTEGER,
            pct_no_hs_degree_18_22 FLOAT,
            pct_no_hs_degree_08_12 FLOAT,
            pct_no_hs_degree_2000 FLOAT,
            FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        ''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS population(
            fips_code INTEGER,
            population_estimate_2020 INTEGER,
            population_estimate_2021 INTEGER,
            population_estimate_2022 INTEGER,
            population_estimate_2023 INTEGER,
            FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        ''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS poverty(
            fips_code INTEGER,
            poverty_percentage FLOAT,
            poverty_percentage_under_18 FLOAT,
            poverty_percentage_5_17 FLOAT,
            FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        ''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS unemployment(
            fips_code INTEGER,
            unemployment_rate_2020 FLOAT,
            unemployment_rate_2021 FLOAT,
            unemployment_rate_2022 FLOAT,
            FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        ''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS food_banks(
            city_id TEXT,
            food_banks_id INTEGER PRIMARY KEY,
            food_bank_name TEXT,
            address TEXT,
            status TEXT,
            FOREIGN KEY (city_id) REFERENCES us_cities(city_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        ''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS fire_emergency_services(
            city_id TEXT,
            fire_emergency_id INTEGER PRIMARY KEY,
            name TEXT,
            address TEXT,
            FOREIGN KEY (city_id) REFERENCES us_cities(city_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        ''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS hospitals(
            hospital_id INTEGER PRIMARY KEY,
            city_id TEXT,
            name TEXT,
            address TEXT,
            status TEXT,
            ownership_information TEXT,
            FOREIGN KEY (city_id) REFERENCES us_cities(city_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        ''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS local_law_enforcement(
            local_law_id INTEGER PRIMARY KEY,
            name VARCHAR(50),
            city_id TEXT,
            address TEXT,
            type_of_law_enforcement TEXT,
            FOREIGN KEY (city_id) REFERENCES us_cities(city_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        ''')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS crime(
            fips_code INTEGER,
            crime_rate_per_100000 FLOAT,
            crime_id INTEGER PRIMARY KEY,
            murder INTEGER,
            rape INTEGER,
            robbery INTEGER,
            burglary INTEGER,
            FOREIGN KEY (fips_code) REFERENCES us_counties(fips_code)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        ''')

        df_counties = pd.read_csv('../Cleaned Data/cleaned_us_counties.csv')
        df_counties.to_sql('us_counties', self.conn, if_exists='append', index=False)

        df_cities = pd.read_csv('../Cleaned Data/cleaned_us_cities.csv')
        df_cities.to_sql('us_cities', self.conn, if_exists='append', index=False)

        df_education = pd.read_csv('../Cleaned Data/cleaned_education.csv')
        df_education.to_sql('education', self.conn, if_exists='append', index=False)

        df_population = pd.read_csv('../Cleaned Data/cleaned_population.csv')
        df_population.to_sql('population', self.conn, if_exists='append', index=False)

        df_poverty = pd.read_csv('../Cleaned Data/cleaned_poverty.csv')
        df_poverty.to_sql('poverty', self.conn, if_exists='append', index=False)

        df_unemployment = pd.read_csv('../Cleaned Data/cleaned_unemployment.csv')
        df_unemployment.to_sql('unemployment', self.conn, if_exists='append', index=False)

        df_food_banks = pd.read_csv('../Cleaned Data/cleaned_food_banks.csv')
        df_food_banks.to_sql('food_banks', self.conn, if_exists='append', index=False)

        df_fire_emergency = pd.read_csv('../Cleaned Data/cleaned_fire_emergency_services.csv')
        df_fire_emergency.to_sql('fire_emergency_services', self.conn, if_exists='append', index=False)

        df_hospitals = pd.read_csv('../Cleaned Data/cleaned_hospitals.csv')
        df_hospitals.to_sql('hospitals', self.conn, if_exists='append', index=False)

        df_law_enforcement = pd.read_csv('../Cleaned Data/cleaned_law_enforcement.csv')
        df_law_enforcement.to_sql('local_law_enforcement', self.conn, if_exists='append', index=False)

        df_crime = pd.read_csv('../Cleaned Data/cleaned_crime.csv')
        df_crime.to_sql('crime', self.conn, if_exists='append', index=False)
    
    # DELETE ALL DATA FROM ALL TABLES
    def delete_data(self):
        cursor = self.conn.cursor()

        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        cursor.execute("BEGIN TRANSACTION;")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        
        for row in cursor.fetchall():
            table_name = row[0]
            print(f"Dropping table: {table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

        cursor.execute("COMMIT;")
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        self.conn.commit()

    # QUERY FUNCTIONS
    def query_by_fips_code(self, fips_code, table_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM " + table_name + " WHERE fips_code = " + str(fips_code))
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return tabulate(rows, headers=columns, tablefmt='pretty'), df
    
    def query_by_city(self, city_id, table_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM " + table_name + " WHERE city_id = " + str(city_id))
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return tabulate(rows, headers=columns, tablefmt='pretty'), df
    
    def get_highest_top_n_crime_rate(self, n):
        cursor = self.conn.cursor()
        query = f"""
                SELECT 
                    c.county_name,
                    c.state_name,
                    cr.crime_rate_per_100000
                FROM 
                    us_counties AS c
                JOIN 
                    crime AS cr ON c.fips_code = cr.fips_code
                ORDER BY 
                    cr.crime_rate_per_100000 DESC
                LIMIT {n}
            """

        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return tabulate(rows, headers=columns, tablefmt='pretty'), df
    
    def get_highest_top_n_poverty(self, n):
        cursor = self.conn.cursor()
        
        query = f"""
            SELECT 
                c.county_name,
                c.state_name,
                p.poverty_percentage
            FROM 
                us_counties AS c
            JOIN 
                poverty AS p ON c.fips_code = p.fips_code
            ORDER BY 
                p.poverty_percentage DESC
            LIMIT {n}; """
        
        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return tabulate(rows, headers=columns, tablefmt='pretty'), df
    
    def get_highest_top_n_unemployment(self, n):
        cursor = self.conn.cursor()
        
        query = f"""
            SELECT 
                c.county_name,
                c.state_name,
                u.unemployment_rate_2022
            FROM 
                us_counties AS c
            JOIN 
                unemployment AS u ON c.fips_code = u.fips_code
            ORDER BY 
                u.unemployment_rate_2022 DESC
            LIMIT {n}; 
            """
        
        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return tabulate(rows, headers=columns, tablefmt='pretty'), df
    
    def get_food_banks_with_percent_poverty(self, percent):
        cursor = self.conn.cursor()

        query = f"""
            SELECT 
                c.county_name,
                c.state_name,
                fb.food_bank_name,
                fb.address
            FROM 
                us_counties AS c
            JOIN 
                poverty AS p ON c.fips_code = p.fips_code
            JOIN 
                us_cities AS ci ON c.fips_code = ci.fips_code
            JOIN 
                food_banks AS fb ON ci.city_id = fb.city_id
            WHERE 
                p.poverty_percentage > {percent}
            ORDER BY 
                p.poverty_percentage DESC;
            """
        
        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return tabulate(rows, headers=columns, tablefmt='pretty'), df
    
    def get_hospital_with_percent_crime_rate(self, crime_rate):
        cursor = self.conn.cursor()

        query = f"""
            SELECT 
                c.county_name,
                c.state_name,
                h.name AS hospital_name,
                h.address AS hospital_address,
                cr.crime_rate_per_100000
            FROM 
                us_counties AS c
            JOIN 
                crime AS cr ON c.fips_code = cr.fips_code
            JOIN 
                us_cities AS ci ON c.fips_code = ci.fips_code
            JOIN 
                hospitals AS h ON ci.city_id = h.city_id
            WHERE 
                cr.crime_rate_per_100000 > {crime_rate}
            ORDER BY 
                cr.crime_rate_per_100000 DESC;
            """
        
        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return tabulate(rows, headers=columns, tablefmt='pretty'), df
    
    def get_counties_with_highest_pop_growth(self, n, year1, year2):
        cursor = self.conn.cursor()

        query = f"""
            SELECT 
                c.county_name,
                c.state_name,
                p.population_estimate_{year1},
                p.population_estimate_{year2},
                (p.population_estimate_{year2} - p.population_estimate_{year1}) AS growth,
                ((p.population_estimate_{year2} - p.population_estimate_{year1}) * 100.0 / p.population_estimate_{year1}) AS growth_percentage
            FROM 
                us_counties AS c
            JOIN 
                population AS p ON c.fips_code = p.fips_code
            WHERE 
                p.population_estimate_{year1} > 0  -- Avoid division by zero
            ORDER BY 
                growth_percentage DESC
            LIMIT {n};
            """
        
        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return tabulate(rows, headers=columns, tablefmt='pretty'), df
    
    def get_lowest_top_n_education(self, n):
        cursor = self.conn.cursor()
        
        query = f"""
           SELECT 
                c.county_name,
                c.state_name,
                e.pct_no_hs_degree_2000
            FROM 
                us_counties AS c
            JOIN 
                education AS e ON c.fips_code = e.fips_code
            ORDER BY 
                e.pct_no_hs_degree_2000 DESC
            LIMIT {n}; 
            """
        
        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return tabulate(rows, headers=columns, tablefmt='pretty'), df
    
    def get_all(self, edu, unemp, pov, crime):
        cursor = self.conn.cursor()
        
        query = f"""
           SELECT 
                c.county_name,
                c.state_name,
                e.pct_no_hs_degree_2000 AS education_level,
                u.unemployment_rate_2022 AS unemployment_rate,
                p.poverty_percentage,
                cr.crime_rate_per_100000
            FROM 
                us_counties AS c
            JOIN 
                education AS e ON c.fips_code = e.fips_code
            JOIN 
                unemployment AS u ON c.fips_code = u.fips_code
            JOIN 
                poverty AS p ON c.fips_code = p.fips_code
            JOIN 
                crime AS cr ON c.fips_code = cr.fips_code
            WHERE 
                e.pct_no_hs_degree_2000 > {edu} 
                AND u.unemployment_rate_2022 > {unemp}   
                AND p.poverty_percentage > {pov}   
                AND cr.crime_rate_per_100000 > {crime}  
            ORDER BY 
                e.pct_no_hs_degree_2000 DESC, u.unemployment_rate_2022 DESC;
        """
                    
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return tabulate(rows, headers=columns, tablefmt='pretty'), df
    
    def update_pop(self, fips_code, population_estimate_2020, population_estimate_2021, population_estimate_2022, population_estimate_2023):
        cursor = self.conn.cursor()
    
        query = f'''
            UPDATE population
            SET 
                population_estimate_2020 = {population_estimate_2020},
                population_estimate_2021 = {population_estimate_2021},
                population_estimate_2022 = {population_estimate_2022},
                population_estimate_2023 = {population_estimate_2023}
            WHERE fips_code = {fips_code};
        '''
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def update_crime(self, fips_code, crime_rate_per_100000):
        cursor = self.conn.cursor()
    
        query = f'''
            UPDATE crime
            SET crime_rate_per_100000 = {crime_rate_per_100000}, murder = 2, burglary = 25
            WHERE fips_code = {fips_code};
        '''
        cursor.execute(query)
        self.conn.commit()
        cursor.close()
    
    def update_crime(self, fips_code, crime_rate_per_100000):
        cursor = self.conn.cursor()
    
        query = f'''
            UPDATE crime
            SET crime_rate_per_100000 = {crime_rate_per_100000}, murder = 2, burglary = 25
            WHERE fips_code = {fips_code};
        '''
        cursor.execute(query)
        self.conn.commit()
        cursor.close()
    
    def update_education(self, fips_code, pct_no_hs_degree_18_22, pct_no_hs_degree_08_12):
        cursor = self.conn.cursor()
    
        query = f'''
            UPDATE education
            SET pct_no_hs_degree_18_22 = {pct_no_hs_degree_18_22}, pct_no_hs_degree_08_12 = {pct_no_hs_degree_08_12}
            WHERE fips_code = {fips_code};
        '''
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def update_food_banks(self, fips_code, status):
        cursor = self.conn.cursor()
    
        query = f'''
            UPDATE food_banks
            SET status = {status},
            WHERE food_banks_id = {fips_code};
        '''
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def update_poverty(self, fips_code, poverty_percentage):
        cursor = self.conn.cursor()
    
        query = f'''
            UPDATE poverty
            SET poverty_percentage = {poverty_percentage}
            WHERE fips_code ={fips_code};
        '''
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def update_hospitals(self, hospital_id, address):
        cursor = self.conn.cursor()
    
        query = f'''
            UPDATE hospitals
            SET address = {address},
            WHERE hospital_id = {hospital_id};
        '''

        cursor.execute(query)
        self.conn.commit()
        cursor.close()
    
    def update_fire_emergency_services(self, fire_emergency_id, name):
        cursor = self.conn.cursor()
    
        query = f'''
            UPDATE fire_emergency_services
            SET name = {name},
            WHERE fire_emergency_id = {fire_emergency_id};
        '''
        
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def get_safety_data(self):
        cursor = self.conn.cursor()

        query = """
            SELECT 
                c.fips_code,
                c.county_name,
                c.state_name,
                cr.crime_rate_per_100000,
                p.poverty_percentage,
                e.pct_no_hs_degree_18_22,
                u.unemployment_rate_2022,
                (SELECT COUNT(*) 
                FROM hospitals h 
                JOIN us_cities ci ON h.city_id = ci.city_id 
                WHERE ci.fips_code = c.fips_code) AS hospital_count,
                (SELECT COUNT(*) 
                FROM fire_emergency_services f 
                JOIN us_cities ci ON f.city_id = ci.city_id 
                WHERE ci.fips_code = c.fips_code) AS fire_service_count
            FROM 
                us_counties AS c
            JOIN 
                crime AS cr ON c.fips_code = cr.fips_code
            JOIN 
                poverty AS p ON c.fips_code = p.fips_code
            JOIN 
                education AS e ON c.fips_code = e.fips_code
            JOIN 
                unemployment AS u ON c.fips_code = u.fips_code;
        """

        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        df = pd.DataFrame(rows, columns=columns)

        df['crime_norm'] = df['crime_rate_per_100000'] / df['crime_rate_per_100000'].max()
        df['poverty_norm'] = df['poverty_percentage'] / df['poverty_percentage'].max()
        df['education_norm'] = df['pct_no_hs_degree_18_22'] / df['pct_no_hs_degree_18_22'].max()
        df['unemployment_norm'] = df['unemployment_rate_2022'] / df['unemployment_rate_2022'].max()
        df['services_norm'] = 1 - ((df['hospital_count'] + df['fire_service_count']) / (df['hospital_count'] + df['fire_service_count']).max())

        weights = {
            'crime_norm': 0.4,
            'poverty_norm': 0.3,
            'education_norm': 0.1,
            'unemployment_norm': 0.1,
            'services_norm': 0.1
        }
        df['safety_index'] = (
            df['crime_norm'] * weights['crime_norm'] +
            df['poverty_norm'] * weights['poverty_norm'] +
            df['education_norm'] * weights['education_norm'] +
            df['unemployment_norm'] * weights['unemployment_norm'] +
            df['services_norm'] * weights['services_norm']
        )

        df = df.sort_values(by='safety_index')

        return df
    
    def get_crime_types_distribution(self):
        cursor = self.conn.cursor()

        query = """
            SELECT
                SUM(murder) AS total_murder,
                SUM(rape) AS total_rape,
                SUM(robbery) AS total_robbery,
                SUM(burglary) AS total_burglary
            FROM
                crime;
        """
        cursor.execute(query)
        row = cursor.fetchone()
        return {
            'total_murder': row[0],
            'total_rape': row[1],
            'total_robbery': row[2],
            'total_burglary': row[3]
        }


    def get_top_crime_counties(self, crime_type, top_n=10):
        cursor = self.conn.cursor()
        query = f"""
            SELECT 
                c.county_name,
                c.state_name,
                SUM(cr.{crime_type}) AS total_count
            FROM 
                us_counties AS c
            JOIN 
                crime AS cr ON c.fips_code = cr.fips_code
            GROUP BY 
                c.county_name, c.state_name
            ORDER BY 
                total_count DESC
            LIMIT {top_n};
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        return pd.DataFrame(rows, columns=columns)


    def get_law_enforcement_by_county(self, crime_threshold):
        cursor = self.conn.cursor()
        query = """
            SELECT 
                uc.fips_code,
                c.county_name,
                c.state_name,
                lle.type_of_law_enforcement AS law_enforcement_type,
                COUNT(*) AS law_enforcement_count
            FROM 
                local_law_enforcement AS lle
            JOIN 
                us_cities AS uc ON lle.city_id = uc.city_id
            JOIN 
                crime AS cr ON uc.fips_code = cr.fips_code
            JOIN 
                us_counties AS c ON cr.fips_code = c.fips_code
            WHERE 
                cr.crime_rate_per_100000 > ?
            GROUP BY 
                uc.fips_code, c.county_name, c.state_name, lle.type_of_law_enforcement
            ORDER BY 
                c.county_name, law_enforcement_count DESC;
        """
        cursor.execute(query, (crime_threshold,))
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    
    def get_all_fips_codes_in_education(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT fips_code FROM education")
        rows = cursor.fetchall()
        fips_codes = [row[0] for row in rows]
        cursor.close()
        return fips_codes

    def get_all_fips_codes_in_population(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT fips_code FROM population")
        rows = cursor.fetchall()
        fips_codes = [row[0] for row in rows]
        cursor.close()
        return fips_codes

    def get_all_fips_codes_in_poverty(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT fips_code FROM poverty")
        rows = cursor.fetchall()
        fips_codes = [row[0] for row in rows]
        cursor.close()
        return fips_codes

    def get_all_fips_codes_in_unemployment(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT fips_code FROM unemployment")
        rows = cursor.fetchall()
        fips_codes = [row[0] for row in rows]
        cursor.close()
        return fips_codes

    def get_all_fips_codes_in_crime(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT fips_code FROM crime")
        rows = cursor.fetchall()
        fips_codes = [row[0] for row in rows]
        cursor.close()
        return fips_codes

    def get_all_city_ids_in_food_banks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT city_id FROM food_banks")
        rows = cursor.fetchall()
        city_ids = [row[0] for row in rows]
        cursor.close()
        return city_ids

    def get_all_city_ids_in_fire_emergency_services(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT city_id FROM fire_emergency_services")
        rows = cursor.fetchall()
        city_ids = [row[0] for row in rows]
        cursor.close()
        return city_ids

    def get_all_city_ids_in_hospitals(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT city_id FROM hospitals")
        rows = cursor.fetchall()
        city_ids = [row[0] for row in rows]
        cursor.close()
        return city_ids

    def get_all_city_ids_in_local_law_enforcement(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT city_id FROM local_law_enforcement")
        rows = cursor.fetchall()
        city_ids = [row[0] for row in rows]
        cursor.close()
        return city_ids

    def get_all_city_ids(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT city_id FROM us_cities")
        rows = cursor.fetchall()
        city_ids = [row[0] for row in rows]
        cursor.close()
        return city_ids
    
    def get_all_fips_codes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT fips_code FROM us_counties")
        rows = cursor.fetchall()
        fips_codes = [row[0] for row in rows]
        cursor.close()
        return fips_codes