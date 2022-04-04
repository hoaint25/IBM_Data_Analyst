#Define a function that makes a graph
import yfinance as yf
import pandas as pd 
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Question 1: Use yfinance to extract stock data 

telsa = yf.Ticker('TSLA')
telsa_data = telsa.history(period = "max")
telsa_data.reset_index(inplace = True)
print(telsa_data.head(10))
print('-------------------------------')

#Question 2: Use Webscraping to extract telsa revenue data

#Use the requests library to download the webpage. Save the text of the response as a variable name html_data
url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
html_data = requests.get(url).text
#parse the html data using beautiful_soup 
soup = BeautifulSoup(html_data, "html5lib")
tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if ('Tesla Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')
        
        for row in rows:
            col = row.find_all('td')
            
            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',','').replace('$','')

                tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)


#Question 3: Use yfinance to extract stock data

#using Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Gamestop and its ticker symbol is GME
gme = yf.Ticker('GME')

#using the ticker object and the function history extract stock information and save it in dataframe named gme_data
gme_data = gme.history(period = 'max')

#reset the index and display the first five rows of the gme_data dataframe using the head function.
gme_data.reset_index(inplace =True)
print(gme_data.head(10))

#Question 4: Use Webscraping to extract GME Revenue Data

#using the requests library to download the webpage 
url = 'https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue'
html_data = requests.get(url).text
#parse the html data using beautiful_soup
soup = BeautifulSoup(html_data,"html5lib")

gme_revenue = pd.DataFrame(columns = ['Date','Revenue'])

for table in soup.find_all('table'):

    if ('GameStop Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')

        for row in rows:
            col = row.find_all('td')

            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',','').replace('$','')
                gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)
print(gme_revenue)

#Question 5: Plot Telsa Stock Graph
make_graph(tesla_data[['Date','Close']], tesla_revenue, 'Tesla')

#Question 6: Plot GmaeStop Stock Graph
make_graph(gme_data[['Date','Close']], gme_revenue, 'GameStop')
