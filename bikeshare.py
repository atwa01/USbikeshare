import time
import pandas as pd
import numpy as np
day_of_week = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june','all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    global city
    city = input('Which city do you want to gather data for ? (Chicago,New york city,Washington)\n').lower()
    while city not in CITY_DATA.keys():

        print("Please select from the 3 cities")
        city = input('Which city do you want to gather data for ? (Chicago,New york city,Washington)\n').lower()



    # get user input for month (all, january, february, ... , june)
    month = input("Which month? all,January,February,March,April,May, or June\n").lower()
    while month not in months:

        print("Please select from the folowing months")
        month = input("Which month? all,January,February,March,April,May, or June\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Choose the day of the week or all days ? \n").lower()
    while day not in day_of_week:
        print("Please type a day of the week")
        day = input("Choose the day of the week or all days ? \n").lower()


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The Most common month is {}".format(common_month))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common day is {}".format(common_day))
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start = df['hour'].mode()[0]
    print("Most common start hour is {}".format(common_start))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is {}'.format(common_start_station))
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is {}'.format(common_end_station))
    # display most frequent combination of start station and end station trip
    df['Combined Trips'] = df['Start Station']+" to "+df['End Station']
    common_combined_trips = df['Combined Trips'].mode()[0]
    print("The most popular trip was from {}".format(common_combined_trips))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_seconds = df['Trip Duration'].sum()
    print(time.strftime("Total Travel time :%H:%M:%S", time.gmtime(total_time_seconds)))

    # display mean travel time
    mean_in_seconds = df['Trip Duration'].mean()
    print(time.strftime("Mean Travel time :%H:%M:%S", time.gmtime(mean_in_seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # Display counts of gender



    # Display earliest, most recent, and most common year of birth
    try:
        print(df['Gender'].value_counts())
        print("Most common birthyear is {}".format(int(df['Birth Year'].mode()[0])))
        print("Earliest Birth Year is {}".format(int(df['Birth Year'].min())))
        print("Earliest Birth Year is {}".format(int(df['Birth Year'].max())))
    except:
        print("This data of this city doesn't include gender nor birth year")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    df = pd.read_csv(CITY_DATA[city])
    rows = 0

    while True:
        display_data = input("Do you want to display 5 rows of raw data? (yes/no) \n").lower()
        if display_data != 'no' and display_data != 'yes':
            print("Please choose yes or no only")
        elif display_data == 'yes':
            print(df.iloc[rows:rows+5])

            rows +=5
        elif display_data == 'no':
                    break




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
