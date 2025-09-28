import plotly.express as px
from app.utils.data_processing import DataProcessing
from dash import Dash, Input, Output, dcc, html

chart_page = html.Div(
    [
        html.H1("London Underground Traffic Analysis"),
        html.Label("Select Year:", style={"margin-bottom": "10px"}),
        dcc.Dropdown(
            id="year-dropdown",
            options=[{"label": year, "value": year} for year in range(2017, 2023)],
            value=2017,  # default value
            style={"color": "black", "margin-bottom": "20px"},
        ),
        html.Label("Select Type:", style={"margin-bottom": "10px"}),
        dcc.Dropdown(
            id="type-dropdown",
            options=[{"label": "Busiest", "value": "busiest"}, {"label": "Quietest", "value": "quietest"}],
            value="busiest",  # default value
            style={"color": "black", "margin-bottom": "20px"},
        ),
        dcc.Graph(id="station-traffic-graph"),
    ],
)


def register_chart_callbacks(app: Dash) -> None:
    @app.callback(
        Output(
            "station-traffic-graph",
            "figure",
        ),
        [
            Input("year-dropdown", "value"),
            Input("type-dropdown", "value"),
        ],
    )
    def update_graph(selected_year: str, traffic_type: str) -> px.bar:
        station_traffic = DataProcessing.load_and_process_data(f"app/data/{selected_year}.xlsx")

        # Sorting based on traffic type
        if traffic_type == "quietest":
            station_traffic = station_traffic.sort_values(by="total_traffic", ascending=True).head(20)
        else:  # Default to 'Busiest'
            station_traffic = station_traffic.sort_values(by="total_traffic", ascending=False).head(20)

        # Plotting

        # Create the bar graph focusing on station traffic
        fig = px.bar(station_traffic, x="station_name", y="total_traffic", title=f"Station Traffic in {selected_year}")
        # Load data for the selected year
        # Update graph aesthetics
        fig.update_layout(
            xaxis_title="Station",
            yaxis_title="Total Traffic",
            plot_bgcolor="white",
            xaxis=dict(categoryorder="total descending"),  # This sorts the bars based on traffic
            title={
                "text": f"Traffic at London Underground Stations in {selected_year}",
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
        )
        fig.update_traces(
            marker_color="rgb(0,123,255)",
            marker_line_color="rgb(8,48,107)",
            marker_line_width=1.5,
            opacity=0.6,
        )

        # Plotting
        fig = px.bar(
            station_traffic,
            x="station_name",
            y="total_traffic",
            labels={"station_name": "Station Name", "total_traffic": "Total Traffic"},
        )

        fig.update_traces(hovertemplate="<b>%{x}</b><br>Total Traffic: %{y}<extra></extra>")

        return fig
