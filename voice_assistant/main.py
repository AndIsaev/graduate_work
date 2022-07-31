import json
import os
import threading
import time
from queue import Queue

from alice.alice_request import AliceRequest
from alice.alice_scenes import SCENES, ErrorAnswerScene, TimeoutAnswerScene, WelcomeScene, move_to_scene
from constants import STATE_REQUEST_KEY
from loguru import logger

main_queue = Queue()


def run(event: dict, context: "runtime.RuntimeContext") -> None:
    request = AliceRequest(event)
    current_scene_id = event.get("state", {}).get(STATE_REQUEST_KEY, {}).get("scene")
    logger.debug(f"Current scene: {current_scene_id}.")
    if current_scene_id is None:
        welcome = WelcomeScene()
        main_queue.put(welcome.reply(request))
    else:
        current_scene = SCENES.get(current_scene_id, WelcomeScene)()
        next_scene = move_to_scene(request)
        logger.debug(f"Next scene: {next_scene}")
        if next_scene is not None:
            logger.debug(f"Moving from scene {current_scene.id()} to {next_scene.id()}")
            main_queue.put(next_scene.reply(request))
        else:
            logger.debug(f"Failed to parse user request at scene {current_scene.id()}")
            error_answer = ErrorAnswerScene()
            main_queue.put(error_answer.reply(request))


def timeout_run(wait_time: float) -> None:
    logger.info(f"Wait {wait_time}.")
    time.sleep(wait_time)
    main_queue.put({"timeout": True})


def handler(event: dict, context: "runtime.RuntimeContext") -> dict:  # type: ignore
    logger.info(f"Incoming request event: {json.dumps(event)}")
    wait_time = round(float(os.environ.get("LIMIT_EXECUTE_SCENE", "2.5")), 1)
    thread_timer = threading.Thread(target=timeout_run, args=(wait_time,))
    thread_main = threading.Thread(target=run, args=(event, context))
    thread_timer.daemon = True
    thread_main.daemon = True
    logger.debug("Start thread_timer.")
    thread_timer.start()
    logger.debug("Start thread_main.")
    thread_main.start()
    logger.debug("Wait to join thread_main.")
    main_response = main_queue.get(block=True)
    logger.info(f"Main response: {main_response}")
    if main_response.get("timeout"):
        timeout_answer_scene = TimeoutAnswerScene()
        fallback = timeout_answer_scene.reply(AliceRequest(event))
    else:
        fallback = main_response
    logger.debug(fallback)
    logger.debug("END")
    return fallback
