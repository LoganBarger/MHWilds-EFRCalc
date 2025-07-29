class Build:
    _WEAPON_LIST = [
        "greatsword", "longsword", "sword and shield", "dual blades", "hammer", 
        "hunting horn", "lance", "gunlance", "switch axe", "charge blade", 
        "insect glaive", "light bowgun", "heavy bowgun", "bow"
    ]
    _BUFF_LIST = [
        "antivirus", "weakness exploit", "maximum might", "latent power", "agitator", 
        "adrenaline Rush", "counterstrike", "burst", "critical boost" , "offensive guard", 
        "critical eye", "attack boost", "peak performance", "foray", "resentment", "ambush"
    ]
    
    _DEFAULT_BUFF_UPTIME_DICT = {
        "antivirus": .8, 
        "weakness exploit": 1.0, 
        "maximum might": 1.0, 
        "latent power": .45, 
        "agitator": .7, 
        "adrenaline Rush": .5, 
        "counterstrike": .6, 
        "burst": 1.0, 
        "critical boost": 1.0, 
        "offensive guard": 1.0, 
        "critical eye": 1.0, 
        "attack boost": 1.0, 
        "peak performance": .5, 
        "foray": .15, 
        "resentment": .5, 
        "ambush": .1
    }

    _SET_BONUS_LIST = [
        "gore magala's tyranny"
    ]
    _DEFAULT_SET_BONUS_UPTIME_DICT = {
        "gore magala's tyranny": .8
    }

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
        if not isinstance(weapon, str):
            raise TypeError("Weapon must be a string")
        weapon = weapon.strip().lower()
        if weapon not in self._WEAPON_LIST:
            raise ValueError("Weapon must be one of the 14 weapons in MH Wilds")
        self._weapon = weapon
    
    @property
    def buffs(self):
        return self._buffs
    
    def add_buff(self, name, level, uptime, is_set_bonus=False):
        max_lvl = Buff.max_level(name)
        if not (0 <= level <= max_lvl):
            raise ValueError(f"{name} level must be between 0 and {max_lvl}")
        
        if not (0.0 <= uptime <= 1.0):
            raise ValueError(f"{name} uptime must be a decimal between 0.0 and 1.0")
        
        buff = Buff(self.weapon, name, level, uptime)
        if is_set_bonus:
            self.set_bonuses.append(buff)
        else:
            self.buffs.append(buff)
        return
    
    @property
    def set_bonuses(self):
        return self._set_bonuses
    
    #TODO add set bonus method
    
    @property
    def base_raw(self):
        return self._base_raw
    
    @base_raw.setter
    def base_raw(self, base_raw):
        try:
            base_raw = int(base_raw)
        except ValueError:
            raise ValueError("Base raw attack must be an integer")
        if not 1 <= base_raw <= 500:
            raise ValueError("Base raw attack must be in range 1-500")
        self._base_raw = base_raw
    
    @property
    def base_crit(self):
        return self._base_crit
    
    @base_crit.setter
    def base_crit(self, base_crit):
        try:
            base_crit = float(base_crit)
        except ValueError:
            raise ValueError("Base crit must be a float")
        if not 0 <= base_crit <= 1:
            raise ValueError("Base crit must be between 0 and 1 (e.g., 0.15 for 15%).")
        self._base_crit = base_crit

    def find_buff(self, name):
        return next((buff for buff in (self.buffs + self.set_bonuses) if buff.name == name), None)
    
    def user_prompt(self, prompt, *, input_type, can_be_none=False, min_val=None, max_val=None, choices=None, skill=None):
        """
        input_type: "string", "int", "float", or "buff"
        - For string: provide choices list
        - For numeric: provide min_val and max_val
        - For buff_lvl: provide skill name
        """
        while True:
            raw = input(prompt).strip()

            # Blank handling
            if not raw:
                if can_be_none:
                    return None
                # sometimes it is valid for the user to leave a prompt answer blank. If this flag is true and the user leaves a blank it will return None.

            # Parse
            try:
                if input_type in ("int", "buff"):
                    val = int(raw)
                elif input_type == "float":
                    val = float(raw)
                else:  # string
                    val = raw.lower()
            except ValueError:
                type_name = {"int": "whole number", "buff": "whole number", "float": "decimal number"}[input_type]
                print(f"Invalid input: input must be a {type_name}")
                continue

            # Validate
            error = None

            if input_type == "string":
                if choices and val not in choices:
                    error = f"must be one of: {', '.join(choices)}"

            elif input_type in ("int", "float"):
                if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                    error = f"must be between {min_val} and {max_val}"

            elif input_type == "buff":
                max_lvl = Buff.max_level(skill)
                if not (0 <= val <= max_lvl):
                    error = f"{skill} level must be between 0 and {max_lvl}"

            if error:
                print(f"Invalid input: {error}")
                continue
            
            return val

    def prompt_build(self):
            self.weapon = self.user_prompt("Which weapon are you using: ", input_type="string", choices=self._WEAPON_LIST)
            self.base_raw = self.user_prompt("What is your base raw attack: ", input_type="int", min_val=1, max_val=500)
            self.base_crit = self.user_prompt("What is your base crit chance percentage: ", input_type="float", min_val=0.0, max_val=1.0)

            print("For the following skills, enter the level your build contains (leave blank if you don't have the skill) and the expected uptime of the skill as a decimal percentage: ")

            # Handle regular buffs

            for skill in self._BUFF_LIST + self._SET_BONUS_LIST:
                skill_input = self.user_prompt(f"{skill}: ", input_type="buff", can_be_none=True, skill=skill)
                uptime_input = self.user_prompt(f"{skill} uptime (leave blank for default): ", input_type="float", can_be_none=True, min_val=0.0, max_val=1.0)

                if skill_input:
                    if skill in self._BUFF_LIST:
                        uptime = uptime_input if uptime_input is not None else self._DEFAULT_BUFF_UPTIME_DICT[skill]
                        self.add_buff(skill, skill_input, uptime)
                    else:
                        uptime = uptime_input if uptime_input is not None else self._DEFAULT_SET_BONUS_UPTIME_DICT[skill]
                        self.add_buff(skill, skill_input, uptime, True)
    
    def calculate_efr(self):
        buff_raw = self.base_raw
        buff_crit = self.base_crit
        avg_dmg_increase = 0
        efr = 0

        offensive_guard = self.find_buff("offensive guard")
        if offensive_guard:
            buff_raw *= (1 + (offensive_guard.get_buff_stats()[0] * offensive_guard.uptime))

        attack_boost = self.find_buff("attack boost")
        if attack_boost:
            if attack_boost.level <= 3:
                buff_raw += attack_boost.get_buff_stats()[0] * attack_boost.uptime
            else:
                buff_raw += attack_boost.get_buff_stats()[0](self.base_raw) * attack_boost.uptime

        ambush = self.find_buff("ambush")
        if ambush:
            buff_raw += ambush.get_buff_stats()[0](self.base_raw) * ambush.uptime

        burst = self.find_buff("burst")
        if burst:
            buff_raw += burst.get_buff_stats()[0] * burst.uptime

        peak_performance = self.find_buff("peak performance")
        if peak_performance:
            buff_raw += peak_performance.get_buff_stats()[0] * peak_performance.uptime

        resentment = self.find_buff("resentment")
        if resentment:
            buff_raw += resentment.get_buff_stats()[0] * resentment.uptime

        agitator = self.find_buff("agitator")
        if agitator:
            buff_raw += agitator.get_buff_stats()[0] * agitator.uptime
            buff_crit += agitator.get_buff_stats()[1] * agitator.uptime

        foray = self.find_buff("foray")
        if foray:
            buff_raw += foray.get_buff_stats()[0] * foray.uptime
            buff_crit += foray.get_buff_stats()[1] * foray.uptime

        counterstrike = self.find_buff("counterstrike")
        if counterstrike:
            buff_raw += counterstrike.get_buff_stats()[0] * counterstrike.uptime

        adrenaline_rush = self.find_buff("adrenaline rush")
        if adrenaline_rush:
            buff_raw += adrenaline_rush.get_buff_stats()[0] * adrenaline_rush.uptime

        gore_set_bonus = self.find_buff("gore magala's tyranny")
        if gore_set_bonus and gore_set_bonus.level == 2:
            # gore magala's tyranny buff gives benefits both when uncured and cured. provided uptime is when the player is cleansed, the rest of the time (player is not cleansed) they get less of a buff.
            buff_raw += (gore_set_bonus.get_buff_stats()[2][0] * gore_set_bonus.uptime) + (gore_set_bonus.get_buff_stats()[1][0] * (1 - gore_set_bonus.uptime))
            buff_crit += (gore_set_bonus.get_buff_stats()[2][1] * gore_set_bonus.uptime)

        weakness_exploit = self.find_buff("weakness exploit")
        if weakness_exploit:
            buff_crit += weakness_exploit.get_buff_stats()[1] * weakness_exploit.uptime

        critical_eye = self.find_buff("critical eye")
        if critical_eye:
            buff_crit += critical_eye.get_buff_stats()[1] * critical_eye.uptime

        maximum_might = self.find_buff("maximum might")
        if maximum_might:
            buff_crit += maximum_might.get_buff_stats()[1] * maximum_might.uptime

        antivirus = self.find_buff("antivirus")
        if antivirus:
            buff_crit += antivirus.get_buff_stats()[1] * antivirus.uptime

        latent_power = self.find_buff("latent power")
        if latent_power:
            buff_crit += latent_power.get_buff_stats()[1] * latent_power.uptime

        critical_boost = self.find_buff("critical boost")
        if critical_boost:
            avg_dmg_increase = buff_crit * critical_boost.get_buff_stats()[1]
        else:
            avg_dmg_increase = buff_crit * .25

        efr = (buff_raw * (1 + avg_dmg_increase)) * 1.32 # white sharpness gives 32% increase after all other buffs are applied.

        return round(efr, 2)

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
        },
        "critical eye": {
            1: [0, .04],
            2: [0, .08],
            3: [0, .12],
            4: [0, .16],
            5: [0, .20]
        }, 
        "attack boost": {
            1: [3, 0],
            2: [5, 0],
            3: [7, 0],
            4: [lambda base_raw: base_raw * .02 + 8, 0],
            5: [lambda base_raw: base_raw * .04 + 9, 0] # attack boost 4 and 5 is a percentage buff based off of base_raw
        },
        "peak performance": {
            1: [3, 0],
            2: [6, 0],
            3: [10, 0],
            4: [15, 0],
            5: [20, 0]
        },
        "foray": {
            1: [6, 0],
            2: [8, .05],
            3: [10, .1],
            4: [12, .15],
            5: [15, .20]
        },
        "resentment": {
            1: [5, 0],
            2: [10, 0],
            3: [15, 0],
            4: [20, 0],
            5: [25, 0]
        }, 
        "ambush": {
            1: [lambda base_raw: base_raw * .05, 0],
            2: [lambda base_raw: base_raw * .10, 0],
            3: [lambda base_raw: base_raw * .15, 0] # ambush is a percentage buff based off of base_raw
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
            case "longsword" | "sword and shield" | "hammer" | "lance" | "gunlance" | "switch axe" | "charge blade" | "insect glaive":
                return self._BURST_WEAPONS["other weapons"][self.level]
            
    def get_gore_set_stats(self):
        match self.level:
            case 1:
                return self._GORE_STATS[1]
            case 2:
                return self._GORE_STATS[2]
            
    @classmethod
    def max_level(cls, skill):
        if skill in cls._SKILLS:
            return max(cls._SKILLS[skill])
        elif skill == "burst":
            return 5
        elif skill == "gore magala's tyranny":
            return 2
            
build = Build()
build.prompt_build()
print(f"Effective Raw: {build.calculate_efr()}")