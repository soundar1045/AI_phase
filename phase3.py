{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang1033{\fonttbl{\f0\fnil\fcharset0 Calibri;}}
{\*\generator Riched20 10.0.18362}\viewkind4\uc1 
\pard\sa200\sl276\slmult1\f0\fs22\lang9 import pandas as pd\par
from mlxtend.frequent_patterns import apriori, association_rules\par
\par
pd.set_option('display.max_columns', None)\par
pd.set_option('display.max_rows', None)\par
pd.set_option('display.width', 500)      \par
\par
df = pd.read_excel("/kaggle/input/market-basket-analysis/Assignment-1_Data.xlsx")\par
def outlier_thresholds(dataframe, variable):\par
    quartile1 = dataframe[variable].quantile(0.01)\par
    quartile3 = dataframe[variable].quantile(0.99)\par
    interquantile_range = quartile3 - quartile1\par
    up_limit = quartile3 + 1.5 * interquantile_range\par
    low_limit = quartile1 - 1.5 * interquantile_range\par
    return low_limit, up_limit\par
def replace_with_thresholds(dataframe, variable):\par
    low_limit, up_limit = outlier_thresholds(dataframe, variable)\par
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit\par
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit\par
def retail_data_prep(dataframe):\par
    dataframe = dataframe[dataframe["Quantity"] > 0]\par
    dataframe = dataframe[dataframe["Price"] > 0]\par
    replace_with_thresholds(dataframe, "Quantity")\par
    replace_with_thresholds(dataframe, "Price")\par
    return dataframe\par
\par
df = retail_data_prep(df)\par
\par
df.describe().T\par
count mean min 25% 50% 75% max std\par
Quantity 519551.0 9.39742 1.0 1.0 3.0 10.0 248.5 21.281261\par
Date 519551 2011-07-04 16:03:31.051080704 2010-12-01 08:26:00 2011-03-28 10:52:00 2011-07-20 11:55:00 2011-10-19 15:08:00 2011-12-09 12:50:00 NaN\par
Price 519551.0 3.32647 0.001 1.25 2.08 4.13 41.94 3.87738\par
CustomerID 387985.0 15317.042994 12346.0 13950.0 15265.0 16837.0 18287.0 1721.813298\par
df_fr = df[df['Country'] == "France"]\par
\par
df_fr.groupby(['BillNo', 'Itemname']).agg(\{"Quantity": "sum"\}).unstack().fillna(0).iloc[0:5, 0:5]\par
Quantity\par
Itemname 10 COLOUR SPACEBOY PEN 12 COLOURED PARTY BALLOONS 12 EGG HOUSE PAINTED WOOD 12 MESSAGE CARDS WITH ENVELOPES 12 PENCIL SMALL TUBE WOODLAND\par
BillNo     \par
536370 0.0 0.0 0.0 0.0 0.0\par
536852 0.0 0.0 0.0 0.0 0.0\par
536974 0.0 0.0 0.0 0.0 0.0\par
537065 0.0 0.0 0.0 0.0 0.0\par
537463 0.0 0.0 0.0 0.0 0.0\par
fr_inv_pro_df=df_fr.groupby(['BillNo', 'Itemname']). \\\par
                agg(\{"Quantity": "sum"\}). \\\par
                unstack(). \\\par
                fillna(0). \\\par
                applymap(lambda x: 1 if x > 0 else 0)\par
\par
frequent_itemsets = apriori(fr_inv_pro_df.astype("bool"),   \par
                            min_support=0.01,\par
                            use_colnames=True)\par
\par
\par
frequent_itemsets.sort_values("support", ascending=False).head()\par
support itemsets\par
330 0.765306 ((Quantity, POSTAGE))\par
332 0.188776 ((Quantity, RABBIT NIGHT LIGHT))\par
371 0.181122 ((Quantity, RED TOADSTOOL LED NIGHT LIGHT))\par
320 0.170918 ((Quantity, PLASTERS IN TIN WOODLAND ANIMALS))\par
315 0.168367 ((Quantity, PLASTERS IN TIN CIRCUS PARADE))\par
}
 