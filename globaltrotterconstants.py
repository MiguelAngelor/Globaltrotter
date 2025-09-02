
import random

#countries that border only 1 other country but are not islands:
notislands = [
    "Canada",
    "Portugal",
    "Denmark",
    "South Korea",
    "Gambia",
    "Papua New Guinea",
    "Qatar",
    "Brunei",
    "Monaco",
    "San Marino",
    "Vatican City",
    "Lesotho"
]

#create random funfact:

def random_funfact(country_data):
    funfact = []

    official_n = country_data.get("name", {}).get("official", "N/A")
    funfact.append(f"Official Name: {official_n}")

    lang = ",".join(country_data.get("languages", {}).values()) if country_data.get("languages") else "N/A"
    funfact.append(f"Language: {lang}")

    popul = country_data.get("population", "N/A")
    funfact.append(f"Population: {popul:,}")

    capital = ",".join(country_data.get("capital", ["N/A"]))
    funfact.append(f"Capital: {capital}")

    area = country_data.get("area", "N/A")
    funfact.append(f"Area: {area:,} km²")

    currency = country_data.get("currencies", {})
    if currency:
        first_c = next(iter(currency.values()))
        currency_name = first_c.get("name", "N/A")
        currency_symbol = first_c.get("symbol", "N/A")
    else:
        currency_name = "N/A"
        currency_symbol = "N/A"

    funfact.append(f"Currency: {currency_name} ({currency_symbol})")

    return random.choice(funfact)

#Milestone Messages courtesy of chatGPT:


end_messages = {
    "By Foot": {
        5: [
            "👣 Your shoes are holding up better than expected!",
            "🥾 You’ve marched across borders—calves of steel!",
            "🍞 Bread, water, and pure grit fuel your steps.",
            "🌻 The road stretches, but you keep walking!",
            "🐾 Locals call you the wandering legend!"
        ],
        10: [
            "🏞️ 10 countries by foot—your legs deserve a medal!",
            "🥖 Blisters? Nah, just battle scars.",
            "🚶 Your footsteps echo across the continent!",
            "🗺️ You’re rewriting maps, step by step.",
            "🔥 Endurance level: mountain goat!"
        ],
        20: [
            "🚶 20 nations later, your sandals have gone legendary!",
            "🌍 Africa’s vastness bows to your footsteps!",
            "🗻 Japan greets the walking wonder!",
            "🥘 Spain again, this time with tapas power!",
            "🏖️ Brazil cheers your foot-powered arrival!"
        ],
        50: [
            "🔥 50 countries! Your legs are now international icons!",
            "🚀 Walking > NASA confirmed at country 50!",
            "👑 You’ve walked more than kings once ruled!",
            "🌌 Even the stars envy your footsteps!",
            "🎉 50 by foot—Guinness World Records, here you come!"
        ]
    },
    "By Car": {
        5: [
            "🚗 Road trip champion at 5 countries!",
            "⛽ Your tank is as endless as your wanderlust.",
            "📻 Radio static, but spirits high!",
            "🏜️ Dusty roads, shiny dreams.",
            "🐘 Unexpected traffic, but you keep rolling!"
        ],
        10: [
            "🛣️ 10th border crossed—tires still rolling strong!",
            "🎶 Your playlist survived the journey!",
            "🌅 Sunsets look better from the driver’s seat.",
            "🚦 Red light? More like world record light.",
            "🥤 Fast food wrappers mark your trail!"
        ],
        20: [
            "🎶 20th stop—your playlist is now legendary.",
            "🚙 Mongolia waves at your muddy SUV!",
            "🗼 France honks from under the Eiffel Tower!",
            "🌊 Chile greets your long-haul cruise control.",
            "🌴 Cuba cheers as your car somehow made it!"
        ],
        50: [
            "🏎️ 50 countries! Your car now deserves citizenship.",
            "🔥 Tires smoking—border patrols bow down!",
            "🎉 Half a hundred road trips complete!",
            "🌍 You’ve driven more than most pilots fly!",
            "🏁 Legendary driver status unlocked!"
        ]
    },
    "By Plane": {
        5: [
            "✈️ 5th landing—frequent flyer unlocked!",
            "🛫 Tray tables up, spirit soaring!",
            "🥤 Free soda never tasted this good.",
            "📸 Clouds make the perfect photo backdrop.",
            "🛄 Luggage still miraculously intact!"
        ],
        10: [
            "🌍 10 stamps—your passport is glowing!",
            "🦴 Jet lag is now your travel buddy.",
            "🛬 Pilots know you by first name now.",
            "🎡 You’ve mastered the duty-free shuffle!",
            "🍿 Airplane snacks are gourmet to you now."
        ],
        20: [
            "🚀 20th flight—your wings are sprouting feathers!",
            "🍜 Vietnam feeds you mid-clouds.",
            "🐧 Antarctica waves from below (chilly landing).",
            "💃 Spain cheers: flamenco at 30,000 feet!",
            "🌋 Iceland erupts in your honor!"
        ],
        50: [
            "🌌 50th country! You basically live in the sky now.",
            "👨‍✈️ Pilot salutes your passport power!",
            "🛫 Air traffic control recognizes your name!",
            "🌍 50 stamps later—you’re a legend at airports.",
            "🥳 Duty-free shops throw you a party!"
        ]
    },
    "By NASA": {
        5: [
            "🚀 5th stop—Houston is impressed!",
            "🪐 Your space suit still looks brand new!",
            "👨‍🚀 Astronaut selfie unlocked!",
            "🌕 Moon says: stylish landing!",
            "✨ Cosmic applause at your milestone!"
        ],
        10: [
            "🛰️ 10 nations later—satellites track your path.",
            "🌌 Your mileage is now galactic!",
            "🔭 Telescopes spot your trail!",
            "👽 Aliens want an autograph!",
            "💫 You bent time zones in half!"
        ],
        20: [
            "🚀 20th touchdown—you’re basically interplanetary.",
            "🌍 Earth looks smaller from up here!",
            "☄️ Comets request your autograph.",
            "🛸 UFO spotted following you to Brazil!",
            "🌠 Shooting stars envy your pace."
        ],
        50: [
            "🌎 50 countries via NASA! You bent spacetime.",
            "🪐 Saturn gives you honorary rings.",
            "👨‍🚀 Astronaut Hall of Fame unlocked!",
            "🚀 Warp drive engaged—Galactic status achieved!",
            "✨ Universe whispers: ‘Legend.’"
        ]
    }
}