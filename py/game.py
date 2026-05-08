# game.py
# The Forgotten Path — Game Logic

import asyncio
from pyscript import document, when

# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

INTRO_TEXT = (
    "You enter a world known as Dervan. Your journey is yours to decide upon. "
    "But decide carefully. Each decision has consequences. Each path opens up "
    "new opportunities. Good Luck."
)

CHARACTER_INTROS = {
    "Gaven": (
        "Gaven was the son of a blacksmith in a town far away "
        "from the capital of Toan."
    ),
    "Amos": None,
    "Kres": None,
}

TYPEWRITER_DELAY = 0.03

# ---------------------------------------------------------------------------
# Screen management
# ---------------------------------------------------------------------------

def show_screen(screen_id: str) -> None:
    """Hide every screen by referencing each one directly by ID.

    We intentionally do NOT use querySelectorAll() here because that returns
    a JavaScript NodeList object. Python cannot iterate over JavaScript objects
    natively — attempting to do so throws a silent exception that causes the
    button to appear broken with no visible error message.
    """
    document.getElementById("title-screen").classList.add("hidden")
    document.getElementById("game-screen").classList.add("hidden")
    document.getElementById(screen_id).classList.remove("hidden")

# ---------------------------------------------------------------------------
# Quest helpers
# ---------------------------------------------------------------------------

def add_quest(quest_id: str, label: str) -> None:
    """Inject a quest item into the quest panel."""
    quest_list = document.getElementById("quest-list")

    item = document.createElement("div")
    item.id = quest_id
    item.className = "quest-item"

    checkbox = document.createElement("span")
    checkbox.className = "quest-checkbox"
    checkbox.id = f"{quest_id}-checkbox"

    text = document.createElement("span")
    text.className = "quest-label"
    text.textContent = label

    item.appendChild(checkbox)
    item.appendChild(text)
    quest_list.appendChild(item)


async def complete_quest(quest_id: str) -> None:
    """Tick the checkbox, wait, then fade and remove the quest item."""
    checkbox = document.getElementById(f"{quest_id}-checkbox")
    item     = document.getElementById(quest_id)

    if checkbox:
        checkbox.classList.add("checked")
    await asyncio.sleep(0.8)

    if item:
        item.classList.add("fade-out")
    await asyncio.sleep(0.5)

    if item:
        item.remove()

# ---------------------------------------------------------------------------
# Typewriter
# ---------------------------------------------------------------------------

async def typewriter(element_id: str, text: str, delay: float = TYPEWRITER_DELAY) -> None:
    """Reveal text one character at a time inside the given element."""
    el = document.getElementById(element_id)
    el.textContent = ""
    for char in text:
        el.textContent += char
        await asyncio.sleep(delay)
    el.classList.add("typing-done")

# ---------------------------------------------------------------------------
# Game flow
# ---------------------------------------------------------------------------

async def start_game() -> None:
    """Run the opening sequence after the title screen is dismissed."""
    await typewriter("intro-text", INTRO_TEXT)
    document.getElementById("character-buttons").classList.remove("hidden")
    add_quest("quest-pick-character", "Pick your adventurer")


def handle_character(name: str) -> None:
    """Shared logic for when any character button is clicked."""
    document.getElementById("character-buttons").classList.add("hidden")

    intro = CHARACTER_INTROS.get(name)
    char_intro_el = document.getElementById("character-intro")
    char_intro_el.textContent = (
        intro if intro else f"{name}'s story is yet to be written..."
    )
    char_intro_el.classList.remove("hidden")
    asyncio.ensure_future(complete_quest("quest-pick-character"))

# ---------------------------------------------------------------------------
# Button event handlers
#
# @when("click", "#element-id") is PyScript 2024.1.1's built-in way to attach
# a Python function to a browser click event. It is async-compatible, meaning
# you can declare the handler as `async def` and use `await` inside it.
#
# Each handler is wrapped in try/except so that if anything goes wrong,
# the error is printed to the browser console (F12 → Console tab) instead
# of disappearing silently.
# ---------------------------------------------------------------------------

@when("click", "#btn-start")
async def on_start_clicked(event) -> None:
    try:
        show_screen("game-screen")
        await start_game()
    except Exception as e:
        print(f"[ERROR] on_start_clicked: {e}")


@when("click", "#btn-gaven")
async def on_gaven_clicked(event) -> None:
    try:
        handle_character("Gaven")
    except Exception as e:
        print(f"[ERROR] on_gaven_clicked: {e}")


@when("click", "#btn-amos")
async def on_amos_clicked(event) -> None:
    try:
        handle_character("Amos")
    except Exception as e:
        print(f"[ERROR] on_amos_clicked: {e}")


@when("click", "#btn-kres")
async def on_kres_clicked(event) -> None:
    try:
        handle_character("Kres")
    except Exception as e:
        print(f"[ERROR] on_kres_clicked: {e}")