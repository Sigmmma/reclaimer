from supyr_struct.apps.binilla.widget_picker import *
from supyr_struct.apps.binilla.field_widgets import *
from ..field_types import *

__all__ = ("WidgetPicker", "def_widget_picker", "add_widget",
           "GdlWidgetPicker", "def_gdl_widget_picker")

class GdlWidgetPicker(WidgetPicker):
    pass

def_gdl_widget_picker = dgdlwp = GdlWidgetPicker()

dgdlwp.copy_widget(Lump, Array)
