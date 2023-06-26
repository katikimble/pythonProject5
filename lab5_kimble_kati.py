# Name: Kati Kimble
# Date: 11/18/2021
# Course: SDEV 300
# File Name: lab5_kimble_kati.py

"""This program shows statistics and a histogram from data, from two csv files."""

import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from tabulate import tabulate

# main menu dictionary
menu = {'1': ' Population Data',
        '2': ' Housing Data',
        '3': ' Exit the Program'}

# population main menu
pop_data_menu = {'a': ' Population for Apr 1',
                 'b': ' Population for Jul 1',
                 'c': ' Change in Population',
                 'd': ' Exit Column',
                 'e': ' Exit the Program'}

# housing main menu
housing_data_menu = {'a': ' Age',
                     'b': ' Number of Bedrooms',
                     'c': ' Year Built',
                     'd': ' Number of Rooms',
                     'e': ' Utility',
                     'f': ' Exit the Column',
                     'g': ' Exit the Program'}


def open_pop_file():
    """This method opens an excel file with population data
     and throws exception if file is not found"""
    try:
        pop_file = pd.read_csv('PopChange.csv', skiprows=[0],
                               names=['ID', 'Geography', 'Target_Geo_ID',
                                      'Target_Geo_ID_2', 'April', 'July', 'Change_Pop'])

    except FileNotFoundError:
        print('This file has not been found!')
        print('Please ensure spelling of file is correct, and try again.')
        sys.exit()

    return pop_file


def open_housing_file():
    """This method opens an excel file with housing
    data and throws exception if file is not found"""
    try:
        housing_file = pd.read_csv('Housing.csv', skiprows=[0],
                                   names=['Age', 'Bedrooms', 'Built',
                                          'Num_Units', 'Rooms', 'Weight', 'Utility'])

    except FileNotFoundError:
        print('This file has not been found!')
        print('Please ensure spelling of file is correct, and try again.')
        sys.exit()

    return housing_file


def main():
    """This method prints the user main menu"""
    print('Select the file you want to analyze: ')
    for key, value in menu.items():
        print(key + '.', value)
    while 1:
        selection = input()
        if selection in menu:
            return selection_menu(selection)

        print('Please enter option \'1\', \'2\', or \'3\'.')


def selection_menu(selection):
    """This method calls a method or exits program based on user selection in main()"""
    if selection == '1':
        print('You have entered Population Data.')
        pop_data_main()
    elif selection == '2':
        print('You have entered Housing Data.')
        housing_data_main()
    elif selection == '3':
        print('Thank you for using this program!')
        sys.exit()


def housing_data_main():
    """This method provides menu options for housing data selection"""
    print('Select the Column you want to analyze: ')
    for key, value in housing_data_menu.items():
        print(key + '.', value)
    while 1:
        selection = input().lower()
        if selection in housing_data_menu:
            return housing_data_selection(selection)
        print('Please enter option \'a\', \'b\', \'c\', \'d\', \'e\', \'f\', or \'g\'')


def housing_data_selection(selection):
    """This method calls stats_func() to populate
    stats and histogram, based on user selection"""

    # Setting the open file to a variable to use within this method
    housing_file = open_housing_file()

    if selection == 'a':
        print('You selected Age')
        print('The statistics for this column are: ')
        # calls method with custom args related to user selection for histogram x value range
        stats_func(housing_file, 'Age', -50, 100, 25)
        housing_data_main()
    elif selection == 'b':
        print('You selected Number of Bedrooms')
        print('The statistics for this column are: ')
        stats_func(housing_file, 'Bedrooms', 0, 8, 1)
        housing_data_main()
    elif selection == 'c':
        print('You selected Year Built')
        print('The statistics for this column are: ')
        stats_func(housing_file, 'Built', 1919, 2020, 20)
        housing_data_main()
    elif selection == 'd':
        print('You selected Number of Rooms')
        print('The statistics for this column are: ')
        stats_func(housing_file, 'Rooms', 0, 15, 2)
        housing_data_main()
    elif selection == 'e':
        print('You selected Utility')
        print('The statistics for this column are: ')
        stats_func(housing_file, 'Utility', 0, 1110, 100)
        housing_data_main()
    elif selection == 'f':
        # back to main menu
        main()
    elif selection == 'g':
        print('Thank you for using this program!')
        sys.exit()


def stats_func(file, col_name, min_graph, max_graph, count_by):
    """This method accepts a data file and the column name and then develops stats
    on that specific column. It then creates a histogram by using arrange() with the given args"""
    count, mean, std, minimum, _, _, _, maximum = file[col_name].describe()
    data_dictionary = [['Count:', count], ['Mean:', mean], ['Standard Dev:', std],
                       ['Minimum:', minimum], ['Maximum:', maximum]]
    data_df = pd.DataFrame(data_dictionary)
    _, axes = plt.subplots()
    data = file[col_name]
    # data for housing displays better with 20 bins
    if col_name in ('Age', 'Bedrooms', 'Built', 'Rooms', 'Utility'):
        data.hist(bins=20)
        plt.title('Housing Data')
    # data for population has a different bin size for better display
    else:
        data.hist(bins=100)
        plt.title('Population Data')
    # customize the x labels with if statements
    if col_name == 'Age':
        plt.xlabel('Age')
    elif col_name == 'Bedrooms':
        plt.xlabel('Number of Bedrooms')
    elif col_name == 'Rooms':
        plt.xlabel('Number of Rooms')
    elif col_name == 'Utility':
        plt.xlabel('Utility')
    elif col_name == 'April':
        plt.xlabel('April Population')
    elif col_name == 'July':
        plt.xlabel('July Population')
    elif col_name == 'Change_Pop':
        plt.xlabel('Change in Population from April to July')
    # adjusts the number change on the x axis, and the amount between each number
    plt.xticks(np.arange(min_graph, max_graph, count_by))
    # all data has the same y label
    plt.ylabel('Data Count')
    # the built column should not be in float format, since we are displaying in years
    if col_name == 'Built':
        print(tabulate(data_df, showindex=False, numalign='left'))
        plt.xlabel('Year Built')
    else:
        print(tabulate(data_df, showindex=False, numalign='left', floatfmt=',.2f'))
        axes.xaxis.set_major_formatter(format_number)
    # show the histogram
    plt.show()


def format_number(data_value, index):
    """This method formats the graph x values"""
    index = ''
    if 1_000_000 > data_value > 999 or -1_000_000 < data_value < -999:
        index = 'K'
        formatter = f'{data_value * 0.001:1.1f}{index}'

    elif data_value >= 1_000_000 or data_value <= -1_000_000:
        index = 'M'
        formatter = f'{data_value * 0.000001:1.1f}{index}'
    else:
        formatter = f'{data_value:g}'
    return formatter


def pop_data_main():
    """This method creates a user menu to select column
    from population file"""
    print('Select the Column you want to analyze: ')
    for key, value in pop_data_menu.items():
        print(key + '.', value)
    while 1:
        selection = input().lower()
        if selection in pop_data_menu:
            return pop_data_selection(selection)
        print('Please enter option \'a\', \'b\', \'c\', or \'d\'.')


def pop_data_selection(selection):
    """This method uses stats_func() to print stats in console and
    to display a custom histogram, based on user input"""
    pop_df = open_pop_file()
    if selection == 'a':
        print('You selected Population for April 1')
        print('The statistics for this column are: ')
        # use stats_function to customize the graph range
        stats_func(pop_df, 'April', 0, 4000000, 500000)
        pop_data_main()
    elif selection == 'b':
        print('You selected Population for July 1')
        print('The statistics for this column are: ')
        stats_func(pop_df, 'July', 0, 4000000, 500000)
        pop_data_main()
    elif selection == 'c':
        print('You selected to Change in Population')
        print('The statistics for this column are: ')
        stats_func(pop_df, 'Change_Pop', -600000, 25000, 100000)
        pop_data_main()
    elif selection == 'd':
        main()
    elif selection == 'e':
        print('Thank you for using this program!')
        sys.exit()


if __name__ == '__main__':
    print('***************** Welcome to the Python Data Analysis App**********')
    main()
