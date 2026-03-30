# Dutch-pharma-energy-production
Analysis of Dutch pharmaceuticals production vs energy consumption (2011–2024). Includes data download, preprocessing, trend analysis, and visualization.

Project Summary

Question and insight

This project asks whether production growth in the Dutch pharmaceuticals manufacturing sector 
has outpaced energy consumption between 2011 and 2024. 
Using CBS open data for sector production and sector energy consumption, the analysis normalizes both series 
to a 2011 = 100 baseline and plots trends. The visual and descriptive insight is that 
production rises substantially while energy consumption increases only slightly, 
implying a decline in energy intensity at the aggregate level and suggesting that 
process intensification, automation, and PAT adoption can further improve efficiency.

Requirements and Setup
Environment
- Python 3.9 or later is recommended.
- Create an isolated environment before installing dependencies.


requests>=2.25.0
numpy>=1.21.0
matplotlib>=3.4.0



Running the script
Run
python pharma_energy_production_analysis.py


What the script does
- Downloads two CBS tables using the CBS OData endpoints.
- Extracts rows (Production and Energy Consumption) for the pharmaceuticals sector (SIC code 323200) for years 2011–2024.
- Normalizes both series to 2011 = 100.
- Fits linear trendlines and prints trendline equations.
- Displays a scatter plot with trendlines.
Notes
- The script uses plt.show() to display the figure.
To save the figure automatically, add plt.savefig("production_vs_energy.png", dpi=300) before plt.show().

Data Source and how it is accessed
Datasets used
- Production by industry: CBS table 85806ENG (Industry; production and sales, changes and index, 2021=100).
- Energy consumption by sector: CBS table 83989ENG (Energy balance sheet; supply and consumption, sector).
CBS portal
- Browse datasets at https://opendata.cbs.nl/.
- The script downloads metadata from the OData API endpoint and iterates the ODataFeed TypedDataSet endpoint 
to retrieve all rows in chunks.
OData endpoints used by the script
- Metadata endpoint pattern
https://opendata.cbs.nl/ODataApi/OData/{TABLE_ID}
- Data feed endpoint pattern with paging
https://opendata.cbs.nl/ODataFeed/OData/{TABLE_ID}/TypedDataSet?$top={chunk_size}&$skip={skip}&$format=json
How the script selects rows
- The script filters rows where the sector code equals 323200 (Manufacture of pharmaceuticals) 
and keeps full-year periods and years 2011–2024.

Reproducibility and implementation notes
Reproducibility checklist
- Ensure the production_id and energy_id variables match the CBS table IDs used in the script.
- Confirm network access to opendata.cbs.nl.
- If the CBS API changes field names, update the column keys used.

License and contact
License
This repository is provided under the MIT License. See LICENSE for details.
Contact
For questions or issues, open an issue in this repository or contact the developer 
via the GitHub profile associated with this repo.
