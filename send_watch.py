import json
import random
import os
import requests

WATCHES_FILE = "watches.json"
STATE_FILE = "state.json"

# Load watches
with open(WATCHES_FILE, "r") as f:
    watches = json.load(f)["watches"]

# Load existing state or create new
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    state = {
        "remaining": [],
        "round": 1,
        "history": []
    }

# If current round exhausted, reshuffle
if not state["remaining"]:
    state["remaining"] = watches[:]
    random.shuffle(state["remaining"])

    # Avoid immediate repeat across rounds
    if state["history"]:
        last_watch = state["history"][-1]

        if state["remaining"][0] == last_watch and len(state["remaining"]) > 1:
            state["remaining"][0], state["remaining"][1] = (
                state["remaining"][1],
                state["remaining"][0],
            )

    if state["history"]:
        state["round"] += 1

# Pick next watch
selected = state["remaining"].pop(0)

# Save history
state["history"].append(selected)

# Save updated state
with open(STATE_FILE, "w") as f:
    json.dump(state, f, indent=2)

# Telegram settings
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

message = (
    f"⌚ Watch Rotation\n\n"
    f"Round: {state['round']}\n"
    f"Today's watch: {selected}\n\n"
    f"Remaining this round: {len(state['remaining'])}"
)

# Send Telegram message
response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(response.status_code)
print(response.text)

print(message)