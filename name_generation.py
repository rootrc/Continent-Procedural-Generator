import numpy as np

syllable_sets = {
    "town_names": {
        "prefixes": [
            "Al", "Bel", "Car", "Dor", "Eld", "Fen", "Gal", "Har", "Ith", "Jar", "Kor", "Lor", "Mor", "Nor",
            "Or", "Pel", "Quel", "Riv", "Sar", "Tor", "Ul", "Val", "Wyn", "Xan", "Yar", "Zel", "Thal", 
            "Bryn", "Cyn", "Drak", "Erin", "Fay", "Grim", "Hel", "Isil", "Jor", "Kael", "Lun", "Mael", "Nym",
            "Oryn", "Pyre", "Quen", "Rhal", "Syr", "Tir", "Umbr", "Vyr", "Wraith", "Xor", "Ys", "Zan"
        ],
        "middles": [
            "a", "e", "i", "o", "u", "ae", "io", "ar", "el", "or", "an", "in", "un", "eth", "ir", "il",
            "on", "yn", "ur", "is", "ol", "ia", "ai", "eo", "uth", "yr", "en", "em", "ith", "ess", "mir"
        ],
        "suffixes": [
            "dale", "ford", "heim", "hold", "mere", "mont", "peak", "reach", "rest", "rock", "stead", "ton", "vale",
            "watch", "wick", "wood", "gate", "keep", "grove", "barrow", "cliff", "hollow", "fall", "pass", "crag",
            "cairn", "meadow", "shard", "spire", "glade", "fen", "moor", "run", "ward", "bridge", "ridge", "thorn"
        ]
    },
    "continent_names": {
        "prefixes": [
            "Aza", "Bel", "Cael", "Dra", "Eri", "Fael", "Gor", "Hara", "Ira", "Jor", "Kael", "Lun", "Myth", "Nara",
            "Oth", "Prya", "Quel", "Rha", "Syl", "Tha", "Ura", "Vyn", "Wen", "Xer", "Yl", "Zha"
        ],
        "middles": [
            "an", "en", "ir", "or", "ar", "el", "un", "yn", "ir", "al", "ia", "ae", "io", "yr", "is", "os", "um", "ar"
        ],
        "suffixes": [
            "thia", "dora", "mora", "land", "terra", "garde", "thos", "dun", "var", "ria", "mir", "dran", "lon", "nara",
            "vaar", "shar", "dria", "thal", "kas", "ros", "vyn", "goth"
        ]
    }
}

def generate_name(set_name):
    syllables = syllable_sets.get(set_name)
    name = np.random.choice(syllables["prefixes"])
    if np.random.rand() > 0.5:
        name += np.random.choice(syllables["middles"])
    name += np.random.choice(syllables["suffixes"])
    return name

def generate_names(cnt, set_name):
    syllables = syllable_sets.get(set_name)
    town_names = []
    for _ in range(cnt):
        name = np.random.choice(syllables["prefixes"])
        if np.random.rand() > 0.5:
            name += np.random.choice(syllables["middles"])
        name += np.random.choice(syllables["suffixes"])
        town_names.append(name)
    return np.array(town_names)

def generate_town_names(num_towns):
    return generate_names(num_towns, "town_names")
    
def generate_continent_name():
    return generate_name("continent_names")