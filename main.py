import requests
import json
import threading
import itertools
import sys
import time
import os

from dotenv import load_dotenv

load_dotenv()


def send_prompt(name, prompt, messages):
    messages.append({"role": "user", "message": prompt})
    data = json.dumps({"name": name, "messages": messages})
    url = os.getenv("URL", "http://localhost:5000/prompt")
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=data,
        )
        response.raise_for_status()
        result = response.json().get("response", "No response")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        result = "Error"

    messages.append({"role": "assistant", "message": result})
    return result


def loader():
    for c in itertools.cycle(["|", "/", "-", "\\"]):
        if done:
            break
        sys.stdout.write(f"\rLoading {c}")
        sys.stdout.flush()
        time.sleep(0.1)


def main():
    global done
    messages = []
    name = input("🤖 >>> What is your name? ")
    print("--------------")
    print(f"🤖 >>> Welcome {name}! Let's get started!")
    print("🤖 >>> Send .exit to close, and .new to start a .new chat.")
    print("--------------")
    while True:
        prompt = input(f"({name}) 🧑🏻‍💻 >>> ")

        if prompt == ".exit":
            break

        if prompt == ".new":
            messages = []
            print("🤖 >>> Starting a new chat.")
            continue

        done = False
        t = threading.Thread(target=loader)
        t.start()

        response = send_prompt(name, prompt, messages)
        done = True
        t.join()

        print("🤖 >>>", response)


if __name__ == "__main__":
    done = False
    main()
