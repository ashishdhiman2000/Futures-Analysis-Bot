NSE Futures Analysis Bot:
- Downloads NSE Futures Bhavcopy for today.
- Based on downloaded files ,computes change in OI wrt previous day.
- Saves Change in OI data in form of a CSV file corresponding to no. of days of data available.
- Useful to choose few(<10) stocks among all available stocks(>150) that are likely to show considerable movement based on change in OI.

How to Use:
- Make sure you have these python libraries installed :pandas ,numpy ,jugaad-data ,win10toast.
- Change parent directory in line 20 to the directory where you want to save the files.
![image](https://user-images.githubusercontent.com/37515765/134634533-e8cf674f-9637-45f4-96b6-6571b614f56d.png) 

Ready to run!

Using windows Task Scheduler,this Script can be run automatically daily at a fixed time after the data is released on NSE.

