import pygame
import random
import json
import platform
import asyncio
from localization import Localization

pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
SCALE_FACTOR = min(SCREEN_WIDTH / 1920, SCREEN_HEIGHT / 1080)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Stroop Test")
clock = pygame.time.Clock()
FPS = 60

def load_config():
    return {
        "screen_width": 1280,
        "screen_height": 720,
        "display_mode": "fullscreen",
        "language": "english",
        "trial_count": 10,
        "button_width": 150,
        "button_height": 80,
        "button_spacing": 20,
        "font_size": 74,
        "small_font_size": 36,
        "square_size": 100
    }

config = load_config()
localization = Localization(config["language"])
font = pygame.font.Font(None, int(config["font_size"] * SCALE_FACTOR))
small_font = pygame.font.Font(None, int(config["small_font_size"] * SCALE_FACTOR))

state = "menu"
running = True
stroop_data = {
    "part": 1,
    "trials_left": config["trial_count"],
    "word": "",
    "color": "",
    "correct_color": "",
    "position": (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
    "start_time": 0,
    "reaction_times": [],
    "correct_clicks": 0,
    "incorrect_clicks": 0,
    "feedback": "",
    "feedback_time": 0,
    "score": 0,
    "total_time": 0
}
countdown_start = 0
countdown_duration = 3000

def create_buttons():
    button_width = int(config["button_width"] * SCALE_FACTOR)
    button_height = int(config["button_height"] * SCALE_FACTOR)
    menu_buttons = [
        {"text": "play", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.3, button_width, button_height), "action": lambda: set_state("countdown"), "color": (200, 200, 200)},
        {"text": "settings", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.45, button_width, button_height), "action": lambda: set_state("settings"), "color": (200, 200, 200)},
        {"text": "exit", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.6, button_width, button_height), "action": lambda: globals().update(running=False), "color": (200, 200, 200)}
    ]
    settings_buttons = [
        {"text": "language", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.3, button_width, button_height), "action": lambda: set_state("language"), "color": (200, 200, 200)},
        {"text": "resolution", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.45, button_width, button_height), "action": lambda: set_state("resolution"), "color": (200, 200, 200)},
        {"text": "display_mode", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.6, button_width, button_height), "action": lambda: set_state("display_mode"), "color": (200, 200, 200)},
        {"text": "back", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.75, button_width, button_height), "action": lambda: set_state("menu"), "color": (200, 200, 200)}
    ]
    language_buttons = [
        {"text": "russian", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.3, button_width, button_height), "action": lambda: change_language("russian"), "color": (200, 200, 200)},
        {"text": "ukrainian", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.45, button_width, button_height), "action": lambda: change_language("ukrainian"), "color": (200, 200, 200)},
        {"text": "english", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.6, button_width, button_height), "action": lambda: change_language("english"), "color": (200, 200, 200)}
    ]
    resolutions = [(800, 600), (1280, 720), (1920, 1080), (2560, 1440)]
    resolution_buttons = [
        {"text": f"{w}x{h}", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * (0.3 + i * 0.15), button_width, button_height), "action": lambda w=w, h=h: change_resolution(w, h), "color": (200, 200, 200)}
        for i, (w, h) in enumerate(resolutions) if w <= info.current_w and h <= info.current_h
    ]
    display_mode_buttons = [
        {"text": "fullscreen", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.3, button_width, button_height), "action": lambda: change_display_mode("fullscreen"), "color": (200, 200, 200)},
        {"text": "noframe", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.45, button_width, button_height), "action": lambda: change_display_mode("noframe"), "color": (200, 200, 200)},
        {"text": "windowed", "rect": pygame.Rect(SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.6, button_width, button_height), "action": lambda: change_display_mode("windowed"), "color": (200, 200, 200)}
    ]
    total_buttons = len(localization.colors)
    total_width = total_buttons * button_width + (total_buttons - 1) * config["button_spacing"]
    start_x = (SCREEN_WIDTH - total_width) / 2
    color_buttons = [
        {"text": name, "rect": pygame.Rect(start_x + i * (button_width + config["button_spacing"]), SCREEN_HEIGHT * 0.75, button_width, button_height), "action": lambda c=name: check_color(c), "color": localization.colors[name]}
        for i, name in enumerate(localization.colors.keys())
    ]
    result_buttons = [
        {"text": "restart", "rect": pygame.Rect(SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.6, SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.1), "action": lambda: reset_game(), "color": (200, 200, 200)},
        {"text": "menu", "rect": pygame.Rect(SCREEN_WIDTH * 0.50, SCREEN_HEIGHT * 0.6, SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.1), "action": lambda: set_state("menu"), "color": (200, 200, 200)}
    ]
    return {
        "menu": menu_buttons,
        "settings": settings_buttons,
        "language": language_buttons,
        "resolution": resolution_buttons,
        "display_mode": display_mode_buttons,
        "color": color_buttons,
        "results": result_buttons
    }

buttons = create_buttons()

def set_state(new_state):
    global state, countdown_start
    state = new_state
    if new_state == "countdown":
        countdown_start = pygame.time.get_ticks()
        reset_game()

def change_language(lang):
    localization.set_language(lang)
    config["language"] = lang
    set_state("settings")

def change_resolution(width, height):
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, SCALE_FACTOR
    SCREEN_WIDTH, SCREEN_HEIGHT = width, height
    SCALE_FACTOR = min(SCREEN_WIDTH / 1920, SCREEN_HEIGHT / 1080)
    config["screen_width"], config["screen_height"] = width, height
    try:
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN if config["display_mode"] == "fullscreen" else pygame.NOFRAME if config["display_mode"] == "noframe" else 0)
        globals().update(font=pygame.font.Font(None, int(config["font_size"] * SCALE_FACTOR)), small_font=pygame.font.Font(None, int(config["small_font_size"] * SCALE_FACTOR)))
        globals().update(buttons=create_buttons())
    except pygame.error:
        screen = pygame.display.set_mode((1280, 720), 0)
        SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
        config["screen_width"], config["screen_height"] = 1280, 720
        config["display_mode"] = "windowed"
    set_state("settings")

def change_display_mode(mode):
    config["display_mode"] = mode
    change_resolution(SCREEN_WIDTH, SCREEN_HEIGHT)

def reset_game():
    global stroop_data
    stroop_data = {
        "part": 1,
        "trials_left": config["trial_count"],
        "word": "",
        "color": "",
        "correct_color": "",
        "position": (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
        "start_time": 0,
        "reaction_times": [],
        "correct_clicks": 0,
        "incorrect_clicks": 0,
        "feedback": "",
        "feedback_time": 0,
        "score": 0,
        "total_time": 0
    }
    start_trial()

def start_trial():
    if stroop_data["trials_left"] > 0:
        stroop_data["trials_left"] -= 1
        color_names = list(localization.colors.keys())
        if stroop_data["part"] == 1:
            color_key = random.choice(color_names)
            stroop_data["word"] = localization.get_color_name(color_key)
            stroop_data["color"] = random.choice(color_names)
            stroop_data["correct_color"] = color_key
            stroop_data["position"] = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        elif stroop_data["part"] == 2:
            stroop_data["word"] = ""
            stroop_data["color"] = random.choice(color_names)
            stroop_data["correct_color"] = stroop_data["color"]
            stroop_data["position"] = (SCREEN_WIDTH * (0.3 + random.random() * 0.4), SCREEN_HEIGHT * (0.3 + random.random() * 0.4))
        elif stroop_data["part"] == 3:
            color_key = random.choice(color_names)
            stroop_data["word"] = localization.get_color_name(color_key)
            stroop_data["color"] = random.choice(color_names)
            stroop_data["correct_color"] = stroop_data["color"]
            stroop_data["position"] = (SCREEN_WIDTH * (0.3 + random.random() * 0.4), SCREEN_HEIGHT * (0.3 + random.random() * 0.4))
        stroop_data["start_time"] = pygame.time.get_ticks()
        update_color_buttons()
    else:
        stroop_data["part"] += 1
        if stroop_data["part"] <= 3:
            stroop_data["trials_left"] = config["trial_count"]
            start_trial()
        else:
            set_state("results")

def update_color_buttons():
    button_width = int(config["button_width"] * SCALE_FACTOR)
    button_height = int(config["button_height"] * SCALE_FACTOR)
    total_buttons = len(localization.colors)
    total_width = total_buttons * button_width + (total_buttons - 1) * config["button_spacing"]
    start_x = (SCREEN_WIDTH - total_width) / 2
    color_names = list(localization.colors.keys())
    random.shuffle(color_names)
    buttons["color"] = [
        {"text": name, "rect": pygame.Rect(start_x + i * (button_width + config["button_spacing"]), SCREEN_HEIGHT * 0.75, button_width, button_height), "action": lambda c=name: check_color(c), "color": localization.colors[name]}
        for i, name in enumerate(color_names)
    ]

def check_color(color):
    if state == "game":
        if color == stroop_data["correct_color"]:
            reaction_time = (pygame.time.get_ticks() - stroop_data["start_time"]) / 1000.0
            stroop_data["reaction_times"].append(reaction_time)
            stroop_data["score"] += 10
            stroop_data["total_time"] += reaction_time
            stroop_data["correct_clicks"] += 1
            stroop_data["feedback"] = localization.get_text("correct")
        else:
            stroop_data["score"] -= 5
            stroop_data["incorrect_clicks"] += 1
            stroop_data["feedback"] = localization.get_text("incorrect")
        stroop_data["feedback_time"] = pygame.time.get_ticks()
        update_color_buttons()
        start_trial()

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            globals().update(running=False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            button_list = buttons.get(state, buttons["color"] if state == "game" else buttons["results"])
            for button in button_list:
                if button["rect"].collidepoint(pos):
                    button["action"]()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if state == "game":
                set_state("menu")
            else:
                globals().update(running=False)

def draw_text(text, font, color, pos):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=pos)
    screen.blit(surface, rect)

def draw_square(color_name, pos):
    size = int(config["square_size"] * SCALE_FACTOR)
    square = pygame.Surface((size, size))
    square.fill(localization.colors[color_name])
    rect = square.get_rect(center=pos)
    screen.blit(square, rect)

def draw_buttons(button_list):
    mouse_pos = pygame.mouse.get_pos()
    for button in button_list:
        color = (150, 150, 150) if button["rect"].collidepoint(mouse_pos) else button["color"]
        pygame.draw.rect(screen, color, button["rect"])
        brightness = sum(button["color"]) / 3
        text_color = (255, 255, 255) if brightness < 128 else (0, 0, 0)
        draw_text(localization.get_text(button["text"]), small_font, text_color, button["rect"].center)

def render():
    screen.fill((255, 255, 255))
    if state in ["menu", "settings", "language", "resolution", "display_mode"]:
        draw_buttons(buttons[state])
    elif state == "countdown":
        elapsed = pygame.time.get_ticks() - countdown_start
        countdown = max(0, 3 - elapsed // 1000)
        draw_text(str(countdown + 1), font, (0, 0, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        if elapsed >= countdown_duration:
            set_state("game")
    elif state == "game":
        if stroop_data["part"] in [1, 3]:
            draw_text(stroop_data["word"], font, localization.colors[stroop_data["color"]], stroop_data["position"])
        elif stroop_data["part"] == 2:
            draw_square(stroop_data["color"], stroop_data["position"])
        draw_buttons(buttons["color"])
        if stroop_data["feedback"] and pygame.time.get_ticks() - stroop_data["feedback_time"] < 500:
            draw_text(stroop_data["feedback"], small_font, (0, 255, 0) if stroop_data["feedback"] == localization.get_text("correct") else (255, 0, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.6))
    elif state == "results":
        avg_time = sum(stroop_data["reaction_times"]) / len(stroop_data["reaction_times"]) if stroop_data["reaction_times"] else 0
        coefficient = 1 / avg_time if avg_time > 0 else 0
        total_clicks = stroop_data["correct_clicks"] + stroop_data["incorrect_clicks"]
        accuracy = (stroop_data["correct_clicks"] / total_clicks * 100) if total_clicks > 0 else 0
        draw_text(localization.get_text("avg_time").format(avg_time=avg_time), font, (0, 0, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.3))
        draw_text(localization.get_text("coefficient").format(coefficient=coefficient), font, (0, 0, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.4))
        draw_text(localization.get_text("accuracy").format(accuracy=accuracy), font, (0, 0, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.5))
        draw_buttons(buttons["results"])
    pygame.display.flip()

async def main():
    global running
    while running:
        handle_events()
        render()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)
    pygame.quit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())