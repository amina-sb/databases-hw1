# Databases HW#1 — Asking Questions with CSV Data

**Dataset:** 2018 Central Park Squirrel Census — Squirrel Data
**Source:** NYC Open Data (dataset ID `vfnx-vebw`)
**Approach:** Option A — native Python with `csv.DictReader`
**Size:** 3,023 rows, 31 columns

---

## Why I chose this dataset

I wanted something small enough to actually open and look at, but with enough structure to ask real questions. A lot of the NYC Open Data sets are hundreds of megabytes of permit records, and I did not want to spend the whole assignment struggling with the download. This one is about 1 MB and every row is one squirrel sighting in Central Park in October 2018.

The other reason is that it has a lot of categorical columns to work with `Shift` is just AM or PM, and for data analyst like me it is very convinient, `Age` is Adult or Juvenile, `Primary Fur Color` is Gray, Cinnamon or Black, and `Location` is Ground Plane or Above Ground. That made it easy to group and count things without having to bucket numbers into ranges first.

I also liked that `Unique Squirrel ID` is built by pasting together the hectare, the shift, the date, and a sequence number. That looked like a analytical key to me, which felt relevant given this is a databases class. It turned out to be more complicated than that, which I get into at the end.

---

## How to run

Put `analysis.py` and `squirrel_census.csv` in the same folder, then:

```
python3 analysis.py
```

---

## Three Data Questions

### Question 1: How many sightings are there for each primary fur color?

**Output:**

```
(blank) : 55
Gray : 2473
Cinnamon : 392
Black : 103
```

**Why the data structure supports this:** `Primary Fur Color` is a categorical column with only three real values, so I can walk through every row once and keep a running count in a dictionary keyed by color. Because `DictReader` gives me each row as a dictionary, I can pull the value out by column name instead of guessing a position number. I also had to handle the 55 rows where the field is an empty string, the sighter did not record a color. I counted those as their own `(blank)` group rather than dropping them, so the four numbers still add up to 3,023.

### Question 2: How many squirrels approached a human, and what percent of all sightings is that?

**Output:**

```
Approached a human: 178
Out of total sightings: 3023
Percent: 5.89
```

**Why the data structure supports this:** `Approaches` is a yes/no column, so filtering it is just a counter that goes up when the condition is true. The one catch is that everything coming out of a CSV is text, so the value is the *string* `"true"`, not a real boolean. Writing `if row["Approaches"]:` would count every single row, since any non-empty string is truthy in Python. I wrote a small `is_true()` helper that lowercases the value and compares it to `"true"`. Since every row is one sighting, dividing by `len(rows)` gives a percentage that actually means something.

### Question 3: For each shift (AM or PM), how many squirrels were on the ground versus above ground?

**Output:**

```
AM + Ground Plane = 875
AM + Above Ground = 449
PM + Ground Plane = 1241
PM + Above Ground = 394
```

**Why the data structure supports this:** So this one needs two categorical columns at the same time, and both `Shift` and `Location` have exactly two values each, so there are only four combinations to check. I looped over the shifts and locations and counted rows matching both conditions. The interesting part is the ratio rather than the raw counts: about 34% of morning sightings were above ground (449 out of 1,324) compared to about 24% in the afternoon (394 out of 1,635). So the squirrels were more likely to be up in trees in the morning. The four numbers only add to 2,959 instead of 3,023 because 64 rows have no `Location` recorded at all, which is a reminder that a breakdown like this quietly drops anything with a missing field.

---

## What the Data Cannot Answer

*(The uniqueness check at the bottom of `analysis.py` prints `Total rows: 3023` and `Distinct IDs: 3018`.)*

The question I actually wanted to answer was how many individual squirrels live in Central Park, and this dataset can not tell me. Every row is a *sighting*, not a squirrel. The `Unique Squirrel ID` column looks like it should solve this, but the ID is built from the hectare, shift, date, and a counter, so the same animal spotted on October 6th and again on October 14th gets two completely different IDs. There's nothing in the data: no tag, no marking, no photo, that links one sighting to another. On top of that the IDs are not even unique as they stand: there are 3,018 distinct values across 3,023 rows, so five got reused by accident during collection. What I think is missing is some kind of stable identifier per animal, which would need real tagging rather than volunteers walking around with clipboards. The assumption that would confuse me here is reading "Gray : 2473" as "there are 2,473 gray squirrels in Central Park." That number is 2,473 *times someone wrote down a gray squirrel*, and a bold squirrel hanging around a busy path near a food cart is going to end up in the data far more often than a shy one in the woods. The blank fields make it worse in a subtle way: 55 rows have no fur color and 64 have no location, and those are probably not missing at random. A squirrel that is far away or moving fast is both harder to identify and more likely to have fields left empty, so the rows I can analyze are already skewed toward the squirrels that sat still and let themselves be observed.
