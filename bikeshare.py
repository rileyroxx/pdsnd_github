import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
#create lists to check for user inputs in code blocks.
city_list = []
month_list = ['jan','feb','mar','apr','may','jun''all']
day_list = ['mon','tue','wed','thu','fri','sat','sun','all']

#Day dictionary with abbreviated form, unique number and full form.
#Use this to cycle through later on to get a nice output instead of just a day number.
day_dict= {'mon':[0, 'Monday'],
           'tue':[1, 'Tuesday'], 
           'wed':[2, 'Wednesday'], 
           'thu':[3, 'Thursday'], 
           'fri':[4, 'Friday'], 
           'sat':[5, 'Saturday'],
           'sun':[6, 'Sunday']}
#Month dictionary with abbreviated form, unique number and full form.
#Use this to cycle through later on to get a nice output instead of just a month number.
month_dict = {'jan':[1, 'January'],
              'feb':[2, 'February'],
              'mar':[3, 'March'],
              'apr':[4, 'April'],
              'may':[5, 'May'],
              'jun':[6, 'June']}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    """
    Use While True loops to manage customer inputs. 
    """
    
    print('Hello! Let\'s explore some US bikeshare data!\nYou can exit at any time by pressing CTRL+C.')
    print("Please be aware that we have limited your month selection to Jan through Jun. This is due to there being no data outside of this range. Thank you")
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        try:
            city = str(input('\nPlease Select your city (Chicago, New York or Washington): ').lower())
            print("User Entered: {}\n".format(city))
            if city.lower() in city_list:
                break
            else:
                print("Not in List. Please Try again.\n")
        except KeyboardInterrupt:
            print("\nYou are now exiting the Program")
            sys.exit()

    while True:
        try:
            month = str(input('Please select your month.\nYou have multiple options; All for all months or Jan, Feb, Mar, Apr, May, Jun: '))
            print("User Entered: {}\n".format(month))
            if month.lower() in month_list:
                month = month.lower()
                break
            else:
                print("Not in List. Please Try again.\n")
            #break
        except KeyboardInterrupt:
            print("\nExiting the Program")
            sys.exit()
    
    while True:
        try:
            day = str(input('Please select your day.\nYou have multiple options; All for all days or Mon, Tue, Wed, Thu, Fri, Sat, Sun: '))
            print("User Entered: {}\n".format(day))
            if day.lower() in day_list:
                day=day.lower()
                break
            else:
                print("Not in List. Please Try again.\n")
            #break
        except KeyboardInterrupt:
            print("\nExiting the Program")
            sys.exit()
    print("\nYou selected City: {}, Month: {}, Day(s): {}.\n".format(city, month, day))
    return city, month, day
    
#Function to load the data
def load_data(city,month,day):
    """Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day"""
    #Manipulate some data to get required data types (eg months, start times etc). Create them as new columns.
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time']) 
    df['Start Date'] = [d.date() for d in df['Start Time']]
    df['Start Day of Week'] = [d.weekday() for d in df['Start Date']] 
    df['Start Month'] = df['Start Time'].dt.month 
    df['hour'] = df['Start Time'].dt.hour
    
# find the most common hour (from 0 to 23)
    
    #if statement to filter whether or not a specific day filter was set.
    if day != 'all':
        for dayname, daynum in day_dict.items(): #cycle through dictionary to find full day name, not abbreviated mon,tue etc.
            if dayname == day:
                print("day name = {}".format(dayname))
                print("day number = {}".format(daynum[0]))
                day_filter = df['Start Day of Week'] == daynum[0] #create boolean decision for whether or not we have the right day.
                df = df[day_filter]
    #if statement to filter whether or not a specific month filter was set.
    if month != 'all':
        for monthname, monthnum in month_dict.items(): #cycle through dictionary to find full day name, not abbreviated mon,tue etc.
            if monthname == month:
                print("month name = {} input {}".format(monthname,month))
                print("month number = {}".format(monthnum[0]))
                month_filter = df['Start Month'] == monthnum[0] #create boolean decision for whether or not we have the right day.
                df = df[month_filter]
                print(df.head())
    return df    
    
def time_stats(df,month,day):
    """
    No nulls to manipulate but, output did need some tidying up due to options (all months or select months).
    When they select all, get the most popular month (this returns a number), then loop through dictionary to get full month name for output.
    Same as above for days. 
    """
    #Displays statistics on the most frequent times of travel.
    day_name = ""
    month_name = ""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        popular_month =  df['Start Month'].mode()[0]
        for monthname, monthnum in month_dict.items(): #cycle through dictionary to find full day name, not abbreviated mon,tue etc.
            for key in monthnum:
                if key == popular_month:
                    month_name = (monthnum[1])
        #print output with full Month name 
        print("This is the most popular month for your selection: {}. This is {}".format(popular_month,month_name))    
    else:
        for monthname, monthnum in month_dict.items(): #cycle through dictionary to find full month name, not abbreviated jan, feb etc.
            if month == monthname:
                monthname = (monthnum[1])
                break
        #print output with full Month name 
        print("You have chosen the month: {}".format(monthname)) 

    # TO DO: display the most common day of week
    if day == 'all':
        popular_day =  df['Start Day of Week'].mode()[0]
        for dayname, daynum in day_dict.items(): #cycle through dictionary to find full day name, not abbreviated mon,tue etc.
            for key in daynum:
                if key == popular_day:
                    day_name = daynum[1]
        #print output with full day name 
        print("This is the most popular day for your selection: {}. This is a {}".format(popular_day,day_name))      
    else:
        for dayname, daynum in day_dict.items(): #cycle through dictionary to find full day name, not abbreviated mon,tue etc.
            if day == dayname:
                day_name = (daynum[1])
                break
        #print output with full Month name 
        print("You have chosen the day: {}".format(day_name))         
        
    # TO DO: display the most common start hour
    popular_hour =  df['hour'].mode()[0]
    print("This is the most popular hour for your selection: {}.".format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    #Displays statistics on the most popular stations and trip.
    """
    This is straightforward, no nulls to manipulate, just pull required data.
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The Most Commonly Used Start Station, for your selection, is: {}".format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("The Most Commonly Used End Station, for your selection, is: {}".format(df['End Station'].mode()[0]))   

    # TO DO: display most frequent combination of start station and end station trip
    df['Start to End Trip'] = df['Start Station'] + " to " + df['End Station'] #create new column to create a journey
    print("The most commonly used start and end station, for your selection, is: {}".format(df['Start to End Trip'].mode()[0])) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    #Displays statistics on the total and average trip duration.
    """
    This is straightforward, no nulls to manipulate, just pull required data.
    """

    print('\nCalculating Trip Durations...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total travel time for your selections is: {}".format(df['Trip Duration'].sum))

    # TO DO: display mean travel time
    print("The average travel time for your selections is: {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def user_stats(df,city):
    #Displays statistics on bikeshare users.
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    """
    get rid of nulls and then work out the values required.
    Use group by into a dataframe and then loop the output to ensure it looks nice.
    """
    user_filter = df['User Type'].notnull()
    df_user_filter = df[user_filter]
    user_filter_df = pd.DataFrame(df_user_filter.groupby(['User Type'])['User Type'].count())
    print("\nThe User Type Counts are as follows:")
    for i in range(user_filter_df.size):
        print(user_filter_df.index[i],":",user_filter_df.iloc[i][0])
    
    # TO DO: Display counts of gender
    """
    Check for Washington as it has no gender data.
    get rid of nulls and then work out the values required.
    Use group by into a dataframe and then loop the output to ensure it looks nice.
    """
    if city.lower() != 'washington':
        gender_filter = df['Gender'].notnull()
        df_gen_filter = df[gender_filter]
        gender_df = pd.DataFrame(df_gen_filter.groupby(['Gender'])['Gender'].count())
        print("\nThe gender Counts are as follows:")
        for i in range(gender_df.size):
            print(gender_df.index[i],":",gender_df.iloc[i][0])
    else:
        print("\nUnfortunately {} does not have any data for Gender.".format(city))
    
    # TO DO: Display earliest, most recent, and most common year of birth
    """
    Check for Washington as it has no birth year data.
    get rid of nulls and then work out the values required.
    """
    if city.lower() != 'washington':
        birthyear_filter = df['Birth Year'].notnull()
        df_birthyear = df[birthyear_filter]
        print("\nThe Earliest Birth Year, for your selection, is: {}".format(int(df_birthyear['Birth Year'].min())))   
        print("The most recent Birth Year, for your selection, is: {}".format(int(df_birthyear['Birth Year'].max())))   
        print("The Most Common Birth Year, for your selection, is: {}".format(int(df_birthyear['Birth Year'].mode()[0])))       

    else:
        print("\nUnfortunately {} does not have any data for Birth Year.".format(city))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def data_scroll(city):
    """
    Code block uses city to read_csv and pull un-edited data.
    Next steps: set up variables. 
    Enter While loop and ask if user wants to scroll through data.
    Yes: create a list of the 5 rows in the dataframe. Iterate the variables by 5
    If they get to the end, print last output and break to main.
    No: Break and exit to main.
    
    """
    df1 = pd.read_csv(CITY_DATA[city])
    aa = df1.shape
    c = aa[0]
    a = 0
    b = 5
    i = 0
    while True:
        try:
            answer = str(input('Would you like to scroll through the dataset?(Yes/No): '))
            print("User Entered: {}\n".format(answer))
            if answer.lower() == 'yes':
                scroll_list = [] #reset scroll_list each time as we iterate through code block
                while i < b:
                    trip_list = list(df1.iloc[i].values) #Create a list of row of index i
                    trip_num = str("Trip "+str(i+1)) #Add a Trip Number item.
                    trip_list.insert(0, trip_num)
                    scroll_list.append(trip_list) 
                    i += 1
                if b + 5 > c:
                    for trips in scroll_list:
                        print(trips)
                    print("This is the last output. Script will now return to restart option.\n")
                    break
                else:
                    for trips in scroll_list:
                        print(trips)
                    a += 5
                    b += 5
                continue
            elif answer.lower() == 'no':
                print("Ok, exiting data view mode")
                break
            else:
                print("Not in List. Please choose yes or no.\n")
        except KeyboardInterrupt:
            print("\nExiting the Program")
            sys.exit()
    
def main():
    for city in CITY_DATA: #Loop enters dictionary into a city list
        city_list.append(city)
    while True:
        city, month, day = get_filters()
        df = load_data(city,month,day)
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        data_scroll(city) #create data scroll function to run at end on raw data with no changes.
        print("Printing Output: City selected: {}, Month selected: {}, Day selected: {}. Datafile used: {}.".format(city,month,day,CITY_DATA[city]))
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt: #Allow for exit at any time.
            print("\nExiting the Program")
            sys.exit()
