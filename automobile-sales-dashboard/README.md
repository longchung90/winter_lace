# Automobile Sales Dashboard

This project is a Dash application that visualizes automobile sales statistics. It provides interactive charts and reports based on user-selected criteria, such as yearly statistics and recession period statistics.

## Project Structure

```
automobile-sales-dashboard
├── src
│   └── app.py          # Main code for the Dash application
├── requirements.txt     # List of dependencies
├── .gitignore           # Files and directories to ignore by Git
└── README.md            # Project documentation
```

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd automobile-sales-dashboard
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Dashboard

To run the Dash application, execute the following command:

```
python src/app.py
```

Once the application is running, open your web browser and navigate to `http://127.0.0.1:8050` to view the dashboard.

## Features

- Interactive dropdown menus to select report types and years.
- Visualizations including line charts, bar charts, and pie charts.
- Insights into automobile sales trends over the years and during recession periods.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.