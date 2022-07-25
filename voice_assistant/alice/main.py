import json
from typing import Dict

from constants import STATE_REQUEST_KEY
from request import Request
from scenes import SCENES, ShortWelcomeScene, WelcomeScene, ErrorAnswerScene


def handler(event: Dict, context: "runtime.RuntimeContext") -> Dict:
    print(f"Incoming request event: {json.dumps(event)}")
    request = Request(event)
    current_scene_id = event.get("state", {}).get(STATE_REQUEST_KEY, {}).get("scene")
    print(f"Current scene: {current_scene_id}.")
    if current_scene_id is None:
        welcome = WelcomeScene()
        return welcome.reply(request)
    current_scene = SCENES.get(current_scene_id, WelcomeScene)()
    next_scene = current_scene.move(request)
    print(f"Next scene: {next_scene}")
    if next_scene is not None:
        print(f"Moving from scene {current_scene.id()} to {next_scene.id()}")
        return next_scene.reply(request)
    else:
        print(f"Failed to parse user request at scene {current_scene.id()}")
        error_answer = ErrorAnswerScene()
        return error_answer.reply(request)
