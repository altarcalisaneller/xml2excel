import xlsxwriter
from bs4 import BeautifulSoup
import pandas as pd
import pandas as pd


file = open("C:/Users/acalisaneller/Desktop/x.xml", encoding="utf8") # file path
soup = BeautifulSoup(file, "lxml")
tag_list = soup.find_all()
kebirKod_liste = []
detayKod_liste = []
kebir_ad_liste = []
detay_ad_liste = []
tarih_liste = []
yevmiye_no_liste = []
aciklama_liste = []
tutar_liste = []
debit_credit_liste = []

for tag in tag_list: # the tags can be changed depending on requirements and xml file.
    if tag.name == 'gl-cor:accountmainid':
        kebirKod_liste.append(tag.text)
    elif tag.name == 'gl-cor:accountsubid':
        detayKod_liste.append(tag.text)
    elif tag.name == 'gl-cor:accountmaindescription':
        kebir_ad_liste.append(tag.text)
    elif tag.name == 'gl-cor:accountsubdescription':
        detay_ad_liste.append(tag.text)
    elif tag.name == 'gl-cor:accountsubdescription':
        detay_ad_liste.append(tag.text)
    elif tag.name == 'gl-cor:postingdate':
        tarih_liste.append(tag.text)
    elif tag.name == 'gl-cor:linenumbercounter':
        yevmiye_no_liste.append(tag.text)
    elif tag.name == 'gl-cor:detailcomment':
        aciklama_liste.append(tag.text)
    elif tag.name == 'gl-cor:amount':
        tutar_liste.append(tag.text)
    elif tag.name == 'gl-cor:debitcreditcode':
        debit_credit_liste.append(tag.text)

total = zip(kebirKod_liste, detayKod_liste, kebir_ad_liste, detay_ad_liste, tarih_liste, yevmiye_no_liste, aciklama_liste, tutar_liste, debit_credit_liste)
df = pd.DataFrame(total, columns=["Kebir_Kod", "Detay_Kod", "Ana_Hesap_Adı", "Detay_Hesap_Adı", "Tarih", "Yevmiye_No", "Açıklama", "Tutar", "DC"])

last_index = len(df.index)
row1 =0
row2 =1
while row1 < last_index:
    if df["DC"][row1:row2].values[0] == "D":
        df["Tutar"][row1:row2] = float(df["Tutar"][row1:row2].values[0])
    else:
        df["Tutar"][row1:row2] = float(df["Tutar"][row1:row2].values[0])  * (-1)
    row1 += 1
    row2 += 1

df.drop("DC", axis = 1, inplace = True)

df['Gun'] = pd.DatetimeIndex(df['Tarih']).day

groupby=df.groupby("Yevmiye_No").groups

df["Karsi_Hesap"]=""

for index, yevmiye_no in df["Yevmiye_No"].items():
    if df["Tutar"][index] >0:
        list = []
        for i in groupby[yevmiye_no]:
            if int(i) != int(index) and df["Tutar"][i] <0:
                list.append(df["Kebir_Kod"][i])
                df["Karsi_Hesap"][index] = set(list)
    else:
        list = []
        for i in groupby[yevmiye_no]:
            if int(i) != int(index) and df["Tutar"][i] >0:
                list.append(df["Kebir_Kod"][i])
                df["Karsi_Hesap"][index] = set(list)

df['Karsi_Hesap'] = df.Karsi_Hesap.astype(str)
df["Karsi_Hesap"] = df["Karsi_Hesap"].str.replace("{","")
df["Karsi_Hesap"] = df["Karsi_Hesap"].str.replace("}","")
df["Karsi_Hesap"] = df["Karsi_Hesap"].str.replace("'","")

df.drop("Gun", axis = 1, inplace = True)

writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter') # give a name to output file
workbook  = writer.book
df.to_excel(writer, sheet_name='Sheet1')
writer.save()
print("done!")
