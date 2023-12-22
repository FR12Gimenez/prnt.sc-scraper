from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import os, sys, ctypes, lxml, time
from prntsc.generate_urls import generate_urls
from pystyle import Colors, Colorate, Center
import concurrent.futures
from colorama import Fore

valid = 0
invalid = 0

def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

logo = """    ____  ____  _   _____________ ______   _____                                
   / __ \/ __ \/ | / /_  __/ ___// ____/  / ___/______________ _____  ___  _____
  / /_/ / /_/  / |/ / / /  \__ \/ /       \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
 / ____/ _, _/|  / / /  ___/ / /___    ___/ / /__/ /  / /_/ / /_/ /  __/ /    
/_/   /_/ |_/_/ |_/ /_/  /____/\____/   /____/\___/_/   \__,_/ .___/\___/_/     
                                                            /_/                 
                               [Github @FR12Gimenez]                            """

logo = Center.XCenter(logo)

def main():
    
    while True:
        print(Colorate.Horizontal(Colors.red_to_blue, logo, 1))
        print(f"{Fore.CYAN}Choose an option:")
        print("1. Check if your IP got banned")
        print("2. Generate images")
        print("3. Exit")
        
        choice = input(f"{Fore.CYAN}> ")
        
        if choice == '1':
            check_ip_banned()
        elif choice == '2':
            generate_images()
        elif choice == '3':
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.")



def check_ip_banned():
    url = "https://prnt.sc/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        status_code = response.status_code

        if status_code == 520: # not banned
            print(f"{Fore.GREEN}[+] Your IP is not banned on prnt.sc (Status Code: {status_code}).")
        elif status_code == 403: # banned
            print(f"{Fore.RED}[!] Your IP may be banned on prnt.sc (Status Code: {status_code}).")
        else: # i dont know
            print(f"{Fore.YELLOW}[?] Unexpected status code: {status_code}")

    except requests.RequestException as e: # banned or just not banned
        print(f"{Fore.RED}[!] IP ban status: {e}") 
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')


def generate_images():
    print(f"{Fore.CYAN}Enter the number of images to scrape: ")
    num_images = int(input(f"{Fore.CYAN}> "))
    print(f"{Fore.CYAN}Enter the number of threads (3 recommended)")
    num_threads = int(input(f"{Fore.CYAN}> "))

    check_dir()
    urls = generate_urls(num_images)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(load_url, urls)

def check_dir():
    cwd = os.getcwd()
    savedir = cwd + "/imgs"
    if not os.path.exists(savedir):
        print("Image save directory does not exist, making folder: 'imgs'\n")
        os.makedirs(savedir)

def load_url(url):
    path = os.getcwd() + "/imgs/"
    file_ext = ".png"
    
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, "lxml")
        img = soup.find("img", {"class": "no-click screenshot-image"}).get("src")
        
        if not img.startswith("https://image.prntscr.com/image/"):
            newurl = generate_urls(1)[0]
            return load_url(newurl)
        
        save_img(img, f"{url[-6:]}{file_ext}", path)
        
    except Exception as e:
        print(f"{Fore.RED}[-] Error loading URL: {e}")
        print(f"{Fore.YELLOW}[?] It seems your IP may be banned. Exit the program manually please!")
        time.sleep(60)

def save_img(img, filename, path):
    global valid, invalid
    print(f"{Fore.YELLOW}[?] Loading <{filename}>...")
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    try:
        req = Request(img, headers=hdr)
        webpage = urlopen(req).read()
        valid += 1
        set_console_title(f"Invalid URL: {invalid} | Valid URL: {valid} | GitHub: @FR12Gimenez")
        with open(path + filename, "wb") as f:
            f.write(webpage)
        print(f"{Fore.GREEN}[+] Success.\n")
    except:
        invalid += 1
        set_console_title(f"Invalid URL: {invalid} | Valid URL: {valid} | GitHub: @FR12Gimenez")
        print(f"{Fore.RED}[-] Invalid URL.")

if __name__ == "__main__":
    main()
