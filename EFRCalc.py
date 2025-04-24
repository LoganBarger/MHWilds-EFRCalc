class Build:
    def __init__(self):
        self.BUFF_LIST = ["antivirus", "weakness exploit", "maximum might", "latent power", "agitator", "adrenaline Rush", "counterstrike", "burst", "critical boost"]
        self.SET_BONUS_LIST = ["gore magala"]
        self.weapon = ""
        self.buffs = []
        self.set_bonuses = []
        self.base_raw = 0
        self.base_crit = 0
        self.buff_raw = 0
        self.buff_crit_chance = 0
        self.avg_dmg_increase = 0

    def prompt_build(self):
            self.weapon = input("Which weapon are you using: ")
            self.base_raw = input("What is your base raw attack: ")
            self.base_crit = input("What is your base crit chance percentage: ")

            print("For the following skills, enter the level your build contains (0 means you don't have the skill): ")
            for skill in self.BUFF_LIST:
                self.buffs.append(
                    Buff(
                        self.weapon, 
                        skill, 
                        int(input(skill + ": "))
                    )      
                )

            for skill in self.SET_BONUS_LIST:
                self.set_bonuses.append(
                    Buff(
                        self.weapon, 
                        skill, 
                        int(input(skill + ": "))
                    )      
                )

            print("=============================")
            for buff in self.buffs:
                print(buff)
            print("==============================")
            for bonus in self.set_bonuses:
                print(bonus)

            return



class Buff:
    def __init__(self, weapon, name, level):
        self.weapon = weapon
        self.name = name
        self.level = level

    def __str__(self):
        return f"{self.name}: {self.level}"

    def get_buff_stats(skill, level):
        skills = {
            "antivirus": {
                1: [0, .03],
                2: [0, .06],
                3: [0, .10]
            },
            "weakness exploit": {
                1: [0, .05],
                2: [0, .10],
                3: [0, .15],
                4: [0, .20],
                5: [0, .30]
            },
            "maximum might": {
                1: [0, .10],
                2: [0, .20],
                3: [0, .30]
            },
            "latent power": {
                1: [0, .10],
                2: [0, .20],
                3: [0, .30],
                4: [0, .40],
                5: [0, .50]
            },
            "agitator": {
                1: [4, .03],
                2: [8, .05],
                3: [12, .07],
                4: [16, .10],
                5: [20, .15]
            },
            "adrenaline Rush": {
                1: [10, 0],
                2: [15, 0],
                3: [20, 0],
                4: [25, 0],
                5: [30, 0]
            },
            "counterstrike": {
                1: [10, 0],
                2: [15, 0],
                3: [25, 0]
            },
            "critical boost": {
                1: [0, .28],
                2: [0, .31],
                3: [0, .34],
                4: [0, .37],
                5: [0, .40]
            }
        }
        
    def get_burst_stats(weapon):
        burst_weapons = {
            "great sword": {
                1: [10, 0],
                2: [12, 0],
                3: [14, 0],
                4: [16, 0],
                5: [18, 0]
            },
            "hunting horn": {
                1: [10, 0],
                2: [12, 0],
                3: [14, 0],
                4: [16, 0],
                5: [18, 0]
            },
            "dual blades": {
                1: [8, 0],
                2: [10, 0],
                3: [12, 0],
                4: [15, 0],
                5: [18, 0]
            },
            "ranged weapons": {
                1: [6, 0],
                2: [7, 0],
                3: [8, 0],
                4: [9, 0],
                5: [10, 0]
            },
            "other weapons": {
                1: [8, 0],
                2: [10, 0],
                3: [12, 0],
                4: [15, 0],
                5: [18, 0]
            }                
        }

        match weapon:
            case "great sword":
                return burst_weapons["great sword"]
            case "hunting horn":
                return burst_weapons["hunting horn"]
            case "dual blades":
                return burst_weapons["dual blades"]
            case "light bowgun" | "heavy bowgun" | "bow":
                return burst_weapons["ranged weapons"]
            case "long sword" | "sword and shield" | "hammer" | "lance" | "gunlance" | "switch axe" | "charge blade" | "insect glaive":
                return burst_weapons["other weapons"]
            
    def get_gore_set_stats(level):
        gore_stats = {
            2: [0, .15],
            4: {
                1: [10, .15], # pre curing
                2: [15, .15]  # post curing
            }
        }

        match level:
            case 2:
                return gore_stats[2]
            case 4:
                return gore_stats[4]
            
build = Build()
build.prompt_build()