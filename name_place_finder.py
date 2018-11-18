import os
import sys
import csv
import argparse

# https://simplemaps.com/data/us-cities

city_state_abbr = []
city_state_full = []
city_list_indicies = []

def city_master_list():
    with open('uscitiesv1.4.csv', 'r') as city_list:
        indicies = csv.reader(city_list)
        city_list_indicies = list(indicies)

        for k in range(len(city_list_indicies)):
            abbr_str = city_list_indicies[k][0] + ', ' + city_list_indicies[k][2]
            full_str = city_list_indicies[k][0] + ', ' + city_list_indicies[k][3]
            city_state_abbr.append(abbr_str)
            city_state_full.append(full_str)

    return city_list_indicies


def find_city_state(TSV_file, TSV_output_file, city_list_indicies):
    with open(TSV_file, 'r') as temp:
        with open(TSV_output_file, 'w') as output:
            reader = csv.reader(temp, delimiter="\t")
            writer = csv.writer(output, delimiter="\t")

            counter = 0

            check_list = list(reader)

            writer.writerow(['Tweet ID', 'Name Place', 'City ID'])

            for i in range(len(check_list)):
                for j in range(len(city_state_abbr)):
                    if city_state_abbr[j] in check_list[i][3] or city_state_full[j] in check_list[i][3]:
                        writer.writerow([check_list[i][1], city_state_full[j], city_list_indicies[j][15]])
                        # print("Found", city_state_full[j])

            print("Finished with", TSV_file)


def parse_args():
    '''
    Parses the command line arguments for the script

    Returns
    -------

    args : object
           Python arg parser object
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('TSV_file', type=str, help='Twitter stream TSV file to find city states.')

    parser.add_argument('TSV_output_file', type=str, help='Output file with found city states.')

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    print("Starting with", args.TSV_file)

    city_list_indicies = city_master_list()

    find_city_state(args.TSV_file, args.TSV_output_file, city_list_indicies)

if __name__ == "__main__":
    main()
