import os
import pandas as pd
import boto3


def main(event, context):
    """Manage the AWS Lambda-function."""
    SYMBOLS = 'symbols_short.csv'
    BUCKET = 'stock-data-jb'
    ITERATOR = setup(SYMBOLS, BUCKET)

    return {
        'statuscode': 200
    }


def setup(bucket_name, file_name):
    """Initialize the crawler."""
    if not os.path.isfile("/tmp/" + file_name):
        s3 = boto3.resource('s3')
        try:
            s3.Bucket(bucket_name).download_file(
                file_name, '/tmp/' + file_name)
        except:
            raise

    return 0


def test_avanza():
    """Test concept - To be updated, or removed."""
    import requests

    # url = 'https://www.avanza.se/aktier/om-aktien.html/5264/handelsbanken-a'
    url = 'https://www.avanza.se/ab/component/highstockchart/getchart/orderbook'

    cookies = {}
    """
        'Humany__parameters': '{"isLoggedIn":["Nej"]}',
        'FSESSIONID': 'jljw9n66435f1sq4seo8mfhz1',
        'AZAABSESSION': 'czx4lpy31b361utgzdr5nkjdh',
        'AZAPLACERAFORUMPERSISTANCE': '0295a5ed20-b678-49eq4oUJuHWH7LBECsoR6kv9Eyb6L0gp7KKeaY2tcjohgh67xWNI6iDbtCdszWpssfwB0',
        'Humany__clientId': 'ef49049e-5d6b-4057-747f-a0c76f4648e5',
        'AZAPERSISTANCE': '0253c8bd2e-1942-40FFNZ0x9866qIKywl4NUACzihFkUTJdksnrLOF9NUWpXoyJgvq2GeDoCNbYjZbiJPvV4',
        'JSESSIONID': '12vy4lnpfpz0nulldlgpbrazn',
    }
    """

    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'br, gzip, deflate',
        'Host': 'www.avanza.se',
        'Accept-Language': 'en-us',
        'Cache-Control': 'no-cache',
        'Origin': 'https://www.avanza.se',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Safari/605.1.15',
        'Referer': 'https://www.avanza.se/aktier/om-aktien.html/5264/handelsbanken-a',
        'Content-Length': '209',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = '{"orderbookId":5264,"chartType":"OHLC","widthOfPlotContainer":558,"chartResolution":"MINUTE","navigator":false,"percentage":false,"volume":true,"owners":false,"start":"2019-09-13T01:00:00.000Z","end":"2019-09-13T21:59:00.000Z","ta":[],"compareIds":[]}'

    response = requests.post('https://www.avanza.se/ab/component/highstockchart/getchart/orderbook',
                             headers=headers, cookies=cookies, data=data)

    # DATA RESOLUTIONS:
    # DAY any data, request max 10 years
    # MINUTE, last four weeks (request 1 day at a time)

    # SAVE DATA AS CSV, NOT PARQUET AT THE MOMENT!

    # response = requests.post(url=url, data=req)
    df_ohlc = pd.DataFrame(response.json()['dataPoints'], columns=[
                           'Date', 'Open', 'High', 'Low', 'Close']).set_index('Date')
    df_volume = pd.DataFrame(response.json()['volumePoints'], columns=[
        'Date', 'Volume']).set_index('Date')

    df = pd.merge(df_ohlc, df_volume, on='Date')

    print(response.json()['allowedResolutions'])
    print(response.json()['ownersPoints'])
    print(response.json().keys())


if __name__ == '__main__':
    # test_ig()
    test_avanza()
