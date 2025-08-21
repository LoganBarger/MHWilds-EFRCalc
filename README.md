## Monster Hunter Wilds – Build Calculator
A Python tool for modeling Monster Hunter Wilds builds by calculating Effective Raw (EFR) based on weapon choice, buffs, and set bonuses. This project demonstrates object-oriented programming (OOP) principles such as encapsulation, data validation, and modular class design.

## Features
- Add buffs (skills) and set bonuses with levels and uptime percentages.
- Validate inputs (weapon type, skill levels, buff uptime, raw attack values, etc.).
- Calculate Effective Raw (EFR) with sharpness and critical modifiers applied.
- Modular Build and Buff classes for extensibility.

## Getting Started
### Prerequisites
- Python 3.10+

### Run the program
```
Python EFRCalc.py
```
you will be prompted to enter:
- Weapon choice
- Base raw attack value
- Base critical chance
- Skill levels and uptime percentages for each buff / set bonus

The program then outputs:
```
Effective Raw: 491.72
```

## Roadmap
- Managed database for buff and weapon stats to decouple the data from the program
- Build a simple UI (either a desktop app with a GUI toolkit or a web app version for broader accessibility)
- Support elemental damage calculations
