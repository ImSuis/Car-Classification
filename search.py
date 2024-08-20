import os
import pandas as pd

csv_dir = 'final_listings_2'

def read_csv_safe(file_path):
    try:
        return pd.read_csv(file_path)
    except (pd.errors.EmptyDataError, UnicodeDecodeError) as e:
        print(f"Error reading {file_path}: {e}")
        return pd.DataFrame()

def find_cheapest_car(model_name):
    exact_file_name = f"{model_name.replace(' ', '_')}.csv"
    exact_file_path = os.path.join(csv_dir, exact_file_name)
    print(f"Looking for exact file: {exact_file_name}")

    if os.path.isfile(exact_file_path):
        print(f"File {exact_file_name} found.")
        df = read_csv_safe(exact_file_path)
        if not df.empty and {'Name', 'Price', 'URL', 'Mileage'}.issubset(df.columns):
            # Clean the 'Price' column
            df['Price'] = pd.to_numeric(df['Price'].replace('[\$,]', '', regex=True), errors='coerce')
            sorted_df = df.sort_values(by='Price')
            cheapest_car = sorted_df.iloc[0].to_dict()
            return cheapest_car
        else:
            print(f"File {exact_file_path} is empty or does not contain required columns. Columns found: {df.columns.tolist()}")
            return None
    else:
        print(f"File {exact_file_name} not found.")

    print(f"Searching through all CSV files in the directory for model: {model_name}")
    all_cars = []

    for file in os.listdir(csv_dir):
        if file.endswith('.csv'):
            file_path = os.path.join(csv_dir, file)
            df = read_csv_safe(file_path)
            if not df.empty and {'Name', 'Price', 'URL', 'Mileage'}.issubset(df.columns):
                df['Price'] = pd.to_numeric(df['Price'].replace('[\$,]', '', regex=True), errors='coerce')
                model_cars = df[df['Name'].str.contains(model_name, case=False, na=False)]
                all_cars.append(model_cars)
            else:
                print(f"File {file_path} does not contain required columns. Columns found: {df.columns.tolist()}")

    if all_cars:
        all_cars_df = pd.concat(all_cars, ignore_index=True)
        if not all_cars_df.empty:
            all_cars_df = all_cars_df.sort_values(by='Price')
            cheapest_car = all_cars_df.iloc[0].to_dict()
            return cheapest_car
        else:
            print(f"No cars found for the model {model_name}.")
    else:
        print(f"No cars found for the model {model_name} in any file.")

    return None

# Example usage
model_name = 'Aston Martin V8 Vantage Coupe 2012'  # Replace with the identified car model
cheapest_car = find_cheapest_car(model_name)
if cheapest_car:
    print(f"The cheapest {model_name} is available for ${cheapest_car['Price']} at {cheapest_car['URL']} with {cheapest_car['Mileage']} miles.")
else:
    print(f"No valid cars found for the model {model_name}.")