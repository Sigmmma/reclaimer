from supyr_struct.apps.binilla.tag_window import *
from supyr_struct.defs.constants import *

def sanitize_path(path):
    return path.replace('\\', '/').replace('/', PATHDIV)

class HaloTagWindow(TagWindow):

    def __init__(self, master, tag=None, *args, **kwargs):
        try:
            tag.tags_dir = master.tags_dir.lower()
            if not tag.tags_dir.endswith(PATHDIV):
                tag.tags_dir += PATHDIV
            tag.rel_filepath = sanitize_path(tag.filepath).lower()
            tag.rel_filepath = tag.rel_filepath.split(tag.tags_dir)[-1]
        except Exception:
            print(format_exc())

        TagWindow.__init__(self, master, tag, *args, **kwargs)
