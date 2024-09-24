'''
Consume Snitch

Reads in a text file called summary, and prints out several barcharts of each players consume use

Structure of file is:
    helers - standard use of helper functions
    snitch functions - parses logs
    plots - plots data

    each plot uses a snitch function to parse the log data


example summary.txt file
!!! note: the extra enemies and data must be removed from the log file

Aeteis deaths:5
   Fire Protection 5 
   Flask of the Titans 1   (93g 46s 83c)
   Mana Potion - Major 1   (1g 83s 98c)
   Nature Protection 4 
   Shadow Protection 4   (27g 33s 96c)

   total spent: 122g 64s 77c
Aretes deaths:8
   Blessed Wizard Oil 2   (9g 77s 76c)
   Brilliant Wizard Oil 1   (1g 65s 56c)
   Dreamshard Elixir 6   (11g 33s 64c)
   Dreamtonic 7   (8g 95s 93c)
   Elixir of Shadow Power 6   (13g 19s 58c)
   Fire Protection 2 
   Flask of Supreme Power 1   (73g 30s 36c)
   Greater Arcane Elixir 6   (20g 45s 82c)
   Healing Potion - Major 1   (43s 72c)
   Invulnerability 7   (13g 56s 67c)
   Medivh's Merlot 1   (4g 11s 57c)
   Nature Protection 1 
   Shadow Protection 3   (20g 50s 47c)
   Tea with Sugar 10 

   total spent: 177g 31s 8c
Bigdaddy deaths:6
   Consecrated Sharpening Stone 2   (10g 61s 84c)
   Elixir of Fortitude 5   (6g 19s 20c)
   Elixir of Superior Defense 5   (19g 2s 85c)
   Elixir of the Mongoose 6   (52g 67s 22c)
   Fire Protection 5 
   Flask of the Titans 1   (93g 46s 83c)
   Free Action Potion 4   (7g 57s 64c)
   Gift of Arthas 4 
   Goblin Sapper Charge 2   (4g 67s 88c)
   Great Rage Potion 6 
   Healing Potion - Major 4   (1g 74s 88c)
   Increased Stamina 5 
   Invulnerability 1   (1g 93s 81c)
   Nature Protection 3 
   Rage of Ages (ROIDS) 6   (26g 35s 50c)
   Rumsey Rum Black Label 6   (5g 7s 12c)
   Spirit of Zanza 5   (11g 66s 70c)
   Tea with Sugar 2 
   Winterfall Firewater 8   (8g 17s 60c)

   total spent: 249g 19s 7c
   
'''


import re
import matplotlib.pyplot as plt

# Helpers
# Function to convert a wow gold string "1g1s1c" into a float 1.0101
def convert_currency_string_to_float(currency_string):
    # Split the input string into individual components
    components = currency_string.split()

    # Initialize variables for gold, silver, and copper values
    gold = 0
    silver = 0
    copper = 0

    # Iterate through components and update values
    for component in components:
        if 'g' in component:
            gold = int(component[:-1]) if component[:-1].isdigit() else 0
        elif 's' in component:
            silver = int(component[:-1]) if component[:-1].isdigit() else 0
        elif 'c' in component:
            copper = int(component[:-1]) if component[:-1].isdigit() else 0


    # Convert values to the final float
    result_float = gold + silver / 100 + copper / 10000
    return result_float


# Snitches - Read logs and snitch the facts
 
def snitch_total_gold(file_path = 'summary.txt'):
    # total gold spent

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Extracting information for each player
    matches = re.finditer(r'(\w+) deaths:(\d+).+?total spent: (\d+g \d+s \d+c)', file_content, flags=re.DOTALL)
    raiders = {}

    for match in matches:
        player_name = match.group(1).capitalize()
        death_count = match.group(2)
        total_spent = match.group(3)
        raiders.update({f"{player_name} ({death_count})" : convert_currency_string_to_float(total_spent)})

    return {k: v for k, v in sorted(raiders.items(), key=lambda item: item[1])}

def snitch_mana_consumes(file_path = 'summary.txt'):
    # total quantity of mana consumes used

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Extracting information for each player
    matches = re.finditer(r'(\w+) deaths:\d+(.+?)(?=(?:\1|total spent))', file_content, flags=re.DOTALL)

    raiders = {}

    for match in matches:
        player_name = match.group(1).capitalize()
        mana_pot_count = re.search(r'Mana Potion - Major (\d+)', match.group(2))
        rejuv_pot_count = re.search(r'Rejuvenation Potion - Major (\d+)', match.group(2))
        tea_count = re.search(r'Tea with Sugar (\d+)', match.group(2))

        if mana_pot_count:
            mana_pot_count = mana_pot_count.group(1)
        else:
            mana_pot_count = 0

        if rejuv_pot_count:
            rejuv_pot_count = rejuv_pot_count.group(1)
        else:
            rejuv_pot_count = 0
        
        if tea_count:
            tea_count = tea_count.group(1)
        else:
            tea_count = 0

        total = float(mana_pot_count) + float(rejuv_pot_count) + float(tea_count)
        raiders.update({f"{player_name}" : total})
        
    return {k: v for k, v in sorted(raiders.items(), key=lambda item: item[1])}

def snitch_caster_consumes(file_path = 'summary.txt'):
    # total quantity of caster dmg consumes used

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Extracting information for each player
    matches = re.finditer(r'(\w+) deaths:\d+(.+?)(?=(?:\1|total spent))', file_content, flags=re.DOTALL)

    raiders = {}

    for match in matches:
        player_name = match.group(1).capitalize()
        fosp = re.search(r'Flask of Supreme Power (\d+)', match.group(2))
        bwo = re.search(r'Brilliant Wizard Oil (\d+)', match.group(2))
        blwo = re.search(r'Blessed Wizard Oil (\d+)', match.group(2))
        dse = re.search(r'Dreamshard Elixir (\d+)', match.group(2))
        dt = re.search(r'Dreamtonic (\d+)', match.group(2))
        gae = re.search(r'Greater Arcane Elixir (\d+)', match.group(2))
        eosp = re.search(r'Elixir of Shadow Power (\d+)', match.group(2))
        eogfp = re.search(r'Elixir of Greater Firepower (\d+)', match.group(2))

        if fosp:
            fosp = fosp.group(1)
        else:
            fosp = 0
        
        if bwo:
            bwo = bwo.group(1)
        else:
            bwo = 0

        if blwo:
            blwo = blwo.group(1)
        else:
            blwo = 0

        if dse:
            dse = dse.group(1)
        else:
            dse = 0
        
        if dt:
            dt = dt.group(1)
        else:
            dt = 0
        
        if gae:
            gae = gae.group(1)
        else:
            gae = 0
        
        if eosp:
            eosp = eosp.group(1)
        else:
            eosp = 0
        
        if eogfp:
            eogfp = eogfp.group(1)
        else:
            eogfp = 0

        total = float(fosp) + float(bwo) + float(blwo) + float(dse) + float(dt) + float(gae) + float(eosp) + float(eogfp)
        raiders.update({f"{player_name}" : total})
        
    return {k: v for k, v in sorted(raiders.items(), key=lambda item: item[1])}

def snitch_melee_consumes(file_path = 'summary.txt'):
    # total quantity of melee dmg consumes used

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Extracting information for each player
    matches = re.finditer(r'(\w+) deaths:\d+(.+?)(?=(?:\1|total spent))', file_content, flags=re.DOTALL)

    raiders = {}

    for match in matches:
        player_name = match.group(1).capitalize()
        eotm = re.search(r'Elixir of the Mongoose (\d+)', match.group(2))
        sots = re.search(r'Strike of the Scorpok (\d+)', match.group(2))
        wffw = re.search(r'Winterfall Firewater (\d+)', match.group(2))
        eotg = re.search(r'Elixir of the Giants (\d+)', match.group(2))
        css = re.search(r'Consecrated Sharpening Stones (\d+)', match.group(2))
        roids = re.search(r'Rage of Ages \(ROIDS\) (\d+)', match.group(2))

        if eotm:
            eotm = eotm.group(1)
        else:
            eotm = 0
        
        if sots:
            sots = sots.group(1)
        else:
            sots = 0

        if wffw:
            wffw = wffw.group(1)
        else:
            wffw = 0
        
        if eotg:
            eotg = eotg.group(1)
        else:
            eotg = 0
        if css:
            css = css.group(1)
        else:
            css = 0
        
        if roids:
            roids = roids.group(1)
        else:
            roids = 0

        total = float(eotm) + float(sots) + float(wffw) + float(eotg) + float(css) + float(roids)
        raiders.update({f"{player_name}" : total})
        
    return {k: v for k, v in sorted(raiders.items(), key=lambda item: item[1])}

def snitch_zanza_consumes(file_path = 'summary.txt'):
    # total quantity of zanza consumes used

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Extracting information for each player
    matches = re.finditer(r'(\w+) deaths:\d+(.+?)(?=(?:\1|total spent))', file_content, flags=re.DOTALL)

    raiders = {}

    for match in matches:
        player_name = match.group(1).capitalize()
        spirit_zanza_count = re.search(r'Spirit of Zanza (\d+)', match.group(2))
        swift_zanza_count = re.search(r'Swiftness of Zanza (\d+)', match.group(2))

        if spirit_zanza_count:
            spirit_zanza_count = spirit_zanza_count.group(1)
        else:
            spirit_zanza_count = 0

        if swift_zanza_count:
            swift_zanza_count = swift_zanza_count.group(1)
        else:
            swift_zanza_count = 0
        
        total = float(spirit_zanza_count) + float(swift_zanza_count)
        raiders.update({f"{player_name}" : total})
        
    return {k: v for k, v in sorted(raiders.items(), key=lambda item: item[1])}

def snitch_shadow_prot_consumes(file_path = 'summary.txt'):
    # Total shadow protection consumes used

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Extracting information for each player
    matches = re.finditer(r'(\w+) deaths:\d+(.+?)(?=(?:\1|total spent))', file_content, flags=re.DOTALL)

    raiders = {}

    for match in matches:
        player_name = match.group(1).capitalize()
        shadow_protection_count = re.search(r'Shadow Protection (\d+)', match.group(2))
        if shadow_protection_count:
            shadow_protection_count = shadow_protection_count.group(1)
        else:
            shadow_protection_count = 0
        raiders.update({f"{player_name}" : float(shadow_protection_count)})
        
    return {k: v for k, v in sorted(raiders.items(), key=lambda item: item[1])}

def snitch_frost_prot_consumes(file_path = 'summary.txt'):
    # Total frost protection consumes used

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Extracting information for each player
    matches = re.finditer(r'(\w+) deaths:\d+(.+?)(?=(?:\1|total spent))', file_content, flags=re.DOTALL)

    raiders = {}

    for match in matches:
        player_name = match.group(1).capitalize()
        shadow_protection_count = re.search(r'Frost Protection (\d+)', match.group(2))
        if shadow_protection_count:
            shadow_protection_count = shadow_protection_count.group(1)
        else:
            shadow_protection_count = 0
        raiders.update({f"{player_name}" : float(shadow_protection_count)})
        
    return {k: v for k, v in sorted(raiders.items(), key=lambda item: item[1])}

def snitch_nature_prot_consumes(file_path = 'summary.txt'):
    # Total nature protection consumes used

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Extracting information for each player
    matches = re.finditer(r'(\w+) deaths:\d+(.+?)(?=(?:\1|total spent))', file_content, flags=re.DOTALL)

    raiders = {}

    for match in matches:
        player_name = match.group(1).capitalize()
        shadow_protection_count = re.search(r'Nature Protection (\d+)', match.group(2))
        if shadow_protection_count:
            shadow_protection_count = shadow_protection_count.group(1)
        else:
            shadow_protection_count = 0
        raiders.update({f"{player_name}" : float(shadow_protection_count)})
        
    return {k: v for k, v in sorted(raiders.items(), key=lambda item: item[1])}


def snitch_flask_consumes(file_path = 'summary.txt'):
    # total quantity of mana consumes used

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Extracting information for each player
    matches = re.finditer(r'(\w+) deaths:\d+(.+?)(?=(?:\1|total spent))', file_content, flags=re.DOTALL)

    raiders = {}

    for match in matches:
        player_name = match.group(1).capitalize()
        p = re.search(r'Flask of Supreme Power (\d+)', match.group(2))
        t = re.search(r'Flask of the Titans (\d+)', match.group(2))
        w = re.search(r'Flask of Distilled Wisdom (\d+)', match.group(2))

        if p:
            p = p.group(1)
        else:
            p = 0

        if t:
            t = t.group(1)
        else:
            t = 0
        
        if w:
            w = w.group(1)
        else:
            w = 0

        total = float(p) + float(t) + float(w)
        raiders.update({f"{player_name}" : total})
        
    return {k: v for k, v in sorted(raiders.items(), key=lambda item: item[1])}

# Plots - visualize snitch data
plt.rcParams['figure.figsize'] = [13, 8] # standardize plot size (in inches)

# plot total_gold
raiders = snitch_total_gold('summary.txt')
players = list(raiders.keys())
costs = list(raiders.values())
plt.barh(players, costs, color='blue')
plt.xlabel(f'Gold Spent\nTotal: {sum(costs)}\nAverage: {sum(costs) / len(players)}')
plt.ylabel('Player')
plt.title('Consume Snitch\nTotal Gold Spent')
plt.show()

# plot mana_consumes
raiders = snitch_mana_consumes('summary.txt')
players = list(raiders.keys())
costs = list(raiders.values())
plt.barh(players, costs, color='blue')
plt.xlabel(f'Mana Pots + Rejuv Pots + Tea Consumed\nTotal: {sum(costs)}\nAverage: {sum(costs) / len(players)}')
plt.ylabel('Player')
plt.title('Consume Snitch\nTotal Mana Consumes')
plt.show()

# plot caster_consumes
raiders = snitch_caster_consumes('summary.txt')
players = list(raiders.keys())
costs = list(raiders.values())
plt.barh(players, costs, color='blue')
plt.xlabel(f'Spell Damage Consumes\nTotal: {sum(costs)}\nAverage: {sum(costs) / len(players)}')
plt.ylabel('Player')
plt.title('Consume Snitch\nTotal Spell Damage Consumes')
plt.show()

# plot melee_consumes
raiders = snitch_melee_consumes('summary.txt')
players = list(raiders.keys())
costs = list(raiders.values())
plt.barh(players, costs, color='blue')
plt.xlabel(f'Melee Damage Consumes\nTotal: {sum(costs)}\nAverage: {sum(costs) / len(players)}')
plt.ylabel('Player')
plt.title('Consume Snitch\nTotal Melee Damage Consumes')
plt.show()

# plot zanza_consumes
raiders = snitch_zanza_consumes('summary.txt')
players = list(raiders.keys())
costs = list(raiders.values())
plt.barh(players, costs, color='blue')
plt.xlabel(f'Zanzas (spirit + swiftness) Consumed\nTotal: {sum(costs)}\nAverage: {sum(costs) / len(players)}')
plt.ylabel('Player')
plt.title('Consume Snitch - Total Zanzas Consumed')
plt.show()

# plot shadow_prot_consumes
raiders = snitch_shadow_prot_consumes('summary.txt')
players = list(raiders.keys())
costs = list(raiders.values())
plt.barh(players, costs, color='blue')
plt.xlabel(f'Shadow Protection Potions Consumed\nTotal: {sum(costs)}\nAverage: {sum(costs) / len(players)}')
plt.ylabel('Player')
plt.title('Consume Snitch\nTotal Shadow Protection Potions Consumed')
plt.show()

# plot frost_prot_consumes
raiders = snitch_frost_prot_consumes('summary.txt')
players = list(raiders.keys())
costs = list(raiders.values())
plt.barh(players, costs, color='blue')
plt.xlabel(f'Frost Protection Potions Consumed\nTotal: {sum(costs)}\nAverage: {sum(costs) / len(players)}')
plt.ylabel('Player')
plt.title('Consume Snitch\nTotal Frost Protection Potions Consumed')
plt.show()

# plot nature_prot_consumes
raiders = snitch_nature_prot_consumes('summary.txt')
players = list(raiders.keys())
costs = list(raiders.values())
plt.barh(players, costs, color='blue')
plt.xlabel(f'Nature Protection Potions Consumed\nTotal: {sum(costs)}\nAverage: {sum(costs) / len(players)}')
plt.ylabel('Player')
plt.title('Consume Snitch - Total Nature Protection Potions Consumed')
plt.show()

# plot flask_consumes
raiders = snitch_flask_consumes('summary.txt')
players = list(raiders.keys())
costs = list(raiders.values())
plt.barh(players, costs, color='blue')
plt.xlabel(f'Flasks Consumed\nTotal: {sum(costs)}\nAverage: {sum(costs) / len(players)}')
plt.ylabel('Player')
plt.title('Consume Snitch - Total Flasks Consumed')
plt.show()