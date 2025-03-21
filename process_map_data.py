import json
import pandas as pd

# -------------------------------
# 1. Load JSON Data from Files
# -------------------------------
def load_json_file(filename):
    """
    Load JSON data from a file.

    :param filename: The name of the JSON file.
    :return: List of dictionaries (JSON data).
    """
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {filename}!")
        return []

# Load JSON files
locations = load_json_file("locations.json")
metadata = load_json_file("metadata.json")

# Ensure data is not empty before proceeding
if not locations or not metadata:
    print("Error: Missing or invalid data files. Exiting program.")
    exit()

# -------------------------------
# 2. Convert Data to Pandas DataFrame
# -------------------------------
df_locations = pd.DataFrame(locations)
df_metadata = pd.DataFrame(metadata)

# Merge both datasets based on 'id'
df_merged = pd.merge(df_locations, df_metadata, on="id", how="left")

# -------------------------------
# 3. Data Analysis
# -------------------------------

# (A) Count the number of valid points per type
valid_points_per_type = df_merged["type"].value_counts()

# (B) Calculate the average rating per type
average_ratings_per_type = df_merged.groupby("type")["rating"].mean()

# (C) Identify the location with the highest number of reviews
if "reviews" in df_merged.columns:
    max_reviews_location = df_merged.loc[df_merged["reviews"].idxmax()]
else:
    max_reviews_location = None

# (D) Identify locations with incomplete data (Bonus Task)
incomplete_data = df_merged[df_merged.isnull().any(axis=1)]

# -------------------------------
# 4. Display Results
# -------------------------------
print("\n--- Valid Points Per Type ---")
print(valid_points_per_type)

print("\n--- Average Rating Per Type ---")
print(average_ratings_per_type)

print("\n--- Location with Highest Reviews ---")
if max_reviews_location is not None:
    print(max_reviews_location)
else:
    print("No reviews data available.")

print("\n--- Locations with Incomplete Data ---")
if incomplete_data.empty:
    print("No locations with incomplete data.")
else:
    print(incomplete_data)

# -------------------------------
# 5. Save Output to a File (Optional)
# -------------------------------
output_data = {
    "valid_points_per_type": valid_points_per_type.to_dict(),
    "average_ratings_per_type": average_ratings_per_type.to_dict(),
    "max_reviews_location": max_reviews_location.to_dict() if max_reviews_location is not None else "No Data",
    "incomplete_data": incomplete_data.to_dict(orient="records")
}

with open("analysis_results.json", "w") as output_file:
    json.dump(output_data, output_file, indent=4)

print("\n✅ Analysis results saved to 'analysis_results.json'.")
