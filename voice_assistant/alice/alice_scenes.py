import inspect
import random
import sys
from abc import ABC
from typing import Optional

from api.fake_db import get_fake_actors, get_fake_film, get_fake_film_list
from constants import (ACTOR_ANSWER_LIST, DIRECTOR_ANSWER_LIST, ERROR_ANSWER_LIST, EXIT_ANSWER_LIST,
                       FILM_DESCRIPTION_ANSWER_LIST, HELP_ANSWER_LIST, SHORT_WELCOME_ANSWER_LIST, STATE_RESPONSE_KEY,
                       TIMEOUT_ANSWER_LIST, TOP_FILMS_ANSWER_LIST, WELCOME_ANSWER_LIST, REPEAT_ANSWER_LIST,
                       UNKNOWN_ANSWER_LIST, FILM_DESCRIPTION_WITH_GENRES_ANSWER_LIST)
from request import Request
from scenes import Scene
from utils import decapitalize, get_person_names, get_search_es_connection

es_api = get_search_es_connection()


class AliceScene(Scene, ABC):
    def _make_response(
        self,
        text: str,
        tts: Optional[str] = None,
        card: Optional[str] = None,
        state: Optional[dict] = None,
        buttons: Optional[str] = None,
        directives: Optional[str] = None,
        end_session: bool = False,
    ) -> dict:
        response = {
            "text": text,
            "tts": tts if tts is not None else text,
        }
        if card is not None:
            response["card"] = card
        if buttons is not None:
            response["buttons"] = buttons
        if directives is not None:
            response["directives"] = directives
        response["end_session"] = str(end_session).lower()
        webhook_response = {
            "response": response,
            "version": "1.0",
            STATE_RESPONSE_KEY: {
                "scene": self.id(),
            },
        }
        if state is not None:
            webhook_response[STATE_RESPONSE_KEY] |= state
        return webhook_response


class WelcomeScene(AliceScene):
    def reply(self, request: Request) -> dict:
        return self._make_response(random.choice(WELCOME_ANSWER_LIST))


class ShortWelcomeScene(WelcomeScene):
    def reply(self, request: Request) -> dict:
        return self._make_response(random.choice(SHORT_WELCOME_ANSWER_LIST))


class HelpScene(AliceScene):
    def reply(self, request: Request) -> dict:
        return self._make_response(random.choice(HELP_ANSWER_LIST))


class ExitScene(AliceScene):
    def reply(self, request: Request) -> dict:
        return self._make_response(random.choice(EXIT_ANSWER_LIST), end_session=True)


class RepeatScene(AliceScene):
    def reply(self, request: Request) -> dict:
        return self._make_response(random.choice(REPEAT_ANSWER_LIST))


class UnknownAnswerScene(AliceScene):
    def reply(self, request: Request) -> dict:
        return self._make_response(random.choice(UNKNOWN_ANSWER_LIST))


class ErrorAnswerScene(AliceScene):
    def reply(self, request: Request) -> dict:
        return self._make_response(random.choice(ERROR_ANSWER_LIST))


class TimeoutAnswerScene(AliceScene):
    def reply(self, request: Request) -> dict:
        return self._make_response(random.choice(TIMEOUT_ANSWER_LIST))


class ActorScene(AliceScene):
    def reply(self, request: Request) -> dict:
        print("Start ActorScene.reply method")
        film_name = ""
        if request.intents.get("actor_of_current_film"):
            # get current film
            film_name = get_fake_film()
            print(f"Current film is {film_name}")
        elif actor_of_named_film := request.intents.get("actor_of_named_film"):
            # get named film
            film_name: str = actor_of_named_film.get("slots").get("film").get("value")
            print(f"Named film is {film_name}")
        if film_name:
            film_name = decapitalize(film_name)
        else:
            return self._make_response(random.choice(UNKNOWN_ANSWER_LIST))
        actors = es_api.find_film_actors(film_name=film_name)
        print(f"Actors are {actors}")
        if not actors:
            return self._make_response(f"К сожалению, не нашла актеров фильма: {film_name}")
        actor_names = get_person_names(actors)
        print(f"Actor names are {actor_names}")
        response = self._make_response(
            random.choice(ACTOR_ANSWER_LIST).format(film=film_name, actors=", ".join(actor_names))
        )
        print(f"Response of ActorScene: {response}")
        return response


class DirectorScene(AliceScene):
    def reply(self, request: Request) -> dict:
        print("Start DirectorScene.reply method")
        film_name = ""
        if request.intents.get("director_of_current_film"):
            # get current film
            film_name = get_fake_film()
            print(f"Current film is {film_name}")
        elif director_of_named_film := request.intents.get("director_of_named_film"):
            # get named film
            film_name: str = director_of_named_film.get("slots").get("film").get("value")
            print(f"Named film is {film_name}")
        if film_name:
            film_name = decapitalize(film_name)
        else:
            return self._make_response(random.choice(UNKNOWN_ANSWER_LIST))
        directors = es_api.find_film_directors(film_name=film_name, limit=1)
        print(f"Actors are {directors}")
        if not directors:
            return self._make_response(f"К сожалению, не нашла режиссера фильма: {film_name}")
        director_names = get_person_names(directors)
        print(f"Director names are {director_names}")
        response = self._make_response(
            random.choice(DIRECTOR_ANSWER_LIST).format(film=film_name, actors=", ".join(director_names))
        )
        print(f"Response of DirectorScene: {response}")
        return response


class FilmDescriptionScene(AliceScene):
    def reply(self, request: Request) -> dict:
        print("Start FilmDescriptionScene.reply method")
        film_name = ""
        if request.intents.get("description_of_current_film"):
            # get current film
            film_name = get_fake_film()
            print(f"Current film is {film_name}")
        elif description_of_named_film := request.intents.get("description_of_named_film"):
            # get named film
            film_name: str = description_of_named_film.get("slots").get("film").get("value")
            print(f"Named film is {film_name}")
        if not film_name:
            return self._make_response(random.choice(UNKNOWN_ANSWER_LIST))
        film_name = decapitalize(film_name)
        films = es_api.find_film_by_name(film_name=film_name)
        if not films:
            error_answer = ErrorAnswerScene()
            return error_answer.reply(request)
        film = films[0]
        print(f"Description is {film}")
        genres = [genre.name for genre in film.genre if genre]
        if genres:
            response = self._make_response(
                random.choice(FILM_DESCRIPTION_WITH_GENRES_ANSWER_LIST).format(
                    film=film.title, description=film.description, imdb_rating=film.imdb_rating, genre=", ".join(genres)
                )
            )
        else:
            response = self._make_response(
                random.choice(FILM_DESCRIPTION_ANSWER_LIST).format(
                    film=film.title, description=film.description, imdb_rating=film.imdb_rating
                )
            )
        print(f"Response of FilmDescriptionScene: {response}")
        return response


class TopFilmsScene(AliceScene):
    def reply(self, request: Request) -> dict:
        print("Start TopFilmsScene.reply method")
        genre: Optional[str] = request.intents.get("top_films").get("slots").get("genre").get("value")
        if genre:
            film_name_list = get_fake_film_list()
        else:
            film_name_list = es_api.find_top_films()
        print(f"Top films are {film_name_list}")
        response = self._make_response(random.choice(TOP_FILMS_ANSWER_LIST).format(films=", ".join(film_name_list)))
        print(f"Response of TopFilmsScene: {response}")
        return response


def _list_scenes() -> list:
    """Получение списка всех сцен."""
    current_module = sys.modules[__name__]
    scenes = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, Scene):
            scenes.append(obj)
    return scenes


def move_to_scene(request: Request) -> AliceScene:
    intents = request.intents
    if intents.get("exit"):
        return ExitScene()
    elif intents.get("welcome"):
        return ShortWelcomeScene()
    elif intents.get("help"):
        return HelpScene()
    elif intents.get("description_of_current_film") or intents.get("description_of_named_film"):
        return FilmDescriptionScene()
    elif intents.get("top_films"):
        return TopFilmsScene()
    elif intents.get("director_of_current_film") or intents.get("director_of_named_film"):
        return DirectorScene()
    elif intents.get("actor_of_named_film") or intents.get("actor_of_current_film"):
        return ActorScene()
    else:
        return ErrorAnswerScene()


SCENES: dict = {scene.id(): scene for scene in _list_scenes()}
