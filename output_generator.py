import pandas as pd

def save_to_excel(mapped_data, filename):
    """Save the mapped data to an Excel file."""
    df = pd.DataFrame(list(mapped_data.items()), columns=["Field", "Value"]).T
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")
