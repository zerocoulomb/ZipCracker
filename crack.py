from argparse import ArgumentParser
from zipcracker import ZipCracker

parser = ArgumentParser(description="Cracker for zip files using dictionary attack")
parser.add_argument("zipfile", help="Target zip file", metavar="ZIPFILE")
parser.add_argument("-w", "--wordlist", required=True,
                    help="Password list")

args = parser.parse_args()

if __name__ == "__main__":

    cracker = ZipCracker(args.zipfile)
    cracker.crack(args.wordlist)
