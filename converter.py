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
    armor = {}
    armors = {}
    _armors_dat = None

    with open(dat, "r") as stream:
        try:
            _armors_dat = stream.read().split('\n')
        except Exception as exc:
            print(exc)

    for vnum, armor_dat in enumerate(_armors_dat):
        armor = armor.copy()
        _armor = armor_dat.split(':')
        _attr = _armor.pop(3)
        _armor = _armor + _attr.split()
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
        armors[vnum] = armor

    with open('conf/armor.yaml', 'w') as file:
        yaml.safe_dump(armors, file, default_flow_style=False)


def _get_barrier(dat="data/barriers.dat"):
    """ convert barriers.dat to yaml """
    barrier = {}
    barriers = {}
    _barriers_dat = None

    with open(dat, "r") as stream:
        try:
            _barriers = stream.read().split('\n')
        except Exception as exc:
            print(exc)

    for vnum, _barrier in enumerate(_barriers):
        _barrier = _barrier.split(':')
        barrier = barrier.copy()
        barrier['type'] = _barrier[0]
        barrier['locked_message'] = _barrier[1]
        barrier['unlocked_message'] = _barrier[2]
        barrier['rogue_message'] = _barrier[3]
        barrier['value'] = _barrier[4]
        barriers[vnum] = barrier

    with open('conf/barriers.yaml', 'w') as file:
        yaml.safe_dump(barriers, file, default_flow_style=False)


def _get_equipment(dat="data/equipment.dat"):
    """
        convert barriers.dat to yaml
        Vnum:NAME:long_name:value:weight:v2:min_equip_effect:max_equip_effect:
            equip_type:v6:charges:equip_sub_type:range:v10:quest_stat:
            v12:v13:level:town:message
        21:torch:a torch:1 10 0 0 450 21 0 0 16 0 0 0 0 0 0 1 255:

    """
    equipment = {}
    equipments = {}
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

        vnum = int(_equipment[0])
        equipment["type"] = _equipment[1].replace(" ", "_")
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

        equipments[vnum] = equipment

    with open('conf/equipment.yaml', 'w') as file:
        yaml.safe_dump(equipments, file, default_flow_style=False)


def _get_mob_weapons(dat="data/mob_weapons.dat"):
    """
    name:type:min:max:v1
    :param dat:
    :return: mob_weapons:
    """
    mob_weapon = {}
    mob_weapons = {}
    _mob_weapons = None

    with open(dat, "r") as stream:
        try:
            _mob_weapons = stream.read().split('\n')
        except Exception as exc:
            print(exc)

    for vnum, _mob_weapon in enumerate(_mob_weapons):
        print(vnum, _mob_weapon)
        _mob_weapon = _mob_weapon.split(':')
        mob_weapon = mob_weapon.copy()
        _attr = _mob_weapon.pop(1)
        _mob_weapon = _mob_weapon + _attr.split()

        mob_weapon["name"] = _mob_weapon[0]
        mob_weapon["type"] = _mob_weapon[0].replace(" ", "_")
        mob_weapon["mob_type"] = int(_mob_weapon[1])
        mob_weapon["min"] = int(_mob_weapon[2])
        mob_weapon["max"] = int(_mob_weapon[3])
        mob_weapon['damage'] = [int(_mob_weapon[2]), int(_mob_weapon[3])]
        mob_weapon["v1"] = int(_mob_weapon[4])

        mob_weapons[vnum] = mob_weapon

    with open('conf/mob_weapons.yaml', 'w') as file:
        yaml.safe_dump(mob_weapons, file, default_flow_style=False)


def _get_mobs(dat="data/mobs.dat"):
    """
    0  vnum	   0
    1  name	   strangle vine
    2  desc	   The strangle vine is a large bulbous plant with several writhing vines sprouting from it. It moves slowly about on gnarled roots.
    3  plur	   strangle vines
    4  weapon	   choking vines
    5  weapon	   null
    6  weapon	   null
    7  track	   0
    8  combat	   90
    9  terrain   4
    10 gold	   0
    11 treasure  0
    12 armor	   0
    13 special   0
    14 hit die   1
    15 regen	   0
    16 min_wep   1
    17 max_wep   4
    18 min_spec  0
    19 max_spec  0
    20 att_eff   0
    21 min_a_eff 0
    22 max_a_eff 0
    23 spec_ab   0
    24 num_att   1
    25 level     1
    26 morale    0
    27 spell_sk  0
    28 spell_ty  0
    29 min_spell 0
    30 max_spell 0
    31 gender    0
    32 sub_type  0

    :param dat:
    :return:
    """
    mob = {}
    mobs = {}
    _mobs = None

    with open(dat, "r") as stream:
        try:
            _mobs = stream.read().split('\n')
        except Exception as exc:
            print(exc)

    for _mob in _mobs:
        _mob = _mob.split(':')
        mob = mob.copy()
        _attr = _mob.pop(3)
        _attr = [int(x) for x in _attr.split()]
        _mob = _mob + _attr

        vnum = int(_mob[0])
        mob["name"] = _mob[1]
        mob["type"] = _mob[1].replace(" ", "_")
        mob["description"] = _mob[2]
        mob["plural"] = _mob[3]
        mob["special_attacks"] = [_mob[4], _mob[5], _mob[6]]
        mob["can_track"] = _mob[7]
        mob["combat_skill"] = _mob[8]
        mob["terrain"] = _mob[9]
        mob["gold"] = _mob[10]
        mob["treasure"] = _mob[11]
        mob["armor"] = _mob[12]
        mob["special_attack_percentage"] = _mob[13]
        mob["hit_dice"] = _mob[14]
        mob["regeneration"] = _mob[15]
        mob["min_weapon_damage"] = _mob[16]
        mob["max_weapon_damege"] = _mob[17]
        mob["weapon_damage"] = [_mob[16], _mob[17]]
        mob["min_special_damage"] = _mob[18]
        mob["max_special_damage"] = _mob[19]
        mob["special_damage"] = [_mob[18], _mob[19]]
        mob["attack_effect"] = _mob[20]
        mob["min_attack_effect"] = _mob[21]
        mob["max_attack_effect"] = _mob[22]
        mob["attack_effect"] = [_mob[21], _mob[22]]
        mob["special_ability"] = _mob[23]
        mob["num_attacks"] = _mob[24]
        mob["level"] = _mob[25]
        mob["morale"] = _mob[26]
        mob["spell_skill"] = _mob[27]
        mob["spell_type"] = _mob[28]
        mob["min_spell"] = _mob[29]
        mob["max_spell"] = _mob[30]
        mob["spells"] = [_mob[29], _mob[30]]
        mob["gender"] = _mob[31]
        mob["subtype"] = _mob[32]

        mobs[vnum] = mob

    with open('conf/mobs.yaml', 'w') as file:
        yaml.safe_dump(mobs, file, default_flow_style=False)


def _get_spells(dat="data/spells.dat"):
    """

    :param dat:
    :return:
    """


def _get_weapons(dat="data/weapons.dat"):
    """

    :param dat:
    :return:
    """


def main():
    """
    function main
    args: none
    returns: none
    """
    _get_armor()
    _get_barrier()
    _get_equipment()
    _get_mob_weapons()
    _get_mobs()

    return 0


if __name__ == '__main__':
    sys.exit(main())