import requests
import csv

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
# create csv file to write results
csvFile = open('outputtest.csv', 'wb')
fieldnames = ['Original_URL', 'Status', 'Redirect', 'Notes']
csvWriter = csv.DictWriter(csvFile, delimiter=",", fieldnames=fieldnames)
csvWriter.writeheader()
# check each line in the txt file
f = open('urls.txt', 'r')
for line in f:
    try:
        r = requests.head(line.strip(), headers=headers, timeout=6, proxies=proxies, allow_redirects=True, verify=False)
        code = r.status_code
        dest = r.url
        history = r.history
    except requests.exceptions.Timeout as e:
        csvWriter.writerow({'Original_URL': line.strip(), 'Status': 'N/A', 'Redirect': 'N/A', 'Notes': 'Timeout'})
    except requests.exceptions.ConnectionError:
        csvWriter.writerow(
            {'Original_URL': line.strip(), 'Status': 'N/A', 'Redirect': 'N/A', 'Notes': 'Resolution Failure'})
    except requests.exceptions.TooManyRedirects:
        csvWriter.writerow(
            {'Original_URL': line.strip(), 'Status': 'N/A', 'Redirect': 'N/A', 'Notes': 'Redirect Loop'})
    else:
        if dest != line.strip():
            csvWriter.writerow({'Original_URL': line.strip(), 'Status': code, 'Redirect': dest, 'Notes': 'N/A'})
        if dest == line.strip():
            csvWriter.writerow({'Original_URL': line.strip(), 'Status': code, 'Redirect': 'N/A', 'Notes': 'N/A'})
