#Import neceassary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO


#Retrieve Data

def retrieve_fuelcheck_monthly_data():
    print("Retrieving NSW FuelCheck monthly data from Jan 2024 – Mar 2025")

    base_url = "https://data.nsw.gov.au/data/dataset/fuel-check"
    html_response = requests.get(base_url)
    soup = BeautifulSoup(html_response.text, "html.parser")

    allowed_extensions = ['.xlsx', '.xls', '.csv']
    long_months = ['january', 'february', 'march', 'april', 'may', 'june',
                   'july', 'august', 'september', 'october', 'november', 'december']
    short_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                    'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    target_patterns = [m + "2024" for m in long_months] + [m + "2024" for m in short_months]
    target_patterns += [m + "2025" for m in long_months[:3]] + [m + "2025" for m in short_months[:3]]
    target_patterns += [m + "25" for m in long_months[:3]] + [m + "25" for m in short_months[:3]]

    download_links = []
    for tag in soup.find_all("a", href=True):
        href = tag['href'].lower()
        if(any(href.endswith(ext) for ext in allowed_extensions)):
            clean_href = href.replace('-', '').replace('_', '')
            if(any(pattern in clean_href for pattern in target_patterns)):
                download_links.append(tag['href'])

    print(f"Found {len(download_links)} monthly files.")

    monthly_dataframes = []
    for file_link in download_links:
        try:
            print(f"Downloading: {file_link}")
            response = requests.get(file_link)
            if(file_link.endswith(('.xls', '.xlsx'))):
                df_month = pd.read_excel(BytesIO(response.content))
            elif(file_link.endswith('.csv')):
                df_month = pd.read_csv(BytesIO(response.content))
            else:
                continue
            df_month['source_file'] = file_link
            monthly_dataframes.append(df_month)
        except Exception as e:
            print(f"Failed to load {file_link}: {e}")

    if(monthly_dataframes):
        combined_df = pd.concat(monthly_dataframes, ignore_index=True)
        print(f"Combined dataset shape: {combined_df.shape}")
        return combined_df
    else:
        print("No data loaded.")
        return pd.DataFrame()
    
#Calling Retrivel Function 

fuelcheck_raw_data = retrieve_fuelcheck_monthly_data()
fuelcheck_raw_data.head()


