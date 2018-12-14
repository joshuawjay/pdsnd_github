import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS_OF_WEEK = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington).
    is_valid = False
    while is_valid == False:
        city = input("\nWhich city would you like to analyze? (Chicago, New York City, or Washington):\n")
        if city.lower() in CITY_DATA:
            is_valid = True
            city = city.lower()
        else:
            print("{} is not a valid value. Please try again.".format(city))

    # Get user input for month (all, january, february, ... , june)
    is_valid = False
    while is_valid == False:
        month = input("\nWhich month would you like to analyze? (January, February, March, April, May, June, or All):\n")
        if month.lower() in MONTHS or month.lower() == 'all':
            is_valid = True
            month = month.lower()
        else:
            print("{} is not a valid value. Please try again.".format(month))

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    is_valid = False
    while is_valid == False:
        day = input("\nWhich day of the week would you like to analyze? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All):\n")
        if day.lower() in DAYS_OF_WEEK or day.lower() == 'all':
            is_valid = True
            day = day.lower()
        else:
            print("{} is not a valid value. Please try again.".format(day))

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['start_hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    df['Station Pair'] = df['Start Station'] + ' to ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def most_common(df, column_name):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (data frame) df - the data frame to calculate on
        (str) column_name - name of the column to calculate the mode (most common)
    Returns:
        most_common_value - the mode in the column_name column
        record_count - the number of times this value occurs
    """
    most_common_value = df[column_name].mode()[0]
    record_count = (df[column_name] == most_common_value).sum()
    return most_common_value, record_count

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month, trip_count = most_common(df, 'month')
    most_common_month_name = MONTHS[most_common_month - 1]
    print(' - The most common month of travel is: {} with {:,} trips.\n'.format(most_common_month_name.title(), trip_count))

    # display the most common day of week
    most_common_day, trip_count = most_common(df, 'day_of_week')
    print(' - The most common day of travel is: {} with {:,} trips.\n'.format(most_common_day.title(), trip_count))

    # display the most common start hour
    most_common_start_hour, trip_count = most_common(df, 'start_hour')
    print(' - The most common start hour of travel is: {} with {:,} trips.\n'.format(most_common_start_hour, trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start, trip_count = most_common(df, 'Start Station')
    print(' - The most common start station is: {} with {:,} trips.\n'.format(most_common_start, trip_count))

    # display most commonly used end station
    most_common_end, trip_count = most_common(df, 'End Station')
    print(' - The most common end station is: {} with {:,} trips.\n'.format(most_common_end, trip_count))


    # display most frequent combination of start station and end station trip
    most_common_pair, trip_count = most_common(df, 'Station Pair')
    print(' - The most common station combination is: {} with {:,} trips.\n'.format(most_common_pair, trip_count))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_formatted_duration_from_seconds(duration_in_seconds):
    m, s = divmod(duration_in_seconds, 60)
    h, m = divmod(m, 60)
    
    return "{:,.2f} hours, {:,.2f} minutes, and {:,.2f} seconds".format(h, m, s)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_sum = df['Trip Duration'].sum()
    print(' - The total travel time is: {}\n'.format(get_formatted_duration_from_seconds(travel_time_sum)))

    # display mean travel time
    travel_time_avg = df['Trip Duration'].mean()
    print(' - The average trip duration is: {}.\n'.format(get_formatted_duration_from_seconds(travel_time_avg)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(' - User Type Counts:\n')
    print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\n - Gender Counts:\n')
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\n - Earliest birth year: {:.0f}\n'.format(df['Birth Year'].min()))
        print(' - Most recent birth year: {:.0f}\n'.format(df['Birth Year'].max()))
        print(' - Most common birth year: {:.0f}\n'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df, page_size):
    """Displays the raw data in pages, allowing the user to decide when to stop."""
    show_more = 'yes'
    page = 0
    columns_to_display = ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type']
    if 'Gender' in df.columns:
        columns_to_display.append('Gender')
        
    if 'Birth Year' in df.columns:
        columns_to_display.append('Birth Year')
    
    while show_more.lower() == 'yes':
        #Display 5 rows
        pd.options.display.max_rows = page_size
        pd.options.display.max_columns = len(columns_to_display)
        print(df[columns_to_display][page*page_size:page*page_size+page_size].to_string())
        
        show_more = input('\nWould you like to see {} more rows? Enter yes or no.\n'.format(page_size))
        if show_more.lower() == 'yes':
            page += 1
    
    return
    
def view_raw_data(df):
	"""Asks the user if they would like to review the raw data and pages through."""
	view_raw_data = input('\nWould you like to view the first rows of the raw data? Enter yes or no.\n')
	if view_raw_data.lower() == 'yes':
		valid = False
		while valid == False:
			page_size = input('\nHow many records would you like to see? Enter 1 through 10.\n')
			
			try:
				page_size = int(page_size)
				if 1 <= page_size <= 10:
					valid = True
			except:
				print('\n{} is not a valid integer between 1 and 10. Please try again.\n'.format(page_size))
		
		display_data(df, page_size)
	
	return page_size
	
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
		view_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
