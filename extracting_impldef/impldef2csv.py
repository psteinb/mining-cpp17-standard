from parsestd import parse_texfile, collapse_sections, flatten_items
from pathlib import Path
import argparse
import sys
import csv

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-j','--nthreads', action='store', default=1, type=int, help="how many threads to use")
    parser.add_argument('-p','--pad_sections', action='store', default=6, type=int, help="how many sections to padd for (0 .. no padding, default: 6)")
    parser.add_argument('-o','--outcsv', action='store', default='output.csv', type=str, help="csv file to output")
    parser.add_argument('-H','--header', action='store_true', default=False,  help="add a header to the output csv")
    parser.add_argument('files', nargs=argparse.REMAINDER, help="input file(s)")

    args = parser.parse_args(argv)

    if "help" in args or len(args.files) == 0:
        parser.print_help()
        return 1
    else:
        print("parsing",len(args.files),"files into",args.outcsv)

    global_flattened = []
    for filestr in args.files:
        ifile = Path(filestr)
        if not ifile.exists():
            print(f"{ifile} does not exist, skipping it")
            continue
        print(f"parsing {ifile}")
        parsed = parse_texfile(ifile)
        collapsed = collapse_sections(parsed,
                                      ifile.name,
                                      args.pad_sections)
        flattened = flatten_items(collapsed)
        global_flattened.extend(flattened)

    with open(args.outcsv, 'w', newline='') as f:

        fieldnames = []
        if args.header:
            for eli in range(len(global_flattened[0])-2):
                if eli%2 == 0:
                    fieldnames.append(f"location_sec{eli//2}")
                    fieldnames.append(f"content_sec{eli//2}")
            fieldnames.append(f"location_impldef")
            fieldnames.append(f"content_impldef")

        writer = csv.writer(f)
        if args.header:
            writer = csv.writer(f)
            writer.writerow(fieldnames)
        writer.writerows(global_flattened)

    return 0

if __name__ == '__main__':
    rv = main(sys.argv[1:])
    sys.exit(rv)
