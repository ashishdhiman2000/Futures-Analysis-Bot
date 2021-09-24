# Code to download csv
from datetime import date
from datetime import datetime
from datetime import timedelta           
from jugaad_data.nse import bhavcopy_save,bhavcopy_fo_save
# from pynse import *
from win10toast import ToastNotifier
import os
print("Futures data bot")
#Notification for 3 sec before running the script
toast = ToastNotifier()
toast.show_toast('Futures_data_bot','Task:Automated data download',duration = 3)
#get today date month and year
today_date = date.today() #- timedelta(2)
year = today_date.year
month = today_date.month
day = today_date.day

#create new folder for new month
parent_dir = r"C:\Users\ashis\Desktop\Stock\fo_stock\\"
directory = str(month)
path = os.path.join(parent_dir,directory)
if day == 1:
    os.mkdir(path)
    
   
# nse = Nse()
# df = nse.bhavcopy_fno(date(year,month,day))
#get directory path of latest month 
path,dirs,files = next(os.walk(r"C:\Users\ashis\Desktop\Stock\fo_stock\\"))
path = r"C:\Users\ashis\Desktop\Stock\fo_stock\\"+dirs[len(dirs)-1]
#get data if available
try:
    # df.to_csv(path)
    bhavcopy_fo_save(date(year,month,day),path)
    print("{}-{}-{} Done".format(int(day),int(month),int(year)))
except:
    print('Data not available for :{}-{}-{}'.format(int(day),int(month),int(year)))

print("Download Task Complete")



#Code to create and save data.csv
import pandas as pd
import numpy as np
####################
#1st part of program
import time
start = time.time()
# Get directory names inside fo_stock directory
path_1,dirs_1,files_1 = next(os.walk(r"C:\Users\ashis\Desktop\Stock\fo_stock\\"))
# store file names in latest month directory available in fo_stock directory
path,dirs,files = next(os.walk(r"C:\Users\ashis\Desktop\Stock\fo_stock\\"+dirs_1[len(dirs_1)-1]))
file_count = len(files)
#df_list stores list of all data frames corresponding to each csv file 
df_list = []
for i in range(file_count):
    temp_df = pd.read_csv(r"C:\Users\ashis\Desktop\Stock\fo_stock\\"+dirs_1[len(dirs_1)-1]+"\\"+files[i])
    df_list.append(temp_df)
for stock in df_list:
    stock.set_index("SYMBOL",inplace = True)
#stock_list is list of unique elements in SYMBOL column(index) of 1st DataFrame(Same for all others)
a = np.array(df_list[len(df_list)-1].index.to_list())
stock_list = list(np.unique(a))
oi_list = []
price = []
timestamp_list = []
for stock in df_list:
    symbol = stock_list[0]
    #symbol data is data frame of rows for which SYMBOL column entry is symbol
    symbol_data = stock.loc[symbol]           
    try:
        #Only include data for FUTSTK in lists of OI and Price
        change_in_oi = symbol_data[symbol_data["INSTRUMENT"]== "FUTSTK"].loc[:,"CHG_IN_OI"].sum()
        oi =symbol_data[symbol_data["INSTRUMENT"]== "FUTSTK"].loc[:,"OPEN_INT"].sum()
        if oi == 0:
            perc = 0
        else:
            perc = change_in_oi/oi
        oi_list.append(perc*100)
        price.append(symbol_data[symbol_data["INSTRUMENT"]== "FUTSTK"].loc[:,"CLOSE"].tolist()[0])
        timestamp_list.append(stock.TIMESTAMP[0])
    except:
        continue
#Create a DataFrame 
df = pd.DataFrame([timestamp_list,oi_list,price]).transpose()
df.columns = ["TIMESTAMP","%_CHG_IN_OI","PRICE"]
df.set_index("TIMESTAMP",inplace = True)
#Arrange order of the dates 
from datetime import datetime
dates = df.index.tolist()
df.index = pd.to_datetime(df.index)
df = df.sort_values(by="TIMESTAMP")
#Calculate Price change(using data for 1st date = 0 for reference)
price_change = [0]
for i in range(len(df.index)-1):
    price_change.append(df.iloc[i+1][1] - df.iloc[i][1])
df["PRICE_CHANGE"] = price_change
df.drop(["PRICE","PRICE_CHANGE"],axis = 1,inplace=True)
df = pd.DataFrame(df.stack())
###################
#2nd part of program
fut_list = []
for symbol in stock_list:
    stock_symbol = symbol
    oi_list = []
    price_list = []
    timestamp_list = []
    test = 0
    #test variable is to filter symbol which don't have FUTSTK data
    for stock in df_list:
        #some stocks are missing in some dates so skip that(data is NAN for those days)
        try:
            symbol_data = stock.loc[stock_symbol]
        except:
            continue     
        try:
            #Only include data for FUTSTK in lists of OI and Price
            change_in_oi = symbol_data[symbol_data["INSTRUMENT"]== "FUTSTK"].loc[:,"CHG_IN_OI"].sum()
            oi =symbol_data[symbol_data["INSTRUMENT"]== "FUTSTK"].loc[:,"OPEN_INT"].sum()
            if oi == 0:
                perc = 0
            else:
                perc = change_in_oi/oi
            oi_list.append(perc*100)
            price_list.append(symbol_data[symbol_data["INSTRUMENT"]== "FUTSTK"].loc[:,"CLOSE"].tolist()[0])
            timestamp_list.append(stock.TIMESTAMP[0])
        except:
            test+=1
            continue
    if test == 0:
        #Create a DataFrame
        df_ = pd.DataFrame([timestamp_list,oi_list,price_list]).transpose()
        df_.columns = ["TIMESTAMP","%_CHG_IN_OI","PRICE"]
        df_.set_index("TIMESTAMP",inplace = True)
        #Arrange order of the dates 
        from datetime import datetime
        dates = df_.index.tolist()
        df_.index = pd.to_datetime(df_.index.tolist())
        df_ = df_.sort_index(axis = 0)
        #Calculate Price change(using data for 1st date = 0 for reference)
        price_change = [0]
        for i in range(len(df_.index)-1):
            price_change.append(df_.iloc[i+1][1] - df_.iloc[i][1])
        df_["PRICE_CHANGE"] = price_change
        df_.drop(["PRICE","PRICE_CHANGE"],axis = 1,inplace=True)
        df_ = pd.DataFrame(df_.stack())
        #create a new column in df (created in 1st part) corresponding to symbol with data of df_
        df[symbol] = df_[0]
data = df.transpose()
data.drop(index = 0 ,inplace = True)
data.to_csv(r"C:\Users\ashis\Desktop\data.csv")
end = time.time()
print("Time taken to run the code :{}\n".format(end - start))
print("Data.csv created") 

input('Press Enter to exit')