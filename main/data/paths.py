"""Module for paths"""
from enum import Enum
from pathlib import Path, WindowsPath
from typing import NamedTuple


class Paths:
    MUSIC = Path("./resources/sounds/music")
    IMAGES = Path("./resources/img")
    BACKGROUNDS = IMAGES / "backgrounds"
    PORTRAITS = IMAGES / "portraits"
    DEFAULT_FONT = Path("resources/fonts/opensans_regular.ttf")
    MAP_ASSETS = IMAGES / "maps"
    CLOTHING_EVENT = IMAGES / "clothing_event"


class Portraits(Enum):
    """Bools decide if the img is flipped and scaled up or not"""

    class Portrait(NamedTuple):
        path: WindowsPath
        modify: bool

    # TODO solve this some other way
    # Icon made by Freepik from www.flaticon.com
    # Source: https://www.flaticon.com/free-icon/jew_2230350
    ELIAS = Portrait(Paths.PORTRAITS / "elias_portrait.png", False)
    # Icon made by Freepik from www.flaticon.com
    # Source: https://www.flaticon.com/free-icon/soldier_773339
    KLAUS = Portrait(Paths.PORTRAITS / "klaus_portrait.png", False)
    # TODO source
    DAD = Portrait(Paths.PORTRAITS / "elias_dad.png", True)
    # Icon made by Wichai.wi from www.flaticon.com
    # Source: https://www.flaticon.com/free-icon/soldier_1909999
    KREUZER = Portrait(Paths.PORTRAITS / "kreuzer.png", False)


class MapAssets:
    # TODO refactor
    # Source: https://kenney.nl/assets/rpg-urban-pack
    SPRITE_SHEET = Paths.IMAGES / "maps/tilemap.png"
    # Created with Tiled out of SPRITE_SHEET file
    MAP_START = Paths.IMAGES / "maps/start.tmx"
    MAP_CONCENTRATION_CAMP = Paths.IMAGES / "maps/con_camp.tmx"
    MAP_WAY_TO_CONCENTRATION_CAMP = Paths.IMAGES / "maps/way_to_con_camp.tmx"
    # Created out of SPRITE_SHEET file using https://www.leshylabs.com/apps/sstool/
    SPRITE_SHEET_METADATA = Paths.IMAGES / "maps/sprites.json"
    CARPENTRY = Paths.MAP_ASSETS / "carpentry.tmx"
    ATTIC = Paths.MAP_ASSETS / "attic.tmx"
    SS_UNIFORM = Paths.CLOTHING_EVENT / "schutzstaffel_einzel.png"
    SA_UNIFORM = Paths.CLOTHING_EVENT / "sturmabteilung_einzel.png"
    ARMED_FORCES_UNIFORM = Paths.CLOTHING_EVENT / "wehrmacht_einzel.png"


class Sound:
    # Source: https://opengameart.org/content/menu-music
    MENU_MUSIC = Paths.MUSIC / "menu.wav"
    # Source: https://opengameart.org/content/vagabond
    GAME_START_MUSIC = Paths.MUSIC / "game_start.mp3"
    # Source: https://opengameart.org/content/dramatic-action
    VEGGIE_STORE_MUSIC = Paths.MUSIC / "veggiestore.mp3"


class Backgrounds:
    # Source: https://www.freepik.com/free-vector/old-nautical-map-template_7998456.htm#page=1&query=history&position=0
    # Map vector created by dgim-studio - www.freepik.com
    MENU_BACKGROUND = Paths.BACKGROUNDS / "menu_background.jpg"
    INTRO_BACKGROUND = Paths.BACKGROUNDS / "snow_bg.jpg"
    # Source: https://github.com/justinmeister/The-Stolen-Crown-RPG/tree/master/resources/graphics
    BACKGROUND_TEXTBOX = Paths.BACKGROUNDS / "dialoguebox.png"
    # Source: https://pixabay.com/de/photos/schwarz-wei%C3%9F-foto-supermarkt-gem%C3%BCse-2086277/
    VEGGIE_STORE_BG = Paths.BACKGROUNDS / "veggie_store.jpg"
    # Source: https://www.1000dokumente.de/dokumente/scan/jpg100/0006_erm_01.jpg
    REICH_LAW_GAZETTE = Paths.BACKGROUNDS / "verordnung.jpg"
    REICH_LAW_GAZETTE_READABLE_1 = Paths.BACKGROUNDS / "verordnung_lesbar_1.png"
    REICH_LAW_GAZETTE_READABLE_2 = Paths.BACKGROUNDS / "verordnung_lesbar_2.png"
    # Source: https://www.stift-ehreshoven.de/files/Bilder/Filmkulisse/Ehreshoven-Slider-Film-11.jpg
    ATTIC_BG = Paths.BACKGROUNDS / "dachboden.jpg"
    # Source: http://www.jacob-pins.de/files/loewenstein_haus_5._haus_r_568x350px.jpg
    ELIAS_DAD_HOUSE = Paths.BACKGROUNDS / "elias_dad_house.jpg"
    # Source: https://www.deutschlandfunk.de/media/thumbs/8/8ed00afab1bb47f6b96f131a9cfdadb6v2_max_460x345_b3535db83dc50e27c1bb1392364c95a2.jpg?key=b33798
    QUIZ_BG = Paths.BACKGROUNDS / "quiz_bg.jpg"
