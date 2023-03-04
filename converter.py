#!/usr/bin/python3
"""
 File Name : mud.py

Basic MUD server module for creating text-based Multi-User Dungeon
(MUD) games.

Contains one class, MudServer, which can be instantiated to start a
server running then used to send and receive messages from players.

 Creation date : Thu Feb  3 20:43:03 PST 2022
 Last update : Thu Feb  3 20:43:03 PST 2022

 author: Mark Frimston - mfrimston@gmail.com
 Updated By : Jeff Brown <jeffbr@gmail.com>
"""
import sys
import yaml
import json


def _get_armor(dat="data/armor.dat"):
    """
     * 3 = Cost
     * 4 = Weight
     * 8 = Type
     * 9 = Armor Rating
     * 17 = Level
     * 18 = Town
     * 19 = Classes
     * 1     2                           3    4   5 6 7 8  9  10 11 12 13 14 15 16 17 18
     * cloak:a cloak:                    10   20  0 0 0 11 0  0  0  0  0  0  0  0  0  0
     * robes:robes:                      20   30  0 0 0 11 1  0  0  0  0  0  0  0  1  1
     * cuirass:a leather cuirass:        40   50  0 0 0 12 2  0  0  0  0  0  0  0  2  1
     * breastplate:a steel breastplate:  200  200 0 0 0 13 4  0  0  0  0  0  0  0  2  1
     * ringmail:ringmail armor:          250  300 0 0 0 13 5  0  0  0  0  0  0  0  3  1
     * chainmail:chainmail armor:        300  400 0 0 0 13 6  0  0  0  0  0  0  0  3  1
     * scalemail;scalemail armor:        400  450 0 0 0 14 8  0  0  0  0  0  0  0  4  1
     * bandmail:banded mail armor:       500  500 0 0 0 14 10 0  0  0  0  0  0  0  6  1
     * platemail:platemail armor:        600  600 0 0 0 14 12 0  0  0  0  0  0  0  8  1
     * demonhide:demonhide armor:        1500 250 0 0 0 15 15 0  0  0  0  0  0  0  10 2
     * dragonscale:dragonscale armor:    1800 500 0 0 0 16 18 0  0  0  0  0  0  0  12 2

    """
    armor = {
        "type": "",
        "type_num": 0,
        "short": "",
        "long": "",
        "ac": 0,
        "value": 0,
        "weight": 0,
        "size": "light",
        "equip": True,
        "etype:": "armor",
        "dtype": "armor",
        "level": 0,
        "town": 0,
        "inv": True,
        "Classes": 0
    }
    armors = []
    _armors_dat = None

    with open("data/armor.dat", "r") as stream:
        try:
            _armors_dat = stream.read().split('\n')
        except Exception as exc:
            print(exc)

    for armor_dat in _armors_dat:
        armor = armor.copy()
        _armor = armor_dat.split(':')
        _attr = _armor[3].split()
        del(_armor[3])
        _armor = _armor + _attr
        print(_armor)
        armor['type'] = _armor[1]
        armor['short'] = _armor[1]
        armor['long'] = _armor[2]
        armor['value'] = _armor[3]
        armor['weight'] = _armor[4]
        armor['type_num'] = _armor[8]
        armor['ac'] = _armor[9]
        armor['level'] = _armor[17]
        armor['town'] = _armor[18]
        armor['classes'] = _armor[19]
        print(armor)
        armors.append(armor)

    return armors


def _get_barrier(dat="data/barriers.dat"):
    """ convert barriers.dat to yaml """
    barrier = {
        "type": "iron door",  # 0
        "etype": "door",
        "value": 1,
        "weight": 1,
        "locked": True,
        "equip": False,
        "inv": False,
        "locked_message": None,
        "unlocked_message": None,
        "rogue_message": None
    }
    barriers = []
    _barriers_dat = None

    with open(dat, "r") as stream:
        try:
            _barriers = stream.read().split('\n')
        except Exception as exc:
            print(exc)

    for _barrier in _barriers:
        _barrier = _barrier.split(':')
        barrier = barrier.copy()
        barrier['type'] = _barrier[0]
        barrier['locked_message'] = _barrier[1]
        barrier['unlocked_message'] = _barrier[2]
        barrier['rogue_message'] = _barrier[3]
        barrier['value'] = _barrier[4]
        barriers.append(barrier)

    return barriers


def _get_equipment(dat="data/equipment.dat"):
    """
        convert barriers.dat to yaml
        Vnum:NAME:long_name:value:weight:v2:min_equip_effect:max_equip_effect:
            equip_type:v6:charges:equip_sub_type:range:v10:quest_stat:
            v12:v13:level:town:message
        21:torch:a torch:1 10 0 0 450 21 0 0 16 0 0 0 0 0 0 1 255:

    """
    equipment = {
        "type": "rope",
        "etype": "gear",
        "dtype": "gear",
        "value": 1,
        "weight": 1,
        "effect": "climb",
        "equip": False,
        "inv": True
    }
    equipments = []
    _equipments = None

    with open(dat, "r") as stream:
        try:
            _equipments = stream.read().split('\n')
        except Exception as exc:
            print(exc)

    for _equipment in _equipments:
        _equipment = _equipment.split(':')
        equipment = equipment.copy()
        _attr = _equipment.pop(3)
        _equipment = _equipment + _attr.split()

        equipment["type"] = _equipment[1].replace(" ", "_")
        equipment["vnum"] = int(_equipment[0])
        equipment["name"] = _equipment[1]
        equipment["description"] = _equipment[2]
        equipment["message"] = _equipment[3]
        equipment["value"] = int(_equipment[4])
        equipment["weight"] = int(_equipment[5])
        equipment["v6"] = _equipment[6]
        equipment["min_equip_effect"] = int(_equipment[7])
        equipment["max_equip_effect"] = int(_equipment[8])
        equipment["equip_type"] = int(_equipment[9])
        equipment["v10"] = _equipment[10]
        equipment["charges"] = int(_equipment[11])
        equipment["equip_sub_type"] = int(_equipment[12])
        equipment["range"] = int(_equipment[13])
        equipment["v10"] = _equipment[14]
        equipment["quest_stat"] = int(_equipment[15])
        equipment["v16"] = _equipment[16]
        equipment["v17"] = _equipment[17]
        equipment["v18"] = _equipment[18]
        equipment["town"] = int(_equipment[19])
        equipment["level"] = int(_equipment[20])

        equipments.append(equipment)

    return equipments


def main():
    """
    function main
    args: none
    returns: none
    """
    print(json.dumps(_get_armor(), indent=4))
    print(json.dumps(_get_barrier(), indent=4))
    print(json.dumps(_get_equipment(), indent=4))

    return 0


if __name__ == '__main__':
    sys.exit(main())