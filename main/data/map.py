"""Map module"""
from pathlib import Path

import pytmx
import pygame

from config.config import Settings
from data.paths import Paths, MapAssets
from data.utils import scale_up_double, draw_hit_box, load_img


class Renderer(object):
    """This object renders tile maps from Tiled"""

    def __init__(self, filename):
        tmx_file = pytmx.load_pygame(filename, pixelalpha=True)
        self.size = (
            tmx_file.width * tmx_file.tilewidth,
            tmx_file.height * tmx_file.tileheight,
        )
        self.tmx_data = tmx_file
        self.tw = self.tmx_data.tilewidth  # 16px
        self.th = self.tmx_data.tileheight  # 16px
        self.tw_d = self.tmx_data.tilewidth * 2  # 32px
        self.th_d = self.tmx_data.tileheight * 2  # 32px
        self.lst_tiles = []
        self.lst_obstacles = []
        self.lst_player_starting_pos = []
        self.dict_events = {}
        self.dict_clickable_objects = {}
        self.lst_elias_escape_events = []

    def _handle_dialogue_objects(self, tile_object, x, y, w, h):
        """Handles map objects that contain dialogue."""
        dict_speakers_with_texts = {}
        dict_speakers = {}
        # TODO make MapObject first
        narration = None
        triggered_by = None
        remove_npc = False
        hide_p1 = False
        hide_p2 = False
        active = True
        # Puts the speakers in a dict
        for key, value in tile_object.properties.items():
            if "speaker" in key:
                dict_speakers[key] = value
            if "narration" in key:
                narration = value
            if key == "triggered_by":
                triggered_by = value
            if key == "remove_npc":
                remove_npc = bool(value)
            if key == "hide_p1":
                hide_p1 = value
            if key == "hide_p2":
                hide_p2 = value
            if key == "active":
                active = value

        # Puts all texts in a dict while assigning the corresponding speakers
        # So the dict looks like this if speaker1 is "elias" and speaker2 is "dad":
        # {"elias": [text1,text2...], "dad": [text1, text2,...]}
        for v in dict_speakers.values():
            dict_speakers_with_texts[v] = [
                value for key, value in tile_object.properties.items() if v in key
            ]
        dict_speakers_with_texts["narration"] = narration
        self.dict_events[tile_object.name] = MapObject(
            x,
            y,
            w,
            h,
            dict_speakers_with_texts,
            dict_speakers,
            triggered_by,
            remove_npc,
            hide_p1,
            hide_p2,
            active,
        )

    def _handle_clickable_map(self, surface, layer):
        for tile_object in layer:
            image = tile_object.image
            is_correct = False
            if image is not None:
                image = pygame.transform.scale(
                    image, (int(tile_object.width), int(tile_object.height))
                )
                surface.blit(image, (tile_object.x, tile_object.y))
            if tile_object.name != "background" and tile_object.type == "clickable":
                try:
                    name = tile_object.properties["name_for_list"]
                except KeyError:
                    name = None
                try:
                    content = tile_object.properties["content"]
                    if "Schutzstaffel" in content:
                        img_uniform = load_img(MapAssets.SS_UNIFORM)
                        # TODO make this property of tile
                        is_correct = True
                    elif "Schutzabteilung" in content:
                        img_uniform = load_img(MapAssets.SA_UNIFORM)
                    elif "Reichswehr" in content:
                        img_uniform = load_img(MapAssets.ARMED_FORCES_UNIFORM)
                    else:
                        img_uniform = None
                    if img_uniform is not None:
                        img_uniform = pygame.transform.scale(img_uniform, (200, 400))
                except KeyError:
                    content = None
                    img_uniform = None
                    # TODO refactor maybe
                if image is not None:
                    rect = image.get_rect(x=tile_object.x, y=tile_object.y)
                else:
                    rect = pygame.Rect(
                        tile_object.x,
                        tile_object.y,
                        tile_object.width,
                        tile_object.height,
                    )
                # Makes rect a little smaller
                rect = rect.inflate(-10, -10)
                self.dict_clickable_objects[tile_object.name] = ClickableObject(
                    name, content, img_uniform, is_correct, rect
                )
                if Settings.DRAW_HIT_BOXES:
                    draw_hit_box(surface, rect)

    def render(self, surface, update_objects: bool, make_soldiers=False):
        """Renders the map and collects all objects in corresponding lists."""

        if self.tmx_data.background_color:
            surface.fill(self.tmx_data.background_color)

        for layer in self.tmx_data.visible_layers:
            # Iterates through every layer and blit all tiles that the layer contains
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tw, y * self.th))

            elif isinstance(layer, pytmx.TiledObjectGroup):
                if update_objects:
                    if "carpentry" in self.tmx_data.filename.as_posix():
                        self._handle_clickable_map(surface, layer)
                    elif "attic" in self.tmx_data.filename.as_posix():
                        self._handle_clickable_map(surface, layer)
                    elif layer.name == "standard_objects":
                        for tile_object in layer:
                            # Since the map is scaled x2, the position, width and height of the tile objects need the same treatment
                            x = tile_object.x * 2
                            y = tile_object.y * 2
                            w = tile_object.width * 2
                            h = tile_object.height * 2
                            if tile_object.name is None:
                                # "Empty" rectangles Objects without name are always obstacles ("empty" rectangles on the map,
                                # meaning they have no
                                # additional properties and no name)
                                self.lst_obstacles.append(MapObject(x, y, w, h))
                            elif "player" in tile_object.name:
                                self.lst_player_starting_pos.append(tile_object)
                            elif "event" in tile_object.name:
                                self._handle_dialogue_objects(tile_object, x, y, w, h)
                if make_soldiers:
                    # Makes objects appear that prevent Elias from proceeding
                    if layer.name == "elias_escape_events":
                        # todo duplicate
                        for tile_object in layer:
                            x = tile_object.x * 2
                            y = tile_object.y * 2
                            w = tile_object.width * 2
                            h = tile_object.height * 2
                            self.lst_elias_escape_events.append(MapObject(x, y, w, h))

    def make_map(self, update_objects=False, double_scale=True, make_soldiers=False):
        temp_surface = pygame.Surface(self.size)
        self.render(temp_surface, update_objects, make_soldiers=make_soldiers)
        if double_scale:
            temp_surface = scale_up_double(temp_surface)
        return temp_surface


class Map:
    def __init__(self, tmx_file: Path, screen: pygame.Surface, double_scale=True):
        self.tmx_file = pytmx.load_pygame(tmx_file)
        # Actual screen
        self.screen = screen
        self.tile_renderer = Renderer(tmx_file)
        self.map_surface = self.tile_renderer.make_map(True, double_scale)
        self.map_rect = self.map_surface.get_rect()
        self.objects = self.tile_renderer.tmx_data.objects

    def draw(self):
        self.screen.blit(self.map_surface, self.map_rect)

    def _make_layer_invisible(self, event=None, layer_name=None):
        for layer in self.tile_renderer.tmx_data.layers:
            if event is not None and event.remove_npc:
                # TODO hack
                if layer.name == "Kreuzer":
                    layer.visible = False
            elif layer_name is not None:
                if layer.name == layer_name:
                    layer.visible = False

    def _make_layer_visible(self, name_layer: str = None):
        for layer in self.tile_renderer.tmx_data.layers:
            if name_layer is not None and name_layer == layer.name:
                layer.visible = True
            elif name_layer is None:
                if not layer.visible:
                    layer.visible = True

    def update(
        self,
        event=None,
        delete=True,
        draw=True,
        update_objects=False,
        make_soldiers=False,
        layer: str or tuple = None,
    ):
        """Used to update map"""
        # TODO refactor this
        if delete:
            self._make_layer_invisible(event, layer)
        else:
            if layer is not None:
                if isinstance(layer, str):
                    self._make_layer_visible(layer)
                elif isinstance(layer, tuple):
                    for lyr in layer:
                        self._make_layer_visible(lyr)
        self.map_surface = self.tile_renderer.make_map(
            update_objects=update_objects, make_soldiers=make_soldiers
        )
        if draw:
            self.draw()

    def delete_object(self, thing):
        for layer in self.tile_renderer.tmx_data.layers:
            if thing in layer.name:
                layer.visible = False

    def update_carpentry(self, thing):
        # TODO refactor, this is only used for the carpentry game
        self.delete_object(thing)
        self.map_surface = self.tile_renderer.make_map(
            update_objects=True, double_scale=False
        )
        self.draw()


class MapObject(pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        w,
        h,
        dict_texts=None,
        dict_speakers=None,
        triggered_by=None,
        remove_npc=False,
        hide_p1=False,
        hide_p2=False,
        active=True,
    ):
        super().__init__()
        self.remove_npc = remove_npc
        self.triggered_by = triggered_by
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.dict_texts = dict_texts
        self.dict_speakers = dict_speakers
        self.hide_p2 = hide_p2
        self.hide_p1 = hide_p1
        self.active = active


class ClickableObject:
    def __init__(self, name, content, img_uniform, is_correct, rect):
        self.name = name
        self.content = content
        self.is_correct = is_correct
        self.img_uniform = img_uniform
        self.rect = rect
