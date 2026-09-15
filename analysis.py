# Databases HW#1 - Asking Questions with CSV Data
# Dataset: 2018 Central Park Squirrel Census - Squirrel Data (NYC Open Data)
# Approach: Option A, native Python with csv.DictReader

import csv

# The CSV needs to be in the same folder as this script
FILENAME = "squirrel_census.csv"

# Read the whole file into a list of dictionaries.
# Each row is one squirrel sighting, and each key is a column name.
with open(FILENAME, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print("Rows loaded:", len(rows))
print("Columns:", len(rows[0]))


# The checkbox columns come in as the text "true" / "false", not real booleans,
# so this helper saves me from retyping the comparison everywhere.
def is_true(value):
    return value.strip().lower() == "true"


# ---------- Task 1: first 2 rows ----------
print("\n--- Task 1: first 2 rows ---")
for row in rows[:2]:
    print(row)


# ---------- Task 2: first row ----------
print("\n--- Task 2: first row ---")
print(rows[0])


# ---------- Task 3: rows 10-19 ----------
# Using index positions 10 through 19, so rows[10:20]
print("\n--- Task 3: rows 10-19 ---")
for i in range(10, 20):
    print(i, rows[i]["Unique Squirrel ID"], rows[i]["Shift"], rows[i]["Primary Fur Color"])


# ---------- Task 4: column names ----------
print("\n--- Task 4: column names ---")
for name in rows[0].keys():
    print(name)


# ---------- Task 5: first 10 values of one column ----------
print("\n--- Task 5: first 10 values of 'Primary Fur Color' ---")
for row in rows[:10]:
    print(row["Primary Fur Color"])


# ---------- Task 6: first 10 rows of three columns ----------
print("\n--- Task 6: first 10 rows of three columns ---")
print("Unique Squirrel ID | Shift | Age")
for row in rows[:10]:
    print(row["Unique Squirrel ID"], "|", row["Shift"], "|", row["Age"])


# ---------- Task 7: the three questions ----------

# Question 1: How many sightings are there for each primary fur color?
print("\n--- Question 1: sightings per primary fur color ---")
color_counts = {}
for row in rows:
    color = row["Primary Fur Color"]
    if color == "":
        color = "(blank)"
    if color in color_counts:
        color_counts[color] = color_counts[color] + 1
    else:
        color_counts[color] = 1

for color in color_counts:
    print(color, ":", color_counts[color])


# Question 2: How many squirrels approached a human, and what percent is that?
print("\n--- Question 2: squirrels that approached a human ---")
approach_count = 0
for row in rows:
    if is_true(row["Approaches"]):
        approach_count = approach_count + 1

percent = (approach_count / len(rows)) * 100
print("Approached a human:", approach_count)
print("Out of total sightings:", len(rows))
print("Percent:", round(percent, 2))


# Question 3: For each shift (AM/PM), how many squirrels were on the ground
# versus above ground?
print("\n--- Question 3: shift vs location breakdown ---")
shifts = ["AM", "PM"]
locations = ["Ground Plane", "Above Ground"]

for shift in shifts:
    for location in locations:
        count = 0
        for row in rows:
            if row["Shift"] == shift and row["Location"] == location:
                count = count + 1
        print(shift, "+", location, "=", count)
# Quick check: is Unique Squirrel ID actually unique?
ids = []
for row in rows:
    ids.append(row["Unique Squirrel ID"])
print("Total rows:", len(ids))
print("Distinct IDs:", len(set(ids)))

