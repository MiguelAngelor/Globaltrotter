import requests
import random
import webbrowser
from globaltrotterconstants import notislands, end_messages, random_funfact, final_map

#__________________GAME MODE__________________#
def choose_mode():
    print("Hello Globetrotter, choose your traverse method:")
    modes = {
        "1": ("By Foot", 3),
        "2": ("By Car", 6),
        "3": ("By Plane", 9),
        "0": ("By NASA", 18)
    }

    for k,v in modes.items():
        print(f"{k}. {v[0]} ({v[1]} lives)")
    
    choice = input("\nEnter 1, 2, 3 or 0: ")
    if choice not in modes: 
        print("\nInvalid choice! Default: By Foot.")
    else:
        hittheroad = ["NASA?! Huston, we have a problem.", "This adventure is sponsored and powered by... your own feet, crazy!", "Time to hit the road, nothing like 4 wheels and A/C.","First Class passangers, time to board!"]
        print("\n" + hittheroad[int(choice)])

    return modes.get(choice, ("By Foot", 3))

#__________________COUNTRIES DATA__________________#

def get_country(country_name):
    #Fetching data from Rest Countries API
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    if response.status_code == 200: #200 means Success, it was found
        data = response.json()
        for country in data:
            if country_name.lower() == country["name"]["common"].lower():
                return country
        print("\nExact match not found! I'll pick it for you.")
        return data[0]
    


def get_neighbors(country_data):
    bordering = country_data.get("borders", [])
    neighbors = []
    for n in bordering:
        url = f"https://restcountries.com/v3.1/alpha/{n}"
        response = requests.get(url)
        if response.status_code == 200:
            neighbors.append(response.json()[0]["name"]["common"])
    
    neighbors_initials = [word[0] for word in neighbors]
    return neighbors, neighbors_initials

#________________________________LIFE BAR and TOKEN______________________________#
life_emoji = {
    "By Foot":["🥾","👣","⛺", "🦶"],
    "By Car":["🚗", "🚙", "🏎️"],
    "By Plane":["✈️","🛩️", "🛪"],
    "By NASA":["🚀","🛰️", "🛸"]
}

token_emoji = {
    "By Foot": "🛶",
    "By Car": "⛽",
    "By Plane": "🎫",
    "By NASA":"🌟"
}

r_index = random.choice([0,1,2])

def lifebar(transport_mode, lives, tokens, index=r_index):
    emoji = life_emoji[transport_mode][index]
    return f"HP: {emoji*lives}\nTokens: {token_emoji[transport_mode] * tokens}"

#________________________________GAME______________________________#

def main():

#ALL ancii art text is by https://patorjk.com/software/taag/:
    print("""
          
 ██████╗ ██╗      ██████╗ ██████╗ ███████╗████████╗██████╗  ██████╗ ████████╗████████╗███████╗██████╗ 
██╔════╝ ██║     ██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
██║  ███╗██║     ██║   ██║██████╔╝█████╗     ██║   ██████╔╝██║   ██║   ██║      ██║   █████╗  ██████╔╝
██║   ██║██║     ██║   ██║██╔══██╗██╔══╝     ██║   ██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗
╚██████╔╝███████╗╚██████╔╝██████╔╝███████╗   ██║   ██║  ██║╚██████╔╝   ██║      ██║   ███████╗██║  ██║
 ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝                                                                                                    
                                    (GitHub: @MiguelAngelor)
                                   (API by restcountries.com)  
              
                                  🌍 Welcome to GLOBETROTTER! 🌏
                             Travel the world, one country at a time!
                                            
                                                Rules:
                                1 - Move to a Neighbour Country.
                                2 - If already visited, you lose 1 life.
                                3 - You have an IslandHopper token! 
                                  3.a. - Type "hop!" to use.
                                  3.b. - Land in an island to earn it back.
                                4- Type "end" for Game Over.
    """)

    transport, lives = choose_mode()
    islandhop = 1
    totalislandhops = 0
    moves = 0
    country_data = None
    visited = []
    #--------Get the Starter country and country data--------#
    while not country_data:
        start_country = input("\nWhat's your country, Globetrotter? ").strip() #strip to remove spaces at the beggining and the end
        country_data = get_country(start_country)
        if not country_data: print("Country not found. Try again!")
    
    current_country = country_data["name"]["common"]
    flag = country_data.get("flag", "")
    print(f"Welcome to {current_country}{flag}! You have {lives} lives and you travel {transport.lower()}.")
    print("\nTime to start your adventure! Remember you can only travel to neighbouring countries!")

    #@@@@==========================MAIN=========================@@@@@
    #@@@@=======================GAME LOOP========================@@@@@
    while lives > 0: 
        moves += 1
        current_country = country_data["name"]["common"]
        visited.append(current_country)
        flag = country_data.get("flag","")
        #--------Get the neighbors and islandhop refresh--------#
        neighbors, neighbors_initials = get_neighbors(country_data)
        if len(neighbors) <= 1 and current_country not in notislands: islandhop += 2
        if islandhop > 3: islandhop = 3

        # Print Lifebar and Tokens
        print(lifebar(transport, lives, tokens=islandhop))


        #--------Globaltrotting - PLAYER Input--------#
        guess = input(f"""\nWe are currently visiting:🡆  {visited[-1]}{flag}  🡄\n📚 {random_funfact(country_data)}\nPrevious Countries:{visited[-2:-5:-1]}\nWhat country shall we go next? """).strip()
        if guess.lower() == "end": break
        
        #--------IslandHopper--------#
        if guess == "hop!" and islandhop > 0:
            country_data = None
            islandhop -= 1
            totalislandhops += 1
            while not country_data:
                guess = input("""
Ⓘ ⓢ ⓛ ⓐ ⓝ ⓓ  🏝️  Ⓗ ⓞ ⓟ ⓟ ⓔ ⓡ !!!
One token consumed, what's your next destination? """).strip()
                country_data = get_country(guess)
                if not country_data: print("Country not found. Try again!")
            islandmessage = {
                "By Foot": f'You made a raft! After a few months you get to {country_data["name"]["common"]}!',
                "By Car":f'You took a ferry. After a few days you get to {country_data["name"]["common"]}.',
                "By Plane":f'You board first class. After a few hours you get to {country_data["name"]["common"]}!',
                "By NASA": f'SONICBOOM!!! after minutes you land at {country_data["name"]["common"]}!'
                }
            print(islandmessage[transport])
            continue
        elif guess == "hop!" and islandhop <= 0:
            guess = input("No more tokens! Where do you want to go? ")


        print("_________________________________________________________________________________")
        #--------get Neighbours--------#
        if guess.lower() in (n.lower() for n in neighbors):
            country_data = get_country(guess)
            if country_data["name"]["common"] in visited: 
                print("Country already visited, lost 1 life.❌")
                lives -= 1
        else:
            lives -=1
            if not neighbors_initials: neighbors_initials = ["None! Nada! No neighbours."]  
            if lives > 0: print(f"\nNo match found. You lost life!❌\nHINT: The neighoring countries start with the letter: {neighbors_initials}")

    #@@@@=======================END OF GAME LOOP========================@@@@@

    while True:
        map = input(f"\nGAME OVER! Did you use a map while playing? Y/N ").lower()
        if map == "y":
            map = "with the help of a Map!"
            break
        elif map == "n":
            map = "all by memory! Wow!"
            break

    total_countries = len(set(visited))
    print("_________________________________________________________________________________")
    print("""
      ╔═╗╔═╗╔╦╗╔═╗  ╔═╗╦  ╦╔═╗╦═╗      
──────║ ╦╠═╣║║║║╣ 🌏║ ║╚╗╔╝║╣ ╠╦╝──────
      ╚═╝╩ ╩╩ ╩╚═╝  ╚═╝ ╚╝ ╚═╝╩╚═      
          """)
    
    print(f"When you look back, this is your trail {life_emoji[transport][r_index] * 3}: {list(enumerate(visited,1))[::-1]}.\n")
    print(f"You visited {total_countries} different countries!\nYou used {moves} moves {map}.\nYou used {totalislandhops} IslandHopper tokens {token_emoji[transport]}.\nYou visited {total_countries/250}% of the countries!\nAll of this {transport.lower()}!") #Rest of Countries API has 250 countries and territories
    print(f"🗺️{final_map(visited)}🗺️")
    #Milestones:
    print('\nMILESTONES:')
    for i in range(1, total_countries+1):
        if i in end_messages[transport]:
            print(f"Visited {i}: {random.choice(end_messages[transport][i])}")
    if total_countries < 5:
        msg = random.choice([
            "Keep going, Globetrotter! 🌍",
            "Adventure awaits—don’t stop now! 🚶",
            "Your journey is just getting started! ✨",
            "Every step counts! 🥾",
            "Onward, explorer! 🗺️"])
        print(f"Visited {i}: {msg}")



    openmap = input("""
______________________________________________________
                    
╔╦╗┬ ┬┌─┐┌┐┌┬┌─┌─┐  ┌─┐┌─┐┬─┐  ╔═╗┬  ┌─┐┬ ┬┬┌┐┌┌─┐  
 ║ ├─┤├─┤│││├┴┐└─┐  ├┤ │ │├┬┘  ╠═╝│  ├─┤└┬┘│││││ ┬  
 ╩ ┴ ┴┴ ┴┘└┘┴ ┴└─┘  └  └─┘┴└─  ╩  ┴─┘┴ ┴ ┴ ┴┘└┘└─┘  
     ╔═╗┬  ┌─┐┌┐ ┌─┐┬ ┌┬┐┬─┐┌─┐┌┬┐┌┬┐┌─┐┬─┐┬      
     ║ ╦│  │ │├┴┐├─┤│  │ ├┬┘│ │ │  │ ├┤ ├┬┘│     
     ╚═╝┴─┘└─┘└─┘┴ ┴┴─┘┴ ┴└─└─┘ ┴  ┴ └─┘┴└─o 
                       🌏
          
   Created by: miguel.orellana.morales@gmail.com
             GitHub: @MiguelAngelOr
    Thanks to: restcountries.com API andBootDev.com.
_______________________________________________________                    

    Do you want to Open your Map? Y/N
          """)

    if openmap.lower() == "y":
        print("Opening. Thank you for your time!")
        webbrowser.open("GlobalTrotter_map.html")
    else:
        print("Declined. Thank you for your time!")
 

if __name__ == "__main__":
    main()
