import os
import re

from traceback import format_exc

from supyr_struct.defs.audio.wav import wav_def

from reclaimer.h2.util import split_raw_pointer
from reclaimer.sounds.adpcm import decode_adpcm_samples, ADPCM_BLOCKSIZE, PCM_BLOCKSIZE

from supyr_struct.buffer import BytearrayBuffer


BAD_PATH_CHAR_REMOVAL = re.compile(r'[<>:"|?*]{1, }')


__all__ = ("extract_h1_sounds", "extract_h2_sounds", )


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

        if not overwrite and os.path.isfile(filepath):
            continue

        if encoding in ("ogg", "wma") or not encoding:
            try:
                folderpath = os.path.dirname(filepath)
                # If the path doesnt exist, create it
                if not os.path.exists(folderpath):
                    os.makedirs(folderpath)

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
    tagpath_base = os.path.join(kw['out_dir'], os.path.splitext(tag_path)[0])
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

            pitchpath_base = os.path.join(pitchpath_base, name)

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
            save_sound_perms(permlist, os.path.join(pitchpath_base, name),
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
    tagpath_base = os.path.join(kw['out_dir'], os.path.splitext(tag_path)[0])

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

            pitchpath_base = os.path.join(pitchpath_base, name)

        perm_index = pr.first_permutation
        perm_count = min(pr.permutation_count, len(permutations) - perm_index)
        if perm_index < 0 or perm_count < 0:
            continue

        for j in range(perm_index, perm_index + perm_count):
            perm = permutations[j]
            name = get_sound_name(import_names, perm.import_name_index)
            if not name: name = str(j)
            permpath_base = os.path.join(pitchpath_base, name)

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
