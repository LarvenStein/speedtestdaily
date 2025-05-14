import requests
from bs4 import BeautifulSoup

def get_speed_values(test_url):
    html = requests.get(test_url).text
    
    return extract_speed_values(html)


def extract_speed_values(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    
    gauge_values = soup.select(".gauge-number.result-data-value")

    download = None
    upload = None
    
    if len(gauge_values) > 0:
        download = gauge_values[0].text.strip()
    if len(gauge_values) > 1:
        upload = gauge_values[1].text.strip()
    
    result_data_elements = soup.select(".result-data")
    ping = None
    if len(result_data_elements) > 2:
        ping = result_data_elements[2].text.strip()
    

    return {
        "download": download,
        "upload": upload,
        "ping": ping
    }
