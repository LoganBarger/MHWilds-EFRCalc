class Build:
    _BUFF_LIST = ["antivirus", "weakness exploit", "maximum might", "latent power", "agitator", "adrenaline Rush", "counterstrike", "burst", "critical boost" , "offensive guard"]
    _DEFAULT_BUFF_UPTIME_DICT = {"antivirus": .8, "weakness exploit": 1, "maximum might": 1, "latent power": 0, "agitator": .7, "adrenaline Rush": 0, "counterstrike": .5, "burst": 1, "critical boost": 1 , "offensive guard": 1}
        #TODO finish
    _SET_BONUS_LIST = ["gore magala's tyranny"]
    _DEFAULT_SET_BONUS_UPTIME_DICT = {"gore magala's tyranny": .8}
        #TODO check with antivirus

    def __init__(self):
        self._weapon = ""
        self._buffs = []
        self._set_bonuses = []
        self._base_raw = 0
        self._base_crit = 0

    @property
    def weapon(self):
        return self._weapon
    
    @weapon.setter
    def weapon(self, weapon):
        self._weapon = weapon
        #TODO add validation
    
    @property
    def buffs(self):
        return self._buffs
    
    #TODO add buff method
    
    @property
    def set_bonuses(self):
        return self._set_bonuses
    
    #TODO add set bonus method
    
    @property
    def base_raw(self):
        return self._base_raw
    
    @base_raw.setter
    def base_raw(self, base_raw):
        self._base_raw = base_raw
        #TODO add validation
    
    @property
    def base_crit(self):
        return self._base_crit
    
    @base_crit.setter
    def base_crit(self, base_crit):
        self._base_crit = base_crit
        #TODO add validation

    def find_buff(self, name):
        return next((buff for buff in (self.buffs + self.set_bonuses) if buff.name == name), None)

    def prompt_build(self):
            self.weapon = input("Which weapon are you using: ")
            self.base_raw = int(input("What is your base raw attack: "))
            self.base_crit = float(input("What is your base crit chance percentage: "))

            print("For the following skills, enter the level your build contains (leave blank if you don't have the skill) and the expected uptime of the skill as a percentage: ")
            for skill in self._BUFF_LIST:
                skill_input = int(input(skill + ": ") or 0)
                uptime_input = float(input(skill + " uptime (leave blank if using default uptimes): ") or 0)

                if skill_input != 0 and uptime_input == 0:
                    self._buffs.append(
                    Buff(
                        self._weapon, 
                        skill, 
                        skill_input,
                        self._DEFAULT_BUFF_UPTIME_DICT[skill]
                    )
                )
                elif skill_input != 0 and uptime_input != 0:
                    self._buffs.append(
                        Buff(
                            self._weapon,
                            skill,
                            skill_input,
                            uptime_input
                        )
                    )
                

            for skill in self._SET_BONUS_LIST:
                skill_input = int(input(skill + ": ") or 0)
                uptime_input = float(input(skill + " uptime (leave blank if using default uptimes): ") or 0)

                if skill_input != 0 and uptime_input == 0:
                    self._set_bonuses.append(
                    Buff(
                        self._weapon, 
                        skill, 
                        skill_input,
                        self._DEFAULT_SET_BONUS_UPTIME_DICT[skill]
                    )
                )
                elif skill_input != 0 and uptime_input != 0:
                    self._set_bonuses.append(
                        Buff(
                            self._weapon,
                            skill,
                            skill_input,
                            uptime_input
                        )
                    )

            # #TODO remove once complete
            # print("TO STRING=====================")
            # for buff in self._buffs:
            #     print(buff)
            # print("==============================")
            # for bonus in self._set_bonuses:
            #     print(bonus)

            return
    
    def calculate_efr(self):
        buff_raw = self.base_raw
        buff_crit_chance = 0
        avg_dmg_increase = 0

        # raw damage buff checks
        offensive_guard = self.find_buff("offensive guard")
        if offensive_guard:
            buff_raw *= (1 + (offensive_guard.get_buff_stats()[0] * offensive_guard.uptime))

        burst = self.find_buff("burst")
        if burst:
            buff_raw += (burst.get_buff_stats()[0] * burst.uptime)

        agitator = self.find_buff("agitator")
        if agitator:
            buff_raw += (agitator.get_buff_stats()[0] * agitator.uptime)

        gore_set_bonus = self.find_buff("gore magala's tyranny")
        if gore_set_bonus and gore_set_bonus.level == 2:
            # gore magala's tyranny buff gives benefits both when uncured and cured. provided uptime is when the player is cleansed, the rest of the time (player is not cleansed) they get less of a buff.
            buff_raw += (gore_set_bonus.get_buff_stats()[2][0] * gore_set_bonus.uptime) + (gore_set_bonus.get_buff_stats()[1][0] * (1 - gore_set_bonus.uptime))

        # critical chance buff checks
        # TODO

        return buff_raw

class Buff:
    _SKILLS = {
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

    _BURST_WEAPONS = {
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
    
    _GORE_STATS = {
        1: [0, .15],
        2: {
            1: [10, .15], # pre curing
            2: [15, .15]  # post curing
        }
    }

    def __init__(self, weapon, name, level, uptime):
        self._weapon = weapon
        self._name = name
        self._level = level
        self._uptime = uptime

    @property
    def weapon(self):
        return self._weapon
    
    @property
    def name(self):
        return self._name
    
    @property
    def level(self):
        return self._level
    
    @property
    def uptime(self):
        return self._uptime

    def __str__(self):
        return f"{self.name}: {self.level}, uptime: {self.uptime * 100:.0f}%"

    def get_buff_stats(self):
        if self.name == "burst":
            return self.get_burst_stats()
        elif self.name == "gore magala's tyranny":
            return self.get_gore_set_stats()
        elif self.name in self._SKILLS:
            return self._SKILLS[self.name][self.level]
        
    def get_burst_stats(self):
        match self.weapon:
            case "great sword":
                return self._BURST_WEAPONS["great sword"][self.level]
            case "hunting horn": 
                return self._BURST_WEAPONS["hunting horn"][self.level]
            case "dual blades":
                return self._BURST_WEAPONS["dual blades"][self.level]
            case "light bowgun" | "heavy bowgun" | "bow":
                return self._BURST_WEAPONS["ranged weapons"][self.level]
            case "long sword" | "sword and shield" | "hammer" | "lance" | "gunlance" | "switch axe" | "charge blade" | "insect glaive":
                return self._BURST_WEAPONS["other weapons"][self.level]
            
    def get_gore_set_stats(self):
        match self.level:
            case 1:
                return self._GORE_STATS[1]
            case 2:
                return self._GORE_STATS[2]
            
build = Build()
build.prompt_build()
print(f"Effective Raw: {build.calculate_efr()}")