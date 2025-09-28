import json

import pandas as pd
import plotly.express as px
from app.utils.data_processing import DataProcessing
from dash import Dash, Input, Output, dcc
from dash.html import H1, Button, Div

map_view = Div(
    [
        H1("Map"),
        Button("Refresh Data", id="refresh-data-button"),
        # Add your components and visualizations using the loaded data
        dcc.Graph(id="map-graph"),
    ],
)


def load_json_data() -> pd.DataFrame:
    """Load station coordinates from a JSON file."""
    with open("app/data/map.json", "r") as file:
        data = json.load(file)
    """
    Extract the features from the JSON data and create a DataFrame with the station name, latitude, longitude, zone, and
    marker color.
    """
    features = data["features"]
    records = [
        {
            "station_name": feature["properties"]["name"],
            "latitude": feature["geometry"]["coordinates"][1],
            "longitude": feature["geometry"]["coordinates"][0],
            "zone": feature["properties"]["zone"],
            "marker-color": feature["properties"].get("marker-color", "green"),
        }
        for feature in features
    ]
    return pd.DataFrame(records)


def fetch_coordinates_for_stations(combined_data: pd.DataFrame) -> pd.DataFrame:
    """Fetch coordinates for each unique station from combined data."""
    average_data = DataProcessing.calculate_average_entries(combined_data)
    # Clean up the station names for merging
    average_data["Station Name"] = average_data["Station Name"].str.strip().str.title()
    coords = load_json_data()  # Load the coordinates
    coords["station_name"] = coords["station_name"].str.strip().str.title()  # Clean up the station names for merging
    # Merge the coordinates with the average data to get the coordinates for each station that are in the average data
    # This will filter out any stations that don't have coordinates
    entries_with_coords = pd.merge(coords, average_data, how="inner", left_on="station_name", right_on="Station Name")
    return entries_with_coords


def setup_map_callback(app: Dash) -> None:
    @app.callback(
        Output("map-graph", "figure"),
        [
            Input("refresh-data-button", "n_clicks"),
        ],
    )
    def update_map(n_clicks):  # type: ignore # noqa
        """Load coordinates from cache or fetch new ones if file doesn't exist."""
        """
            We refresh the data by loading the combined data for the years 2017 to 2022 and fetching the coordinates for
            each station. We then create a scatter mapbox plot using Plotly Express and return the figure.

            The data is refreshed when the 'Refresh Data' button is clicked.
        """
        years = list(range(2017, 2022))  # Example years
        combined_data = DataProcessing.load_combined_data(years, 100)
        coordinates_df = fetch_coordinates_for_stations(combined_data)
        fig = px.scatter_mapbox(
            coordinates_df,
            lat="latitude",
            lon="longitude",
            hover_name="station_name",
            hover_data={
                "zone": False,
                "latitude": False,
                "longitude": False,
                "Average Entries": ":,",
            },
            size="Average Entries",
            color="marker-color",
            color_discrete_map="identity",
            size_max=45,
            zoom=10,
            center={"lat": 51.5074, "lon": -0.1278},
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
