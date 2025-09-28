import pandas as pd


class DataProcessing:
    @staticmethod
    def load_and_process_data(filepath: str, limit: int = 20) -> pd.DataFrame:
        """
        Load and process data from an Excel file.
        :param filepath:
        :param limit:
        :return:
        """
        """
        Added a check for the year in the filepath to handle the different sheet names in the 2022 file.
        User "skiprows" to skip the first 5 rows and "header" to set the column names. We are doing this since the
        column names are in the 6th row of the Excel file.
        """
        if "2022" not in filepath:
            data = pd.read_excel(filepath, sheet_name="Annualised", skiprows=5, header=[0, 1])
        else:
            data = pd.read_excel(filepath, sheet_name="AC22", skiprows=5, header=[0, 1])

        # Flatten the column names
        data.columns = ["_".join(col).strip() if "Unnamed" not in col[0] else col[1] for col in data.columns.values]

        # Apply a unified lowercase to avoid case sensitivity issues
        data.columns = data.columns.str.lower()  # type: ignore

        # Map column names to a standard set
        column_mapping = {
            "mode": "transport_mode",
            "nlc": "nlc",
            "asc": "asc",
            "station": "station_name",
            "coverage": "coverage_type",
            "source": "data_source",
            "monday_entries": "monday_entries",
            "monday_exits": "monday_exits",
            "weekday(mon-fri)_entries": "weekday_entries",
            "weekday(mon-thu)_entries": "weekday_entries",
            "friday_entries": "friday_entries",
            "saturday_entries": "saturday_entries",
            "sunday_entries": "sunday_entries",
            "weekday(mon-thu)_exits": "weekday_exits",
            "weekday(mon-fri)_exits": "weekday_exits",
            "friday_exits": "friday_exits",
            "saturday_exits": "saturday_exits",
            "sunday_exits": "sunday_exits",
            "annualised_en/ex": "annual_entries_exits",
        }

        # Rename the already existing column names to the new column names
        data.rename(columns=column_mapping, inplace=True)

        # Calculate entries and exits dynamically based on available columns
        entry_columns = [col for col in data.columns if "entries" in col]
        exit_columns = [col for col in data.columns if "exits" in col]

        # Assign the sum of the entry columns to the total_entries column
        if entry_columns:
            data["total_entries"] = data[entry_columns].sum(axis=1)

        # Assign the sum of the exit columns to the total_exits column
        data["total_exits"] = data[exit_columns].sum(axis=1)

        # Calculate total traffic
        data["total_traffic"] = data["total_entries"] + data["total_exits"]

        # Check for the existence of 'station_name' before grouping
        if "station_name" not in data.columns:
            return pd.DataFrame()  # Return empty DataFrame or handle as needed

        # Group by station name and sum the traffic
        station_traffic = data.groupby("station_name")["total_traffic"].sum().reset_index()

        # Sort and limit to top 20
        station_traffic = station_traffic.sort_values(by="total_traffic", ascending=False).head(limit)

        return station_traffic

    @staticmethod
    def load_combined_data(years: list[int], limit: int = 20) -> pd.DataFrame:
        """
        Load and process data for multiple years.
        :param years:
        :param limit:
        :return:
        """
        frames = []
        for year in years:
            """
            Here we are assuming that the data is stored in Excel files with the year as the filename.
            We loop through the years and load the data for each year and append it to the frames list.
            """
            filepath = f"app/data/{year}.xlsx"
            df = DataProcessing.load_and_process_data(filepath, limit)
            df["year"] = year
            frames.append(df)

        combined_data = pd.concat(frames)  # Combine the data for all years
        return combined_data

    # Calculate average entries for each station over the years
    @staticmethod
    def calculate_average_entries(combined_data: pd.DataFrame) -> pd.DataFrame:
        # Assuming 'station_name' and 'total_entries' are columns in your DataFrame
        average_data = combined_data.groupby("station_name")["total_traffic"].mean().reset_index()
        average_data.columns = ["Station Name", "Average Entries"]
        return average_data
