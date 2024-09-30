import socket
import requests
import time
from ipwhois import IPWhois
from pprint import pprint
from colorama import Fore, Style, init
import folium

# Инициализация colorama
init(autoreset=True)

# Функция для получения локального IP-адреса
def get_local_ip():
    local_ip = socket.gethostbyname(socket.gethostname())
    return local_ip

# Функция для получения публичного IP-адреса
def get_public_ip():
    try:
        public_ip = requests.get('https://api.ipify.org').text
        return public_ip
    except requests.RequestException as e:
        return f"Error fetching public IP: {e}"

# Выбор действия
choose = input(f"""" 
                   _____________
                  /             \\          Welcome to {Fore.RED + "IPhunter"}{Fore.WHITE} 
                 /               \\         if you want to find approximate device geolocation enter {Fore.LIGHTBLUE_EX + "1."}{Fore.WHITE}
                /                 \\        if you want to find device full information enter {Fore.LIGHTBLUE_EX + "2."}{Fore.WHITE}
               |        I P        |       if you want to search your public IP address enter {Fore.LIGHTBLUE_EX + "3."}{Fore.WHITE}
                \\                 /        
                  \\_____________/
                      ||    ||
                      ||    ||
                      ||    ||
                      ||    ||
                        ||||
                        ||||                
                         ||                
                         ||
                         ||
""")

# Определение функций для получения IP и информации
def IP_GEOLOCATION(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,org,as,mobile,proxy,hosting,query")
        data = response.json()
        
        if data['status'] == 'success':
            area = folium.Map(location=[data['lat'], data['lon']])
            folium.Marker(
                location=[data['lat'], data['lon']],
                popup=data['city'],
                tooltip=data['country']
            ).add_to(area)
            area.save("map.html")  # Сохранение карты в файл
            print("Map has been saved to map.html")
        else:
            print("Failed to retrieve geolocation information.")
    except Exception as e:
        print(f"Error getting geolocation: {e}")

def get_device_info(ip_address):
    print("\n--- DETERMINING DEVICE INFORMATION ---\n")
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        print(f"Device name: {hostname}")
    except socket.herror:
        print(f"Could not find device name for IP: {ip_address}")
    
    print("\n--- GEOLOCATION BY IP ---\n")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,country,regionName,city,lat,lon,isp,org,as,mobile,proxy,hosting,query")
        data = response.json()

        if data['status'] == 'success':
            print(f"Country: {data['country']}")
            print(f"Region: {data['regionName']}")
            print(f"City: {data['city']}")
            print(f"Latitude: {data['lat']}")
            print(f"Longitude: {data['lon']}")
            print(f"Provider: {data['isp']}")
            print(f"Organization: {data['org']}")
            print(f"ASN: {data['as']}")
            print(f"Mobile connection: {'yes' if data['mobile'] else 'no'}")
            print(f"Proxy is used: {'yes' if data['proxy'] else 'no'}")
            print(f"Hosting: {'yes' if data['hosting'] else 'no'}")
        else:
            print("Failed to retrieve geolocation information.")
    except Exception as e:
        print(f"Error getting geolocation: {e}")

    print("\n--- WHOIS INFORMATION ---\n")
    try:
        obj = IPWhois(ip_address)
        results = obj.lookup_rdap(depth=1)
        print(f"ASN: {results['asn']}")
        print(f"IP belongs: {results['asn_description']}")
        print(f"IP range (CIDR): {results['asn_cidr']}")
        print(f"Organization: {results['network']['name']}")
        print(f"Network type: {results['network']['type']}")
        print("\n--- Full WHOIS information ---\n")
        pprint(results)
    except Exception as e:
        print(f"Error getting IP owner information: {e}")

# Основная логика

# Получаем локальный и публичный IP-адреса
local_ip = get_local_ip()
public_ip = get_public_ip()

# Ввод IP адреса в зависимости от выбора пользователя
if choose == "1":
    ip_address = input("Enter IP: ")
    IP_GEOLOCATION(ip_address)
elif choose == "2":
    ip_address = input("Enter IP: ")
    get_device_info(ip_address)
elif choose == "3":
    # Только при выборе "3" показываем публичный IP
    print(f"Your public IP address is: {public_ip}")
else:
    print("Invalid choice. Please select 1, 2, or 3.")

# Ожидание
for x in range(100):
    print(".")
    time.sleep(1)  # Ожидание в 1 секунду
