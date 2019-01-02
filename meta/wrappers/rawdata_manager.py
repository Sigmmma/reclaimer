import zlib


def decompress_lzx_stream(stream, start, comp_size, uncomp_offset, uncomp_size):
    stream.seek(start)
    comp_data = stream.read(comp_size)
    return comp_data


def decompress_deflate_stream(stream, start, comp_size, uncomp_offset, uncomp_size):
    stream.seek(start)
    comp_data = stream.read(comp_size)
    decompressor = zlib.decompressobj(-15)
    uncomp_data = decompressor.decompress(comp_data, uncomp_offset + uncomp_size)
    return uncomp_data[uncomp_offset: ]


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
            self._zone_meta = parent_halo_map.get_root_tag(
                "cache_file_resource_gestalt")
            self._play_meta = parent_halo_map.get_root_tag(
                "cache_file_resource_layout_table")

    def add_shared_map_name(self, ext_cache_name, map_name):
        assert isinstance(map_name, str)
        if not self._play_meta:
            return

        ext_cache_refs = self._play_meta.external_cache_references.STEPTREE
        for i in range(len(ext_cache_refs)):
            curr_ext_cache_name = ext_cache_refs[i].map_path.lower().\
                                  replace("\\", "/").split("/")[-1].\
                                  split(".")[0]
            if curr_ext_cache_name == ext_cache_name:
                self._map_index_to_name[i] = map_name
                break

    def get_halo_map(self, map_index):
        if map_index < 0:
            return self._parent_halo_map
        elif self._parent_halo_map:
            return self._parent_halo_map.maps.get(
                self._map_index_to_name.get(map_index))

    def get_tag_resource_data(self, tag_rsrc_index, *chunk_sizes):
        tag_rsrc_datas = []
        tag_rsrc_info = self.get_tag_resource(tag_rsrc_index)
        if not tag_rsrc_info:
            return tag_rsrc_datas

        segment_info = self.get_segment_info(tag_rsrc_info.segment_index)
        chunk_sizes += (None, ) * (len(segment_info) - len(chunk_sizes))
        chunk_sizes = list(chunk_sizes)
        for raw_page_index, chunk_offset, seg_sizes in segment_info:
            raw_page_data = self.get_raw_page_data(raw_page_index, chunk_offset,
                                                   chunk_sizes.pop(0))
            if raw_page_data is None: continue

            # ignoring seg_sizes for now
            tag_rsrc_data = raw_page_data

            tag_rsrc_datas.append(tag_rsrc_data)

        return tag_rsrc_datas

    def get_raw_page_data(self, raw_page_index, chunk_offset=0, chunk_size=None):
        raw_page = self.get_raw_page(raw_page_index)
        if raw_page is None: return None

        halo_map = self.get_halo_map(raw_page.shared_cache_index)
        if halo_map is None: return None

        map_data = halo_map.map_data
        data_offset = halo_map.map_pointer_converter.v_ptr_to_f_ptr(
            raw_page.block_offset)
        comp_size = raw_page.compressed_block_size
        if chunk_size is None:
            chunk_size = raw_page.uncompressed_block_size

        if raw_page.compression_codec.enum_name == "NONE":
            map_data.seek(data_offset + chunk_offset)
            uncomp_data = map_data.read(chunk_size)
        elif raw_page.compression_codec.enum_name == "deflate":
            uncomp_data = decompress_deflate_stream(
                map_data, data_offset, comp_size, chunk_offset, chunk_size)
        elif raw_page.compression_codec.enum_name == "lzx":
            uncomp_data = decompress_lzx_stream(
                map_data, data_offset, comp_size, chunk_offset, chunk_size)
        else:
            raise ValueError("Unknown compression codec '%s'" %
                             raw_page.compression_codec.data)

        if len(uncomp_data) < chunk_size:
            # pad the data up to the requested size
            uncomp_data += b'\x00' * (chunk_size - len(uncomp_data))

        return uncomp_data

    def get_tag_resource_fixup(self, tag_rsrc_index):
        tag_rsrc_info = self.get_tag_resource(tag_rsrc_index)
        if not tag_rsrc_info:
            return (b'', (), ())

        fixup_chunk = self._zone_meta.fixup_info.data[
            tag_rsrc_info.fixup_info_offset:
            tag_rsrc_info.fixup_info_offset + tag_rsrc_info.fixup_info_size
            ]

        return (fixup_chunk, tag_rsrc_info.resource_fixups.STEPTREE,
                tag_rsrc_info.resource_definition_fixups.STEPTREE)

    def get_segment_info(self, segment_index):
        if self._play_meta and isinstance(segment_index, int):
            raw_sizes = self._play_meta.raw_sizes.STEPTREE
            segments = self._play_meta.segments.STEPTREE
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
                        segment.segment_offsets[i],
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
            raw_pages = self._play_meta.raw_pages.STEPTREE
            if page_index in range(len(raw_pages)):
                return raw_pages[page_index]

    def get_tag_resource(self, tag_rsrc_index):
        if self._zone_meta and isinstance(tag_rsrc_index, int):
            tag_resources = self._zone_meta.tag_resources.STEPTREE
            if tag_rsrc_index in range(len(tag_resources)):
                return tag_resources[tag_rsrc_index]
