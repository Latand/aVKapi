import json
import typing
from dataclasses import dataclass
from . import base
from . import fields
from .base import VKObject
from ..utils.helper import Item, HelperMode


class Colours:
    mode = HelperMode.lowercase
    PRIMARY = Item()
    DEFAULT = Item()
    NEGATIVE = Item()
    POSITIVE = Item()

    BLUE = PRIMARY
    WHITE = DEFAULT
    RED = NEGATIVE
    GREEN = POSITIVE


class Keyboard(VKObject):
    buttons: 'typing.List[typing.List[KeyboardButton]]' = fields.ListOfLists(base='KeyboardButton', default=[])
    one_time: base.Boolean

    def __init__(self, buttons: 'typing.List[typing.List[KeyboardButton]]' = None,
                 one_time: base.Boolean = False,
                 row_width: base.Integer = 3):
        super(Keyboard, self).__init__(one_time=one_time,
                                       buttons=buttons,
                                       conf={'row_width': row_width})

    @property
    def row_width(self):
        return self.conf.get('row_width', 3)

    @row_width.setter
    def row_width(self, value):
        self.conf['row_width'] = value

    def add(self, *args):
        """
        Add buttons

        :param args:
        :return: self
        :rtype: :obj:`types.Keyboard`
        """
        row = []
        for index, button in enumerate(args, start=1):
            row.append(button)
            if index % self.row_width == 0:
                self.buttons.append(row)
                row = []
        if len(row) > 0:
            self.buttons.append(row)
        return self

    def row(self, *args):
        """
        Add row

        :param args:
        :return: self
        :rtype: :obj:`types.Keyboard`
        """
        btn_array = []
        for button in args:
            btn_array.append(button)
        self.buttons.append(btn_array)
        return self

    def insert(self, button):
        """
        Insert button to last row

        :param button:
        :return: self
        :rtype: :obj:`types.Keyboard`
        """
        if self.buttons and len(self.buttons[-1]) < self.row_width:
            self.buttons[-1].append(button)
        else:
            self.add(button)
        return self


class KeyboardButton(VKObject):
    action: typing.Dict
    color: base.String = fields.Field()

    def __init__(self, label: base.String,
                 payload: base.String,
                 color: base.String = Colours.DEFAULT):
        self.label = label
        self.color = color
        self.payload = payload
        self.action = {"type": "text", "label": self.label, "payload": json.dumps({"button": self.payload})}
        super(KeyboardButton, self).__init__(action=self.action,
                                             color=self.color)


class EmptyKeyboard(Keyboard):
    def __init__(self):
        super().__init__(buttons=[])


@dataclass
class ListOfButtons:
    buttons: typing.List
    payloads: typing.List
    row_sizes: typing.List[int]
    colours: typing.List = None
    """
    Использование:
    ListOfButtons(buttons=["Кнопка Белая", "Кнопка Синяя", "Кнопка Красная", "Кнопка Зеленая"],
                  colours=[Colours.WHITE, Colours.BLUE, Colours.RED, Colours.GREEN],
                  row_sizes=[1, 2, 1],
                  payloads=["payload1", "payload2", "payload3", "payload4"]).keyboard
    row_sizes - количество кнопок в ряде
    """

    @property
    def keyboard(self):
        return generate_keyboard(self)


def generate_keyboard(args: ListOfButtons):
    if len(args.row_sizes) > 10:
        raise IndexError("Максимум 10 линий кнопок")
    if max(args.row_sizes) > 4:
        raise IndexError("Максимум 4 кнопки на линию")
    keyboard = Keyboard()
    if not (len(args.buttons) == len(args.payloads) == len(args.colours)):
        raise IndexError("Все списки должны быть одной длины!")

    if not args.row_sizes:
        for num, button in enumerate(args.buttons):
            keyboard.add(KeyboardButton(label=str(button),
                                        payload=str(args.payloads[num]),
                                        color=args.colours[num]))
    else:
        count = 0
        for row_size in args.row_sizes:
            keyboard.row(*[KeyboardButton(label=str(label), payload=str(payload), color=color)
                           for label, payload, color in
                           tuple(zip(args.buttons, args.payloads, args.colours))[count:count + row_size]])
            count += row_size
    return keyboard
