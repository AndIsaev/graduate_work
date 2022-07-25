import inspect
import random
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from api.fake_db import FAKE_FILMS, FAKE_PERSONS
from api.models import Person
from constants import (
    ACTOR_ANSWER_LIST,
    DIRECTOR_ANSWER_LIST,
    ERROR_ANSWER_LIST,
    EXIT_ANSWER_LIST,
    FILM_ANSWER_LIST,
    SHORT_WELCOME_ANSWER_LIST,
    STATE_RESPONSE_KEY,
    TIMEOUT_ANSWER_LIST,
    WELCOME_ANSWER_LIST,
    HELP_ANSWER_LIST,
)
from request import Request
from utils import get_search_es_connection, decapitalize

es_api = get_search_es_connection()


class Scene(ABC):
    @classmethod
    def id(cls) -> str:
        return cls.__name__

    @abstractmethod
    def reply(self, request: Request) -> Dict:
        """Генерация ответа сцены"""
        raise NotImplementedError()

    @abstractmethod
    def move(self, request: Request) -> "Scene":
        """Генерация ответа сцены"""
        raise NotImplementedError()

    def fallback(self) -> Dict:
        return self._make_response(random.choice(ERROR_ANSWER_LIST))

    def timeout_fallback(self) -> Dict:
        return self._make_response(random.choice(TIMEOUT_ANSWER_LIST))

    def _make_response(
            self,
            text: str,
            tts: str = None,
            card: str = None,
            state: Optional[Dict] = None,
            buttons: str = None,
            directives: str = None,
            end_session: bool = False,
    ) -> Dict:
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
            webhook_response[STATE_RESPONSE_KEY].update(state)
        return webhook_response


class ExitScene(Scene):
    def move(self, request: Request) -> Scene:
        return ShortWelcomeScene()

    def reply(self, request: Request) -> Dict:
        return self._make_response(random.choice(EXIT_ANSWER_LIST), end_session=True)


class ActorScene(Scene):
    def move(self, request: Request) -> Scene:
        if request.intents.get("exit"):
            return ExitScene()
        elif request.intents.get("welcome"):
            return ShortWelcomeScene()
        elif request.intents.get("help"):
            return HelpScene()
        elif request.intents.get("film"):
            return FilmScene()
        elif request.intents.get("director"):
            return DirectorScene()
        elif request.intents.get("actor_of_named_film") or request.intents.get("actor_of_current_film"):
            return self
        else:
            return ErrorAnswerScene()

    def reply(self, request: Request) -> Dict:
        print("Start ActorScene.reply method")
        film = ""
        if request.intents.get("actor_of_current_film"):
            # get current film
            film = self.get_current_film()
            print(f"Current film is {film}")
        elif actor_of_named_film := request.intents.get("actor_of_named_film"):
            # get named film
            film: str = actor_of_named_film.get("slots").get("film").get("value")
            if film:
                film = decapitalize(film)
            print(f"Named film is {film}")
        actors = self.get_actors_from_es(film)
        print(f"Actors are {actors}")
        actor_names = self.get_actor_names(actors)
        print(f"Actor names are {actor_names}")
        response = self._make_response(
            random.choice(ACTOR_ANSWER_LIST).format(
                film=film,
                actors=", ".join(actor_names)
            )
        )
        print(f"Response: {response}")
        return response

    @staticmethod
    def get_current_film():
        # temp way
        return random.choice(FAKE_FILMS)

    @staticmethod
    def get_actors_from_es(film):
        # temp way
        actors = []
        person_list = FAKE_PERSONS.copy()
        for _ in range(3):
            person = random.choice(person_list)
            person_list.remove(person)
            actors.append(Person(**{'uuid': 'e42d300d-d671-4877-aa3f-d7fb1ced52ad', 'full_name': person}))
        return actors

    @staticmethod
    def get_actor_names(actors):
        return [actor.full_name for actor in actors if actor]


class FilmScene(Scene):
    def move(self, request: Request) -> Scene:
        raise NotImplementedError()

    def reply(self, request: Request) -> Dict:
        return self._make_response(random.choice(FILM_ANSWER_LIST))


class DirectorScene(Scene):
    def move(self, request: Request) -> Scene:
        raise NotImplementedError()

    def reply(self, request: Request) -> Dict:
        return self._make_response(random.choice(DIRECTOR_ANSWER_LIST))


class HelpScene(Scene):
    def move(self, request: Request) -> Scene:
        if request.intents.get("exit"):
            return ExitScene()
        elif request.intents.get("welcome"):
            return ShortWelcomeScene()
        elif request.intents.get("help"):
            return self
        elif request.intents.get("film"):
            return FilmScene()
        elif request.intents.get("director"):
            return DirectorScene()
        elif request.intents.get("actor_of_named_film") or request.intents.get("actor_of_current_film"):
            return ActorScene()
        else:
            return ErrorAnswerScene()

    def reply(self, request: Request) -> Dict:
        return self._make_response(random.choice(HELP_ANSWER_LIST))


class WelcomeScene(Scene):
    def move(self, request: Request) -> Scene:
        intents = request.intents
        if intents.get("exit"):
            return ExitScene()
        elif intents.get("welcome"):
            return ShortWelcomeScene()
        elif intents.get("help"):
            return HelpScene()
        elif intents.get("film"):
            return FilmScene()
        elif intents.get("director"):
            return DirectorScene()
        elif intents.get("actor_of_named_film") or request.intents.get("actor_of_current_film"):
            return ActorScene()
        else:
            return ErrorAnswerScene()

    def reply(self, request: Request) -> Dict:
        return self._make_response(random.choice(WELCOME_ANSWER_LIST))


class ErrorAnswerScene(Scene):
    def move(self, request: Request) -> Scene:
        return ShortWelcomeScene()

    def reply(self, request: Request) -> Dict:
        return self._make_response(random.choice(ERROR_ANSWER_LIST))


class TimeoutAnswerScene(Scene):
    def move(self, request: Request) -> Scene:
        return ShortWelcomeScene()

    def reply(self, request: Request) -> Dict:
        return self._make_response(random.choice(TIMEOUT_ANSWER_LIST))


class ShortWelcomeScene(WelcomeScene):
    def reply(self, request: Request) -> Dict:
        return self._make_response(random.choice(SHORT_WELCOME_ANSWER_LIST))


def _list_scenes() -> List:
    current_module = sys.modules[__name__]
    scenes = []
    for name, obj in inspect.getmembers(current_module):
        if inspect.isclass(obj) and issubclass(obj, Scene):
            scenes.append(obj)
    return scenes


SCENES: Dict = {scene.id(): scene for scene in _list_scenes()}
