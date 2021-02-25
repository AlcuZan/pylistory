from typing import Optional

import pygame
import thorpy
from pygame_menu import Menu

import data.public as public
import data.utils
from data import utils
from data.dialogue import DialogueHandler
from data.quiz import Quiz
from data.textbox import TextBox, UniformDescriptionBox, BoxWithPortrait, ItemListBox
from data.texts import NarrationTexts, Dialogues, TextForTextBox
from data.utils import Window, GameStates, load_img, set_music
from data.paths import MapAssets, Sound, Backgrounds
from data.player import Player, Keys
from config.config import Settings, Resolutions, TextBoxSettings, Misc, Colors
from data.map import Map


class Game:
    """Base class for game."""

    pass


class Game1933(Game):
    """Class for the game TODO this is only scenario 1933"""

    def __init__(
        self,
        window: Window,
        menu: Optional[Menu] = None,
    ):
        self.window = window
        self.menu = menu
        self._state = GameStates.PAUSED
        self.playing = False
        self.start_map = None
        self.con_camp_map = None
        self.way_to_con_camp_map = None
        self.carpentry = None
        self.attic = None
        self.text_box = None
        self.p1 = None
        self.show_p1 = True
        self.p2 = None
        self.show_p2 = False
        self.dialogue_handler = None
        # Show players after dialogue, putting their position at the bottom of the event rect
        self.show_players_after_event = False
        self.veggie_store_bg = load_img(Backgrounds.VEGGIE_STORE_BG)
        self.dad_house_bg = load_img(Backgrounds.ELIAS_DAD_HOUSE)
        self.attic_bg = load_img(Backgrounds.ATTIC_BG)
        self.document = load_img(Backgrounds.REICH_LAW_GAZETTE)
        self.document_readable_1 = load_img(Backgrounds.REICH_LAW_GAZETTE_READABLE_1)
        self.document_readable_2 = load_img(Backgrounds.REICH_LAW_GAZETTE_READABLE_2)
        self.show_document = False
        self.map_to_draw = None
        self.event = None
        self.start_attic_event = False
        self.start_kreuzer_quiz = False

    def start_scenario(self):
        """
        Executes scenario. First, creates the instances of the map and players, sets the clock
        then starts the main game loop. In the game loop the order of these steps is very important:
        1. Draw the map. If this isn't done first, there will be visual disturbances like the player figures creating
        streaks behind them.
        2. Get user input. This must be done before updating and drawing the player images because otherwise they won't behave
        like intended.
        3. Update the players, that means animating the player figure and handling movement including collision detection
        (with map objects)
        4. Update the screen, which is a necessary step that needs to be done at the end of every game loop

        """
        self.start_map = Map(MapAssets.MAP_START, self.window.screen)
        self.carpentry = Map(
            MapAssets.CARPENTRY, self.window.screen, double_scale=False
        )
        self.attic = Map(MapAssets.ATTIC, self.window.screen, double_scale=False)
        public.clock.tick(Settings.FPS)  # Sets frame rate
        if Settings.TEST:
            self._state = GameStates.QUIZ
        else:
            self.map_to_draw = self.start_map
            self.dialogue_handler = DialogueHandler(
                self.window, self.start_map, self.start_map.tile_renderer.dict_events
            )
            self._create_players()
            # Play intro, then start game
            self.dialogue_handler.play_narrator_text(
                [NarrationTexts.INTRO_TEXT_ELIAS, NarrationTexts.INTRO_TEXT_KLAUS],
                Backgrounds.INTRO_BACKGROUND,
            )
            self._state = GameStates.PLAYING

        if not Settings.MUTE:
            set_music(Sound.GAME_START_MUSIC)

        while not self._state.quit:
            self._play_state()
            self._dialogue_state()
            self._carpentry_state()
            self._attic_state()
            self._quiz_state()
            self._ending_state()

    def handle_map_events(self):
        # TODO hackfix
        try:
            if self.p2.rect.colliderect(
                self.dialogue_handler.dict_events["event_klaus_gets_things"]
            ):
                self.p1.can_move = True
                self.p2.reset()
                self.p2.can_move = False
                # TODO Klaus should say this
                self.dialogue_handler.play_narrator_text(
                    NarrationTexts.KLAUS_WAITS_IN_FRONT_OF_CARPENTRY
                )
        except KeyError:
            pass
        for event_name, event in self.dialogue_handler.dict_events.items():
            if event.active:
                if self.p1.rect.colliderect(event) and self.show_p1:
                    self.event = event
                    if event.hide_p1 and event.active:
                        self.show_p1 = False
                        self.map_to_draw.draw()
                    # Elias walks into veggie store and disappears, then Klaus narration starts
                    if "veggie_store" in event_name:
                        self.map_to_draw.update(layer="Kreuzer", delete=False)
                        self.show_p2 = True
                        self.dialogue_handler.play_narrator_text(
                            NarrationTexts.KLAUS_MEETS_KREUZER
                        )
                        self.map_to_draw.draw()
                    if event_name == "event_klaus_shows_document":
                        self.show_document = True
                    # Elias walks into the hiding place so Klaus can get things
                    if event_name == "event_elias_hides" and event.active:
                        self.dialogue_handler.play_narrator_text(
                            NarrationTexts.ELIAS_HIDES
                        )
                        self.dialogue_handler.dict_events[
                            "event_klaus_gets_things"
                        ].active = True
                        self.show_p2 = True
                        self.p2.can_move = True
                    if event_name == "event_elias_and_klaus_talk_to_kreuzer":
                        self.p1.can_move = False
                    if event_name == "event_game_over":
                        if self.p2.can_move:
                            self.p1.can_move = False
                            self._state = GameStates.PLAYING
                        else:
                            self.p1.can_move = False
                            self.dialogue_handler.play_narrator_text(
                                NarrationTexts.ENDING_EVENT
                            )
                            self._state = GameStates.TO_BE_CONTINUED
                    elif (
                        "player1" in event.triggered_by
                        and not event_name == "event_elias_hides"
                        and not event_name == "event_game_over"
                    ):
                        self._state = GameStates.DIALOGUE
                        # Player 1 steps on an object that has text he can trigger
                        self.pass_args_to_dialogue_handler(event_name, event)
                        # After this, dialogue_state will be executed

                if self.p2.rect.colliderect(event) and self.show_p2:
                    self.event = event
                    if "player" in event.triggered_by and event.active:
                        self._state = GameStates.DIALOGUE
                        if event.hide_p2 and event.active and not self.show_p1:
                            self.show_p2 = False
                            self.map_to_draw.draw()
                        # Klaus walks into veggie store so the veggie store event starts
                        if "veggie_store" in event_name:
                            self.dialogue_handler.dict_events[
                                "event_elias_and_klaus_talk_to_dad"
                            ].active = True
                            self.dialogue_handler.dict_events[
                                "event_klaus_shows_document"
                            ].active = True
                            self.load_veggie_store()
                            self.show_players_after_event = True
                        # Elias and Klaus talk to Dad after veggie store
                        if event_name == "event_elias_and_klaus_talk_to_dad":
                            # TODO shouldnt be necessary but without it the 2 dont disappear at this event
                            self.show_p2 = False
                            self.show_p1 = False
                            self.dialogue_handler.play_narrator_text(
                                NarrationTexts.ELIAS_AND_KLAUS_GO_TO_DAD
                            )
                            self.load_dad_house()
                            # Make soldiers appear
                            self.map_to_draw.update(
                                delete=False,
                                draw=False,
                                update_objects=False,
                                make_soldiers=True,
                                layer=("elias_escape_events", "Soldiers"),
                            )
                            self.show_players_after_event = True
                            if not self.show_p1:
                                self.dialogue_handler.dict_events[
                                    "event_elias_and_klaus_talk_after_dad"
                                ].active = True
                            self.dialogue_handler.dict_events[
                                "event_elias_hides"
                            ].active = True
                            self.p1.can_move = False
                        if event_name == "event_klaus_gets_things":
                            self.dialogue_handler.play_narrator_text(
                                NarrationTexts.KLAUS_ENTERS_CARPENTRY
                            )
                            self._state = GameStates.CARPENTRY

                        if event_name == "event_klaus_shows_document":
                            self.show_document = True

                        if event_name == "event_elias_hides":
                            self.load_attic()  # then dialogue, then state change to attic
                            self.start_attic_event = True
                            self.map_to_draw.update(
                                layer="Kreuzer_new", draw=False, delete=False
                            )
                            self.dialogue_handler.dict_events[
                                "event_elias_and_klaus_talk_to_kreuzer"
                            ].active = True
                        if event_name == "event_elias_and_klaus_talk_to_kreuzer":
                            self.start_kreuzer_quiz = True
                            self.p1.can_move = True
                        if event_name == "event_game_over":
                            if self.p1.can_move:
                                self.p2.can_move = False
                                self._state = GameStates.PLAYING
                            else:
                                self.p2.can_move = False
                                self.dialogue_handler.play_narrator_text(
                                    NarrationTexts.ENDING_EVENT
                                )
                                self._state = GameStates.TO_BE_CONTINUED

                        # Player 2 steps on an object that has text he can trigger, dialogue is only triggered when the event is
                        # active though
                        if event.active and not event_name == "event_game_over":
                            self.pass_args_to_dialogue_handler(event_name, event)

    def _carpentry_state(self):
        objects = None
        if self._state.carpentry:
            self.map_to_draw = self.carpentry
            self.window.set_screen(Resolutions.CARPENTRY)
            objects = self.map_to_draw.tile_renderer.dict_clickable_objects
        while self._state.carpentry:
            # TODO put all of that elsewhere
            if not objects:
                # All objects have been clicked so play narration text, show p2 again and allow him to move,
                # switch the state and delete the event that enables p2 to enter the carpentry
                self.dialogue_handler.play_narrator_text(
                    NarrationTexts.KLAUS_LEAVES_CARPENTRY
                )
                self.show_p2 = True
                self.p2.can_move = True
                # Player appears at the midbottom of the event rect
                self.p2.rect.midbottom = self.event.rect.midbottom
                self._state = GameStates.PLAYING
                del self.dialogue_handler.dict_events[self.event.name]
            else:
                self.map_to_draw.draw()
                self.text_box = ItemListBox(window=self.window)
                lst_names = [obj.name for obj in objects.values()]
                self.text_box.make_textbox(lst_names)
                collision = False
                thing = None
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for (
                    key,
                    clickable,
                ) in self.map_to_draw.tile_renderer.dict_clickable_objects.items():
                    if clickable.rect.collidepoint(mouse_x, mouse_y):
                        collision = True
                        thing = key

                if utils.mouse_clicked():
                    # User clicked on an image so it disappears
                    if collision:
                        if thing is not None:
                            del self.map_to_draw.tile_renderer.dict_clickable_objects[
                                thing
                            ]
                            self.map_to_draw.update_carpentry(thing)
                pygame.display.update()

    def _attic_state(self):
        # TODO should probably be a class
        if self._state.attic:
            self.map_to_draw = self.attic
            self.text_box = UniformDescriptionBox(self.window)

        while self._state.attic:
            collision = False
            clicked_obj = None
            chosen_correct = False
            chosen_incorrect = False
            self.map_to_draw.draw()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not chosen_correct:
                for (
                    key,
                    clickable,
                ) in self.map_to_draw.tile_renderer.dict_clickable_objects.items():
                    if clickable.rect.collidepoint(mouse_x, mouse_y):
                        clicked_obj = clickable
                        collision = True
                        # Textbox contains information about uniform
                        self.text_box.make_textbox(clickable.content)
                        # Show the uniform
                        # Todo put it elsewhere
                        self.window.screen.blit(
                            clickable.img_uniform,
                            clickable.img_uniform.get_rect(topleft=(0, 300)),
                        )

            if utils.mouse_clicked():
                if collision:
                    self.load_attic()
                    if clicked_obj.is_correct:
                        chosen_correct = True
                    else:
                        chosen_incorrect = True
            while chosen_correct:
                self._clothing_chosen_textbox(Dialogues.CLOTHING_CHOSEN_CORRECT)
                if utils.continue_text():
                    chosen_correct = False
                    self.show_p1 = True
                    self.show_p2 = True
                    self.start_attic_event = False
                    self._state = GameStates.PLAYING
            while chosen_incorrect:
                self._clothing_chosen_textbox(Dialogues.CLOTHING_CHOSEN_INCORRECT)
                if utils.continue_text():
                    chosen_incorrect = False
            pygame.display.update()

    def _clothing_chosen_textbox(self, text: TextForTextBox):
        self.text_box.text_offset_left = TextBoxSettings.DIALOGUE_TEXT_OFFSET_LEFT
        self.text_box.make_textbox(text)
        pygame.display.update()
        # Reset offset
        self.text_box.text_offset_left = 200

    def _ending_state(self):
        while self._state.to_be_continued:
            self.window.screen.fill(Colors.BLACK)
            self.text_box.make_textbox(NarrationTexts.ENDING)
            pygame.display.update()
            if utils.continue_text():
                self._state = GameStates.QUIT

    def _play_state(self):
        if self._state.playing:
            self.window.set_screen(Resolutions.DEFAULT)
            self.map_to_draw = self.start_map
            self.dialogue_handler.play_narrator_text(
                NarrationTexts.FEW_MONTHS_LATER, Backgrounds.INTRO_BACKGROUND
            )

        while self._state.playing:
            self.map_to_draw.draw()
            self.handle_map_events()
            self._handle_input()
            if self.p1 is not None and self.show_p1:
                self.p1.update(self.map_to_draw)
                self.p1.draw()
            if self.p2 is not None and self.show_p2:
                self.p2.update(self.map_to_draw)
                self.p2.draw()
            pygame.display.update()

    def _quiz_state(self):
        if self._state.quiz:
            self.quiz = Quiz(self.window, self.window.screen.get_rect().midtop)
        while self._state.quiz:
            for event in pygame.event.get():
                # Quiz reacts to events like clicking
                self.quiz.menu.react(event)
                if self.quiz.menu.leave:
                    if self.quiz.quiz_failed:
                        self._state = GameStates.TO_BE_CONTINUED
                    else:
                        self.start_kreuzer_quiz = False
                        self.map_to_draw.update(layer="Kreuzer_new")
                        self.dialogue_handler.dict_events[
                            "event_game_over"
                        ].active = True
                        self._state = GameStates.PLAYING
            pygame.display.update()

    def pass_args_to_dialogue_handler(self, event_name, event):
        """Passes current event to dialogue handler"""
        self.dialogue_handler.event = event
        self.dialogue_handler.event.name = event_name
        self.dialogue_handler.dict_texts = event.dict_texts
        self.dialogue_handler.dict_speakers = event.dict_speakers
        self.dialogue_handler.name_event = event_name
        self.dialogue_handler.narration = event.dict_texts["narration"]

    def _reset_players(self):
        # Reset players so they stand still during and after dialogue
        for p in (self.p1, self.p2):
            p.reset()

    def _show_document(self, img, pos=Misc.DOCUMENT_POS):
        while True:
            self.window.screen.blit(img, pos)
            pygame.display.update()
            if utils.continue_text():
                break

    def _dialogue_state(self):
        if self._state.dialogue:
            self._reset_players()
            self.dialogue_handler.state = GameStates.DIALOGUE
            self.dialogue_handler.play_dialogue()
            if self.dialogue_handler.is_done():
                if self.show_document:
                    self.document = pygame.transform.scale(
                        self.document,
                        (
                            int(self.document.get_size()[0] / 1.5),
                            int(self.document.get_size()[1] / 1.5),
                        ),
                    )
                    self.window.set_screen(self.document.get_size())
                    self._show_document(self.document, Misc.DEFAULT_POS)
                    self._show_document(self.document_readable_1)
                    self._show_document(self.document_readable_2)
                    self.show_document = False
                if self.start_attic_event:
                    self._state = GameStates.ATTIC
                elif self.start_kreuzer_quiz:
                    self._state = GameStates.QUIZ
                else:
                    if self.show_players_after_event:
                        self.p1.rect.midbottom = self.event.rect.midbottom
                        self.p2.rect.midbottom = self.event.rect.midbottom
                        self.show_p1 = True
                        self.show_p2 = True
                    self._state = GameStates.PLAYING

    def load_veggie_store(self):
        """Loads veggie store bg and blits it for veggie store scene."""

        def blit_store():
            self.window.screen.blit(self.veggie_store_bg, Misc.DEFAULT_POS)

        blit_store()
        self.dialogue_handler.play_narrator_text(NarrationTexts.ELIAS_WAITS_FOR_ORDER)
        blit_store()

    def load_attic(self):
        """Loads attic bg and blits it for attic scene."""
        self.window.screen.blit(self.attic_bg, Misc.DEFAULT_POS)

    def load_dad_house(self):
        self.dad_house_bg = pygame.transform.scale(
            self.dad_house_bg, self.window.screen.get_size()
        )
        self.window.screen.blit(self.dad_house_bg, Misc.DEFAULT_POS)

    def _handle_input(self):
        """Handles player input using pygame events."""
        for event in pygame.event.get():
            # User clicked close (the X button in the upper right corner of the window)
            if event.type == pygame.QUIT:
                data.utils.quit_game()
            # Key is pressed
            if event.type == pygame.KEYDOWN:
                # Player pressed Escape
                # TODO pause menu
                if event.key == pygame.K_ESCAPE:
                    if Settings.MENU_ENABLED:  # TODO only for testing, delete
                        self._return_to_menu()
                    else:
                        data.utils.quit_game()
                # h as debug key TODO delete
                elif event.key == pygame.K_h:
                    breakpoint()

            if self.p1 is not None and self.show_p1:
                self.p1.handle_movement_input(event)
            if self.p2 is not None and self.show_p2:
                self.p2.handle_movement_input(event)

    def _create_players(self):
        """Objects contain spawn points for players"""
        for tile_object in self.start_map.tile_renderer.lst_player_starting_pos:
            if tile_object.name == "player_1":
                self.p1 = Player(
                    public.p1_char,
                    self.window,
                    # For some reason, putting *2 into the Player init doesn't work
                    pos_x=tile_object.x * 2,
                    pos_y=tile_object.y * 2,
                    keys=Keys(1),
                )
            if tile_object.name == "player_2":
                self.p2 = Player(
                    public.p2_char,
                    self.window,
                    pos_x=tile_object.x * 2,
                    pos_y=tile_object.y * 2,
                    keys=Keys(2),
                )

    def _return_to_menu(self):
        if self.menu:
            self._state = GameStates.QUIT
            self.menu.reset(1)  # Back to main menu
            self.menu.enable()
