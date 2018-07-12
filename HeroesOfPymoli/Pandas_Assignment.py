
#### Heroes Of Pymoli Data Analysis

# Dependencies and Setup
import pandas as pd
import numpy as np

# Read Raw data file
file_to_load = "Resources/purchase_data.csv"
purchase_data = pd.read_csv(file_to_load)

# Basic Observation
len(purchase_data) #780 lines of observations
purchase_data.head()
list(purchase_data) #['Purchase ID', 'SN', 'Age', 'Gender', 'Item ID', 'Item Name', 'Price']

#### 01 Player Count ####

# 1-1 Display the total number of players
unique_player_count=len(purchase_data["SN"].unique()) #576 unique SNs

q1={'Total Players':[unique_player_count]}
q1=pd.DataFrame(data=q1)

print(q1)  



#### 02 Purchasing Analysis (Total) ####

# 2-1 Number of Unique Items
unique_itemid_count=len(purchase_data["Item ID"].unique())

print(unique_itemid_count) #183 unique items by Item ID

# 2-2 Average Purchase Price 
avg_purchase_price= round(purchase_data["Price"].mean(),2) #3.05 USD
print("$",avg_purchase_price)

# 2-3 Total Number of Purchases
number_of_purchases=purchase_data['Purchase ID'].count() #780

# 2-4 Total Revenue
total_revenue=round(purchase_data['Price'].sum(),2) #2379.77 USD


# Consolidation
q2={'Number of Unique Items':[unique_itemid_count],
    'Average Price':[avg_purchase_price],
    'Number of Purchases':[number_of_purchases],
    'Total Revenue':[total_revenue]}
q2=pd.DataFrame(data=q2, columns=['Number of Unique Items', 'Average Price', 'Number of Purchases','Total Revenue'])

# Formatting
q2["Average Price"]=q2["Average Price"].map("${:.2f}".format)
q2["Total Revenue"]=q2["Total Revenue"].map("${:.2f}".format)

print(q2)



#### 03 Gender Demoraphics ####

# 3-1 Percentage and Count of Male Players
gender_breakdown = purchase_data.groupby(['Gender'])['SN'].count()
gender_breakdown=pd.DataFrame(data=gender_breakdown)
gender_breakdown["Percentage of Players"]=(gender_breakdown["SN"]/number_of_purchases)*100
gender_breakdown["Percentage of Players"]=gender_breakdown["Percentage of Players"].map("{:.2f}%".format)
gender_breakdown=gender_breakdown.rename(columns={"SN":"Total Count"})

q3=gender_breakdown[["Percentage of Players","Total Count"]].sort_values(["Total Count"],ascending=False)

print(q3)



#### 04 Purchasing Analysis by Gender ####

# 4-1 Purchase Count by Gender
gender_purchase_count = pd.DataFrame(purchase_data.groupby(['Gender'])['Purchase ID'].count())
gender_purchase_count=gender_purchase_count.rename(columns={"Purchase ID":"Purchase Count"})

 
# 4-2 Average Purchase Price by Gender
gender_avg_price = pd.DataFrame(purchase_data.groupby(['Gender'])['Price'].mean())
gender_avg_price["Price"]=gender_avg_price["Price"].map("${:.2f}".format)
gender_avg_price=gender_avg_price.rename(columns={"Price":"Average Purchase Price"})

# 4-3 Total Purchase Value by Gender
gender_total_purchase = pd.DataFrame(purchase_data.groupby(['Gender'])['Price'].sum())
gender_total_purchase["Price"]=gender_total_purchase["Price"].map("${:.2f}".format)
gender_total_purchase=gender_total_purchase.rename(columns={"Price":"Total Purchase Value"})

# 4-4 Normalized Totals by Gender <- What is definition of normalization? 
normalized_total=gender_avg_price
normalized_total=normalized_total.rename(columns={"Average Purchase Price":"Normalized Totals"})

# Consolidation
q4=pd.concat([gender_purchase_count,gender_avg_price,gender_total_purchase,normalized_total],axis=1)

print(q4)

#### 05 Age Demographics ####

# 5-1 Create Bins
purchase_data["Age"].max() #45 as oldest age
purchase_data["Age"].min() #7 as youngest age

age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
 
# 5-2 Add Bins to DataFrame
purchase_data["Age Group"] = pd.cut(purchase_data["Age"], age_bins, labels=group_names)

# 5-3 Purchase Count by Age Group
agegroup_purchase_count = pd.DataFrame(purchase_data.groupby(['Age Group'])['Purchase ID'].count())
agegroup_purchase_count=agegroup_purchase_count.rename(columns={"Purchase ID":"Total Count"})

# 5-4 Percentage of Players by Age Group
agegroup_purchase_count["Percentage of Players"]=(agegroup_purchase_count["Total Count"]/number_of_purchases)*100
agegroup_purchase_count["Percentage of Players"]=agegroup_purchase_count["Percentage of Players"].map("{:.2f}%".format)
 
# 5-5 Average Purchase Price by Age Group
agegroup_avg_price = pd.DataFrame(purchase_data.groupby(['Age Group'])['Price'].mean())
agegroup_avg_price=agegroup_avg_price.rename(columns={"Price":"Average Purchase Price"})
agegroup_avg_price ["Average Purchase Price"]=agegroup_avg_price ["Average Purchase Price"].map("${:.2f}".format)


#5-6 Total Purchase Value by Age Group
agegroup_total_purchase = pd.DataFrame(purchase_data.groupby(['Age Group'])['Price'].sum())
agegroup_total_purchase = agegroup_total_purchase.rename(columns={"Price":"Total Purchase Value"})
agegroup_total_purchase["Total Purchase Value"]=agegroup_total_purchase ["Total Purchase Value"].map("${:.2f}".format)


#5-7 Normalized Totals by Age Group <- What is definition of normalization? 
agegroup_normalized_totals=agegroup_avg_price
agegroup_normalized_totals=agegroup_normalized_totals.rename(columns={"Average Purchase Price":"Normalized Totals"})

# Consolidation
q5=pd.concat([agegroup_purchase_count,agegroup_avg_price,agegroup_total_purchase,agegroup_normalized_totals],axis=1)

print(q5)



#### 06 Top Spenders ####


# 6-1 Total Purchase Value by SN:
sn_total_purchase=pd.DataFrame(purchase_data.groupby(['SN'])['Price'].sum())
sn_total_purchase=sn_total_purchase.rename(columns={"Price":"Total Purchase Value"})

# 6-2 Purchase Count by SN
sn_purchase_count=pd.DataFrame(purchase_data.groupby(['SN'])['Purchase ID'].count())
sn_purchase_count=sn_purchase_count.rename(columns={"Purchase ID":"Purchase Count"})

# 6-3 Average Purchase Price by SN
sn_purchase_avg=pd.DataFrame(purchase_data.groupby(['SN'])['Price'].mean())
sn_purchase_avg=sn_purchase_avg.rename(columns={"Price":"Average Purchase Price"})
sn_purchase_avg["Average Purchase Price"]=sn_purchase_avg ["Average Purchase Price"].map("${:.2f}".format)

# 6-4 Consolidation
q6=pd.concat([sn_purchase_count,sn_purchase_avg,sn_total_purchase],axis=1)

# 6-5 Sort to Identify Top 5
q6=q6.sort_values('Total Purchase Value', ascending=False).head(5)
q6["Total Purchase Value"]=q6["Total Purchase Value"].map("${:.2f}".format)

print(q6)


#### 07 Most Popular Items ####
#Identify the 5 most popular items by purchase count, then list (in a table):

# 7-1 Total Purchase Count by Item ID
item_purchase_count=pd.DataFrame(purchase_data.groupby(['Item ID','Item Name','Price'])['Purchase ID'].count()).reset_index()
item_purchase_count=item_purchase_count.rename(columns={"Purchase ID":"Purchase Count"})
item_purchase_count=item_purchase_count.rename(columns={"Price":"Item Price"})


# 7-2 Total Purchase Value by Item ID:
item_total_purchase=pd.DataFrame(purchase_data.groupby(['Item ID'])['Price'].sum())
item_total_purchase=item_total_purchase.rename(columns={"Price":"Total Purchase Value"}).reset_index()

# 7-3 Consolidation
q7=pd.merge(item_purchase_count,item_total_purchase,on="Item ID",how="outer")

# 7-4 Sort to Identify Top 5 by Purchase Count
q7=q7.sort_values('Purchase Count', ascending=False).head(5)
q7["Total Purchase Value"]=q7["Total Purchase Value"].map("${:.2f}".format)
q7["Item Price"]=q7["Item Price"].map("${:.2f}".format)
q7=q7[["Item Name","Purchase Count","Item Price","Total Purchase Value"]]
print(q7)


#### 08 Most Profitable Items ####
#Identify the 5 most profitable items by total purchase value, then list (in a table):

# 8-1 Sort to Identify Top 5 by Total Purchase Value
q8=pd.merge(item_purchase_count,item_total_purchase,on="Item ID",how="outer")

q8=q8.sort_values('Total Purchase Value', ascending=False).head(5)
q8["Total Purchase Value"]=q8["Total Purchase Value"].map("${:.2f}".format)
q8["Item Price"]=q8["Item Price"].map("${:.2f}".format)
q8=q8[["Item Name","Purchase Count","Item Price","Total Purchase Value"]]
print(q8)
