
class TagIndexManager:
    _tag_index = ()
    _tag_index_map = ()

    def __init__(self, tag_index, tag_index_map=None):
        self._tag_index = tag_index
        if tag_index_map:
            self._tag_index_map = dict(tag_index_map)
        else:
            self._tag_index_map = {}
            for i in range(len(tag_index)):
                self._tag_index_map[tag_index[i].id & 0xFFff] = i

        # 0xFFff is reserved to mean NULL, so don't map it
        self._tag_index_map.pop(0xFFff, None)

    def translate_tag_id(self, tag_id):
        tag_id &= 0xFFff
        if tag_id in self._tag_index_map:
            return self._tag_index_map[tag_id]
        return tag_id

    def get_tag_index_ref(self, tag_id):
        tag_id = self.translate_tag_id(tag_id)
        if tag_id in range(len(self._tag_index)):
            return self._tag_index[tag_id]
