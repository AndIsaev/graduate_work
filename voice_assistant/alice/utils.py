from typing import Optional


def get_alice_intent_genre(entity_genre: str) -> Optional[str]:
    if "action" == entity_genre:
        return "боевик"
    elif "western" == entity_genre:
        return "вестерн"
    elif "gangster" == entity_genre:
        return "гангстер"
    elif "detective" == entity_genre:
        return "детектив"
    elif "drama" == entity_genre:
        return "драма"
    elif "historical" == entity_genre:
        return "исторический"
    elif "comedy" == entity_genre:
        return "комедия"
    elif "music_comedy" == entity_genre:
        return "музыкальная комедия"
    elif "melodrama" == entity_genre:
        return "мелодрама"
    elif "noir" == entity_genre:
        return "нуар"
    elif "adventure" == entity_genre:
        return "приключенческий"
    elif "fairytale" == entity_genre:
        return "сказка"
    elif "tragedy" == entity_genre:
        return "трагедия"
    elif "thriller" == entity_genre:
        return "триллер"
    elif "fantastic" == entity_genre:
        return "фантастика"
    elif "fantasy" == entity_genre:
        return "фентези"
    elif "disaster" == entity_genre:
        return "катастрофа"
    elif "horror" == entity_genre:
        return "ужас"
    else:
        return None
