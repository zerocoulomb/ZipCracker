import zipfile
import tqdm
import argparse
import sys
from colorama import Fore,init

init(autoreset=True)

parser= argparse.ArgumentParser(usage="python zipcracker.py --zipfile [ZIP] --wordlist [PASS LIST]")
parser.add_argument("-z","--zipfile",required=True,help="Target zip file")
parser.add_argument("-w","--wordlist",required=True,help="Password list")

args = parser.parse_args()

class ZipCracker():
    def __init__(self,zip_path) -> None:        
       self.IS_CRACKED = None
       try: 
        self.zip_file = zipfile.ZipFile(zip_path)
       except:
           print("Please enter exists arguments")
           sys.exit(0)
    def crack(self,pass_path):
        try:  
          pass_file = open(pass_path,"rb")
        except:
          print("Please enter exists arguments") 
          sys.exit(0)
        pass_list = pass_file.readlines()
        test_count = len(pass_list)
        print("\n")
        for password in tqdm.tqdm(pass_list,total=test_count,desc=Fore.BLUE+"Cracking"+Fore.RESET,unit=" password",colour="GREEN",ncols=120):
          try: 
            self.zip_file.extractall(pwd=password.strip())
            self.IS_CRACKED = password.strip().decode()
            break
          except KeyboardInterrupt:
               sys.exit(0)  
          except:
              continue
        self.is_cracked() 
    def is_cracked(self):
        if not self.IS_CRACKED == None:
            print(Fore.BLUE+"\nStatus:"+Fore.GREEN+" cracked\n\n"+Fore.BLUE+"Password: "+Fore.GREEN +self.IS_CRACKED+ "\n")
        else:
             print(Fore.BLUE+"\nStatus:"+Fore.RED +" not cracked\n")   
if __name__ == "__main__":        
   cracker = ZipCracker(args.zipfile)
   cracker.crack(args.wordlist)         
                