from datetime import date
import pandas as pd
from scipy import optimize
import numpy as ny
import matplotlib . pyplot as plt
import scipy.linalg as la
data = pd.read_excel("C:/Users/owner/Desktop/466a1.xlsx")
def coupon_date(d1, d2):
    format_d1 = date(int(d1[0:4]), int(d1[5:7]), int(d1[8:10]))
    format_d2 = date(int(d2[0:4]), int(d2[5:7]), int(d2[8:10]))

    difference = (format_d1 - format_d2).days

    while (difference <= 0):
        difference = difference + 180

    return difference
# this function calculates days since last coupon payment
bond_date = ['2022/01/10','2022/01/11','2022/01/12','2022/01/13',
'2022/01/14','2022/01/17','2022/01/18','2022/01/19','2022/01/20','2022/01/21']

# I am assuming every year has 365 days for simplicity. Then it follows the date since last coupon payment is same for every bond maturing in the same month i.e. 
# the one maturing in 2025/03 has same accured interest days as the on maturing in 2026/03
# the following functions calculates accured interest for each day. coupon is rate / 365 * 2
i =0 
mar_2025 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/03/01')
    mar_2025.append(AIM*1.25/180/2)
    i = i + 1
mar_2025

i =0 
mar_2022 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/03/01')
    mar_2022.append(AIM*0.5/180/2)
    i = i + 1
mar_2022

i =0 
mar_2026 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/03/01')
    mar_2026.append(AIM*0.25/180/2)
    i = i + 1
mar_2026

i =0 
mar_2027 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/03/01')
    mar_2027.append(AIM*1.25/180/2)
    i = i + 1
mar_2027

i =0 
mar_2023 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/03/01')
    mar_2023.append(AIM*1.75/180/2)
    i = i + 1
mar_2023

i = 0
mar_2024 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/03/01')
    mar_2024.append(AIM*2.25/180/2)
    i = i + 1
mar_2024


i = 0
aug_2022 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/08/01')
    aug_2022.append(AIM*0.25/180/2)
    i = i + 1
aug_2022

i = 0
aug_2023 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/08/01')
    aug_2023.append(AIM*0.25/180/2)
    i = i + 1
aug_2023

i = 0
sep_2024 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/09/01')
    sep_2024.append(AIM*1.5/180/2)
    i = i + 1
sep_2024

i = 0
sep_2025 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/09/01')
    sep_2025.append(AIM*0.5/180/2)
    i = i + 1
sep_2025

i = 0
sep_2026 = []
for i in range(len(bond_date)):
    AIM = coupon_date(bond_date[i],'2026/09/01')
    sep_2026.append(AIM*1/180/2)
    i = i + 1
sep_2026
# I calculated accured interest for each bond, now I will change the clean price to dirty price
AI_ALL = []
AI_ALL.append(aug_2023)
AI_ALL.append(mar_2025)
AI_ALL.append(sep_2025)
AI_ALL.append(mar_2026)
AI_ALL.append(sep_2026)
AI_ALL.append(mar_2027)
AI_ALL.append(mar_2023)
AI_ALL.append(mar_2024)
AI_ALL.append(sep_2024)
AI_ALL.append(aug_2022)
AI_ALL.append(mar_2022)

print(data)
# put AI of one bond for each day in a list and create a bigger list for 11 bonds
def get_dirty_price(data,list):
    result = []
    for row in range(11):
         for column in range(10):
            result.append(data.iloc[row, column + 4] + AI_ALL[row][column])
    return result
dirty_price_all = get_dirty_price(data, AI_ALL)
print(len(dirty_price_all))

# now we calculate YTM using dirty price and cash flow formula, dirty_price = sum(coupon/(1+1/2r)^i+(100+coupon)/(1+1/2ytm)^number_of_periods). for the sum,
# if its feb then we are done. if its march then we need discount one more month. 
# note only one month of coupon should be considered, rest is reflected in dirty price

def get_ytm(dirty_price,number_of_periods,coupon):
    list_temp = []
    for i in range(number_of_periods):
        list_temp.append(i+1)
    ytm = lambda r: (sum(coupon / 2 / (1+r/2) ** i for i in list_temp) + (100+coupon/2) / (1+r/2) ** number_of_periods )/ (1+r/2) ** (1/6) - dirty_price
    #this is to minimize this equation sum(coupon / 2 / (1+r/2) ** i for i in list_temp) + (100+coupon/2) / (1+r/2) ** number_of_periods )/ (1+r/2) ** (1/6) - DP = 0 to calculate ytm 
    return optimize.newton(ytm,0.05) * 100
    #note this is for those bond that has one more month to discount, i will write another function for those have their bond payment on august and feb.
def get_ytm_aug(dirty_price,number_of_periods,coupon):
    list_temp = []
    for i in range(number_of_periods):
        list_temp.append(i+1)
    ytm_aug = lambda r: sum(coupon / 2 / (1+r/2) ** i for i in list_temp) + (100+coupon/2) / (1+r/2) ** number_of_periods  - dirty_price
    return optimize.newton(ytm_aug,0.05) * 100
#get_ytm_aug(99.796,1,0.25)
#now we put ytm in lists corresponding to each day
AUG_2023 = []
for i in range(10):
    ytm_temp = get_ytm_aug(dirty_price_all[i],3,0.25)
    AUG_2023.append(ytm_temp)
print(AUG_2023)


MAR_2025 = []
for i in range(10):
    ytm_temp = get_ytm(dirty_price_all[i+10],6,1.25)
    MAR_2025.append(ytm_temp)
print(MAR_2025)

SEP_2025 = []
for i in range(10):
    ytm_temp = get_ytm(dirty_price_all[i+20],7,0.5)
    SEP_2025.append(ytm_temp)
print(SEP_2025)

MAR_2026 = []
for i in range(10):
    ytm_temp = get_ytm(dirty_price_all[i+30],8,0.25)
    MAR_2026.append(ytm_temp)
print(MAR_2026)

SEP_2026 = []
for i in range(10):
    ytm_temp = get_ytm(dirty_price_all[i+40],9,1)
    SEP_2026.append(ytm_temp)
print(SEP_2026)

MAR_2027 = []
for i in range(10):
    ytm_temp = get_ytm(dirty_price_all[i+50],10,1.25)
    MAR_2027.append(ytm_temp)
print(MAR_2027)

MAR_2023 = []
for i in range(10):
    ytm_temp = get_ytm(dirty_price_all[i+60],2,1.75)
    MAR_2023.append(ytm_temp)
print(MAR_2023)

MAR_2024 = []
for i in range(10):
    ytm_temp = get_ytm(dirty_price_all[i+70],4,2.25)
    MAR_2024.append(ytm_temp)
print(MAR_2024)

SEP_2024 = []
for i in range(10):
    ytm_temp = get_ytm(dirty_price_all[i+80],6,1.5)
    SEP_2024.append(ytm_temp)
print(SEP_2024)

AUG_2022 = []
for i in range(10):
    ytm_temp = get_ytm_aug(dirty_price_all[i+90],1,0.25)
    AUG_2022.append(ytm_temp)
print(AUG_2022)
all = [AUG_2022 , MAR_2023 , AUG_2023 , MAR_2024 , SEP_2024 , MAR_2025, SEP_2025 , MAR_2026 , SEP_2026 , MAR_2027]
print(all[1][0])
jan_10= []
jan_11= []
jan_12= []
jan_13= []
jan_14= []
jan_17= []
jan_18= []
jan_19= []
jan_20= []
jan_21= []
for i in range(10):
    jan_10.append(all[i][0])
    jan_11.append(all[i][1])
    jan_12.append(all[i][2])
    jan_13.append(all[i][3])
    jan_14.append(all[i][4])
    jan_17.append(all[i][5])
    jan_18.append(all[i][6])
    jan_19.append(all[i][7])
    jan_20.append(all[i][8])
    jan_21.append(all[i][9])
#collect ytm for ecery day
year = [0.6,1,1.5,2,2.5,3,3.5,4,4.4,5]
print(jan_10)
plt.plot(year,jan_10)
plt.plot(year,jan_11)
plt.plot(year,jan_12)
plt.plot(year,jan_13)
plt.plot(year,jan_14)
plt.plot(year,jan_17)
plt.plot(year,jan_18)
plt.plot(year,jan_19)
plt.plot(year,jan_20)
plt.plot(year,jan_21)
plt.xlabel('number of years')
plt.ylabel('yield (%)')
plt.title('yield curve')
plt.savefig('ytm1')
#plot ytm


# now we calculate spot rate for Jan 10. assume the accured interest is the same for every day ie. AI on Jan 10 is same on AI on Jan 21 since the coupon payment is too small.
# at march 2022, treat this one as zero coupon bond
def get_spot_rate_0(dirty_price):
    spot_rate_0 = - ny.log(dirty_price/100) / (1/6)
    return spot_rate_0
#get_spot_rate_0(dirty_price_all[101])
spot_0 = []
for i in range(10):
    spot_0_temp = get_spot_rate_0(dirty_price_all[i+100])
    spot_0.append(spot_0_temp)
print(spot_0)
# when t = 1
def get_spot_rate_1(dirty_price):
    spot_rate_1 = lambda s: 100 / ny.exp(s+spot_0[i]/6) + 0.125 / ny.exp(s+spot_0[i]/6) - dirty_price
    return optimize.newton(spot_rate_1,0.05) 
#get_spot_rate_1(dirty_price_all[91])
spot_1 = []
for i in range(10):
    spot_1_temp = get_spot_rate_1(dirty_price_all[i+90])
    spot_1.append(spot_1_temp)
print(spot_1)

# when t = 2
# in the following we calculate t = 3, t = 4 .....t = 10
def get_spot_rate_2(dirty_price):
    for i in range(10):
        spot_rate_2 = lambda s: 100 / ny.exp(s+spot_1[i]+spot_0[i]/6) + 0.875 / ny.exp(s+spot_1[i]+spot_0[i]/6) + 0.875 / ny.exp(spot_1[i]+spot_0[i]/6) - dirty_price
        return optimize.newton(spot_rate_2,0.01) 
spot_2 = []
#dirty_price_all[60]
for i in range(10):
    spot_2_temp = get_spot_rate_2(dirty_price_all[i+60])
    spot_2.append(spot_2_temp)
print(spot_2)

def get_spot_rate_3(dirty_price):
    for i in range(10):
        spot_rate_3 = lambda s: 100 / ny.exp(s+spot_1[i]+spot_2[i]+spot_0[i]/6) + 0.125 / ny.exp(s+spot_1[i]+spot_2[i]+spot_0[i]/6) + 0.125 / ny.exp(spot_1[i]+spot_2[i]+spot_0[i]/6) +0.125/ ny.exp(spot_1[i]+spot_0[i]/6) - dirty_price
        return optimize.newton(spot_rate_3,0.01) 
spot_3 = []

for i in range(10):
    spot_3_temp = get_spot_rate_3(dirty_price_all[i])
    spot_3.append(spot_3_temp)
print(spot_3)

def get_spot_rate_4(dirty_price):
    for i in range(10):
        spot_rate_4 = lambda s: 100 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_0[i]/6) + 1.125 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_0[i]/6) + 1.125 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_0[i]/6)  + 1.125/ ny.exp(spot_1[i]+spot_2[i]+spot_0[i]/6) + 1.125/ ny.exp(spot_1[i]+spot_0[i]/6) - dirty_price
        return optimize.newton(spot_rate_4,0.01) 
spot_4 = []

for i in range(10):
    spot_4_temp = get_spot_rate_4(dirty_price_all[i+70])
    spot_4.append(spot_4_temp)
print(spot_4)

def get_spot_rate_5(dirty_price):
    for i in range(10):
        spot_rate_5 = lambda s: 100 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_0[i]/6) + 0.75 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_0[i]/6) + 0.75 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_0[i]/6)  + 0.75/ ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_0[i]/6) + 0.75/ ny.exp(spot_1[i]+spot_2[i]+spot_0[i]/6) +0.75/ ny.exp(spot_1[i]+spot_0[i]/6)- dirty_price
        return optimize.newton(spot_rate_5,0.01) 
spot_5 = []

for i in range(10):
    spot_5_temp = get_spot_rate_5(dirty_price_all[i+80])
    spot_5.append(spot_5_temp)
print(spot_5)

def get_spot_rate_6(dirty_price):
    for i in range(10):
        spot_rate_6 = lambda s: 100 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_0[i]/6) +0.625 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_0[i]/6)+0.625 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_0[i]/6)+ 0.625 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_0[i]/6)  + 0.625/ ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_0[i]/6) + 0.625/ ny.exp(spot_1[i]+spot_2[i]+spot_0[i]/6) +0.625/ ny.exp(spot_1[i]+spot_0[i]/6)- dirty_price
        return optimize.newton(spot_rate_6,0.01) 
spot_6 = []

for i in range(10):
    spot_6_temp = get_spot_rate_6(dirty_price_all[i+10])
    spot_6.append(spot_6_temp)
print(spot_6)

def get_spot_rate_7(dirty_price):
    for i in range(10):
        spot_rate_7 = lambda s: 100 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_0[i]/6) +0.25 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_0[i]/6)+0.25 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_0[i]/6)+0.25 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_0[i]/6) + 0.25 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_0[i]/6)  + 0.25/ ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_0[i]/6) + 0.25/ ny.exp(spot_1[i]+spot_2[i]+spot_0[i]/6) +0.25/ ny.exp(spot_1[i]+spot_0[i]/6)- dirty_price
        return optimize.newton(spot_rate_7,0.01) 
spot_7 = []

for i in range(10):
    spot_7_temp = get_spot_rate_7(dirty_price_all[i+20])
    spot_7.append(spot_7_temp)
print(spot_7)

def get_spot_rate_8(dirty_price):
    for i in range(10):
        spot_rate_8 = lambda s: 100 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_0[i]/6) +0.125 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_0[i]/6)+0.125 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_0[i]/6)+0.125 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_0[i]/6)+0.125 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_0[i]/6)+ 0.125 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_0[i]/6) + 0.125 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_0[i]/6)   + 0.125/ ny.exp(spot_1[i]+spot_2[i]+spot_0[i]/6) +0.125/ ny.exp(spot_1[i]+spot_0[i]/6)- dirty_price
        return optimize.newton(spot_rate_8,0.01) 
spot_8 = []

for i in range(10):
    spot_8_temp = get_spot_rate_8(dirty_price_all[i+30])
    spot_8.append(spot_8_temp)
print(spot_8)

def get_spot_rate_9(dirty_price):
    for i in range(10):
        spot_rate_9 = lambda s: 100 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_8[i]+spot_0[i]/6) +0.5 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_8[i]+spot_0[i]/6)+0.5 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_8[i]+spot_0[i]/6)+0.5 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_0[i]/6)+0.5 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_0[i]/6)+0.5 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_0[i]/6)+ 0.5 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_0[i]/6) + 0.5 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_0[i]/6)  + 0.5/ ny.exp(spot_1[i]+spot_2[i]+spot_0[i]/6) +0.5/ ny.exp(spot_1[i]+spot_0[i]/6)- dirty_price
        return optimize.newton(spot_rate_9,0.01) 
spot_9 = []

for i in range(10):
    spot_9_temp = get_spot_rate_9(dirty_price_all[i+40])
    spot_9.append(spot_9_temp)
print(spot_9)

def get_spot_rate_10(dirty_price):
    for i in range(10):
        spot_rate_10 = lambda s: 100 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_8[i]+spot_9[i]+spot_0[i]/6) +0.625 / ny.exp(s+spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_8[i]+spot_9[i]+spot_0[i]/6)+0.625 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_8[i]+spot_9[i]+spot_0[i]/6)+0.625 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_8[i]+spot_0[i]/6)+0.625 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_7[i]+spot_0[i]/6)+0.625 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_6[i]+spot_0[i]/6)+0.625 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_5[i]+spot_0[i]/6) + 0.625 / ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_4[i]+spot_0[i]/6)  + 0.625/ ny.exp(spot_1[i]+spot_2[i]+spot_3[i]+spot_0[i]/6) + 0.625/ ny.exp(spot_1[i]+spot_2[i]+spot_0[i]/6) +0.625/ ny.exp(spot_1[i]+spot_0[i]/6)- dirty_price
        return optimize.newton(spot_rate_10,0.01) 
spot_10 = []

for i in range(10):
    spot_10_temp = get_spot_rate_10(dirty_price_all[i+50])
    spot_10.append(spot_10_temp)
print(spot_10)

spot_1_year = []
for i in range(10):
    a = spot_1[i] + spot_2[i] - spot_0[i] / 6
    spot_1_year.append(a)
print(spot_1_year)
s1 = []
s2 = []
s3 = []
s4 = []
s5 = []
s6 = []
s7 = []
s8 = []
s9 = []
s10 = []
spot = (spot_1_year,spot_3,spot_4,spot_5,spot_6,spot_7,spot_8,spot_9,spot_10)
for i in range(9):
    s1.append(spot[i][0])
    s2.append(spot[i][1])
    s3.append(spot[i][2])
    s4.append(spot[i][3])
    s5.append(spot[i][4])
    s6.append(spot[i][5])
    s7.append(spot[i][6])
    s8.append(spot[i][7])
    s9.append(spot[i][8])
    s10.append(spot[i][9])

# since they are expontials, we can just add them up.
# note (spot1+spot2) is the 13 month spot rate we need to subtract one month spot rate
year = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
plt.plot(year,s1, label = 'Jan 10')
plt.plot(year,s2, label = 'Jan 11')
plt.plot(year,s3, label = 'Jan 12')
plt.plot(year,s4, label = 'Jan 13')
plt.plot(year,s5, label = 'Jan 14')
plt.plot(year,s6, label = 'Jan 17')
plt.plot(year,s7, label = 'Jan 18')
plt.plot(year,s8, label = 'Jan 19')
plt.plot(year,s9, label = 'Jan 20')
plt.plot(year,s10, label = 'Jan 21')
plt.legend
plt.ylabel('spot rate for each day')
plt.xlabel('number of years')
plt.title('spot curve')
plt.savefig('spot')
fwd_temp = (jan_10, jan_11, jan_12,jan_13,jan_14,jan_17,jan_18,jan_19,jan_20,jan_21)
jan_10_fwd = []
jan_11_fwd = []
jan_12_fwd = []
jan_13_fwd = []
jan_14_fwd = []
jan_17_fwd = []
jan_18_fwd = []
jan_19_fwd = []
jan_20_fwd = []
jan_21_fwd = []
# calculate foward rate using ytm and spot rate
jan_10_fwd.append(((1+jan_10[1]/100) ** 4 / ny.exp(spot_1_year[0]) - 1 ))
jan_10_fwd.append((((1+jan_10[1]/100) ** 6 / ny.exp(spot_1_year[0])) ** 0.5 -1))
jan_10_fwd.append((((1+jan_10[1]/100) ** 8 / ny.exp(spot_1_year[0]))  ** (1/3)-1))
jan_10_fwd.append((((1+jan_10[1]/100) ** 10 / ny.exp(spot_1_year[0]))  **(0.25)-1))
print(jan_10_fwd)
jan_11_fwd.append(((1+jan_11[1]/100) ** 4 / ny.exp(spot_1_year[0]) - 1 ))
jan_11_fwd.append((((1+jan_11[1]/100) ** 6 / ny.exp(spot_1_year[0])) ** 0.5 -1))
jan_11_fwd.append((((1+jan_11[1]/100) ** 8 / ny.exp(spot_1_year[0]))  ** (1/3)-1))
jan_11_fwd.append((((1+jan_11[1]/100) ** 10 / ny.exp(spot_1_year[0]))  **(0.25)-1))
print(jan_11_fwd)
jan_12_fwd.append(((1+jan_12[1]/100) ** 4 / ny.exp(spot_1_year[0]) - 1 ))
jan_12_fwd.append((((1+jan_12[1]/100) ** 6 / ny.exp(spot_1_year[0])) ** 0.5 -1))
jan_12_fwd.append((((1+jan_12[1]/100) ** 8 / ny.exp(spot_1_year[0]))  ** (1/3)-1))
jan_12_fwd.append((((1+jan_12[1]/100) ** 10 / ny.exp(spot_1_year[0]))  **(0.25)-1))
print(jan_12_fwd)
jan_13_fwd.append(((1+jan_13[1]/100) ** 4 / ny.exp(spot_1_year[0]) - 1 ))
jan_13_fwd.append((((1+jan_13[1]/100) ** 6 / ny.exp(spot_1_year[0])) ** 0.5 -1))
jan_13_fwd.append((((1+jan_13[1]/100) ** 8 / ny.exp(spot_1_year[0]))  ** (1/3)-1))
jan_13_fwd.append((((1+jan_13[1]/100) ** 10 / ny.exp(spot_1_year[0]))  **(0.25)-1))
print(jan_13_fwd)
jan_14_fwd.append(((1+jan_14[1]/100) ** 4 / ny.exp(spot_1_year[0]) - 1 ))
jan_14_fwd.append((((1+jan_14[1]/100) ** 6 / ny.exp(spot_1_year[0])) ** 0.5 -1))
jan_14_fwd.append((((1+jan_14[1]/100) ** 8 / ny.exp(spot_1_year[0]))  ** (1/3)-1))
jan_14_fwd.append((((1+jan_14[1]/100) ** 10 / ny.exp(spot_1_year[0]))  **(0.25)-1))
print(jan_14_fwd)
jan_17_fwd.append(((1+jan_17[1]/100) ** 4 / ny.exp(spot_1_year[0]) - 1 ))
jan_17_fwd.append((((1+jan_17[1]/100) ** 6 / ny.exp(spot_1_year[0])) ** 0.5 -1))
jan_17_fwd.append((((1+jan_17[1]/100) ** 8 / ny.exp(spot_1_year[0]))  ** (1/3)-1))
jan_17_fwd.append((((1+jan_17[1]/100) ** 10 / ny.exp(spot_1_year[0]))  **(0.25)-1))
print(jan_17_fwd)
jan_18_fwd.append(((1+jan_18[1]/100) ** 4 / ny.exp(spot_1_year[0]) - 1 ))
jan_18_fwd.append((((1+jan_18[1]/100) ** 6 / ny.exp(spot_1_year[0])) ** 0.5 -1))
jan_18_fwd.append((((1+jan_18[1]/100) ** 8 / ny.exp(spot_1_year[0]))  ** (1/3)-1))
jan_18_fwd.append((((1+jan_18[1]/100) ** 10 / ny.exp(spot_1_year[0]))  **(0.25)-1))
print(jan_18_fwd)
jan_19_fwd.append(((1+jan_19[1]/100) ** 4 / ny.exp(spot_1_year[0]) - 1 ))
jan_19_fwd.append((((1+jan_19[1]/100) ** 6 / ny.exp(spot_1_year[0])) ** 0.5 -1))
jan_19_fwd.append((((1+jan_19[1]/100) ** 8 / ny.exp(spot_1_year[0]))  ** (1/3)-1))
jan_19_fwd.append((((1+jan_19[1]/100) ** 10 / ny.exp(spot_1_year[0]))  **(0.25)-1))
print(jan_19_fwd)
jan_20_fwd.append(((1+jan_20[1]/100) ** 4 / ny.exp(spot_1_year[0]) - 1 ))
jan_20_fwd.append((((1+jan_20[1]/100) ** 6 / ny.exp(spot_1_year[0])) ** 0.5 -1))
jan_20_fwd.append((((1+jan_20[1]/100) ** 8 / ny.exp(spot_1_year[0]))  ** (1/3)-1))
jan_20_fwd.append((((1+jan_20[1]/100) ** 10 / ny.exp(spot_1_year[0]))  **(0.25)-1))
print(jan_20_fwd)
jan_21_fwd.append(((1+jan_21[1]/100) ** 4 / ny.exp(spot_1_year[0]) - 1 ))
jan_21_fwd.append((((1+jan_21[1]/100) ** 6 / ny.exp(spot_1_year[0])) ** 0.5 -1))
jan_21_fwd.append((((1+jan_21[1]/100) ** 8 / ny.exp(spot_1_year[0]))  ** (1/3)-1))
jan_21_fwd.append((((1+jan_21[1]/100) ** 10 / ny.exp(spot_1_year[0]))  **(0.25)-1))
print(jan_21_fwd)
fwd = ['1yr-1yr', '1yr-2yr' , '1yr-3yr' , '1yr-4yr']
plt.plot(fwd,jan_10_fwd)
plt.plot(fwd,jan_11_fwd)
plt.plot(fwd,jan_12_fwd)
plt.plot(fwd,jan_13_fwd)
plt.plot(fwd,jan_14_fwd)
plt.plot(fwd,jan_17_fwd)
plt.plot(fwd,jan_18_fwd)
plt.plot(fwd,jan_19_fwd)
plt.plot(fwd,jan_20_fwd)
plt.plot(fwd,jan_21_fwd)
plt.ylabel('forward rates')
plt.savefig('fwd')
# 1st row of matrix
mat_1 = []
for i in range(9):
    a = ny.log(jan_10[i+1]/jan_10[i])
    mat_1.append(a)
mat_2 = []
for i in range(9):
    a = ny.log(jan_11[i+1]/jan_10[i])
    mat_2.append(a)
mat_3 = []
for i in range(9):
    a = ny.log(jan_12[i+1]/jan_12[i])
    mat_3.append(a)
mat_4 = []
for i in range(9):
    a = ny.log(jan_13[i+1]/jan_13[i])
    mat_4.append(a)
mat_5 = []
for i in range(9):
    a = ny.log(jan_14[i+1]/jan_14[i])
    mat_5.append(a)
mat = ny.zeros([5, 9])
mat[0] = mat_1
mat[1] = mat_2
mat[2] = mat_3
mat[3] = mat_4
mat[4] = mat_5
ytm_cov = ny .cov (mat)
print(ytm_cov)
ytm_eigen_val = la.eigvals(ytm_cov)
print(ytm_eigen_val)
ytm_eigen_vec = la.eig(ytm_cov)
print(ytm_eigen_vec)




fwd_date = (jan_10_fwd,jan_11_fwd,jan_12_fwd,jan_13_fwd,jan_14_fwd,jan_17_fwd,jan_18_fwd,jan_19_fwd,jan_20_fwd,jan_21_fwd)
one_one = []
one_two = []
one_three = []
one_four = []
for i in range(10):
    one_one.append(fwd_date[i][0])
    one_two.append(fwd_date[i][1])
    one_three.append(fwd_date[i][2])
    one_four.append(fwd_date[i][3])

mat_a = []
for i in range(9):
    a = ny.log(one_one[i+1]/one_one[i])
    mat_a.append(a)
mat_b = []
for i in range(9):
    a = ny.log(one_two[i+1]/one_two[i])
    mat_b.append(a)
mat_c = []
for i in range(9):
    a = ny.log(one_three[i+1]/one_three[i])
    mat_c.append(a)
mat_d = []
for i in range(9):
    a = ny.log(one_four[i+1]/one_four[i])
    mat_d.append(a)
mat2 = ny.zeros([4, 9])
mat2[0] = mat_a
mat2[1] = mat_b
mat2[2] = mat_c
mat2[3] = mat_d
mat2
fwd_cov = ny.cov(mat2)
fwd_eigen_val = la.eigvals(fwd_cov)
print(fwd_eigen_val)
fwd_eigen_vec = la.eig(fwd_cov)
print(fwd_eigen_vec)