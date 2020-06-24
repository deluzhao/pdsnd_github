import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Gets user input for the chosen city (chicago, new york city, washington). Uses a while loop to force a valid input.
    city = ""
    while (city != "chicago" and city != "new york city" and city != "washington"):
        city = input("Which city would you like to explore? ").lower()
        if (city != "chicago" and city != "new york city" and city != "washington"):
            print("Your input was invalid. Please try again. ")
    # Gets user input for month (all, january, february, ... , june).
    if (city == 'new york city'):
        city = 'new_york_city'
    mlist = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = ""
    while month not in mlist:
        month = input("Which month, choosing from the first six months, would you like to filter by? Type 'all' for no filter. ").lower()
        if month not in mlist:
            print("Your input was invalid. Please try again. ")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    dlist = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ""
    while day not in dlist:
        day = input("Which day of the week would you like to filter by? Type 'all' for no filter. ").lower()
        if day not in dlist:
            print("Your input was invalid. Please try again. ")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city + '.csv')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if (month != 'all'):
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if (day != 'all'):
        day = day.title()
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # TO DO: display the most common month
    cs_month = df['month'].value_counts().index[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    cs_month = months[cs_month-1]
    print("The most common month is", cs_month.title() + ". If you filtered for a specific month, the most frequent month would be the same as the specific month.")
    # TO DO: display the most common day of week
    cs_dow = df['day_of_week'].value_counts().index[0]
    print("The most common day of week is", cs_dow + ". If you filtered for a specific day, the most frequent day would be the same as the specific day.")

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    cs_hour = df['hour'].value_counts().index[0]
    if (cs_hour >= 0 and cs_hour <= 11):
        p_hour = str(cs_hour) + ":00 AM."
    elif (cs_hour == 12):
        p_hour = str(cs_hour) + ":00 PM."
    else:
        p_hour = str(cs_hour-12) + ":00 PM."
    print("The most common start hour is", p_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start = df['Start Station'].value_counts().index[0]
    s_count = 0
    for i in df['Start Station']:
        if (i == start):
            s_count += 1
    print ("The most commonly used start station is", start, 'with', s_count, "uses.")
    # TO DO: display most commonly used end station
    end = df['End Station'].value_counts().index[0]
    e_count = 0
    for i in df['End Station']:
        if (i == end):
            e_count += 1
    print ("The most commonly used end station is", end, "with", e_count, "uses.")
    # TO DO: display most frequent combination of start station and end station trip

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    teh = pd.DataFrame.sum(df['End Time'].dt.hour)
    tsh = pd.DataFrame.sum(df['Start Time'].dt.hour)
    total_hours = teh - tsh
    tem = pd.DataFrame.sum(df['End Time'].dt.minute)
    tsm = pd.DataFrame.sum(df['Start Time'].dt.minute)
    total_min = tem - tsm
    tes = pd.DataFrame.sum(df['End Time'].dt.second)
    tss = pd.DataFrame.sum(df['Start Time'].dt.second)
    total_sec = tes - tss
    total_min += total_sec//60
    total_sec = total_sec%60
    total_hours += total_min//60
    total_min = total_min%60
    print("The total travel time is", total_hours, "hours,", total_min, "minutes, and", total_sec, "seconds.")

    # TO DO: display mean travel time
    aeh = pd.DataFrame.mean(df['End Time'].dt.hour)
    ash = pd.DataFrame.mean(df['Start Time'].dt.hour)
    avg_hours = aeh - ash
    aem = pd.DataFrame.mean(df['End Time'].dt.minute)
    asm = pd.DataFrame.mean(df['Start Time'].dt.minute)
    avg_min = aem - asm
    aes = pd.DataFrame.mean(df['End Time'].dt.second)
    ass = pd.DataFrame.mean(df['Start Time'].dt.second)
    avg_sec = aes - ass
    avg_min += avg_hours*60
    avg_sec += avg_min%1*60
    avg_min -= avg_min%1
    print("The average travel time is approximately", int(avg_min), "minutes, and", int(avg_sec), "seconds.")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    customers = 0
    subscribers = 0
    for i in df['User Type']:
        if i == 'Subscriber':
            subscribers += 1
        if i == 'Customer':
            customers += 1
    print('There are', customers, "customers and", subscribers, "subscribers.")

    # TO DO: Display counts of gender
    males = 0
    females = 0
    unknowns = 0
    try:
        for i in df['Gender']:
            if i == 'Male':
                males += 1
            elif i == 'Female':
                females += 1
            else:
                unknowns += 1
        print('There are', males, "males,", females, "females, and", unknowns, "users with unknown gender.")
    except:
        print("There is no data on genders for Washington.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        latest = int(df['Birth Year'].max())
        mcyear = int(df['Birth Year'].mode())
        print('The earliest year of birth is', str(earliest) + '. The most recent birth year is', str(latest) + '. The most common year of birth is', str(mcyear) + '.')
    except:
        print("There is no data on birth years for Washington.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    more_data = input('Would you like to see the raw data? Please type "yes" or "no". ')
    count = 0
    while more_data == 'yes':
        print(df[count:count+5])
        count += 5
        more_data = input('Would you like to see more? ')
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
