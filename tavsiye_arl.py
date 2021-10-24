###############################################
# ASSOCIATION RULE LEARNING (BİRLİKTELİK KURALI ÖĞRENİMİ)
###############################################

# Amacımız online retail II veri setine biliktelik analizi uygulayarak
# kullanıcılara ürün satın alma sürecinde ürün önermek.

# 1. Veri Ön İşleme
# 2. ARL Veri Yapısını Hazırlama
# 3. Birliktelik Kurallarının Çıkarılması
# 4. Çalışmanın Fonksiyonlaştırılması
# 5. Sepet Aşamasındaki Kullanıcılara Ürün Önerisinde Bulunmak



###################################
# Veri Ön İşleme
###################################

import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 500)
# çıktının tek bir satırda olmasını sağlar.
pd.set_option("display.expand_frame_repr", False)
from mlxtend.frequent_patterns import apriori, association_rules

df = pd.read_excel(r"C:\Users\Hp\Desktop\Online_Retail_II\Online_Retail_II.xlsx", sheet_name="Year 2010-2011")
# df_= df.copy()


def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
# Değişkeni büyükten küçüğe sıralayıp 0.01 ve 0.99 luk değerleri alıyoruz.
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
# Eğer bu değer 1.5 kat fazlaysa üst limit, azsa alt limit diyoruz.

    return low_limit, up_limit
# Şu anda frekans saydıracağımız için aykırı değerlere hassasiyet vardır.
# Bundan dolayı aykırı değerleri ve eşik değerleri hesaplamak için fonksiyon yazmalıyız.
# Bir değişkenin genel dağılımının dışındaki değerlere aykırı değer adı verilir.
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit
# Bu eşik değerlere göre aykırı değerleri eşik değerlerle değiştime işlemi yapılmalıdır.

def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
# Quantity, price'taki aykırı değerlerle limit değerleri değiştirme işlemi
    return dataframe
def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)


df = retail_data_prep(df)

####################################################
# ARL Veri Yapısını Hazırlama (Invoice-Product Matrix)
####################################################

df_ger = df[df["Country"] == "Germany"]

check_df(df_ger)

df_ger.groupby(["Invoice", "Description"]).agg({"Quantity": "sum"}).head(20)

df_ger.groupby(["Invoice", "Description"]).agg({"Quantity": "sum"}).unstack().iloc[0:20, 0:20]

df_ger.groupby(["Invoice", "Description"]).agg({"Quantity": "sum"}).unstack().fillna(0).iloc[0:20, 0:20]

df_ger.groupby(["Invoice", "Description"]). \
    agg({"Quantity": "sum"}). \
    unstack(). \
    fillna(0). \
    applymap(lambda x:1 if x > 0 else 0).iloc[0:20, 0:20]
# tüm satır ve sütunları gezer.

def create_invoice_product_df(dataframe, id=False) :
    if id:
        return dataframe.groupby(["Invoice", "StockCode"])["Quantity"].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(["Invoice", "Description"])["Quantity"].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)

ger_inv_pro_df = create_invoice_product_df(df_ger)

ger_inv_pro_df = create_invoice_product_df(df_ger, id=True)

def check_id(dataframe, stock_code):
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)

check_id(df_ger, 21987)
check_id(df_ger, 23235)
check_id(df_ger, 22747)

####################################################
# Birliktelik Kurallarının Çıkarılması
####################################################

frequent_itemsets = apriori(ger_inv_pro_df, min_support=0.01, use_colnames=True)

frequent_itemsets.sort_values("support", ascending=False).head()

rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
rules.sort_values("support", ascending=False).head()

rules.sort_values("lift", ascending=False).head()

####################################################
# Sepet Aşamasındaki Kullanıcılara Ürün Önerisinde Bulunmak
####################################################

product_id = 21987
product_id1 = 23235
product_id2 = 22747

check_id(df, product_id)

product_id_list = [21987, 23235, 22747]
sorted_rules = rules.sort_values("lift", ascending=False)

recommendation_list = []
for i, product in enumerate(sorted_rules["antecedents"]):
    for j in list(product):
        if j in product_id_list:
            recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

recommendation_list[0:2]

check_id(df, 22556)

check_df(df, recommendation_list[0])

def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

    return recommendation_list[0:rec_count]

arl_recommender(rules, 21987, 1)
arl_recommender(rules, 23235, 1)
arl_recommender(rules, 22747, 1)

check_id(df, 21086)
check_id(df, 23244)
check_id(df, 22745)


