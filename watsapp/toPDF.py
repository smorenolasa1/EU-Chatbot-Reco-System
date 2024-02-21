from fpdf import FPDF

def create_pdf_from_string(input_string, output_filename="output.pdf"):
    """
    Creates a PDF file from the given input string.

    Args:
        input_string (str): The Python string to be included in the PDF.
        output_filename (str, optional): The desired filename for the output PDF. Defaults to "output.pdf".
    """
    # Create an instance of the FPDF class
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set the font (you can choose other fonts too)
    pdf.set_font("Times", size=11)

    # Add the input string to the PDF
    pdf.multi_cell(0, 10, txt=input_string, align="L")

    # Save the PDF
    pdf.output(output_filename)

    print(f"PDF created successfully! Saved as {output_filename}")

# Example usage
farm_information_template = """
Farm Information:

Farm's name: {farm_name}
Owner/Manager's name: {owner_name}
Location: {location}
Total farm area (hectares): {farm_area}
Number of dairy cows: {num_cows}
Type of dairy production system: {production_system}

Section 1:
Enteric fermentation:
Total methane emissions (kg CO2-eq): {methane_emissions}
Calculation method/model used: {methane_calculation}

Section 2:
Manure management:
Methane emissions from manure management: {manure_methane_emissions}
Nitrous oxide emissions from manure management: {manure_nitrous_emissions}
Manure management system: {manure_system}
Calculation method/model used: {manure_calculation}

Section 3:
Feed production:
CO2 emissions from feed production: {feed_co2_emissions}
Feed type: {feed_type}
Quantity (tons): {feed_quantity}
Source: {feed_source}
Calculation method/model used: {feed_calculation}

Section 4:
Energy use on the farm:
Electricity consumption (kWh): {electricity_consumption}
Fuel consumption (L/m3): {fuel_consumption}
Fuel type: {fuel_type}
Total CO2 emissions from energy use: {energy_co2_emissions}
Calculation method/model used: {energy_calculation}

Section 5:
Land use, land-use change, and forestry (LULUCF):
Changes in land use: {land_use_changes}
CO2 sequestration or emissions due to LULUCF: {lulucf_co2}
Description of land use change: {land_use_description}
Calculation method/model used: {lulucf_calculation}

Section 6:
Additional emissions and offsets:
Other GHG emissions: {other_emissions_source}, {other_emissions_quantity}
Carbon credits or offsets purchased: {carbon_credits_source}, {carbon_credits_quantity}

Summary of total GHG emissions:
Enteric fermentation: {enteric_fermentation_total}
Manure management: {manure_management_total}
Feed production: {feed_production_total}
Energy use on the farm: {energy_use_total}
LULUCF: {lulucf_total}
Other sources: {other_sources_total}

Declaration:
Statement of accuracy and truthfulness: [Signature]
Date: {declaration_date}
Compliance with EU greenhouse gas emissions reporting requirements for dairy farms: {eu_compliance}
"""

# Example variables
variables = {
    'farm_name': 'Example Farm',
    'owner_name': 'John Doe',
    'location': '123 Farm Road, Farmville, Country X',
    'farm_area': '100',
    'num_cows': '50',
    'production_system': 'Grazing',
    'methane_emissions': '1000',
    'methane_calculation': 'Method A',
    'manure_methane_emissions': '500',
    'manure_nitrous_emissions': '200',
    'manure_system': 'System B',
    'manure_calculation': 'Method C',
    'feed_co2_emissions': '300',
    'feed_type': 'Type X',
    'feed_quantity': '200',
    'feed_source': 'Own production',
    'feed_calculation': 'Method D',
    'electricity_consumption': '10000',
    'fuel_consumption': '5000',
    'fuel_type': 'Diesel',
    'energy_co2_emissions': '1500',
    'energy_calculation': 'Method E',
    'land_use_changes': 'Conversion of forest to pasture',
    'lulucf_co2': '-500',
    'land_use_description': 'Increase in pasture area',
    'lulucf_calculation': 'Method F',
    'other_emissions_source': 'Source A',
    'other_emissions_quantity': '200',
    'carbon_credits_source': 'Source B',
    'carbon_credits_quantity': '100',
    'enteric_fermentation_total': '1000',
    'manure_management_total': '700',
    'feed_production_total': '300',
    'energy_use_total': '1500',
    'lulucf_total': '-500',
    'other_sources_total': '100',
    'declaration_date': 'February 18, 2024',
    'eu_compliance': 'Yes'
}

# Generate the PDF
create_pdf_from_string(farm_information_template.format(**variables), "farm_information.pdf")