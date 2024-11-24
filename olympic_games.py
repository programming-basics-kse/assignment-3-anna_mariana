import argparse

parser=argparse.ArgumentParser("Olympic game table")
parser.add_argument('input_file',type=argparse.FileType('r'),help="File to input")
parser.add_argument('-medals', nargs='?',type=str,help="-medals")
parser.add_argument('-country', nargs='?',type=str,help="Name of team or abbreviation")
parser.add_argument('-year', nargs='?',type=int,help="Year of the olympiad")
parser.add_argument('-output', nargs='?',type=argparse.FileType('w'),help="result.txt")
args=parser.parse_args()
input_table=[]
output_table=[]
medal_counts = {"Gold": 0, "Silver": 0, "Bronze": 0}
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