import pygame
import random
import json
import platform
import asyncio
from typing import Dict, List, Tuple, Callable
from dataclasses import dataclass
from pathlib import Path
from localization import Localization

@dataclass
class GameConfig:
    screen_width: int = 1280
    screen_height: int = 720
    display_mode: str = "fullscreen"
    language: str = "english"
    trial_count: int = 10
    button_width: int = 150
    button_height: int = 80
    button_spacing: int = 20
    font_size: int = 74
    small_font_size: int = 36
    square_size: int = 100

    @classmethod
    def load(cls) -> 'GameConfig':
        try:
            config_path = Path("config.json")
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(**data)
        except Exception as e:
            print(f"Error loading config: {e}")
        return cls()

    def save(self) -> None:
        try:
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(self.__dict__, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

class Button:
    def __init__(self, text: str, rect: pygame.Rect, action: Callable, color: Tuple[int, int, int]):
        self.text = text
        self.rect = rect
        self.action = action
        self.color = color

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, localization: Localization) -> None:
        mouse_pos = pygame.mouse.get_pos()
        color = (150, 150, 150) if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        brightness = sum(self.color) / 3
        text_color = (255, 255, 255) if brightness < 128 else (0, 0, 0)
        text_surface = font.render(localization.get_text(self.text), True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class StroopTest:
    def __init__(self):
        pygame.init()
        self.info = pygame.display.Info()
        self.config = GameConfig.load()
        self.setup_display()
        self.setup_game_state()

    def setup_display(self) -> None:
        self.SCREEN_WIDTH = self.info.current_w
        self.SCREEN_HEIGHT = self.info.current_h
        self.SCALE_FACTOR = min(self.SCREEN_WIDTH / 1920, self.SCREEN_HEIGHT / 1080)
        
        try:
            if self.config.display_mode == "fullscreen":
                self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
            elif self.config.display_mode == "noframe":
                self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.NOFRAME)
            else:
                self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height))
        except pygame.error:
            self.screen = pygame.display.set_mode((1280, 720))
            self.config.screen_width = 1280
            self.config.screen_height = 720
            self.config.display_mode = "windowed"
            self.config.save()

        pygame.display.set_caption("Stroop Test")
        self.clock = pygame.time.Clock()
        self.FPS = 60

    def setup_game_state(self) -> None:
        self.localization = Localization(self.config.language)
        self.font = pygame.font.Font(None, int(self.config.font_size * self.SCALE_FACTOR))
        self.small_font = pygame.font.Font(None, int(self.config.small_font_size * self.SCALE_FACTOR))
        
        self.state = "menu"
        self.running = True
        self.stroop_data = self.create_stroop_data()
        self.countdown_start = 0
        self.countdown_duration = 3000
        self.buttons = self.create_buttons()

    def create_stroop_data(self) -> Dict:
        return {
            "part": 1,
            "trials_left": self.config.trial_count,
            "word": "",
            "color": "",
            "correct_color": "",
            "position": (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2),
            "start_time": 0,
            "reaction_times": [],
            "correct_clicks": 0,
            "incorrect_clicks": 0,
            "feedback": "",
            "feedback_time": 0,
            "score": 0,
            "total_time": 0
        }

    def create_buttons(self) -> Dict[str, List[Button]]:
        button_width = int(self.config.button_width * self.SCALE_FACTOR)
        button_height = int(self.config.button_height * self.SCALE_FACTOR)

        menu_buttons = [
            Button("play", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.3, button_width, button_height),
                  lambda: self.set_state("countdown"), (200, 200, 200)),
            Button("settings", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.45, button_width, button_height),
                  lambda: self.set_state("settings"), (200, 200, 200)),
            Button("exit", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.6, button_width, button_height),
                  lambda: setattr(self, 'running', False), (200, 200, 200))
        ]

        settings_buttons = [
            Button("language", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.3, button_width, button_height),
                  lambda: self.set_state("language"), (200, 200, 200)),
            Button("resolution", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.45, button_width, button_height),
                  lambda: self.set_state("resolution"), (200, 200, 200)),
            Button("display_mode", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.6, button_width, button_height),
                  lambda: self.set_state("display_mode"), (200, 200, 200)),
            Button("back", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.75, button_width, button_height),
                  lambda: self.set_state("menu"), (200, 200, 200))
        ]

        language_buttons = [
            Button("russian", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.3, button_width, button_height),
                  lambda: self.change_language("russian"), (200, 200, 200)),
            Button("ukrainian", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.45, button_width, button_height),
                  lambda: self.change_language("ukrainian"), (200, 200, 200)),
            Button("english", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.6, button_width, button_height),
                  lambda: self.change_language("english"), (200, 200, 200))
        ]

        resolutions = [(800, 600), (1280, 720), (1920, 1080), (2560, 1440)]
        resolution_buttons = [
            Button(f"{w}x{h}", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * (0.3 + i * 0.15), button_width, button_height),
                  lambda w=w, h=h: self.change_resolution(w, h), (200, 200, 200))
            for i, (w, h) in enumerate(resolutions) if w <= self.info.current_w and h <= self.info.current_h
        ]

        display_mode_buttons = [
            Button("fullscreen", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.3, button_width, button_height),
                  lambda: self.change_display_mode("fullscreen"), (200, 200, 200)),
            Button("noframe", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.45, button_width, button_height),
                  lambda: self.change_display_mode("noframe"), (200, 200, 200)),
            Button("windowed", pygame.Rect(self.SCREEN_WIDTH * 0.4, self.SCREEN_HEIGHT * 0.6, button_width, button_height),
                  lambda: self.change_display_mode("windowed"), (200, 200, 200))
        ]

        total_buttons = len(self.localization.colors)
        total_width = total_buttons * button_width + (total_buttons - 1) * self.config.button_spacing
        start_x = (self.SCREEN_WIDTH - total_width) / 2
        color_buttons = [
            Button(name, pygame.Rect(start_x + i * (button_width + self.config.button_spacing),
                                   self.SCREEN_HEIGHT * 0.75, button_width, button_height),
                  lambda c=name: self.check_color(c), self.localization.colors[name])
            for i, name in enumerate(self.localization.colors.keys())
        ]

        result_buttons = [
            Button("restart", pygame.Rect(self.SCREEN_WIDTH * 0.35, self.SCREEN_HEIGHT * 0.6,
                                        self.SCREEN_WIDTH * 0.15, self.SCREEN_HEIGHT * 0.1),
                  lambda: self.reset_game(), (200, 200, 200)),
            Button("menu", pygame.Rect(self.SCREEN_WIDTH * 0.50, self.SCREEN_HEIGHT * 0.6,
                                     self.SCREEN_WIDTH * 0.15, self.SCREEN_HEIGHT * 0.1),
                  lambda: self.set_state("menu"), (200, 200, 200))
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

    def set_state(self, new_state: str) -> None:
        self.state = new_state
        if new_state == "countdown":
            self.countdown_start = pygame.time.get_ticks()
            self.reset_game()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.state == "game":
                    self.set_state("menu")
                else:
                    self.running = False

    def handle_mouse_click(self, pos: Tuple[int, int]) -> None:
        button_list = self.buttons.get(self.state, 
                                     self.buttons["color"] if self.state == "game" else self.buttons["results"])
        for button in button_list:
            if button.rect.collidepoint(pos):
                button.action()

    async def run(self) -> None:
        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(self.FPS)
            await asyncio.sleep(1.0 / self.FPS)
        pygame.quit()

    def render(self) -> None:
        self.screen.fill((255, 255, 255))
        
        if self.state in ["menu", "settings", "language", "resolution", "display_mode"]:
            self.render_buttons(self.buttons[self.state])
        elif self.state == "countdown":
            self.render_countdown()
        elif self.state == "game":
            self.render_game()
        elif self.state == "results":
            self.render_results()
            
        pygame.display.flip()

    def render_buttons(self, button_list: List[Button]) -> None:
        for button in button_list:
            button.draw(self.screen, self.small_font, self.localization)

    def render_countdown(self) -> None:
        elapsed = pygame.time.get_ticks() - self.countdown_start
        countdown = max(0, 3 - elapsed // 1000)
        self.draw_text(str(countdown + 1), self.font, (0, 0, 0), (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2))
        if elapsed >= self.countdown_duration:
            self.set_state("game")

    def render_game(self) -> None:
        if self.stroop_data["part"] in [1, 3]:
            self.draw_text(self.stroop_data["word"], self.font, 
                         self.localization.colors[self.stroop_data["color"]], 
                         self.stroop_data["position"])
        elif self.stroop_data["part"] == 2:
            self.draw_square(self.stroop_data["color"], self.stroop_data["position"])
        
        self.render_buttons(self.buttons["color"])
        
        if (self.stroop_data["feedback"] and 
            pygame.time.get_ticks() - self.stroop_data["feedback_time"] < 500):
            color = (0, 255, 0) if self.stroop_data["feedback"] == self.localization.get_text("correct") else (255, 0, 0)
            self.draw_text(self.stroop_data["feedback"], self.small_font, color, 
                         (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT * 0.6))

    def render_results(self) -> None:
        avg_time = (sum(self.stroop_data["reaction_times"]) / 
                   len(self.stroop_data["reaction_times"])) if self.stroop_data["reaction_times"] else 0
        coefficient = 1 / avg_time if avg_time > 0 else 0
        total_clicks = self.stroop_data["correct_clicks"] + self.stroop_data["incorrect_clicks"]
        accuracy = (self.stroop_data["correct_clicks"] / total_clicks * 100) if total_clicks > 0 else 0
        
        self.draw_text(self.localization.get_text("avg_time").format(avg_time=avg_time), 
                      self.font, (0, 0, 0), (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT * 0.3))
        self.draw_text(self.localization.get_text("coefficient").format(coefficient=coefficient), 
                      self.font, (0, 0, 0), (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT * 0.4))
        self.draw_text(self.localization.get_text("accuracy").format(accuracy=accuracy), 
                      self.font, (0, 0, 0), (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT * 0.5))
        self.render_buttons(self.buttons["results"])

    def draw_text(self, text: str, font: pygame.font.Font, color: Tuple[int, int, int], 
                 pos: Tuple[int, int]) -> None:
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=pos)
        self.screen.blit(surface, rect)

    def draw_square(self, color_name: str, pos: Tuple[int, int]) -> None:
        size = int(self.config.square_size * self.SCALE_FACTOR)
        square = pygame.Surface((size, size))
        square.fill(self.localization.colors[color_name])
        rect = square.get_rect(center=pos)
        self.screen.blit(square, rect)

    def reset_game(self) -> None:
        self.stroop_data = self.create_stroop_data()
        self.start_trial()

    def start_trial(self) -> None:
        if self.stroop_data["trials_left"] > 0:
            self.stroop_data["trials_left"] -= 1
            color_names = list(self.localization.colors.keys())
            
            if self.stroop_data["part"] == 1:
                color_key = random.choice(color_names)
                self.stroop_data["word"] = self.localization.get_color_name(color_key)
                self.stroop_data["color"] = random.choice(color_names)
                self.stroop_data["correct_color"] = color_key
                self.stroop_data["position"] = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2)
            elif self.stroop_data["part"] == 2:
                self.stroop_data["word"] = ""
                self.stroop_data["color"] = random.choice(color_names)
                self.stroop_data["correct_color"] = self.stroop_data["color"]
                self.stroop_data["position"] = (
                    self.SCREEN_WIDTH * (0.3 + random.random() * 0.4),
                    self.SCREEN_HEIGHT * (0.3 + random.random() * 0.4)
                )
            elif self.stroop_data["part"] == 3:
                color_key = random.choice(color_names)
                self.stroop_data["word"] = self.localization.get_color_name(color_key)
                self.stroop_data["color"] = random.choice(color_names)
                self.stroop_data["correct_color"] = self.stroop_data["color"]
                self.stroop_data["position"] = (
                    self.SCREEN_WIDTH * (0.3 + random.random() * 0.4),
                    self.SCREEN_HEIGHT * (0.3 + random.random() * 0.4)
                )
            
            self.stroop_data["start_time"] = pygame.time.get_ticks()
            self.update_color_buttons()
        else:
            self.stroop_data["part"] += 1
            if self.stroop_data["part"] <= 3:
                self.stroop_data["trials_left"] = self.config.trial_count
                self.start_trial()
            else:
                self.set_state("results")

    def update_color_buttons(self) -> None:
        button_width = int(self.config.button_width * self.SCALE_FACTOR)
        button_height = int(self.config.button_height * self.SCALE_FACTOR)
        total_buttons = len(self.localization.colors)
        total_width = total_buttons * button_width + (total_buttons - 1) * self.config.button_spacing
        start_x = (self.SCREEN_WIDTH - total_width) / 2
        
        color_names = list(self.localization.colors.keys())
        random.shuffle(color_names)
        
        self.buttons["color"] = [
            Button(name, 
                  pygame.Rect(start_x + i * (button_width + self.config.button_spacing),
                            self.SCREEN_HEIGHT * 0.75, button_width, button_height),
                  lambda c=name: self.check_color(c),
                  self.localization.colors[name])
            for i, name in enumerate(color_names)
        ]

    def check_color(self, color: str) -> None:
        if self.state == "game":
            if color == self.stroop_data["correct_color"]:
                reaction_time = (pygame.time.get_ticks() - self.stroop_data["start_time"]) / 1000.0
                self.stroop_data["reaction_times"].append(reaction_time)
                self.stroop_data["score"] += 10
                self.stroop_data["total_time"] += reaction_time
                self.stroop_data["correct_clicks"] += 1
                self.stroop_data["feedback"] = self.localization.get_text("correct")
            else:
                self.stroop_data["score"] -= 5
                self.stroop_data["incorrect_clicks"] += 1
                self.stroop_data["feedback"] = self.localization.get_text("incorrect")
            
            self.stroop_data["feedback_time"] = pygame.time.get_ticks()
            self.update_color_buttons()
            self.start_trial()

    def change_language(self, lang: str) -> None:
        self.localization.set_language(lang)
        self.config.language = lang
        self.config.save()
        self.set_state("settings")

    def change_resolution(self, width: int, height: int) -> None:
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = width, height
        self.SCALE_FACTOR = min(self.SCREEN_WIDTH / 1920, self.SCREEN_HEIGHT / 1080)
        self.config.screen_width, self.config.screen_height = width, height
        
        try:
            if self.config.display_mode == "fullscreen":
                flags = pygame.FULLSCREEN
            elif self.config.display_mode == "noframe":
                flags = pygame.NOFRAME
            else:
                flags = 0
            
            self.screen = pygame.display.set_mode((width, height), flags)
            self.font = pygame.font.Font(None, int(self.config.font_size * self.SCALE_FACTOR))
            self.small_font = pygame.font.Font(None, int(self.config.small_font_size * self.SCALE_FACTOR))
            self.buttons = self.create_buttons()
        except pygame.error:
            self.screen = pygame.display.set_mode((1280, 720), 0)
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1280, 720
            self.config.screen_width, self.config.screen_height = 1280, 720
            self.config.display_mode = "windowed"
        
        self.config.save()
        self.set_state("settings")

    def change_display_mode(self, mode: str) -> None:
        self.config.display_mode = mode
        self.config.save()
        self.change_resolution(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

def main():
    game = StroopTest()
    if platform.system() == "Emscripten":
        asyncio.ensure_future(game.run())
    else:
        asyncio.run(game.run())

if __name__ == "__main__":
    main()