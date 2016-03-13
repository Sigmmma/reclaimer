import os
from traceback import format_exc

from supyr_struct.editor.editor_window import TagEditorWindow

try:
    if __name__ == "__main__":
        main_window = TagEditorWindow(curr_dir = os.path.abspath(os.curdir))
        main_window.mainloop()

except Exception:
    print(format_exc())
    input()
