# Based onGameReady at Network.as

import base64
import json
import struct
import gzip

# During the game data loading, it expects to receive many XML data to be reloaded. To progress smoothly without any error in the middle, send all XML data.
def generate_binaries(entries):
    payload = bytearray()

    # sending x number of files
    payload.append(len(entries))

    for path, uri, is_compressed in entries:
        with open(path, "rb") as f:
            raw = f.read()

        data = raw if is_compressed else gzip.compress(raw)

        encoded_uri = uri.encode("utf-8")
        payload += struct.pack("<H", len(encoded_uri))
        payload += encoded_uri
        payload += struct.pack("<I", len(data))
        payload += data

    return bytes(payload)

# Cost table, possibly the game building, upgrade, or item prices?
def generate_cost_table():
    return json.dumps(
        {
            "buildings": {
                "barricade": {"wood": 10, "metal": 5},
                "turret": {"wood": 50, "metal": 25}
            },
            "upgrades": {
                "storage": {"cost": 1000},
                "speed": {"cost": 500}
            }
        }
    )

# The survivor data table, obtained from Survivor.as, SurvivorClass.as, and Attributes.as. Requires an id, baseAttributes, and levelAttributes. They are mostly mocked and copy pasted.
def generate_srv_table():
    return json.dumps({
        "fighter": {
            "id": "fighter",
            "maleUpper": "fighter_upper_m",
            "maleLower": "fighter_lower_m",
            "femaleUpper": "fighter_upper_f",
            "femaleLower": "fighter_lower_f",
            "baseAttributes": {
                "health": 1,
                "combatProjectile": 1,
                "combatMelee": 1,
                "combatImprovised": 1,
                "movement": 1,
                "scavenge": 1,
                "healing": 0,
                "trapSpotting": 0,
                "trapDisarming": 0
            },
            "levelAttributes": {
                "health": 0.1,
                "combatProjectile": 0.05,
                "combatMelee": 0.05,
                "combatImprovised": 0.05,
                "movement": 0.03,
                "scavenge": 0.03,
                "healing": 0.02,
                "trapSpotting": 0.01,
                "trapDisarming": 0.01
            },
            "weapons": {
                "classes": ["rifle", "melee"],
                "types": ["primary", "secondary"]
            },
            "hideHair": False
        },
        "medic": {
            "id": "medic",
            "maleUpper": "fighter_upper_m",
            "maleLower": "fighter_lower_m",
            "femaleUpper": "fighter_upper_f",
            "femaleLower": "fighter_lower_f",
            "baseAttributes": {
                "health": 1.0,
                "combatProjectile": 0.6,
                "combatMelee": 0.7,
                "combatImprovised": 0.5,
                "movement": 1.1,
                "scavenge": 0.9,
                "healing": 1.5,
                "trapSpotting": 0.5,
                "trapDisarming": 0.5
            },
            "levelAttributes": {
                "health": 0.1,
                "combatProjectile": 0.05,
                "combatMelee": 0.05,
                "combatImprovised": 0.05,
                "movement": 0.03,
                "scavenge": 0.03,
                "healing": 0.02,
                "trapSpotting": 0.01,
                "trapDisarming": 0.01
            },
            "weapons": {
                "classes": ["rifle", "melee"],
                "types": ["primary", "secondary"]
            },
            "hideHair": False
        },
        "scavenger": {
            "id": "scavenger",
            "maleUpper": "fighter_upper_m",
            "maleLower": "fighter_lower_m",
            "femaleUpper": "fighter_upper_f",
            "femaleLower": "fighter_lower_f",
            "baseAttributes": {
                "health": 0.9,
                "combatProjectile": 0.5,
                "combatMelee": 0.6,
                "combatImprovised": 0.7,
                "movement": 1.4,
                "scavenge": 1.6,
                "healing": 0.3,
                "trapSpotting": 0.8,
                "trapDisarming": 0.5
            },
            "levelAttributes": {
                "health": 0.1,
                "combatProjectile": 0.05,
                "combatMelee": 0.05,
                "combatImprovised": 0.05,
                "movement": 0.03,
                "scavenge": 0.03,
                "healing": 0.02,
                "trapSpotting": 0.01,
                "trapDisarming": 0.01
            },
            "weapons": {
                "classes": ["rifle", "melee"],
                "types": ["primary", "secondary"]
            },
            "hideHair": False
        },
        "engineer": {
            "id": "engineer",
            "maleUpper": "fighter_upper_m",
            "maleLower": "fighter_lower_m",
            "femaleUpper": "fighter_upper_f",
            "femaleLower": "fighter_lower_f",
            "baseAttributes": {
                "health": 1.0,
                "combatProjectile": 0.6,
                "combatMelee": 0.5,
                "combatImprovised": 0.9,
                "movement": 1.0,
                "scavenge": 1.0,
                "healing": 0.2,
                "trapSpotting": 1.2,
                "trapDisarming": 1.5
            },
            "levelAttributes": {
                "health": 0.1,
                "combatProjectile": 0.05,
                "combatMelee": 0.05,
                "combatImprovised": 0.05,
                "movement": 0.03,
                "scavenge": 0.03,
                "healing": 0.02,
                "trapSpotting": 0.01,
                "trapDisarming": 0.01
            },
            "weapons": {
                "classes": ["rifle", "melee"],
                "types": ["primary", "secondary"]
            },
            "hideHair": False
        },
        "recon": {
            "id": "recon",
            "maleUpper": "fighter_upper_m",
            "maleLower": "fighter_lower_m",
            "femaleUpper": "fighter_upper_f",
            "femaleLower": "fighter_lower_f",
            "baseAttributes": {
                "health": 1.0,
                "combatProjectile": 1.4,
                "combatMelee": 0.7,
                "combatImprovised": 0.6,
                "movement": 1.5,
                "scavenge": 1.2,
                "healing": 0.1,
                "trapSpotting": 1.0,
                "trapDisarming": 0.8
            },
            "levelAttributes": {
                "health": 0.1,
                "combatProjectile": 0.05,
                "combatMelee": 0.05,
                "combatImprovised": 0.05,
                "movement": 0.03,
                "scavenge": 0.03,
                "healing": 0.02,
                "trapSpotting": 0.01,
                "trapDisarming": 0.01
            },
            "weapons": {
                "classes": ["rifle", "melee"],
                "types": ["primary", "secondary"]
            },
            "hideHair": False
        },
        "player": {
            "id": "player",
            "maleUpper": "fighter_upper_m",
            "maleLower": "fighter_lower_m",
            "femaleUpper": "fighter_upper_f",
            "femaleLower": "fighter_lower_f",
            "baseAttributes": {
                "health": 1.0,
                "combatProjectile": 1.0,
                "combatMelee": 1.0,
                "combatImprovised": 1.0,
                "movement": 1.0,
                "scavenge": 1.0,
                "healing": 1.0,
                "trapSpotting": 1.0,
                "trapDisarming": 1.0
            },
            "levelAttributes": {
                "health": 0.1,
                "combatProjectile": 0.05,
                "combatMelee": 0.05,
                "combatImprovised": 0.05,
                "movement": 0.03,
                "scavenge": 0.03,
                "healing": 0.02,
                "trapSpotting": 0.01,
                "trapDisarming": 0.01
            },
            "weapons": {
                "classes": ["rifle", "melee"],
                "types": ["primary", "secondary"]
            },
            "hideHair": False
        },
        "unassigned": {
            "id": "unassigned",
            "maleUpper": "fighter_upper_m",
            "maleLower": "fighter_lower_m",
            "femaleUpper": "fighter_upper_f",
            "femaleLower": "fighter_lower_f",
            "baseAttributes": {
                "health": 0,
                "combatProjectile": 0,
                "combatMelee": 0,
                "combatImprovised": 0,
                "movement": 0,
                "scavenge": 0,
                "healing": 0,
                "trapSpotting": 0,
                "trapDisarming": 0
            },
            "levelAttributes": {
                "health": 0.1,
                "combatProjectile": 0.05,
                "combatMelee": 0.05,
                "combatImprovised": 0.05,
                "movement": 0.03,
                "scavenge": 0.03,
                "healing": 0.02,
                "trapSpotting": 0.01,
                "trapDisarming": 0.01
            },
            "weapons": {
                "classes": ["rifle", "melee"],
                "types": ["primary", "secondary"]
            },
            "hideHair": False
        }
    })


# Player login state, includes info updates from server and the thing that has been going on since player offline (like finished war or attack report).
# Data is mostly mocked or empty.
def generate_login_state():
    dummy_upgrades = base64.b64encode(b'\x00' * 10).decode('utf-8')

    return json.dumps({
        "settings": {
            "volume": 0.8,
            "language": "en"
        },
        "news": {
            "event": "Double XP Weekend"
        },
        "sales": [
            ["weapons", "discount"],
            ["armor", "clearance"]
        ],
        "allianceWinnings": {
            "gold": 500,
            "medals": 2
        },
        "recentPVPList": [
            {"opponent": "Player123", "result": "win"},
            {"opponent": "Player456", "result": "loss"}
        ],

        # All of below is used by playerObject
        "invsize": 50,
        "upgrades": dummy_upgrades,
        "allianceId": None,
        "allianceTag": None,
        "longSession": True,
        "leveledUp": False,
        "promos": [],
        "promoSale": None,
        "dealItem": None,
        "leaderResets": 0,
        "unequipItemBinds": False,
        "globalStats": {},
        "inventory": [],
        "neighborHistory": {},
        "zombieAttack": False,
        "zombieAttackLogins": 0,
        "offersEnabled": False,
        "lastLogout": None,  # or datetime int64
        "prevLogin": None    # or datetime int64
    })
