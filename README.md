# consumesnitch
visualize consume expenditures

wowcombatlog -> summarizeconsumes -> consumesnitch

Reads in a text file called, and prints out several barcharts of each players consume use

Structure of file is:
    helpers - standard use of helper functions
    snitch functions - parses logs
    plots - plots data

each plot uses a snitch function to parse the log data


example summary.txt file

note: the extra enemies and data must be removed from the log file

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


made by volcker