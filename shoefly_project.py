import codecademylib3
import pandas as pd

ad_clicks = pd.read_csv("ad_clicks.csv")

# Examines the first few rows
print(ad_clicks.head())

# shows views by utm_source
ad_platform = ad_clicks.groupby("utm_source").user_id.count().reset_index()

# creates a column which is True if ad_click_timestamp is not null
ad_clicks["is_click"] = ~ad_clicks.ad_click_timestamp.isnull()

clicks_by_source = (
    ad_clicks.groupby(["utm_source", "is_click"]).user_id.count().reset_index()
)

# creates pivot
clicks_pivot = clicks_by_source.pivot(
    columns="is_click", index="utm_source", values="user_id"
).reset_index()

clicks_pivot["percent_clicked"] = (
    clicks_pivot[True] / clicks_pivot[True] + clicks_pivot[False]
)

print(clicks_pivot)

# Counts how many people there is in each experimental group
print(ad_clicks["experimental_group"].value_counts())

# checks to see if a greater percentage of user clicked on Ad A or Ad B
percentage_by_group = (
    ad_clicks.groupby(["experimental_group", "is_click"]).user_id.count().reset_index()
)
percentage_by_group_pivot = percentage_by_group.pivot(
    columns="is_click", index="experimental_group", values="user_id"
)
percentage_by_group_pivot["percent_clicked"] = (
    percentage_by_group_pivot[True] / percentage_by_group_pivot[True]
    + percentage_by_group_pivot[False]
)
print(percentage_by_group_pivot)

# creates new Dataframes for each experimental group
a_clicks = ad_clicks[ad_clicks.experimental_group == "A"]
b_clicks = ad_clicks[ad_clicks.experimental_group == "B"]

# calculates the percent of users who clicked on the ad by day
clicks_by_day = a_clicks.groupby(["is_click", "day"]).user_id.count().reset_index()
clicks_by_day_pivot = clicks_by_day.pivot(
    columns="is_click", index="day", values="user_id"
).reset_index()

clicks_by_day_pivot["percent_clicked"] = (
    clicks_by_day_pivot[True] / clicks_by_day_pivot[True] + clicks_by_day_pivot[False]
)
print(clicks_by_day_pivot)
