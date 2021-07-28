from .admin import IsAdmin
from .text_button import TextButton


def setup(dp):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(TextButton)