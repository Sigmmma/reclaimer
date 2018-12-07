

class RawdataManager:
    # tags with zone references:
    # bitm, jmad, mode, pmdf, sLdT, sbsp, snd!
    _parent_halo_map = None

    _zone_meta = None
    _play_meta = None

    _map_index_to_name = ()

    def __init__(self, parent_halo_map):
        self._parent_halo_map = parent_halo_map
        self._map_index_to_name = {}
        if parent_halo_map:
            self.zone_meta = parent_halo_map.root_tags.get(
                "cache_file_resource_gestalt")
            self.play_meta = parent_halo_map.root_tags.get(
                "cache_file_resource_layout_table")

    def add_halo_map_name_by_index(self, map_name, map_index):
        assert isinstance(map_name, str)
        assert isinstance(map_index, int)
        self._map_index_to_name[map_index] = map_name

    def get_halo_map(self, map_index):
        if self._parent_halo_map:
            return self.parent_halo_map.maps.get(
                self._map_index_to_name.get(map_index))

    def get_tag_resource_data(self, tag_rsrc_index, decompress=True):
        tag_rsrc_info = self.get_tag_resource(tag_rsrc_index)
        if not tag_rsrc_info:
            return ()

        segment_info = self.get_segment_info(tag_rsrc_info.segment_index)

    def get_tag_resource_fixup(self, tag_rsrc_index):
        tag_rsrc_info = self.get_tag_resource(tag_rsrc_index)
        if not tag_rsrc_info:
            return ()

        fixup_chunk = self.zone_meta.fixup_information.data[
            tag_rsrc_info.fixup_info_offset:
            tag_rsrc_info.fixup_info_offset +  tag_rsrc_info.fixup_info_size
            ]

        return (fixup_chunk, tag_rsrc_info.resource_fixups_array.STEPTREE,
                tag_rsrc_info.resource_definition_fixups_array.STEPTREE)

    def get_segment_info(self, segment_index):
        if self._play_meta and isinstance(page_index, int):
            raw_sizes = self._play_meta.raw_sizes.STEPTREE
            segments = self._play_meta.segments_array.STEPTREE
            if segment_index in range(len(segments)):
                segment = segments[segment_index]
                page_infos = []
                for i in range(len(segment.page_indices)):
                    page_info = [-1, 0, []]
                    page_infos.append(page_info)

                    raw_page_index = segment.page_indices[i]
                    raw_page = self.get_raw_page(raw_page_index)
                    if not raw_page:
                        continue

                    seg_sizes = []
                    page_info[:] = (
                        raw_page_index,
                        segment.page_indices[i],
                        seg_sizes
                        )
                    size_index = segment.raw_size_indices[i]
                    if size_index == -1:
                        seg_sizes.append((0, raw_page.uncompressed_block_size))
                    else:
                        for chunk in seg_sizes[size_index].chunks.STEPTREE:
                            seg_sizes.append((chunk[0], chunk[1]))

                return page_infos

        return ()

    def get_raw_page(self, page_index):
        if self._play_meta and isinstance(page_index, int):
            raw_pages = self._play_meta.raw_pages_array.STEPTREE
            if page_index in len(range(raw_pages)):
                return raw_pages[page_index]

    def get_tag_resource(self, tag_rsrc_index):
        if self._zone_meta and isinstance(tag_rsrc_index, int):
            tag_resources = self._zone_meta.tag_resources_array.STEPTREE
            if tag_rsrc_index in len(range(tag_resources)):
                return tag_resources[tag_rsrc_index]
