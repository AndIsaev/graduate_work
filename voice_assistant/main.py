import json
import os
import threading
import time

from alice.alice_scenes import SCENES, ErrorAnswerScene, TimeoutAnswerScene, WelcomeScene, move_to_scene

from constants import STATE_REQUEST_KEY
from alice.alice_request import AliceRequest

handler_response: dict = {}


def run(event: dict, context: "runtime.RuntimeContext") -> None:
    global handler_response
    request = AliceRequest(event)
    current_scene_id = event.get("state", {}).get(STATE_REQUEST_KEY, {}).get("scene")
    print(f"Current scene: {current_scene_id}.")
    if current_scene_id is None:
        welcome = WelcomeScene()
        handler_response = welcome.reply(request)
    else:
        current_scene = SCENES.get(current_scene_id, WelcomeScene)()
        next_scene = move_to_scene(request)
        print(f"Next scene: {next_scene}")
        if next_scene is not None:
            print(f"Moving from scene {current_scene.id()} to {next_scene.id()}")
            handler_response = next_scene.reply(request)
        else:
            print(f"Failed to parse user request at scene {current_scene.id()}")
            error_answer = ErrorAnswerScene()
            handler_response = error_answer.reply(request)


def timeout_run(wait_time: float) -> None:
    global handler_response
    print(f"Wait {wait_time}, Handler response: {handler_response}")
    time.sleep(wait_time)
    handler_response = {"timeout": True}


def handler(event: dict, context: "runtime.RuntimeContext") -> dict:
    global handler_response
    if handler_response:
        handler_response = {}
    print(f"Incoming request event: {json.dumps(event)}")
    wait_time = round(float(os.environ.get("LIMIT_EXECUTE_SCENE", "2.5")), 1)
    thread_timer = threading.Thread(target=timeout_run, args=(wait_time,))
    thread_main = threading.Thread(target=run, args=(event, context))
    thread_timer.daemon = True
    thread_main.daemon = True
    print("Start thread_timer.")
    thread_timer.start()
    print("Start thread_main.")
    thread_main.start()
    print("Wait to join thread_main.")
    index = 0
    while True:
        print(f"Index: {index}. Fallback: {handler_response}")
        if handler_response:
            if handler_response.get("timeout"):
                timeout_answer_scene = TimeoutAnswerScene()
                fallback = timeout_answer_scene.reply(AliceRequest(event))
            else:
                fallback = handler_response
            print(fallback)
            print("END")
            return fallback
        index += 1
        time.sleep(0.1)
