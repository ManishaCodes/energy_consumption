import pandas as pd
import numpy as np
import json

# ---------------------------------------------
# Load your dataset
# ---------------------------------------------
df = pd.read_csv("combined_energy_power_dataset.csv")

# Drop unwanted columns (to get exactly 36 features)
df = df.drop(columns=['Unnamed: 0', 'month'], errors='ignore')

# ---------------------------------------------
# Select one row as example input
# ---------------------------------------------
sample = df.iloc[0].values.tolist()

# Make sure there are exactly 36 features
sample = sample[:36]
if len(sample) < 36:
    sample += [0.0] * (36 - len(sample))

# ---------------------------------------------
# Convert to clean numeric list
# ---------------------------------------------
clean_sample = []
for x in sample:
    if pd.isna(x):
        clean_sample.append(0.0)
    elif isinstance(x, (np.integer, np.int64, np.int32)):
        clean_sample.append(int(x))
    elif isinstance(x, (np.floating, np.float32, np.float64)):
        clean_sample.append(float(x))
    else:
        try:
            clean_sample.append(float(x))
        except:
            clean_sample.append(0.0)

# ---------------------------------------------
# Prepare JSON format for API or Java input
# Model expects input shape: (1, 1, 36)
# ---------------------------------------------
data = {"input": [[clean_sample]]}

# Verify shape
arr = np.array(data["input"])
print("📏 Shape that will be saved:", arr.shape)  # should print (1, 1, 36)

# ---------------------------------------------
# Save to sample_input.json
# ---------------------------------------------
with open("sample_input.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("✅ sample_input.json created successfully with", len(clean_sample), "features.")
