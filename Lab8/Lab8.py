import argparse
import test1
import xlsxwriter

keys = []
dataset = []

parser = argparse.ArgumentParser(description="Program is used to do analysis of the tennis games dataset, including: creating ranking of players, counting number of players, statistics about mathces made inside and outside")
parser.add_argument('dataset', help="Dataset file that program should work with (should be a .csv file")
parser.add_argument('-o', help="Destination file to write results of execution to (should be an .xlsx file)")
parser.add_argument('-l', help="The number of lines to read (default 13000)")
args = parser.parse_args()

#handling files not ending with csv
if not args.dataset.endswith('.csv'):
    print("Filename should end with .csv")
    quit()

#handling file not found
try:
    csvfile = open(args.dataset, newline='')
except FileNotFoundError:
    print(f'File not found: {args.dataset}')
    quit()

print(f'Filename of dataset: {args.dataset} \n')


#reading from csv file into a list
with csvfile:
    csvreader = test1.reader(csvfile, delimiter=',', quotechar='|')
    for i in range(0, int(args.l) if args.l is not None else 13000):
        if i == 0:
            keys = next(csvreader)
        dataset.append(next(csvreader))

#percentage of matches
print(f'Columns in the dataset: \n{keys}\n')

#statistical data
#players ranking
players = {}

for row in dataset:
    try:
        players[row[10]] = (players[row[10]][0] + 1, players[row[10]][1])
    except KeyError:
        players[row[10]] = (1, 0)
    try:
        players[row[9]] = (players[row[10]][0] + 1, players[row[10]][1] + 1)
    except KeyError:
        players[row[9]] = (1, 1)

print("10 best players by game/win ratio: ")
ranked = sorted(list(players.items()), key=lambda x: x[1][1]/x[1][0] + x[1][0]/10000, reverse=True)
for i in range(0, 10):
    print(f'{ranked[i][0]}  games:{ranked[i][1][0]},   won{ranked[i][1][1]}')

#games outside and inside
games_outdoor = 0

for row in dataset:
    if(row[5].lower() == 'outdoor'):
        games_outdoor += 1
percents_outdoor = 100/(len(dataset) / games_outdoor)
print(f'Games played outdoor: {percents_outdoor}%')
print(f'Games played indoor: {100 - percents_outdoor}%\n')

#total number of players
total_players = len(ranked)
print(f'Total number of players in the ranking: {total_players}')

dest_filename = args.o
if dest_filename is not None:
    if dest_filename.endswith(".xlsx"):
        print(f'Writing to {dest_filename}')
        workbook = xlsxwriter.Workbook(dest_filename)
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, 'Total games outdoor:')
        worksheet.write(0, 1, games_outdoor)
        worksheet.write(1, 0, 'Percentage of games outdoor:')
        worksheet.write(1, 1, 100 /(len(dataset) / games_outdoor))

        worksheet.write(3, 0, "Players in the rating: ")
        worksheet.write(3, 1, total_players)

        worksheet.write(5, 0, "Name")
        worksheet.write(5, 1, "Games played:")
        worksheet.write(5, 2, "Games won:")
        worksheet.write(5, 3, "Winning rate:")
        row_num = 6
        for row in ranked:
            worksheet.write(row_num, 0, row[0])
            worksheet.write(row_num, 1, row[1][0])
            worksheet.write(row_num, 2, row[1][1])
            worksheet.write(row_num, 3, row[1][1]/row[1][0])
            row_num += 1

        workbook.close()
    else:
        print(f"Invalid filename to write: {dest_filename} should end with .xlsx")
