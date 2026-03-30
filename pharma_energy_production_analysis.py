# -*- coding: utf-8 -*-

"""
Created on Mon Mar 30 15:56:28 2026

@author: evg-chembio
"""

import requests
import numpy as np
import matplotlib.pyplot as plt

"""
# Dataset structure, Column names and Sector ids come from the CBS dataset structure
#"Key":"323200 ","Title":"21 Manufacture of pharmaceuticals",
#"Description":"Manufacture of basic pharmaceutical products and pharmaceutical preparations",
#"CategoryGroupID":6
"""

def download_cbs_table(table_id, chunk_size=10000):
    """
    Downloads ALL rows from a CBS dataset using the ODataFeed endpoint.
    Returns a dictionary with:
      - metadata
      - data (list of rows)
    """

    # Metadata comes from ODataApi (JSON by default)
    metadata_url = f"https://opendata.cbs.nl/ODataApi/OData/{table_id}"
    metadata = requests.get(metadata_url).json()

    # Data must come from ODataFeed to support $skip
    base_url = f"https://opendata.cbs.nl/ODataFeed/OData/{table_id}/TypedDataSet"

    all_rows = []
    skip = 0

    while True:
        url = (
            f"{base_url}"
            f"?$top={chunk_size}"
            f"&$skip={skip}"
            f"&$format=json"
        )

        response = requests.get(url)
        try:
            data = response.json()
        except Exception:
            print("Non‑JSON response received:")
            print(response.text[:500])
            raise

        rows = data.get("value", [])
        if not rows:
            break

        all_rows.extend(rows)
        skip += chunk_size

    return {"metadata": metadata, "data": all_rows}

def extract_pharma_rd(data_dict,table_id):
    """
    Extracts R&D expenditure for the pharmaceutical industry over time
    from CBS dataset.

    Returns a dictionary:
        { year: expenditure }
    """
    rows = data_dict["data"]

    output_dict = {}

    for row in rows:
        
        # Column names come from the CBS dataset structure
        if table_id == '85806ENG': # For production data
            
            sector = row.get("SectorBranchesSIC2008")
            year = row.get("Periods")
            production = row.get("Production_1")
    
            # Keep only pharmaceutical manufacturing (323200), whole year (JJ00) and 2011-2024 data
            if sector == "323200" and year[4:] == 'JJ00' and int(year[:4])>2010 and int(year[:4])<2025:
                output_dict[int(year[:4])] = production
        
        elif table_id == '83989ENG': # For energy consumption data
            sector = row.get("Sectors")
            year = row.get("Periods")
            energy = row.get("TotalEnergyConsumption_7")

            # Keep only pharmaceutical manufacturing (323200), full data and not repeated from the table
            # and 2011-2024 data
            if sector == "323200 " and int(year[:4]) not in output_dict.keys() and int(year[:4])>2010:
                output_dict[int(year[:4])] = energy

    return output_dict


if __name__ == "__main__":
        
    production_id = '85806ENG' #Industry; production and sales, changes and index, 2021=100
    energy_id = '83989ENG' #Energy balance sheet; supply and consumption, sector

    # Step 1: Download datasets
    print('Downloading Production by sector Dataset...')
    cbs_data_production = download_cbs_table(production_id)
    print('Completed.\n')
    print('Downloading Energy consumption by sector Dataset...')
    cbs_data_energy = download_cbs_table(energy_id)
    print('Completed.\n')

    # Step 2: Extract pharma R&D expenditure over time
    production_time_dict = extract_pharma_rd(cbs_data_production,production_id)
    energy_time_dict = extract_pharma_rd(cbs_data_energy,energy_id)

    #Step 3: Data normalization to a base value (2011=100)
    base_value_prod = production_time_dict[2011]
    base_value_energy = energy_time_dict[2011]
    
    years = []
    
    for key in production_time_dict.keys():
        years.append(key)
        production_time_dict[key] = production_time_dict[key] * 100 / base_value_prod
        energy_time_dict[key] = energy_time_dict[key] * 100 / base_value_energy

    #Step 4: Plot data
    years = np.array(years)                     # x-axis
    production = np.array([key for key in production_time_dict.values()]) #y1 axis
    energy = np.array([key for key in energy_time_dict.values()])   #y2 axis

    
    # -----------------------------
    # Trendlines (1st degree polynomial)
    # -----------------------------
    prod_coeffs = np.polyfit(years, production, 1)
    energy_coeffs = np.polyfit(years, energy, 1)
    
    prod_trend = np.poly1d(prod_coeffs)
    energy_trend = np.poly1d(energy_coeffs)
    
    # -----------------------------
    # Print equations
    # -----------------------------
    print("Production trendline: y = {:.4f}x + {:.4f}".format(prod_coeffs[0], prod_coeffs[1]))
    print("Energy trendline:     y = {:.4f}x + {:.4f}".format(energy_coeffs[0], energy_coeffs[1]))
    
    # -----------------------------
    # Plot
    # -----------------------------
    plt.figure(figsize=(10,6))
    
    # Data points
    plt.scatter(years, production, color='blue', label='Production (2011 = 100)')
    plt.scatter(years, energy, color='red', label='Energy consumption (2011 = 100)')
    
    # Trendlines
    plt.plot(years, prod_trend(years), color='blue', linestyle='--', label='Production trendline')
    plt.plot(years, energy_trend(years), color='red', linestyle='--', label='Energy consumption trendline')
    
    # Labels and title
    plt.title("Normalized Production and Energy consumption in the \'Manufacture of pharmaceuticals\' sector\nover recent years in the Netherlands")
    plt.xlabel("Year")
    plt.ylabel("Normalized value")
    
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()