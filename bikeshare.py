import datetime
import time, calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'febuary', 'march', 'april', 'may', 'june', 'all']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']







def get_filters():


       
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\n')
    print('Hello! Let\'s explore some US bikeshare data!')
    print('\n')
    # get user input for city (chicago, new york city, washington). 
    while True:
        city = str(input('Would you like to see data for Chicago, new york city, or Washington?'))
        if city in CITY_DATA.keys():
            print ('\n' 'You have chosen', city.title(), 'as your city.')  
            print('\n')
            break
        else: 
            print('\n')
            print ('Pleasure be sure you entered either Chicago, New York City or Washinton')
            print('\n') 

    while True:
       
        load_data = str(input('would you like to see the raw data? please input yes or no')) 

        if load_data == 'yes':
            df = pd.read_csv(CITY_DATA[city]) 
            start_row, end_row = 0, 10 
                    
            while end_row <= df['Start Time'].index[-1] and load_data == 'yes':
                df0 = pd.read_csv(CITY_DATA[city]).iloc[start_row:end_row]
                print(df0)
                start_row += 10
                end_row += 10
                load_data = str(input('would you like to see the next ten lines of raw data? please input yes or no'))  
            else:
                break                     
        elif load_data == 'no' :
            break      
        else:
            print('please enter yes or no')
                
    while True:
        p_selector = (input('would you like your data by day or month')) 
        if p_selector == 'month' or p_selector == 'day':
            break
        else: 
            print('please input day or month')
        

    if p_selector == 'month':
        day = 'all'                 
    # get user input for month (all, january, february, ... , june)
        while True:
            month = str(input('Which month - January, February, March, April, May, June, or all')) 
            if month in MONTHS:
                print('You have choosen', month.title(), 'as your month')
                break
            else:
                print('please select month from January to June or all')
    # else get user input for day of week (all, monday, tuesday, ... sunday)
    else:
        month = 'all'
        while True:        
            day = str(input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All?'))                
            if day in DAYS:
                print('You have choosen', day.title(), 'as your prefeered day' )                    
                break               
            else:
                print('\n')
                print('Please enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All') 
                print('\n')
    


    print('\n', 'You have chosen to view data for city:', city, 'month/s:', month, 'and day/s:', day)
    print('-'*80)
    return city, month, day

             


def load_data(city, month, day):
    
    """
    Loads data for the specified city and filters by month and day .

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day

    """
      # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])



    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])    

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday   
    df['hour'] = df['Start Time'].dt.hour 
    
    # filter by month 
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month =  MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month] 

        # filter by day of week 
    if day != 'all':
        # filter by day of week to create the new dataframe
        month =  DAYS.index(month) + 1
        df = df[df['day_of_week'] == day]
    return df
  
def time_stats(df):
    
    start_time = time.time()
    """Displays statistics on the most frequent times of travel."""
        # display the most common month
    most_com_month = df['month'].mode()[0]        
    print("The most common month is: ", calendar.month_name[most_com_month])
   
    #display the most common day
    most_com_day = df['day_of_week'].value_counts().idxmax()
    print("The most common day is: ", calendar.day_name[most_com_day])         
   
    # display the most common start hour
    most_common_hr = df['hour'].value_counts().idxmax()
    print("The most common hour is :", most_common_hr)
   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    maxSS = df['Start Station'].value_counts().idxmax()
    print('Most commonly used start station: ', maxSS)

    # display most commonly used end station
    maxES = df['End Station'].value_counts().idxmax()
    print('Most commonly used end station: ', maxES)

    # display most frequent combination of start station and end station trip
    frequent_trip = df[['Start Station', 'End Station']].value_counts().idxmax()
    print('The most commonly used start station and end station {}:'.format(frequent_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    time_traveld = df['Trip Duration'].sum()
    time_traveldhr = time_traveld % 3600
    time_traveldmin = (time_traveld - (time_traveldhr*3600))%60
    time_traveldsec = (time_traveld - (time_traveldhr*3600) - (time_traveldmin*60))%60
    print('Total travel time: {} hours {} minutes {} seconds'.format(time_traveldhr, time_traveldmin, time_traveldsec) )  


    # display mean travel time
    mean_traveld = df['Trip Duration'].mean()
    print('Mean travel time', mean_traveld)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Counts of user types {}'.format(user_type))
    print('')

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('Counts of gender {}'.format(gender_count))
    except:
        print('\n', "There is no 'Gender' column in this file. ")

    # Display earliest, most recent, and most common year of birth
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
