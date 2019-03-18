import re
try:
    import arbytmap
    if not hasattr(arbytmap, "FORMAT_P8"):
        arbytmap.FORMAT_P8 = "P8"

        """ADD THE P8 FORMAT TO THE BITMAP CONVERTER"""
        arbytmap.register_format(format_id=arbytmap.FORMAT_P8,
                                 depths=(8,8,8,8))

    if not hasattr(arbytmap, "FORMAT_P8_BUMP"):
        arbytmap.FORMAT_P8_BUMP = "P8-BUMP"

        """ADD THE P8 FORMAT TO THE BITMAP CONVERTER"""
        arbytmap.register_format(format_id=arbytmap.FORMAT_P8_BUMP,
                                 depths=(8,8,8,8))

    from arbytmap import Arbytmap, bitmap_io, TYPE_2D, TYPE_3D, TYPE_CUBEMAP,\
         FORMAT_A8, FORMAT_L8, FORMAT_AL8, FORMAT_A8L8,\
         FORMAT_R5G6B5, FORMAT_A1R5G5B5, FORMAT_A4R4G4B4,\
         FORMAT_X8R8G8B8, FORMAT_A8R8G8B8,\
         FORMAT_DXT1, FORMAT_DXT3, FORMAT_DXT5, FORMAT_CTX1, FORMAT_DXN,\
         FORMAT_DXT3Y, FORMAT_DXT3A, FORMAT_DXT3AY,\
         FORMAT_DXT5Y, FORMAT_DXT5A, FORMAT_DXT5AY,\
         FORMAT_P8_BUMP, FORMAT_P8, FORMAT_V8U8, FORMAT_R8G8,\
         FORMAT_R16G16B16F, FORMAT_A16R16G16B16F,\
         FORMAT_R32G32B32F, FORMAT_A32R32G32B32F
except ImportError:
    arbytmap = Arbytmap = None

from array import array
from copy import deepcopy
from math import sqrt
from os import makedirs
from os.path import dirname, exists, join, isfile, splitext
from struct import Struct as PyStruct, unpack, pack_into
from traceback import format_exc

from supyr_struct.buffer import BytearrayBuffer
from supyr_struct.defs.constants import *
from supyr_struct.defs.util import *
from supyr_struct.defs.audio.wav import wav_def
from supyr_struct.field_types import FieldType

from reclaimer.util import is_protected_tag, is_reserved_tag, get_is_xbox_map,\
     fourcc
from reclaimer.h2.util import *
from reclaimer.h3.util import get_virtual_dimension,\
     get_pixel_bytes_size, get_h3_pixel_bytes_size
from reclaimer.adpcm import decode_adpcm_samples, ADPCM_BLOCKSIZE, PCM_BLOCKSIZE
from reclaimer.hek.defs.objs.matrices import Matrix, matrix_to_quaternion,\
     axis_angle_to_quat, quat_to_axis_angle, multiply_quaternions
from reclaimer.bitmaps.p8_palette import HALO_P8_PALETTE, STUBBS_P8_PALETTE
from reclaimer.hmt import parse_hmt_message
from reclaimer.hsc import get_hsc_data_block, hsc_bytecode_to_string
from reclaimer.model.jms import write_jms, JmsModel, JmsNode,\
     JmsMaterial, JmsMarker, JmsVertex, JmsTriangle
from reclaimer.animation.jma import JmaAnimation, JmaNode, JmaNodeState,\
     write_jma, get_anim_ext

#each sub-bitmap(cubemap face) must be a multiple of 128 bytes
CUBEMAP_PADDING = 128

BAD_PATH_CHAR_REMOVAL = re.compile(r'[<>:"|?*]{1, }')


def get_pad_size(size, mod): return 


def save_sound_perms(permlist, filepath_base, sample_rate,
                     channels=1, overwrite=True, decode_adpcm=True):
    wav_file = wav_def.build()
    for i in range(len(permlist)):
        encoding, samples = permlist[i]
        filepath = filepath_base
        if not samples:
            continue

        if len(permlist) > 1: filepath += "__%s" % i

        if encoding in ("ogg", "wma"):
            filepath += ".%s" % encoding
        elif not encoding:
            filepath += ".bin"
        else:
            filepath += ".wav"

        filepath = BAD_PATH_CHAR_REMOVAL.sub("_", filepath)

        if not overwrite and isfile(filepath):
            continue

        if encoding in ("ogg", "wma") or not encoding:
            try:
                folderpath = dirname(filepath)
                # If the path doesnt exist, create it
                if not exists(folderpath):
                    makedirs(folderpath)

                with open(filepath, "wb") as f:
                    f.write(samples)
            except Exception:
                print(format_exc())
        else:
            wav_file.filepath = filepath

            wav_fmt = wav_file.data.format
            wav_fmt.channels = channels
            wav_fmt.sample_rate = sample_rate
            wav_fmt.bits_per_sample = 16
            wav_fmt.byte_rate = ((wav_fmt.sample_rate *
                                  wav_fmt.bits_per_sample *
                                  wav_fmt.channels) // 8)

            samples_len = len(samples)
            if "adpcm" in encoding and decode_adpcm:
                samples = decode_adpcm_samples(samples, channels)

                wav_fmt.fmt.set_to('pcm')
                wav_fmt.block_align = 2 * wav_fmt.channels
                samples_len = len(samples) * 2  # UInt16 array, not bytes
            elif encoding == "none":
                wav_fmt.fmt.set_to('pcm')
                wav_fmt.block_align = 2 * wav_fmt.channels
            else:
                wav_fmt.fmt.set_to('ima_adpcm')
                wav_fmt.block_align = ADPCM_BLOCKSIZE * wav_fmt.channels
                wav_fmt.byte_rate = int(wav_fmt.byte_rate *
                                        ADPCM_BLOCKSIZE/PCM_BLOCKSIZE/2)

            wav_file.data.wav_data.audio_data = samples
            wav_file.data.wav_data.audio_data_size = samples_len
            wav_file.data.wav_header.filesize = 36 + samples_len

            wav_file.serialize(temp=False, backup=False)


def extract_h1_sounds(tagdata, tag_path, **kw):
    overwrite = kw.get('overwrite', True)
    decode_adpcm = kw.get('decode_adpcm', True)
    tagpath_base = join(kw['out_dir'], splitext(tag_path)[0])
    pitch_ranges = tagdata.pitch_ranges.STEPTREE
    same_pr_names = {}

    channels = tagdata.encoding.data + 1
    sample_rate = 22050 * (tagdata.sample_rate.data + 1)

    for i in range(len(pitch_ranges)):
        pr = pitch_ranges[i]
        perms = pr.permutations.STEPTREE
        pitchpath_base = tagpath_base
        if len(pitch_ranges) > 1:
            name = pr.name if pr.name else str(i)

            same_pr_ct = same_pr_names.get(name, 0)
            same_pr_names[name] = same_pr_ct + 1
            if same_pr_ct: name += "_%s" % same_pr_ct

            pitchpath_base = join(pitchpath_base, name)

        same_names_permlists = {}
        actual_perm_count = pr.actual_permutation_count
        unchecked_perms = set(range(len(pr.permutations.STEPTREE)))

        perm_indices = range(min(actual_perm_count, len(unchecked_perms)))
        if not perm_indices:
            perm_indices = unchecked_perms

        while perm_indices:
            # loop over all of the actual permutation indices and combine
            # the permutations they point to into a list with a shared name.
            # we do this so we can combine the permutations together into one.
            for j in perm_indices:
                perm = perms[j]
                compression = perm.compression.enum_name
                name = perm.name if perm.name else str(j)
                permlist = same_names_permlists.get(name, [])
                same_names_permlists[name] = permlist

                while j in unchecked_perms:
                    perm = perms[j]
                    if compression != perm.compression.enum_name:
                        # cant combine when compression is different
                        break

                    unchecked_perms.remove(j)
                    permlist.append(perm)

                    j = perm.next_permutation_index

            perm_indices = set(unchecked_perms)

        merged_permlists = {}
        for name, permlist in same_names_permlists.items():
            merged_permlists[name] = merged_permlist = []
            merged_data = b''
            for perm in permlist:
                compression = perm.compression.enum_name
                if compression == "ogg":
                    # cant combine this shit
                    merged_permlist.append((compression, perm.samples.data))
                    continue

                merged_data += perm.samples.data

            if merged_data:
                merged_permlist.append((compression, merged_data))


        for name, permlist in merged_permlists.items():
            save_sound_perms(permlist, join(pitchpath_base, name),
                             sample_rate, channels, overwrite, decode_adpcm)


def get_sound_name(import_names, index):
    if index < 0 or index >= len(import_names):
        return ""
    return import_names[index].string


def extract_h2_sounds(tagdata, tag_path, **kw):
    halo_map = kw.get('halo_map')
    if not halo_map:
        print("Cannot run this function on tags.")
        return

    overwrite = kw.get('overwrite', True)
    decode_adpcm = kw.get('decode_adpcm', True)
    tagpath_base = join(kw['out_dir'], splitext(tag_path)[0])

    ugh__meta = halo_map.ugh__meta
    if ugh__meta is None:
        return "    No sound_cache_file_gestalt to read sounds from."

    import_names = ugh__meta.import_names.STEPTREE
    pitch_ranges = ugh__meta.pitch_ranges.STEPTREE
    permutations = ugh__meta.permutations.STEPTREE
    perm_chunks  = ugh__meta.permutation_chunks.STEPTREE

    same_pr_names = {}

    channels    = {0: 1,     1: 2,     2: 6    }.get(tagdata.encoding.data)
    sample_rate = {0: 22050, 1: 44100, 2: 32000}.get(tagdata.sample_rate.data)
    compression = ""
    if channels in (1, 2):
        compression = tagdata.compression.enum_name

    if tagdata.encoding.enum_name == "codec":
        pass # return "    CANNOT YET EXTRACT THIS FORMAT."
        '''
        The codec format seems to be encoded with wmaudio2.

        Bytes:
            0-31
                Two nearly identical GUIDs, with the second one specifying in
                its first 2 bytes that the audio data is encoded with wmaudio2.
            32-39
                Unknown, but always seems to be 01 00 00 00  00 00 00 00
            40-43
                Number of blocks of data(same value found in the header below)
            44-55
                Unknown, but I think it always seems to be the same.
            56-87
                wav_format header struct. sig is "ZYU\x00" instead of "fmt ",
                length is 28 instead of 20, and fmt is(always?) 0x0161,
                which is the format code for wmaudio2.
                channels, sample_rate, byte_rate, block_align, and
                bits_per_sample all seem to be set properly. the value
                for block_align is the same as bytes 40-43
            88-91
                Unknown. Might be something to specify the data length?

            Everything after this appears to be audio data.
        '''

    pr_index = tagdata.pitch_range_index
    pr_count = min(tagdata.pitch_range_count, len(pitch_ranges) - pr_index)
    if pr_index < 0 or pr_count < 0:
        # nothing to extract
        return

    for i in range(pr_index, pr_index + pr_count):
        pr = pitch_ranges[i]
        pitchpath_base = tagpath_base
        if pr_count > 1:
            name = get_sound_name(import_names, pr.import_name_index)
            if not name: name = str(i)

            same_pr_ct = same_pr_names.get(name, 0)
            same_pr_names[name] = same_pr_ct + 1
            if same_pr_ct: name += "_%s" % same_pr_ct

            pitchpath_base = join(pitchpath_base, name)

        perm_index = pr.first_permutation
        perm_count = min(pr.permutation_count, len(permutations) - perm_index)
        if perm_index < 0 or perm_count < 0:
            continue

        for j in range(perm_index, perm_index + perm_count):
            perm = permutations[j]
            name = get_sound_name(import_names, perm.import_name_index)
            if not name: name = str(j)
            permpath_base = join(pitchpath_base, name)

            chunk_index = perm.first_chunk
            chunk_count = min(perm.chunk_count, len(perm_chunks) - chunk_index)
            if chunk_index < 0 or chunk_count < 0:
                continue

            merged_data = b''
            for k in range(chunk_index, chunk_index + chunk_count):
                ptr, map_name = split_raw_pointer(perm_chunks[k].pointer)
                size = perm_chunks[k].size
                this_map = halo_map
                if map_name != "local":
                    this_map = halo_map.maps.get(map_name)

                if this_map is None:
                    continue
                elif this_map.map_data is None:
                    continue

                this_map.map_data.seek(ptr)
                merged_data += this_map.map_data.read(size)

            permpath_base = permpath_base.replace('|', '')
            save_sound_perms([(compression, merged_data)], permpath_base,
                             sample_rate, channels, overwrite, decode_adpcm)


def extract_bitmaps(tagdata, tag_path, **kw):
    filepath_base = join(kw['out_dir'], splitext(tag_path)[0])
    ext = kw.get("bitmap_ext", "").strip(". ")
    keep_alpha = kw.get("bitmap_keep_alpha", True)
    engine = kw.pop('engine', '')
    pix_data = tagdata.processed_pixel_data.STEPTREE
    if 'halo_map' in kw:
        engine = kw['halo_map'].engine

    p8_palette = STUBBS_P8_PALETTE if "stubbs" in engine else HALO_P8_PALETTE
    if not ext:
        ext = "dds"

    is_xbox = get_is_xbox_map(engine)
    is_gen3 = hasattr(tagdata, "zone_assets_normal")
    if Arbytmap is None:
        # cant extract xbox bitmaps yet
        return "    Arbytmap not loaded. Cannot extract bitmaps."

    arby = Arbytmap()
    bitm_i = 0
    multi_bitmap = len(tagdata.bitmaps.STEPTREE) > 1
    size_calc = get_h3_pixel_bytes_size if is_gen3 else get_pixel_bytes_size
    dim_calc = get_virtual_dimension if is_gen3 else None

    for bitmap in tagdata.bitmaps.STEPTREE:
        typ = bitmap.type.enum_name
        fmt = bitmap.format.enum_name
        w = bitmap.width
        h = bitmap.height
        d = bitmap.depth
        tiled = False
        if hasattr(bitmap, "format_flags"):
            tiled = bitmap.format_flags.tiled

        filepath = filepath_base
        if multi_bitmap:
            filepath += "__%s" % bitm_i
            bitm_i += 1

        tex_block = []
        tex_info = dict(
            width=w, height=h, depth=d, mipmap_count=bitmap.mipmaps,
            swizzled=bitmap.flags.swizzled, big_endian=is_gen3,
            packed=True, tiled=tiled, tile_method="DXGI",
            packed_width_calc=dim_calc, packed_height_calc=dim_calc,
            filepath=filepath + "." + ext,
            )
        tex_info["texture_type"] = {
            "texture_2d": TYPE_2D, "texture_3d": TYPE_3D,
            "cubemap": TYPE_CUBEMAP}.get(typ, TYPE_2D)
        tex_info["sub_bitmap_count"] = {
            "texture_2d": 1, "texture_3d": 1,
            "cubemap": 6, "multipage_2d": d}.get(typ, 1)
        if typ == "multipage_2d":
            tex_info.update(depth=1)
            d = 1


        if fmt == "p8_bump":
            tex_info.update(
                palette=[p8_palette.p8_palette_32bit_packed]*(bitmap.mipmaps + 1),
                palette_packed=True, indexing_size=8, format=FORMAT_P8_BUMP)
        else:
            tex_info["format"] = {
                "a8": FORMAT_A8, "y8": FORMAT_L8, "ay8": FORMAT_AL8,
                "a8y8": FORMAT_A8L8, "p8": FORMAT_A8,
                "v8u8": FORMAT_V8U8, "g8b8": FORMAT_R8G8,
                "x8r8g8b8": FORMAT_A8R8G8B8, "a8r8g8b8": FORMAT_A8R8G8B8,
                "r5g6b5": FORMAT_R5G6B5, "a1r5g5b5": FORMAT_A1R5G5B5,
                "a4r4g4b4": FORMAT_A4R4G4B4,
                "dxt1": FORMAT_DXT1, "dxt3": FORMAT_DXT3, "dxt5": FORMAT_DXT5,
                "ctx1": FORMAT_CTX1, "dxn": FORMAT_DXN, "dxt5ay": FORMAT_DXT5AY,
                "dxt3a": FORMAT_DXT3A, "dxt3y": FORMAT_DXT3Y,
                "dxt5a": FORMAT_DXT5A, "dxt5y": FORMAT_DXT5Y,
                "rgbfp16": FORMAT_R16G16B16F, "argbfp32": FORMAT_A32R32G32B32F,
                "rgbfp32": FORMAT_R32G32B32F}.get(fmt, None)


        arby_fmt = tex_info["format"]
        if arby_fmt is None:
            continue

        i_max = tex_info["sub_bitmap_count"] if is_xbox else bitmap.mipmaps + 1
        j_max = bitmap.mipmaps + 1 if is_xbox else tex_info['sub_bitmap_count']
        off = bitmap.pixels_offset
        for i in range(i_max):
            if not is_xbox:
                mip_size = size_calc(arby_fmt, w, h, d, i, tiled)

            for j in range(j_max):
                if is_xbox:
                    mip_size = size_calc(arby_fmt, w, h, d, j, tiled)

                if fmt == "p8_bump":
                    tex_block.append(
                        array('B', pix_data[off: off + (mip_size // 4)]))
                    off += len(tex_block[-1])
                else:
                    off = bitmap_io.bitmap_bytes_to_array(
                        pix_data, off, tex_block,
                        arby_fmt, 1, 1, 1, mip_size)

            # skip the xbox alignment padding to get to the next texture
            if is_xbox and typ == "cubemap":
                off += ((CUBEMAP_PADDING - (off % CUBEMAP_PADDING)) %
                        CUBEMAP_PADDING)


        if is_xbox and typ == "cubemap":
            template = tuple(tex_block)
            i = 0
            for f in (0, 2, 1, 3, 4, 5):
                for m in range(bitmap.mipmaps + 1):
                    tex_block[m*6 + f] = template[i]
                    i += 1

        if not tex_block:
            # nothing to extract
            continue

        arby.load_new_texture(texture_block=tex_block, texture_info=tex_info,
                              tile_mode=False, swizzle_mode=False)
        arby.save_to_file(keep_alpha=keep_alpha)


def extract_unicode_string_list(tagdata, tag_path, **kw):
    return extract_string_list(tagdata, tag_path, "utf-16-le", **kw)


def extract_string_list(tagdata, tag_path, encoding="latin-1", **kw):
    filepath = join(kw['out_dir'], splitext(tag_path)[0] + ".txt")
    if isfile(filepath) and not kw.get('overwrite', True):
        return

    out_data = b""
    for b in tagdata.strings.STEPTREE:
        string = b.data
        string += "\r\n###END-STRING###\r\n"  # cr + lf
        out_data += string.encode(encoding)

    try:
        folderpath = dirname(filepath)
        # If the path doesnt exist, create it
        if not exists(folderpath):
            makedirs(folderpath)

        with open(filepath, "wb") as f:
            if encoding == "utf-16-le":
                f.write(b"\xFF\xFE")  # little endian unicode sig
            f.write(out_data)
    except Exception:
        return format_exc()


def extract_hud_message_text(tagdata, tag_path, **kw):
    filepath = join(kw['out_dir'], splitext(tag_path)[0] + ".hmt")
    if isfile(filepath) and not kw.get('overwrite', True):
        return

    out_data = b""
    for i in range(tagdata.messages.size):
        try:
            name = tagdata.messages.STEPTREE[i].name
            string = parse_hmt_message(tagdata, i)[0]
        except Exception:
            print(format_exc())
            continue

        out_data += ("%s=%s" % (name, string)).encode("utf-16-le")
        out_data += b"\x0D\x00\x0A\x00"  # cr + lf

    try:
        folderpath = dirname(filepath)
        # If the path doesnt exist, create it
        if not exists(folderpath):
            makedirs(folderpath)

        with open(filepath, "wb") as f:
            f.write(b"\xFF\xFE")  # little endian unicode sig
            f.write(out_data)
    except Exception:
        return format_exc()

    return


def extract_h1_scnr_data(tagdata, tag_path, **kw):
    filepath_base = join(kw['out_dir'], dirname(tag_path), "scripts")
    overwrite = kw.get('overwrite', True)
    hsc_node_strings_by_type = kw.get("hsc_node_strings_by_type", ())
    # If the path doesnt exist, create it
    if not exists(filepath_base):
        makedirs(filepath_base)

    engine = kw.get('engine')
    if not engine and 'halo_map' in kw:
        engine = kw['halo_map'].engine

    syntax_data = get_hsc_data_block(tagdata.script_syntax_data.data)
    string_data = tagdata.script_string_data.data.decode("latin-1")
    if not syntax_data or not string_data:
        return "No script data to extract."

    already_sorted = set()
    for typ, arr in (("global", tagdata.globals.STEPTREE),
                     ("script", tagdata.scripts.STEPTREE)):
        filepath = join(filepath_base, "%ss" % typ)
        comments = ""
        src_file_i = 0
        global_uses  = {}
        static_calls = {}
        if typ == "global":
            sort_by = global_uses
            try:
                comments += "; scenario names(each sorted alphabetically)\n"
                comments += "\n;   object names:\n"
                for name in sorted(set(obj.name for obj in
                                       tagdata.object_names.STEPTREE)):
                    comments += ";     %s\n" % name

                comments += "\n;   trigger volumes:\n"
                for name in sorted(set(tv.name for tv in
                                       tagdata.trigger_volumes.STEPTREE)):
                    comments += ";     %s\n" % name

                comments += "\n;   device groups:\n"
                for name in sorted(set(dg.name for dg in
                                       tagdata.device_groups.STEPTREE)):
                    comments += ";     %s\n" % name

            except Exception:
                pass
        else:
            sort_by = static_calls

        try:
            sources = {}
            for i in range(len(arr)):
                # assemble source code for each function/global
                name = arr[i].name
                global_uses[name]  = set()
                static_calls[name] = set()
                sources[name] = hsc_bytecode_to_string(
                    syntax_data, string_data, i, tagdata.scripts.STEPTREE,
                    tagdata.globals.STEPTREE, typ, engine,
                    global_uses=global_uses[name],
                    hsc_node_strings_by_type=hsc_node_strings_by_type,
                    static_calls=static_calls[name])

            sorted_sources = []
            need_to_sort = sources
            while need_to_sort:
                # sort the functions/globals so dependencies come first
                next_need_to_sort = {}
                for name in sorted(need_to_sort.keys()):
                    source = need_to_sort[name]
                    if sort_by[name].issubset(already_sorted):
                        sorted_sources.append(source)
                        already_sorted.add(name)
                    else:
                        next_need_to_sort[name] = source

                if need_to_sort.keys() == next_need_to_sort.keys():
                    print("Could not sort these %ss so dependencies come first:" % typ)
                    for src in need_to_sort.keys():
                        print("\t%s" % src)
                        sorted_sources.append(src)
                    break
                need_to_sort = next_need_to_sort

            merged_sources = []
            merged_src = ""
            for src in sorted_sources:
                if not src:
                    continue
                # concatenate sources until they are too large to be compiled
                if len(merged_src) + len(src) > 262100:
                    merged_sources.append(merged_src)
                    merged_src = ""

                merged_src += src + "\n\n\n"

            if merged_src:
                merged_sources.append(merged_src)

            i = 0
            for out_data in merged_sources:
                # write sources to hsc files
                if len(merged_sources) > 1:
                    fp = "%s_%s.hsc" % (filepath, i)
                else:
                    fp = "%s.hsc" % filepath

                if not overwrite and isfile(fp):
                    continue

                # apparently the scripts use latin1 encoding, who knew....
                with open(fp, "w", encoding='latin1') as f:
                    f.write("; Extracted with Reclaimer\n\n")
                    f.write(out_data)
                    f.write(comments)

                i += 1
        except Exception:
            return format_exc()

    # TEMPORARY CODE
    #from reclaimer.enums import TEST_PRINT_HSC_BUILT_IN_FUNCTIONS
    #TEST_PRINT_HSC_BUILT_IN_FUNCTIONS()
    # TEMPORARY CODE


def extract_physics(tagdata, tag_path, **kw):
    filepath = join(kw['out_dir'], dirname(tag_path), "physics", "physics.jms")
    if not kw.get('overwrite', True) and isfile(filepath):
        return

    jms_data = JmsModel()
    nodes = jms_data.nodes = [JmsNode("root")]
    markers = jms_data.markers

    child_node_ct = 0
    for mp in tagdata.mass_points.STEPTREE:
        child_node_ct = max(child_node_ct, mp.model_node)
        fi, fj, fk = mp.forward
        ui, uj, uk = mp.up
        si, sj, sk = uj*fk - fj*uk, uk*fi - fk*ui, ui*fj - fi*uj

        matrix = Matrix(
            ((fi, fj, fk),
             (si, sj, sk),
             (ui, uj, uk)))
        i, j, k, w = matrix_to_quaternion(matrix)
        # no idea why I have to invert these
        w = -w
        if w < 0:
            i, j, k, w = -i, -j, -k, -w

        markers.append(
            JmsMarker(
                mp.name, "physics", -1, mp.model_node, i, j, k, w,
                mp.position.x * 100, mp.position.y * 100, mp.position.z * 100,
                mp.radius * 100,
                ))

    if child_node_ct > 0:
        # make some fake nodes
        nodes[0].first_child = 1
        for i in range(child_node_ct):
            nodes.append(JmsNode("node_%s" % (i + 1), -1, i + 2))
        nodes[-1].sibling_index = -1

    write_jms(filepath, jms_data)


def extract_model(tagdata, tag_path, **kw):
    filepath_base = join(kw['out_dir'], dirname(tag_path), "models")

    global_markers = {}
    materials = []
    regions = []
    nodes = []

    for b in tagdata.markers.STEPTREE:
        marker_name = b.name

        for inst in b.marker_instances.STEPTREE:
            try:
                region = tagdata.regions.STEPTREE[inst.region_index]
            except Exception:
                print("Invalid region index in marker '%s'" % marker_name)
                continue

            try:
                perm = region.permutations.STEPTREE[inst.permutation_index]
                perm_name = perm.name
                if (perm.flags.cannot_be_chosen_randomly and
                    not perm_name.startswith("~")):
                    perm_name += "~"
            except Exception:
                print("Invalid permutation index in marker '%s'" % marker_name)
                continue

            perm_markers = global_markers.setdefault(perm_name, [])

            trans = inst.translation
            rot = inst.rotation
            perm_markers.append(JmsMarker(
                marker_name, perm_name, inst.region_index, inst.node_index,
                rot.i, rot.j, rot.k, rot.w,
                trans.x * 100, trans.y * 100, trans.z * 100,
                1.0
                ))

    for b in tagdata.nodes.STEPTREE:
        trans = b.translation
        rot = b.rotation
        nodes.append(JmsNode(
            b.name, b.first_child_node, b.next_sibling_node,
            rot.i, rot.j, rot.k, rot.w,
            trans.x * 100, trans.y * 100, trans.z * 100
            ))

    for b in tagdata.shaders.STEPTREE:
        materials.append(JmsMaterial(
            b.shader.filepath.split("/")[-1].split("\\")[-1])
            )

    markers_by_perm = {}
    geoms_by_perm_lod_region = {}

    u_scale = tagdata.base_map_u_scale
    v_scale = tagdata.base_map_v_scale

    for region in tagdata.regions.STEPTREE:
        region_index = len(regions)
        regions.append(region.name)
        for perm in region.permutations.STEPTREE:
            perm_name = perm.name
            if (perm.flags.cannot_be_chosen_randomly and
                not perm_name.startswith("~")):
                perm_name += "~"

            geoms_by_lod_region = geoms_by_perm_lod_region.setdefault(perm_name, {})

            perm_markers = markers_by_perm.setdefault(perm_name, [])
            if hasattr(perm, "local_markers"):
                for m in perm.local_markers.STEPTREE:
                    trans = m.translation
                    rot = m.rotation
                    perm_markers.append(JmsMarker(
                        m.name, perm_name, region_index, m.node_index,
                        rot.i, rot.j, rot.k, rot.w,
                        trans.x * 100, trans.y * 100, trans.z * 100,
                        1.0
                        ))

            last_geom_index = -1
            for lod_num in range(5):
                geoms_by_region = geoms_by_lod_region.get(lod_num, {})
                region_geoms = geoms_by_region.get(region.name, [])

                geom_index = perm[
                    perm.NAME_MAP["superlow_geometry_block"] + (4 - lod_num)]

                if (geom_index in region_geoms or
                    geom_index == last_geom_index):
                    continue

                geoms_by_lod_region[lod_num] = geoms_by_region
                geoms_by_region[region.name] = region_geoms
                region_geoms.append(geom_index)
                last_geom_index = geom_index

    try:
        use_local_nodes = tagdata.flags.parts_have_local_nodes
    except Exception:
        use_local_nodes = False
    def_node_map = list(range(128))
    def_node_map.append(-1)

    # use big endian since it will have been byteswapped
    comp_vert_unpacker = PyStruct(">3f3I2h2bh").unpack_from
    uncomp_vert_unpacker = PyStruct(">14f2h2f").unpack_from

    for perm_name in sorted(geoms_by_perm_lod_region):
        geoms_by_lod_region = geoms_by_perm_lod_region[perm_name]
        perm_markers = markers_by_perm.get(perm_name)
        
        for lod_num in sorted(geoms_by_lod_region):
            if lod_num == -1:
                continue

            filepath = join(filepath_base, perm_name)
            if   lod_num == 4:
                filepath += " superlow.jms"
            elif lod_num == 3:
                filepath += " low.jms"
            elif lod_num == 2:
                filepath += " medium.jms"
            elif lod_num == 1:
                filepath += " high.jms"
            else:
                filepath += " superhigh.jms"

            markers = list(perm_markers)
            markers.extend(global_markers.get(perm_name, ()))
            verts = []
            tris = []

            geoms_by_region = geoms_by_lod_region[lod_num]
            for region_name in sorted(geoms_by_region):
                region_index = regions.index(region_name)
                geoms = geoms_by_region[region_name]

                for geom_index in geoms:
                    try:
                        geom_block = tagdata.geometries.STEPTREE[geom_index]
                    except Exception:
                        print("Invalid geometry index '%s'" % geom_index)
                        continue

                    for part in geom_block.parts.STEPTREE:
                        v_origin = len(verts)
                        shader_index = part.shader_index

                        try:
                            node_map = list(part.local_nodes)
                            node_map.append(-1)
                            compressed = False
                        except (AttributeError, KeyError):
                            compressed = True

                        if not use_local_nodes:
                            node_map = def_node_map

                        try:
                            unparsed = isinstance(
                                part.triangles.STEPTREE.data, bytearray)
                        except Exception:
                            unparsed = False

                        # TODO: Make this work in meta(parse verts and tris)
                        try:
                            if compressed and unparsed:
                                vert_data = part.compressed_vertices.STEPTREE.data
                                for off in range(0, len(vert_data), 32):
                                    v = comp_vert_unpacker(vert_data, off)
                                    n = v[3]
                                    ni = (n&1023) / 1023
                                    nj = ((n>>11)&1023) / 1023
                                    nk = ((n>>22)&511) / 511
                                    if (n>>10)&1: ni = ni - 1.0
                                    if (n>>21)&1: nj = nj - 1.0
                                    if (n>>31)&1: nk = nk - 1.0

                                    verts.append(JmsVertex(
                                        v[8]//3,
                                        v[0] * 100, v[1] * 100, v[2] * 100,
                                        ni, nj, nk,
                                        v[9]//3, 1.0 - (v[10]/32767),
                                        u_scale * v[6]/32767, 1.0 - v_scale * v[7]/32767))
                            elif compressed:
                                for v in part.compressed_vertices.STEPTREE:
                                    n = v[3]
                                    ni = (n&1023) / 1023
                                    nj = ((n>>11)&1023) / 1023
                                    nk = ((n>>22)&511) / 511
                                    if (n>>10)&1: ni = ni - 1.0
                                    if (n>>21)&1: nj = nj - 1.0
                                    if (n>>31)&1: nk = nk - 1.0

                                    verts.append(JmsVertex(
                                        v[8]//3,
                                        v[0] * 100, v[1] * 100, v[2] * 100,
                                        ni, nj, nk,
                                        v[9]//3, 1.0 - (v[10]/32767),
                                        u_scale * v[6]/32767, 1.0 - v_scale * v[7]/32767))
                            elif not compressed and unparsed:
                                vert_data = part.uncompressed_vertices.STEPTREE.data
                                for off in range(0, len(vert_data), 68):
                                    v = uncomp_vert_unpacker(vert_data, off)
                                    verts.append(JmsVertex(
                                        node_map[v[14]],
                                        v[0] * 100, v[1] * 100, v[2] * 100,
                                        v[3], v[4], v[5],
                                        node_map[v[15]], max(0, min(1, v[17])),
                                        u_scale * v[12], 1.0 - v_scale * v[13]))
                            else:
                                for v in part.uncompressed_vertices.STEPTREE:
                                    verts.append(JmsVertex(
                                        node_map[v[14]],
                                        v[0] * 100, v[1] * 100, v[2] * 100,
                                        v[3], v[4], v[5],
                                        node_map[v[15]], max(0, min(1, v[17])),
                                        u_scale * v[12], 1.0 - v_scale * v[13]))
                        except Exception:
                            print(format_exc())
                            print("If you see this, tell Moses to stop "
                                  "fucking with the vertex definition.")

                        try:
                            if unparsed:
                                tri_block = part.triangles.STEPTREE.data
                                tri_list = [-1] * (len(tri_block) // 2)
                                for i in range(len(tri_list)):
                                    # assuming big endian
                                    tri_list[i] = (
                                        tri_block[i * 2 + 1] +
                                        (tri_block[i * 2] << 8))
                                    if tri_list[i] > 32767:
                                        tri_list[i] = -1
                            else:
                                tri_block = part.triangles.STEPTREE
                                tri_list = []
                                for triangle in tri_block:
                                    tri_list.extend(triangle)

                            swap = True
                            for i in range(len(tri_list) - 2):
                                v0 = tri_list[i]
                                v1 = tri_list[i + 1 + swap]
                                v2 = tri_list[i + 2 - swap]
                                if v0 != -1 and v1 != -1 and v2 != -1:
                                    # remove degens
                                    if v0 != v1 and v0 != v2 and v1 != v2:
                                        tris.append(JmsTriangle(
                                            region_index, shader_index,
                                            v0 + v_origin,
                                            v1 + v_origin,
                                            v2 + v_origin))
                                swap = not swap
                        except Exception:
                            print(format_exc())
                            print("Could not parse triangle blocks.")

            write_jms(filepath, JmsModel(
                "", tagdata.node_list_checksum, nodes, materials,
                markers, regions, verts, tris))


def apply_frame_info_to_state(state, dx=0, dy=0, dz=0, dyaw=0):
    x, y, z = state.pos_x + dx, state.pos_y + dy, state.pos_z + dz
    i, j, k, w = multiply_quaternions(
        axis_angle_to_quat(1, 0, 0, -dyaw),
        (state.rot_i, state.rot_j, state.rot_k, state.rot_w),
        )
    return JmaNodeState(i, j, k, w, x, y, z, state.scale)


def extract_animation(tagdata, tag_path, **kw):
    if not tagdata.animations.STEPTREE:
        return

    filepath_base = join(kw['out_dir'], dirname(tag_path), "animations")
    endian = ">"
    if kw.get('halo_map') and kw.get('halo_map').engine != "halo1anni":
        endian = "<"

    unpack_trans = PyStruct(endian + "3f").unpack
    unpack_ijkw  = PyStruct(endian + "4h").unpack
    unpack_dxdy  = PyStruct(endian + "2f").unpack
    unpack_float = PyStruct(endian + "f").unpack

    anim_nodes = []
    for node in tagdata.nodes.STEPTREE:
        anim_nodes.append(JmaNode(node.name, node.first_child_node_index,
                                  node.next_sibling_node_index))

    if not anim_nodes:
        print("WARNING: Animation tag missing nodes.\n"
              "\tFake nodes will be created to allow compiling the animations.\n"
              "\tAnimation tags compiled from these files won't import onto\n"
              "\ttheir gbxmodel in 3DS Max, as their node names won't match.")
        for i in range(tagdata.animations.STEPTREE[0].node_count):
            anim_nodes.append(JmaNode("fake_node%s" % i, -1, i + 1))

        anim_nodes[0].first_child = 1
        anim_nodes[-1].first_child = -1
        anim_nodes[0].sibling_index = anim_nodes[-1].sibling_index = -1


    for anim in tagdata.animations.STEPTREE:
        try:
            anim_type = anim.type.enum_name
            frame_info_type = anim.frame_info_type.enum_name.lower()
            world_relative = anim.flags.world_relative

            has_dxdy = "dx" in frame_info_type
            has_dz   = "dz" in frame_info_type
            has_dyaw = "dyaw" in frame_info_type

            anim_ext = get_anim_ext(anim_type, frame_info_type, world_relative)

            filepath = join(filepath_base, anim.name + anim_ext)
            if not kw.get('overwrite', True) and isfile(filepath):
                return

            frame_count = anim.frame_count
            node_count  = anim.node_count
            trans_int = anim.trans_flags0 + (anim.trans_flags1 << 32)
            rot_int   = anim.rot_flags0   + (anim.rot_flags1   << 32)
            scale_int = anim.scale_flags0 + (anim.scale_flags1 << 32)

            trans_flags = tuple(bool(trans_int & (1 << i)) for i in range(node_count))
            rot_flags   = tuple(bool(rot_int   & (1 << i)) for i in range(node_count))
            scale_flags = tuple(bool(scale_int & (1 << i)) for i in range(node_count))

            frame_info   = anim.frame_info.STEPTREE
            default_data = anim.default_data.STEPTREE
            frame_data   = anim.frame_data.STEPTREE

            anim_frames = []

            frame_info_size = {
                "dx,dy": 8,
                "dx,dy,dyaw": 12,
                "dx,dy,dz,dyaw": 16}.get(frame_info_type, 0) * frame_count
            frame_size = (12 * sum(trans_flags) + 8 * sum(rot_flags) +
                          4  * sum(scale_flags))
            default_data_size = anim.node_count * (12 + 8 + 4) - frame_size
            uncomp_data_size = frame_size * anim.frame_count
            if len(anim_nodes) != anim.node_count:
                print("Skipping animation with different number of nodes "
                      "than the tag contains: '%s'" % anim.name)
                continue
            elif frame_info_size > len(frame_info):
                print("Skipping animation with less frame_info data "
                      "than it is expected to contain: '%s'" % anim.name)
                continue
            elif default_data_size > len(default_data):
                print("Skipping animation with less default_data "
                      "than it is expected to contain: '%s'" % anim.name)
                continue
            elif uncomp_data_size > len(frame_data):
                print("Skipping animation with less frame_data "
                      "than it is expected to contain: '%s'" % anim.name)
                continue
            elif anim.flags.compressed_data and sum(default_data) == 0:
                print("Skipping compressed animation without uncompressed "
                      "animation data: '%s'" % anim.name)
                continue


            # sum the frame info changes for each frame
            off = 0
            root_node_infos = [[0.0, 0.0, 0.0, 0.0] for i in
                               range(anim.frame_count + 1)]
            dx = dy = dz = dyaw = 0.0
            for f in range(anim.frame_count):
                if has_dxdy:
                    dx, dy = unpack_dxdy(frame_info[off: off + 8])
                    off += 8

                if has_dz:
                    dz = unpack_float(frame_info[off: off + 4])[0]
                    off += 4

                if has_dyaw:
                    dyaw = unpack_float(frame_info[off: off + 4])[0]
                    off += 4

                x, y, z, yaw = root_node_infos[f]
                root_node_infos[f + 1][:] = [x + dx, y + dy, z + dz, yaw + dyaw]


            off = 0
            def_node_states = []
            if anim_type == "overlay":
                anim_frames.append(def_node_states)

            for n in range(anim.node_count):
                i = j = k = x = y = z = 0.0
                w = scale = 1.0
                if not rot_flags[n]:
                    i, j, k, w = unpack_ijkw(default_data[off: off + 8])
                    rot_len = i**2 + j**2 + k**2 + w**2
                    if rot_len:
                        rot_len = sqrt(rot_len)
                        i /= rot_len
                        j /= rot_len
                        k /= rot_len
                        w /= rot_len
                    else:
                        i = j = k = 0.0
                        w = 1.0

                    off += 8

                if not trans_flags[n]:
                    x, y, z = unpack_trans(default_data[off: off + 12])
                    off += 12

                if not scale_flags[n]:
                    scale = unpack_float(default_data[off: off + 4])[0]
                    off += 4

                def_node_states.append(JmaNodeState(i, j, k, w, x, y, z, scale))


            off = 0
            for f in range(anim.frame_count):
                node_states = []
                anim_frames.append(node_states)
                for n in range(anim.node_count):
                    def_state = def_node_states[n]
                    if rot_flags[n]:
                        i, j, k, w = unpack_ijkw(frame_data[off: off + 8])
                        rot_len = i**2 + j**2 + k**2 + w**2
                        if rot_len:
                            rot_len = sqrt(rot_len)
                            i /= rot_len
                            j /= rot_len
                            k /= rot_len
                            w /= rot_len
                        else:
                            i = j = k = 0.0
                            w = 1.0
                        off += 8
                    else:
                        i, j, k, w = (def_state.rot_i, def_state.rot_j,
                                      def_state.rot_k, def_state.rot_w)

                    if trans_flags[n]:
                        x, y, z = unpack_trans(frame_data[off: off + 12])
                        off += 12
                    else:
                        x, y, z = def_state.pos_x, def_state.pos_y, def_state.pos_z

                    if scale_flags[n]:
                        scale = unpack_float(frame_data[off: off + 4])[0]
                        off += 4
                    else:
                        scale = def_state.scale

                    node_states.append(JmaNodeState(i, j, k, w, x, y, z, scale))

                    if n == 0:
                        node_states[-1] = apply_frame_info_to_state(
                            node_states[-1], *root_node_infos[f])


            if anim_type != "overlay":
                # copy the first frame to the last frame
                node_states = deepcopy(anim_frames[0])
                anim_frames.append(node_states)

                if root_node_infos:
                    # add the last root info to the last frame, but make
                    # sure to remove the frame_info from the first frame
                    dx0, dy0, dz0, dyaw0 = root_node_infos[0]
                    dx1, dy1, dz1, dyaw1 = root_node_infos[-1]

                    node_states[0] = apply_frame_info_to_state(
                        node_states[0], dx1 - dx0, dy1 - dy0,
                        dz1 - dz0, dyaw1 - dyaw0)

            write_jma(
                filepath,
                JmaAnimation(
                    anim.name, anim.node_list_checksum,
                    anim_type, frame_info_type, anim.flags.world_relative,
                    anim_nodes, anim_frames)
                )
        except Exception:
            print(format_exc())
            print("Could not extract animation.")


h1_data_extractors = {
    'phys': extract_physics,
    'mode': extract_model, 'mod2': extract_model,
    'antr': extract_animation, 'magy': extract_animation,
    #'coll': extract_collision,
    #'sbsp': None, 'font': None, 'unic': None,
    'str#': extract_string_list, 'ustr': extract_unicode_string_list,
    "bitm": extract_bitmaps, "snd!": extract_h1_sounds,
    "hmt ": extract_hud_message_text, 'scnr': extract_h1_scnr_data,
    }

h2_data_extractors = {
    #'mode', 'coll', 'phmo', 'jmad',
    #'sbsp',

    #'unic',
    "bitm": extract_bitmaps, "snd!": extract_h2_sounds,
    }

h3_data_extractors = {
    "bitm": extract_bitmaps,
    }
