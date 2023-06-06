import os
from os.path import exists
from collections import defaultdict
from datetime import datetime
import csv

# == INSTRUCTIONS ==
#
# Below, you'll find lots of incomplete functions.
#
# Your job: Implement each function so that it does its job effectively.
#
# Tips:
# * Use the material, Python Docs and Google as much as you want
#
# * A warning: the data you are using may not contain quite what you expect;
#   cleaning data (or changing your program) might be necessary to cope with
#   "imperfect" data

# == EXERCISES ==

# Purpose: return a boolean, False if the file doesn't exist, True if it does
# Example:
#   Call:    does_file_exist("nonsense")
#   Returns: False
#   Call:    does_file_exist("AirQuality.csv")
#   Returns: True
# Notes:
# * Use the already imported "os" module to check whether a given filename exists

def does_file_exist(filename):
    if os.path.exists(filename):
        return True
    else:
        return False
    

# Purpose: get the contents of a given file and return them; if the file cannot be
# found, return a nice error message instead
# Example:
#   Call: get_file_contents("AirQuality.csv")
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;[...]
#     [...]
#   Call: get_file_contents("nonsense")
#   Returns: "This file cannot be found!"
# Notes:
# * Learn how to open file as read-only
# * Learn how to close files you have opened
# * Use readlines() to read the contents
# * Use should use does_file_exist()

def get_file_contents(filename):
    if does_file_exist(filename):
        with open(filename, 'r') as my_file: #auto closes file
            content = my_file.readlines() #creates list with all lines from file
            header = content[0].strip() #remove end of line with strip
            body = content[1:]
        return header, body
    return "This file cannot be found!"


# Purpose: fetch Christmas Day (25th December) air quality data rows, and if
# boolean argument "include_header_row" is True, return the first header row
# from the filename as well (if it is False, omit that row)
# Example:
#   Call: christmas_day_air_quality("AirQuality.csv", True)
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
#   Call: christmas_day_air_quality("AirQuality.csv", False)
#   Returns:
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
# Notes:
# * should use get_file_contents() - N.B. as should any subsequent
# functions you write, using anything previously built if and where necessary

def christmas_day_air_quality(filename, include_header_row):
    header, body = get_file_contents(filename)
    result = []
    for line in body:
        if "25/12/2004" in line:
            result.append(line)
    if include_header_row:
        return [header] + result
    else:
        return result


# Purpose: fetch Christmas Day average of "PT08.S1(CO)" values to 2 decimal places
# Example:
#   Call: christmas_day_average_air_quality("AirQuality.csv")
#   Returns: 1439.21
# Data sample:
# Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH;;
# 10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;13,6;48,9;0,7578;;

def christmas_day_average_air_quality(filename):
    contents = christmas_day_air_quality(filename, False)
    value = 0
    for data_row in contents:
        col = data_row.split(';') #split string into seperate columns
        if col[3]:
            value += int(col[3]) #get 3rd col and convert to int
    result = value / len(contents)
    return (round(result, 2))



# Purpose: scrape all the data and calculate average values for each of the 12 months
#          for the "PT08.S1(CO)" values, returning a dictionary of keys as integer
#          representations of months and values as the averages (to 2 decimal places)
# Example:
#   Call: get_averages_for_month("AirQuality.csv")
#   Returns: {1: 1003.47, [...], 12: 948.71}
# Notes:
# * Data from months across multiple years should all be averaged together

def get_averages_for_month(filename):
    header, body = get_file_contents(filename)
    my_dict = defaultdict(list) #defaultdict sets empty list as default value
    for line in body:
        col = line.strip().split(';')
        date, values = col[0], col[3]
        if date:  # skip lines without a date
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            my_dict[date_obj.month].append(float(values)) #key = month, values = PTO8.S1(CO) for each month
    
    for month in my_dict: #get average
        avg_val = sum(my_dict[month]) / len(my_dict[month])
        my_dict[month] = round(avg_val, 2)
    
    return my_dict

# Purpose: write only the rows relating to March (any year) to a new file, in the same
# location as the original, including the header row of labels
# Example
#   Call: create_march_data("AirQuality.csv")
#   Returns: nothing, but writes header + March data to file called
#            "AirQualityMarch.csv" in same directory as "AirQuality.csv"

def create_march_data(filename):
    header, body = get_file_contents(filename)
    with open("AirQualityMarch.csv", 'w') as file:
        file.write(header.strip() + "\n")
        for line in body:
            col = line.strip().split(';')
            date = col[0]
            if date:
                date_obj = datetime.strptime(date, '%d/%m/%Y')
            if date_obj.month == 3:
                file.write(line) #adds each line onto seperate row
    return None


    

# Purpose: write monthly responses files to a new directory called "monthly_responses",
# in the same location as AirQuality.csv, each using the name format "mm-yyyy.csv",
# including the header row of labels in each one.
# Example
#   Call: create_monthly_responses("AirQuality.csv")
#   Returns: nothing, but files such as monthly_responses/05-2004.csv exist containing
#            data matching responses from that month and year

def create_monthly_responses(filename):
    new_dict = defaultdict(list)
    new_dir = 'monthly_responses'
    os.makedirs(new_dir, exist_ok=True) #create dir if it doesn't exist
    header, body = get_file_contents(filename)
    for line in body:
        col = line.strip().split(';')
        date = col[0]
        if date:
            date_obj = datetime.strptime(date, '%d/%m/%Y')
            new_dict[date_obj.strftime('%m-%Y')].append(col) #strftime to reformat datetime object
    for unique_date in new_dict:
        file_path = os.path.join(new_dir, f"{unique_date}.csv") #create path
        if not os.path.exists(file_path): #if file dpesn't exist, write file with header
            with open(file_path, "w") as file:
                writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_NONE) #csv writer object
                writer.writerow(header.split(';'))
                writer.writerows(new_dict[unique_date])
        else: #else append so file isn't overwritten
            with open(file_path, "a") as file:
                writer.writerows(new_dict[unique_date])
    return None
        
