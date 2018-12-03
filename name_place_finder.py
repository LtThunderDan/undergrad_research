import os
import sys
import csv
import argparse
import glob

# https://simplemaps.com/data/us-cities

# twitter.com/anyuser/status/541278904204668929

hashtag_state_full =  ['\'Alabama\'', '\'Alaska\'', '\'Arizona\'', '\'Arkansas\'', \
    '\'California\'', '\'Colorado\'', '\'Connecticut\'', '\'Delaware\'', '\'Florida\'', \
    '\'Georgia\'', '\'Hawaii\'', '\'Idaho\'', '\'Illinois\'' , '\'Indiana\'' , '\'Iowa' , \
    '\'Kansas\'' , '\'Kentucky\'' , '\'Louisiana\'' , '\'Maine\'' , '\'Maryland\'' , \
    '\'Massachusetts\'' , '\'Michigan\'' , '\'Minnesota\'' , '\'Mississippi\'' , \
    '\'Missouri\'' , '\'Montana\'' '\'Nebraska\'' , '\'Nevada' , '\'NewHampshire\'' , \
    '\'NewJersey\'' , '\'NewMexico\'' , '\'NewYork\'' , '\'NorthCarolina\'' , \
    '\'NorthDakota\'' , '\'Ohio' , '\'Oklahoma\'' , '\'Oregon\'' , '\'Pennsylvania\'', \
    '\'RhodeIsland\'', '\'SouthCarolina\'' , '\'SouthDakota\'' , '\'Tennessee\'' , \
    '\'Texas\'' , '\'Utah\'' , '\'Vermont\'' , '\'Virginia\'' , '\'Washington\'' , \
    '\'WestVirginia\'' , '\'Wisconsin\'', '\'Wyoming\'']

hashtag_state_abbr = ['\'AL\'', '\'AK\'', '\'AZ\'', '\'AR\'', '\'CA\'', '\'CO\'', \
    '\'CT\'', '\'DE\'', '\'FL\'', '\'GA\'', '\'HI\'', '\'ID\'', '\'IL\'', '\'IN\'', \
    '\'IA\'', '\'KS\'', '\'KY\'', '\'LA\'', '\'ME\'', '\'MD\'', '\'MA\'', '\'MI\'', \
    '\'MN\'', '\'MS\'', '\'MO\'', '\'MT\'', '\'NE\'', '\'NV\'', '\'NH\'', '\'NJ\'', \
    '\'NM\'', '\'NY\'', '\'NC\'', '\'ND\'', '\'OH\'', '\'OK\'', '\'OR\'', '\'PA\'', \
    '\'RI\'', '\'SC\'', '\'SD\'', '\'TN\'', '\'TX\'', '\'UT\'', '\'VT\'', '\'VA\'', \
    '\'WA\'', '\'WV\'', '\'WI\'', '\'WY\'']




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

            check_list = list(reader)

            writer.writerow(['Tweet ID', 'Name Place', 'City ID'])

            for i in range(len(check_list)):
                for j in range(len(city_state_abbr)):
                    if city_state_abbr[j] in check_list[i][3] or city_state_full[j] in check_list[i][3]:
                        writer.writerow([check_list[i][1], city_state_full[j], city_list_indicies[j][15]])
                        # print("Found", city_state_full[j])

            for k in range(len(check_list)):
                for m in range(len(hashtag_state_full)):
                    if hashtag_state_abbr[m] in check_list[k][13]:
                        writer.writerow([check_list[k][1], hashtag_state_abbr[m]])
                        # print("Found abbr hashtag", hashtag_state_abbr[m])
                    if hashtag_state_full[m] in check_list[k][13]:
                        writer.writerow([check_list[k][1], hashtag_state_full[m]])
                        # print("Found full hashtag", hashtag_state_full[m])



def parse_args():
    '''
    Parses the command line arguments for the script

    Returns
    -------

    args : object
           Python arg parser object
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')

    # parser.add_argument('TSV_file', type=str, help='Twitter stream TSV file to find city states.')

    parser.add_argument('TSV_output_file', type=str, help='Output file with found city states.')

    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    ooze = glob.glob('2018_10_16_*_name_place.csv')

    for i in range(len(ooze)):
        city_list_indicies = city_master_list()
        find_city_state(ooze[i], args.TSV_output_file, city_list_indicies)

if __name__ == "__main__":
    main()
