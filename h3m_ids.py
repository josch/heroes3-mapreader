# -*- coding: utf-8 -*-

h3m_versions = {0x0E:"RoE", 0x15:"AB", 0x1C:"SoD", 0x33:"WoG"}
h3m_diffictulties = {0:"Easy", 1:"Normal", 2:"Hard", 3:"Expert", 4:"Impossible"}
h3m_player_colors = {0:"Red", 1:"Blue", 2:"Tan", 3:"Green", 4:"Orange", 5:"Purple", 6:"Teal", 7:"Pink"}
h3m_encoding_quirks = {"ISO-8859-2":"Windows-1250"}
h3m_ai_types = {0:"Random", 1:"Warrior", 2:"Builder", 3:"Explorer"}
h3m_alignments = {1:"Castle", 2:"Rampart", 3:"Tower", 4:"Inferno", 5:"Necropolis", 6:"Dungeon", 7:"Stronghold", 8:"Fortress", 9:"Conflux", 10:"Random"}
h3m_victory_conditions = {0:"Acquire artifact", 1:"Accumulate creatures", 2:"Accumulate resources", 3:"Upgrade town", 4:"Build Grail", 5:"Defeat hero", 6:"Capture town", 7:"Defeat monster", 8:"Flag all dwellings", 9:"Flag all mines", 10:"Transport artifact", 0xFF:"None"}
h3m_loss_conditions = {0:"Lose town", 1:"Lose hero", 2:"Time limit", 0xFF:"None"}
h3m_resource_types = {0:"Wood", 1:"Mercury", 2:"Ore", 3:"Sulfur", 4:"Crystal", 5:"Gems", 6:"Gold"}
h3m_terrain_types = {0:"Dirt", 1:"Desert", 2:"Grassland", 3:"Snow", 4:"Swamp", 5:"Rough", 6:"Subterraean", 7:"Lava", 8:"Water", 9:"Rock"}

h3m_hero_types = {
# Knights
0:"Orrin",
1:"Valeska",
2:"Edric",
3:"Sylvia",
4:"Lord Haart",
5:"Sorsha",
6:"Christian",
7:"Tyris",
# Clerics
8:"Rion",
9:"Adela",
10:"Cuthbert",
11:"Adelaide",
12:"Ingham",
13:"Sanya",
14:"Loynis",
15:"Caitlin",
# Rangers
16:"Mephala",
17:"Ufretin",
18:"Jenova",
19:"Ryland",
20:"Thorgrim",
21:"Ivor",
22:"Clancy",
23:"Kyrre",
# Druids
24:"Coronius",
25:"Uland",
26:"Elleshar",
27:"Gem",
28:"Malcom",
29:"Melodia",
30:"Alagar",
31:"Aeris",
# Alchemists
32:"Piquedram",
33:"Thane",
34:"Josephine",
35:"Neela",
36:"Torosar",
37:"Fafner",
38:"Rissa",
39:"Iona",
# Wizards
40:"Astral",
41:"Halon",
42:"Serena",
43:"Daremyth",
44:"Theodorus",
45:"Solmyr",
46:"Cyra",
47:"Aine",
# Demoniacs
48:"Fiona",
49:"Rashka",
50:"Marius",
51:"Ignatius",
52:"Octavia",
53:"Calh",
54:"Pyre",
55:"Nymus",
# Heretics
56:"Ayden",
57:"Xyron",
58:"Axsis",
59:"Olema",
60:"Calid",
61:"Ash",
62:"Zydar",
63:"Xarfax",
# Death Knights
64:"Straker",
65:"Vokial",
66:"Moandor",
67:"Charna",
68:"Tamika",
69:"Isra",
70:"Clavius",
71:"Galthran",
# Necromancers
72:"Septienna",
73:"Aislinn",
74:"Sandro",
75:"Nimbus",
76:"Thant",
77:"Xsi",
78:"Vidomina",
79:"Nagash",
# Overlords
80:"Lorelei",
81:"Arlach",
82:"Dace",
83:"Ajit",
84:"Damacon",
85:"Gunnar",
86:"Synca",
87:"Shakti",
# Warlocks
88:"Alamar",
89:"Jaegar",
90:"Malekith",
91:"Jeddite",
92:"Geon",
93:"Deemer",
94:"Sephinroth",
95:"Darkstorn",
# Barbarians
96:"Yog",
97:"Gurnisson",
98:"Jabarkas",
99:"Shiva",
100:"Gretchin",
101:"Krellion",
102:"Crag Hack",
103:"Tyraxor",
# Battle Mages
104:"Gird",
105:"Vey",
106:"Dessa",
107:"Terek",
108:"Zubin",
109:"Gundula",
110:"Oris",
111:"Saurug",
# Beastmasters
112:"Bron",
113:"Drakon",
114:"Wystan",
115:"Tazar",
116:"Alkin",
117:"Korbac",
118:"Gerwulf",
119:"Broghild",
# Witches
120:"Mirlanda",
121:"Rosic",
122:"Voy",
123:"Verdish",
124:"Merist",
125:"Styg",
126:"Andra",
127:"Tiva",
# Planeswalkers
128:"Pasis",
129:"Thunar",
130:"Ignissa",
131:"Lacus",
132:"Monere",
133:"Erdamon",
134:"Fiur",
135:"Kalt",
# Elementalists
136:"Luna",
137:"Brissa",
138:"Ciele",
139:"Labetha",
140:"Inteus",
141:"Aenain",
142:"Gelare",
143:"Grindan",
# Extension Heroes
144:"Sir Mullich",
145:"Adrienne",
146:"Catherine",
147:"Dracon",
148:"Gelu",
149:"Kilgor",
150:"Lord Haart",
151:"Mutare",
152:"Roland",
153:"Mutare Drake",
154:"Boragus",
155:"Xeron"}


h3m_artifact_types = {
0:"Spell book",
1:"Spell Scroll",
2:"Grail",
3:"Catapult",
4:"Ballista",
5:"Ammo Cart",
6:"First Aid Tent",
7:"Centaur Axe",
8:"Blackshard of the Dead Knight",
9:"Greater Gnoll's Flail",
10:"Ogre's Club of Havoc",
11:"Sword of Hellfire",
12:"Titan's Gladius",
13:"Shield of the Dwarven Lords",
14:"Shield of the Yawning Dead",
15:"Buckler of the Gnoll King",
16:"Targ of the Rampaging Ogre",
17:"Shield of the Damned",
18:"Sentinel's Shield",
19:"Helm of the Alabaster Unicorn",
20:"Skull Helmet",
21:"Helm of Chaos",
22:"Crown of the Supreme Magi",
23:"Hellstorm Helmet",
24:"Thunder Helmet",
25:"Breastplate of Petrified Wood",
26:"Rib Cage",
27:"Scales of the Greater Basilisk",
28:"Tunic of the Cyclops King",
29:"Breastplate of Brimstone",
30:"Titan's Cuirass",
31:"Armor of Wonder",
32:"Sandals of the Saint",
33:"Celestial Necklace of Bliss",
34:"Lion's Shield of Courage",
35:"Sword of Judgement",
36:"Helm of Heavenly Enlightenment",
37:"Quiet Eye of the Dragon",
38:"Red Dragon Flame Tongue",
39:"Dragon Scale Shield",
40:"Dragon Scale Armor",
41:"Dragonbone Greaves",
42:"Dragon Wing Tabard",
43:"Necklace of Dragonteeth",
44:"Crown of Dragontooth",
45:"Still Eye of the Dragon",
46:"Clover of Fortune",
47:"Cards of Prophecy",
48:"Ladybird of Luck",
49:"Badge of Courage",
50:"Crest of Valor",
51:"Glyph of Gallantry",
52:"Speculum",
53:"Spyglass",
54:"Amulet of the Undertaker",
55:"Vampire's Cowl",
56:"Dead Man's Boots",
57:"Garniture of Interference",
58:"Surcoat of Counterpoise",
59:"Boots of Polarity",
60:"Bow of Elven Cherrywood",
61:"Bowstring of the Unicorn's Mane",
62:"Angel Feather Arrows",
63:"Bird of Perception",
64:"Stoic Watchman",
65:"Emblem of Cognizance",
66:"Statesman's Medal",
67:"Diplomat's Ring",
68:"Ambassador's Sash",
69:"Ring of the Wayfarer",
70:"Equestrian's Gloves",
71:"Necklace of Ocean Guidance",
72:"Angel Wings",
73:"Charm of Mana",
74:"Talisman of Mana",
75:"Mystic Orb of Mana",
76:"Collar of Conjuring",
77:"Ring of Conjuring",
78:"Cape of Conjuring",
79:"Orb of the Firmament",
80:"Orb of Silt",
81:"Orb of Tempestuous Fire",
82:"Orb of Driving Rain",
83:"Recanter's Cloak",
84:"Spirit of Oppression",
85:"Hourglass of the Evil Hour",
86:"Tome of Fire Magic",
87:"Tome of Air Magic",
88:"Tome of Water Magic",
89:"Tome of Earth Magic",
90:"Boots of Levitation",
91:"Golden Bow",
92:"Sphere of Permanence",
93:"Orb of Vulnerability",
94:"Ring of Vitality",
95:"Ring of Life",
96:"Vial of Lifeblood",
97:"Necklace of Swiftness",
98:"Boots of Speed",
99:"Cape of Velocity",
100:"Pendant of Dispassion",
101:"Pendant of Second Sight",
102:"Pendant of Holiness",
103:"Pendant of Life",
104:"Pendant of Death",
105:"Pendant of Free Will",
106:"Pendant of Negativity",
107:"Pendant of Total Recall",
108:"Pendant of Courage",
109:"Everflowing Crystal Cloak",
110:"Ring of Infinite Gems",
111:"Everpouring Vial of Mercury",
112:"Inexhaustible Cart of Ore",
113:"Eversmoking Ring of Sulfur",
114:"Inexhaustible Cart of Lumber",
115:"Endless Sack of Gold",
116:"Endless Bag of Gold",
117:"Endless Purse of Gold",
118:"Legs of Legion",
119:"Loins of Legion",
120:"Torso of Legion",
121:"Arms of Legion",
122:"Head of Legion",
123:"Sea Captain's Hat",
124:"Spellbinder's Hat",
125:"Shackles of War",
126:"Orb of Inhibition",
127:"Vial of Dragon Blood",
128:"Armageddon's Blade",
129:"Angelic Alliance",
130:"Cloak of the Undead King",
131:"Elixir of Life",
132:"Armor of the Damned",
133:"Statue of Legion",
134:"Power of the Dragon Father",
135:"Titan's Thunder",
136:"Admiral's Hat",
137:"Bow of the Sharpshooter",
138:"Wizard's Well",
139:"Ring of the Magi",
140:"Cornucopia",
141:"Magic Wand",						# WoG artifact
142:"Gold Tower Arrow",					# WoG artifact
143:"Monster's Power",					# WoG artifact
144:"Highlighted Slot",					# Not an actual artifact, internal use only
145:"Artifact Lock",					# Not an actual artifact, internal use only
146:"Axe of Smashing",					# WoG Commander artifact
147:"Mithril Mail",						# WoG Commander artifact
148:"Sword of Sharpness",				# WoG Commander artifact
149:"Helm of Immortality",				# WoG Commander artifact
150:"Pendant of Sorcery",				# WoG Commander artifact
151:"Boots of Haste",					# WoG Commander artifact
152:"Bow of Seeking",					# WoG Commander artifact
153:"Dragon Eye Ring",					# WoG Commander artifact
154:"Hardened Shield",					# WoG Commander artifact
155:"Slava's Ring of Power",			# WoG Commander artifact
156:"Warlord's banner",					# WoG artifact
157:"Crimson Shield of Retribution",	# WoG artifact
158:"Barbarian Lord's Axe of Ferocity",	# WoG artifact
159:"Dragonheart",						# WoG artifact
160:"Gate Key",							# WoG artifact
161:"Blank Helmet",						# Blank artifact
162:"Blank Sword",						# Blank artifact
163:"Blank Shield",						# Blank artifact
164:"Blank Horned Ring",				# Blank artifact
165:"Blank Gemmed Ring",				# Blank artifact
166:"Blank Neck Broach",				# Blank artifact
167:"Blank Armor",						# Blank artifact
168:"Blank Surcoat",					# Blank artifact
169:"Blank Boots",						# Blank artifact
170:"Blank Horn"}						# Blank artifact


h3m_creature_types = {
0:"Pikeman",
1:"Halberdier",
2:"Archer",
3:"Marksman",
4:"Griffin",
5:"Royal Griffin",
6:"Swordsman",
7:"Crusader",
8:"Monk",
9:"Zealot",
10:"Cavalier",
11:"Champion",
12:"Angel",
13:"Archangel",
14:"Centaur",
15:"Centaur Captain",
16:"Dwarf",
17:"Battle Dwarf",
18:"Wood Elf",
19:"Grand Elf",
20:"Pegasus",
21:"Silver Pegasus",
22:"Dendroid Guard",
23:"Dendroid Soldier",
24:"Unicorn",
25:"War Unicorn",
26:"Green Dragon",
27:"Gold Dragon",
28:"Gremlin",
29:"Master Gremlin",
30:"Stone Gargoyle",
31:"Obsidian Gargoyle",
32:"Stone Golem",
33:"Iron Golem",
34:"Mage",
35:"Arch Mage",
36:"Genie",
37:"Master Genie",
38:"Naga",
39:"Naga Queen",
40:"Giant",
41:"Titan",
42:"Imp",
43:"Familiar",
44:"Gog",
45:"Magog",
46:"Hell Hound",
47:"Cerberus",
48:"Demon",
49:"Horned Demon",
50:"Pit Fiend",
51:"Pit Lord",
52:"Efreeti",
53:"Efreet Sultan",
54:"Devil",
55:"Arch Devil",
56:"Skeleton",
57:"Skeleton Warrior",
58:"Walking Dead",
59:"Zombie",
60:"Wight",
61:"Wraith",
62:"Vampire",
63:"Vampire Lord",
64:"Lich",
65:"Power Lich",
66:"Black Knight",
67:"Dread Knight",
68:"Bone Dragon",
69:"Ghost Dragon",
70:"Troglodyte",
71:"Infernal Troglodyte",
72:"Harpy",
73:"Harpy Hag",
74:"Beholder",
75:"Evil Eye",
76:"Medusa",
77:"Medusa Queen",
78:"Minotaur",
79:"Minotaur King",
80:"Manticore",
81:"Scorpicore",
82:"Red Dragon",
83:"Black Dragon",
84:"Goblin",
85:"Hobgoblin",
86:"Wolf Rider",
87:"Wolf Raider",
88:"Orc",
89:"Orc Chieftain",
90:"Ogre",
91:"Ogre Mage",
92:"Roc",
93:"Thunderbird",
94:"Cyclops",
95:"Cyclops King",
96:"Behemoth",
97:"Ancient Behemoth",
98:"Gnoll",
99:"Gnoll Marauder",
100:"Lizardman",
101:"Lizard Warrior",
102:"Gorgon",
103:"Mighty Gorgon",
104:"Serpent Fly",
105:"Dragon Fly",
106:"Basilisk",
107:"Greater Basilisk",
108:"Wyvern",
109:"Wyvern Monarch",
110:"Hydra",
111:"Chaos Hydra",
112:"Air Elemental",
113:"Earth Elemental",
114:"Fire Elemental",
115:"Water Elemental",
116:"Gold Golem",
117:"Diamond Golem",
118:"Pixie",
119:"Sprite",
120:"Psychic Elemental",
121:"Magic Elemental",
122:"NOT USED (attacker)",
123:"Ice Elemental",
124:"NOT USED (defender)",
125:"Magma Elemental",
126:"NOT USED (3)",
127:"Storm Elemental",
128:"NOT USED (4)",
129:"Energy Elemental",
130:"Firebird",
131:"Phoenix",
132:"Azure Dragon",
133:"Crystal Dragon",
134:"Faerie Dragon",
135:"Rust Dragon",
136:"Enchanter",
137:"Sharpshooter",
138:"Halfling",
139:"Peasant",
140:"Boar",
141:"Mummy",
142:"Nomad",
143:"Rogue",
144:"Troll",
145:"Catapult (specialty X1)",
146:"Ballista (specialty X1)",
147:"First Aid Tent (specialty X1)",
148:"Ammo Cart (specialty X1)",
149:"Arrow Towers (specialty X1)",
150:"Supreme Archangel",
151:"Diamond Dragon",
152:"Lord of Thunder",
153:"Antichrist",
154:"Blood Dragon",
155:"Darkness Dragon",
156:"Ghost Behemoth",
157:"Hell Hydra",
158:"Sacred Phoenix",
159:"Ghost",
160:"Emissary of War",
161:"Emissary of Peace",
162:"Emissary of Mana",
163:"Emissary of Lore",
164:"Fire Messenger",
165:"Earth Messenger",
166:"Air Messenger",
167:"Water Messenger",
168:"Gorynych",
169:"War zealot",
170:"Arctic Sharpshooter",
171:"Lava Sharpshooter",
172:"Nightmare",
173:"Santa Gremlin",
174:"Paladin (attacker)",
175:"Hierophant (attacker)",
176:"Temple Guardian (attacker)",
177:"Succubus (attacker)",
178:"Soul Eater (attacker)",
179:"Brute (attacker)",
180:"Ogre Leader (attacker)",
181:"Shaman (attacker)",
182:"Astral Spirit (attacker)",
183:"Paladin (defender)",
184:"Hierophant (defender)",
185:"Temple Guardian (defender)",
186:"Succubus (defender)",
187:"Soul Eater (defender)",
188:"Brute (defender)",
189:"Ogre Leader (defender)",
190:"Shaman (defender)",
191:"Astral Spirit (defender)",
192:"Sylvan Centaur",
193:"Sorceress",
194:"Werewolf",
195:"Hell Steed",
196:"Dracolich"}