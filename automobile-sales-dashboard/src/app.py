import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the data
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# List of years
year_list = sorted(data['Year'].unique())

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    html.Div([
        html.Label("Report type:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Select Statistics',
            placeholder='Select a report type.'
        )
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select-year',
            placeholder='Select-year'
        )
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Br(),
    html.Div(id='output-container')
])

# Enable/disable year dropdown based on statistics selection
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def toggle_year_dropdown(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

# Main callback to update charts
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Line chart of average sales over recession years
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales Fluctuation Over Recession Period")
        )

        # Plot 2: Bar chart of average sales by vehicle type
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(avg_sales, x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Number of Vehicles Sold by Vehicle Type")
        )

        # Plot 3: Pie chart of ad expenditure share by vehicle type
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, names='Vehicle_Type', values='Advertising_Expenditure',
                          title='Share of Each Vehicle Type in Total Expenditure During Recessions')
        )

        # Plot 4: Bar chart for effect of unemployment rate
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                          title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [
            html.Div([R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div([R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year is not None:
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly automobile sales (line chart for all years)
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, x='Year', y='Automobile_Sales', title='Total Yearly Automobile Sales')
        )

        # Plot 2: Monthly automobile sales (line chart for all months)
        mas = data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales')
        )

        # Plot 3: Bar chart for average vehicles sold by type in selected year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                          title=f'Average Vehicles Sold by Vehicle Type in {input_year}')
        )

        # Plot 4: Pie chart for ad expenditure by vehicle type in selected year
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, names='Vehicle_Type', values='Advertising_Expenditure',
                          title=f'Share of Each Vehicle Type in Total Expenditure in {input_year}')
        )

        return [
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex'})
        ]
    else:
        return html.Div("Please select a valid report type and year.")

if __name__ == '__main__':
    app.run()