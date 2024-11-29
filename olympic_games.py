import argparse

parser=argparse.ArgumentParser("Olympic game table")
parser.add_argument('input_file',type=argparse.FileType('r'),help="File to input")
parser.add_argument('-medals', nargs='?',type=str,help="-medals")
parser.add_argument('-country', nargs='?',type=str,help="Name of team or abbreviation")
parser.add_argument('-year', nargs='?',type=int,help="Year of the olympiad")
parser.add_argument('-total', nargs='?', type=str, help="Number of olympic medals by year")
parser.add_argument('-output', nargs='?',type=argparse.FileType('w'),help="result.txt")
parser.add_argument('-overall',nargs='*',type=str,help="countries")
args=parser.parse_args()
input_table=[]
output_table=[]
medal_counts = {"Gold": 0, "Silver": 0, "Bronze": 0}
years_medal_dict={}
with args.input_file as input_file:
    for line in input_file:
        line=line[:-1]
        input_table.append(line.split('\t'))
if args.country and args.year:
    for line in input_table:
        if (line[6] == args.country or line[7] == args.country) and int(line[9]) == args.year and line[14] in medal_counts:
           output_table.append(f"{line[1]} - {line[2]} - {line[14]}")
           medal_counts[line[14]] += 1
    if output_table:
        print("\nTop 10 Medalists:")
        for line in output_table[:10]:
            print(line)

        print("\nMedal Summary:")
        for medal, count in medal_counts.items():
            print(f"{medal}: {count}")

        if args.output:
            with args.output as output_file:
                output_file.write("Top 10 Medalists:\n")
                for line in output_table[:10]:
                    output_file.write(line+ "\n")
                output_file.write("\nMedal Summary:\n")
                for medal, count in medal_counts.items():
                    output_file.write(f"{medal}: {count}\n")
    else:
        print("No records found matching the criteria.")

if args.total:
    medal_counts = {}
    for line in input_table:
        if int(line[9]) == args.total:
            country = line[6] or line[7]
            medal = line[14]
            if country not in medal_counts:
                medal_counts[country] = {'Gold': 0, "Silver": 0, "Bronze": 0}
            if medal in medal_counts[country]:
                medal_counts[country][medal] += 1

        if medal_counts:
            print(f"\nMedal counts for {args.total}:")
            result = []
            for country, medals in medal_counts.items():
                result.append(f'{country} - {medals["Gold"]} - {medals["Silver"]} - {medals["Bronze"]}')
            for row in result:
                print(row)

        if args.output:
            with args.output as output_file:
                output_file.write("Medal Summary:\n")
                for row in result:
                    output_file.write(f"{row}\n")
else:
    print(f"No records found matching the criteria for the year {args.total}.")

if args.overall:
    for line in input_table:
        if line[9].isdigit():
            year = int(line[9])
        medal = line[14]
        country = line[6]
        country_initials=line[7]
        if (country in args.overall) or (country_initials in args.overall):
            key = country if country in args.overall else country_initials
            if key not in years_medal_dict:
                years_medal_dict[key] = {}
            if year not in years_medal_dict[key]:
                years_medal_dict[key][year] = 0
            years_medal_dict[key][year] += 1
    for country in args.overall:
        if country in years_medal_dict:
            best_year = None
            max_medals = 0
            for year, medal_count in years_medal_dict[country].items():
                if medal_count > max_medals:
                    max_medals = medal_count
                    best_year = year
            if best_year is not None:
                print(f"{country}: {best_year} ({max_medals} medals)")
        else:
            print(f"{country}: No data available")