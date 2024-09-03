import pandas as pd

# Load the dataset
df = pd.read_csv('../data/attractions_cities.csv')

# Check for duplicates based on both 'City' and 'Attractions' columns
duplicates = df[df.duplicated(subset=['City', 'Attractions'], keep=False)]

# Display duplicates if any are found
if not duplicates.empty:
    print("Found duplicate rows:")
    print(duplicates)
    
    # Drop duplicates, keeping the first occurrence
    df_cleaned = df.drop_duplicates(subset=['City', 'Attractions'], keep='first')
    print("\nDuplicates have been removed.")
else:
    df_cleaned = df
    print("No duplicates found.")

# Save the cleaned dataset
df_cleaned.to_csv('../data/cleaned_dataset.csv', index=False)

print("Cleaned dataset saved as 'cleaned_dataset.csv'.")
