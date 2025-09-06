import requests
import random
import webbrowser
import time #to create a small delay before opening the map
from globetrotterconstants import notislands, end_messages, random_funfact, final_map

#__________________GAME MODE__________________#
def choose_mode():
    modes = {
        "1": ("By Foot", 3, "This adventure is powered by... your own feet, that's crazy!"),
        "2": ("By Car", 6, "Time to hit the road, nothing like 4 wheels and A/C."),
        "3": ("By Plane", 9, "First Class passangers, time to board"),
        "0": ("By NASA", 18, "NASA?! Huston, we have a problem.")
            }
    print("Hello Globetrotter, choose your traverse method:")
    for k, (name, lives, _) in modes.items():
        print(f"{k}. {name} ({lives} lives)")
    
    choice = input("\nEnter 1, 2, 3 or 0: ")
    mode, lives, message = modes.get(choice, ("By Foot", 3, "Invalid choice! Default: By Foot.\nThis adventure is sponsored by... your own feet, crazy!"))
    print("\n" + message)
    return mode, lives

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

def get_flag(country): #using .get for safety
    return country.get("flag","")

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
    return f"HP: {(emoji+' ')*lives}\nTokens: {(token_emoji[transport_mode]+' ') * tokens}"

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
    flag = get_flag(country_data)
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
        if len(neighbors) <= 1 and current_country not in notislands: 
            islandhop = min(islandhop + 2, 3)

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
            print("_________________________________________________________________________________")
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
        
        #Final Check of the LOOP:
        if lives == 0: print("Wrong move! ;_;" )
    #@@@@=======================END OF GAME LOOP========================@@@@@

    while True:
        map = input(f"\nGAME OVER! Did you open a map while playing? Y/N ").lower()
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
    print(f"You visited {total_countries} different countries!\n"
                       f"You used {moves} moves {map}.\n"
                       f"You used {totalislandhops} IslandHopper tokens {token_emoji[transport]}.\n"
                       f"You visited {(total_countries/250)*100:.2f}% of the countries!\n" #Rest of Countries API has 250 countries and territories
                       f"All of this {transport.lower()}!") 

    #Milestones:
    print('\nMILESTONES:')
    if total_countries < 5:
        msg = random.choice([
            "Keep going, Globetrotter! 🌍",
            "Adventure awaits—don’t stop now! 🚶",
            "Your journey is just getting started! ✨",
            "Every step counts! 🥾",
            "Onward, explorer! 🗺️"])
        print(f"Visited {total_countries}: {msg}")
        
    for i in range(1, total_countries+1):
        if i in end_messages[transport]:
            print(f"Visited {i}: {random.choice(end_messages[transport][i])}")

    create_map = input("\nDraw a Map (html file) of your adventure? (Y/N)")

    #drawing map
    if create_map.lower() == "y":
        mapmessage, filename = final_map(visited, life_emoji[transport][r_index])
        print(f"\n{mapmessage}")
        time.sleep(0.15) #100 ms of delay to open the map
        webbrowser.open(filename)
    else:
        print("\nNo map was created.")

    print("""
______________________________________________________
                    
╔╦╗┬ ┬┌─┐┌┐┌┬┌─┌─┐  ┌─┐┌─┐┬─┐  ╔═╗┬  ┌─┐┬ ┬┬┌┐┌┌─┐  
 ║ ├─┤├─┤│││├┴┐└─┐  ├┤ │ │├┬┘  ╠═╝│  ├─┤└┬┘│││││ ┬  
 ╩ ┴ ┴┴ ┴┘└┘┴ ┴└─┘  └  └─┘┴└─  ╩  ┴─┘┴ ┴ ┴ ┴┘└┘└─┘  
      ╔═╗┬  ┌─┐┌┐ ┌─┐┌┬┐┬─┐┌─┐┌┬┐┌┬┐┌─┐┬─┐┬      
      ║ ╦│  │ │├┴┐├┤  │ ├┬┘│ │ │  │ ├┤ ├┬┘│     
      ╚═╝┴─┘└─┘└─┘└─┘ ┴ ┴└─└─┘ ┴  ┴ └─┘┴└─o 
                       🌏
          
   Created by: miguel.orellana.morales@gmail.com
             GitHub: @MiguelAngelOr
    Thanks to: restcountries.com API andBootDev.com.
      Ascii: https://patorjk.com/software/taag/
                Map library: Folium
_______________________________________________________\n""")                    
###opening map (OPTIONAL) NOT USED
#   if create_map.lower() == "y":
#        openmap = input("""
#          +-+-+-+-+ +-+-+-+-+ +-+-+-+-+
#          |D|r|a|w| |y|o|u|r| |M|a|p|:|
#          +-+-+-+-+ +-+-+-+-+ +-+-+-+-+
#        Do you want to Open your Map? Y/N
#          """)
#        if openmap.lower() == "y":
#            print("""
#       Opening... Thanks for your time, see you soon!
#          """)
#            webbrowser.open(filename)
#        else:
#            print("""
# Map was not opened at this time. Thanks for your time, see you soon!
#          """)###


if __name__ == "__main__":
    main()
