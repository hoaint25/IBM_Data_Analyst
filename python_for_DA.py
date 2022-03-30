#Define a function that makes a dashboard

from turtle import title
import pandas as pd
pd.set_option('display.max_column', False)
from bokeh.plotting import figure, output_file, show,output_notebook
output_notebook()

def make_dashboard(x, gdp_change, unemployment, title, file_name):
    output_file(file_name)
    p = figure(title=title, x_axis_label='year', y_axis_label='%')
    p.line(x.squeeze(), gdp_change.squeeze(), color="firebrick", line_width=4, legend="% GDP change")
    p.line(x.squeeze(), unemployment.squeeze(), line_width=4, legend="% unemployed")
    show(p)

links={'GDP':'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/PY0101EN/projects/coursera_project/clean_gdp.csv',\
       'unemployment':'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/PY0101EN/projects/coursera_project/clean_unemployment.csv'}

#Question 1: Create a dataframe that contains the GDP data and display the first five rows of the dataframe

import pandas as pd
import ssl 
from urllib.request import urlopen
import io

#ignore that 
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#create dataframe
csv_path = links['GDP']
html = urlopen(csv_path, context=ctx).read()
data = io.BytesIO(html)
gdp_df = pd.read_csv(data, index_col=0)
gdp_df['date'] = gdp_df.index
gdp_df.reset_index(inplace = True, drop = True)
print(gdp_df.head(10))
print('----------------------------')

#Question 2: create a dataframe that contains the unemployment data.

csv_path = links['unemployment']
html = urlopen(csv_path, context = ctx).read()
data = io.BytesIO(html)
unemp_df = pd.read_csv(data, index_col = 0)
unemp_df['date'] = unemp_df.index
unemp_df.reset_index(inplace = True, drop = True)
print(unemp_df.head(10))
print('----------------------------')

#Question 3: Display a dataframe where unemployment was greater than 8.5%.

df = unemp_df[unemp_df['unemployment'] > 8.5]
print(df)
print('----------------------------')

#Question 4: Use function make_dashboard to make a dashboard

#create a new dataframe with column date
x = gdp_df[['date']]
#create a new dataframe with the column 'change-current' called gdp_change from the dataframe contains the GDP data 
gdp_change = gdp_df[['change-current']]
#create a new dataframe with the columns 'unemployment' called unemployment from the dataframe that contains unemployment data
unemployment = unemp_df[['unemployment']]
#Give your dashboard a string title, and assign it to the variable title
title = "Analyzing US Economic Data"
file_name = "index.html"
#call the function make_dashboard to produce a dashboard
# Fill up the parameters in the following function:
make_dashboard(x=x, gdp_change=gdp_change, unemployment=unemployment, title=title, file_name=file_name)
