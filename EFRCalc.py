class Build:
    def __init__(self):
        self.BUFF_LIST = ["antivirus", "weakness exploit", "maximum might", "latent power", "agitator", "adrenaline Rush", "counterstrike", "burst", "critical boost" , "offensive guard"]
        self.DEFAULT_BUFF_UPTIME_DICT = {"antivirus": 0, "weakness exploit": 1, "maximum might": 1, "latent power": 0, "agitator": .7, "adrenaline Rush": 0, "counterstrike": .5, "burst": 1, "critical boost": 1 , "offensive guard": 1}
            #TODO finish
        self.SET_BONUS_LIST = ["gore magala"]
        self.DEFAULT_SET_BONUS_UPTIME_DICT = {"gore magala": .8}
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

            print("For the following skills, enter the level your build contains (leave blank if you don't have the skill) and the expected uptime of the skill as a percentage: ")
            for skill in self.BUFF_LIST:
                skill_input = int(input(skill + ": ") or 0)
                uptime_input = float(input(skill + " uptime (leave blank if using default uptimes): ") or 0)

                if skill_input != 0 and uptime_input == 0:
                    self.buffs.append(
                    Buff(
                        self.weapon, 
                        skill, 
                        skill_input,
                        self.DEFAULT_BUFF_UPTIME_DICT[skill]
                    )
                )
                elif skill_input != 0 and uptime_input != 0:
                    self.buffs.append(
                        Buff(
                            self.weapon,
                            skill,
                            skill_input,
                            uptime_input
                        )
                    )
                

            for skill in self.SET_BONUS_LIST:
                skill_input = int(input(skill + ": ") or 0)
                uptime_input = float(input(skill + " uptime (leave blank if using default uptimes): ") or 0)

                if skill_input != 0 and uptime_input == 0:
                    self.buffs.append(
                    Buff(
                        self.weapon, 
                        skill, 
                        skill_input,
                        self.DEFAULT_SET_BONUS_UPTIME_DICT[skill]
                    )
                )
                elif skill_input != 0 and uptime_input != 0:
                    self.buffs.append(
                        Buff(
                            self.weapon,
                            skill,
                            skill_input,
                            uptime_input
                        )
                    )

            print("TO STRING=====================")
            for buff in self.buffs:
                print(buff)
            print("==============================")
            for bonus in self.set_bonuses:
                print(bonus)

            return



class Buff:
    def __init__(self, weapon, name, level, uptime):
        self.weapon = weapon
        self.name = name
        self.level = level
        self.uptime = uptime

    def __str__(self):
        return f"{self.name}: {self.level}, uptime: {self.uptime}"

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
            "adrenaline rush": {
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
            },
            "offensive guard": {
                1: [.05, 0],
                2: [.10, 0],
                3: [.15, 0]
            }
        }

        if skill in skills:
            return skills[skill][level]
        
    def get_burst_stats(weapon, level):
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
                return burst_weapons["great sword"][level]
            case "hunting horn":
                return burst_weapons["hunting horn"][level]
            case "dual blades":
                return burst_weapons["dual blades"][level]
            case "light bowgun" | "heavy bowgun" | "bow":
                return burst_weapons["ranged weapons"][level]
            case "long sword" | "sword and shield" | "hammer" | "lance" | "gunlance" | "switch axe" | "charge blade" | "insect glaive":
                return burst_weapons["other weapons"][level]
            
    def get_gore_set_stats(level):
        gore_stats = {
            1: [0, .15],
            2: {
                1: [10, .15], # pre curing
                2: [15, .15]  # post curing
            }
        }

        match level:
            case 1:
                return gore_stats[1]
            case 2:
                return gore_stats[2]
            
build = Build()
build.prompt_build()