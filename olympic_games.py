import argparse

parser=argparse.ArgumentParser("Olympic game table")
parser.add_argument('input_file',type=argparse.FileType('r'),help="File to input")
parser.add_argument('-medals', nargs='?',type=str,help="-medals")
parser.add_argument('-country', nargs='?',type=str,help="Name of team or abbreviation")
parser.add_argument('-year', nargs='?',type=int,help="Year of the olympiad")
parser.add_argument('-total', nargs='?', type=str, help="Number of olympic medals by year")
parser.add_argument('-output', nargs='?',type=argparse.FileType('w'),help="result.txt")
parser.add_argument("-interactive", nargs='?', type = str, help = "Interactive mode")
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
    if args.country != line[6] or args.country != line[7]:
        print("Maybe you wrote incorrect country")
    if args.year != line[9]:
        print("Maybe we don't have this year in our list or in this year there wasn't olympiad")
    else:
        print("No records found matching the criteria.")

if args.total:
    total_medal_counts = {}
    for line in input_table:
        if line[9].isdigit():
            year = int(line[9])
        country = line[6] or line[7]
        medal = line[14]
        if country not in total_medal_counts:
            total_medal_counts[country] = {'Gold': 0, "Silver": 0, "Bronze": 0}
        if medal in total_medal_counts[country]:
            total_medal_counts[country][medal] += 1

    if total_medal_counts:
        print(f"\nMedal counts for the year {args.total}:")
        result = []
        for country, medals in total_medal_counts.items():
            result.append(f'{country} - Gold: {medals["Gold"]}, Silver: {medals["Silver"]}, Bronze: {medals["Bronze"]}')
        for row in result:
            print(row)

        if args.output:
            with args.output as output_file:
                output_file.write(f"Medal Summary for {args.total}:\n")
                for row in result:
                    output_file.write(f"{row}\n")
    else:
        print(f"No records found matching the criteria for the year {args.total}.")

if args.interactive:
    print("Welcome to interactive mode! Write a country/country code or 'exit' to exit")
    while True:
        task = input("Choose: Country or its code or Exit")
        if task.lower() == 'exit':
            print("Exiting... \nBye!")
            break

        country_stats = []
        for line in input_table:
            line=line[:-1]
            if line[6] == task or line[7] == task:
                country_stats.append(line)
        if not country_stats:
            print(f"No data available for '{task}'.")
            continue

        first_participation_year = None
        first_participation_city = None
        for row in country_stats:
            year = int(row[9])
            city = row[11]
            if first_participation_year is None or year < first_participation_year:
                first_participation_year = year
                first_participation_city = city

        medals_by_year = {}
        for row in country_stats:
            year = int(row[9])
            medal = row[14]
            if medal not in medals_by_year:
                medals_by_year[year] = {"Gold": 0, "Silver": 0, "Bronze": 0}
            if medal in medals_by_year[year]:
                medals_by_year[year][medal] += 1

        best_year, max_medals = None, 0
        worst_year, min_medals = None, 0
        for medals in medals_by_year.items():
            total_medals = sum(medals.values())
            if total_medals > max_medals:
                best_year, max_medals = year, total_medals
            if total_medals < min_medals:
                worst_year, min_medals = year, total_medals

        total_olympics = len(medals_by_year)
        total_gold, total_silver, total_bronze = 0, 0, 0
        for medals in medals_by_year.values():
            total_gold += medals["Gold"]
            total_silver += medals["Silver"]
            total_bronze += medals["Bronze"]
        if total_olympics > 0:
            average_gold = total_gold / total_olympics
            average_silver = total_silver / total_olympics
            average_bronze = total_bronze / total_olympics
        else:
            average_gold = 0
            average_silver = 0
            average_bronze = 0

        print(f"\nStatistics for {task}:")
        print(f"- First participation: {first_participation_year} in {first_participation_city}")
        print(f"- Best Olympics: {best_year} ({max_medals} medals)")
        print(f"- Worst Olympics: {worst_year} ({min_medals} medals)")
        print(f"- Average medals per Olympics:")
        print(f"  Gold: {average_gold:}, Silver: {average_silver:}, Bronze: {average_bronze:}\n")

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
