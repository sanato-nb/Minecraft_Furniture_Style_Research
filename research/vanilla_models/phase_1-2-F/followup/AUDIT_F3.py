"""Check reusable model surfaces and animation frames against the pinned client."""
import argparse
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageDraw

DATA = Path('research/vanilla_models/phase_1-2-F/entry6')
SOURCE = Path('1.21.11')
MODELS = SOURCE / 'assets/minecraft/models/block'
JAR_SHA1 = 'ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd'


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def write(path, values):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, values[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(values)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def matching(jar, path):
    data = path.read_bytes()
    if data != jar.read(path.relative_to(SOURCE).as_posix()):
        raise ValueError(f'JAR differs from extracted source: {path}')
    return data


def model_path(ref):
    return SOURCE / 'assets/minecraft/models' / (ref.removeprefix('minecraft:') + '.json')


def basename(path):
    return path.stem


def model_context(models, model):
    chain = []
    while model in models and model not in chain:
        chain.append(model)
        ref = models[model].get('parent')
        if not ref:
            break
        model = model_path(ref)
    textures = {}
    provider = None
    for path in reversed(chain):
        data = models[path]
        textures.update(data.get('textures', {}))
        if 'elements' in data:
            provider = path
    return chain, provider, textures


def texture_path(ref, textures):
    seen = set()
    key = ref.removeprefix('#')
    while key in textures and key not in seen:
        seen.add(key)
        ref = textures[key]
        key = ref.removeprefix('#')
    if ref.startswith('#') or '/' not in ref:
        return None
    namespace, sep, identifier = ref.partition(':')
    if not sep:
        namespace, identifier = 'minecraft', namespace
    path = SOURCE / f'assets/{namespace}/textures/{identifier}.png'
    return path if path.is_file() else None


def decode(jar, path):
    data = matching(jar, path)
    with Image.open(io.BytesIO(data)) as encoded:
        return data, encoded.convert('RGBA')


def make_sheet(path, sections, cells, step):
    canvas = Image.new('RGB', (31 + cells * step, 28 + sum(rows * step + 24 for _, _, rows in sections)), '#252a31')
    draw = ImageDraw.Draw(canvas)
    y = 10
    for label, frames, count_rows in sections:
        draw.text((10, y), label, fill='white')
        y += 19
        for idx, (tag, image) in enumerate(frames):
            x = 12 + idx % cells * step
            top = y + idx // cells * step
            preview = image.copy()
            preview.thumbnail((step - 12, step - 17), Image.Resampling.NEAREST)
            if max(preview.size) < step - 17:
                ratio = max(1, (step - 17) // max(preview.size))
                preview = preview.resize(tuple(n * ratio for n in preview.size), Image.Resampling.NEAREST)
            draw.rectangle((x, top, x + step-8, top + step-12), fill='#59606b')
            canvas.paste(preview, (x + 1, top + 1), preview)
            draw.text((x, top + step - 11), tag, fill='white')
        y += count_rows * step + 5
    canvas.save(path)


def audit_templates(jar, output, preview):
    baseline = rows(DATA / 'F3_UNBOUND_OR_TEMPLATE_38.csv')
    raw_models = {path: json.loads(path.read_bytes()) for path in MODELS.glob('*.json')}
    contexts = {path: model_context(raw_models, path) for path in sorted(raw_models)}
    descendants = defaultdict(list)
    for child, (chain, provider, textures) in contexts.items():
        for ancestor in chain[1:]:
            descendants[ancestor].append((child, chain, provider, textures))

    summary, evidence, sections = [], [], []
    for row in baseline:
        template = Path(row['model_path'])
        if blob(matching(jar, template)) != row['model_sha']:
            raise ValueError(f'Model hash mismatch: {template}')
        _, provider, _ = contexts[template]
        candidates = descendants[template]
        eligible = [(child, chain, textures) for child, chain, effective, textures in candidates
                    if provider and effective == provider]
        refs = [face['texture'] for element in raw_models.get(provider, {}).get('elements', [])
                for face in element.get('faces', {}).values()]
        counter = Counter()
        images = {}
        for child, chain, textures in eligible:
            paths = [texture_path(ref, textures) for ref in refs]
            if not paths or any(path is None for path in paths):
                continue
            for path in chain:
                matching(jar, path)
            per_png = Counter(paths)
            counter.update(per_png)
            for png, nfaces in sorted(per_png.items()):
                if png not in images:
                    data, rgba = decode(jar, png)
                    images[png] = (blob(data), rgba)
                sha, rgba = images[png]
                evidence.append(dict(template=template, child=child, geometry_provider=provider,
                                     png=png, png_git_sha=sha, faces=nfaces,
                                     rgba_sha256=digest(rgba.tobytes()),
                                     child_git_sha=blob(child.read_bytes()),
                                     width=rgba.width, height=rgba.height))
        children = {item['child'] for item in evidence if item['template'] == template}
        status = ('E_EXCEPTION_NO_GENERAL_SURFACE' if row['E_exception'] == 'true'
                  else 'CHILD_SURFACES_VERIFIED' if children else 'NO_RESOLVED_CHILD_SURFACE')
        summary.append(dict(template=template, template_git_sha=row['model_sha'],
                            geometry_provider=provider or '', original_faces=row['face_count'],
                            descendants=len(candidates), same_geometry_descendants=len(eligible),
                            fully_bound_children=len(children), unique_child_png=len(counter), status=status))
        if images:
            example = list(sorted(images.items()))[:10]
            sections.append((basename(template) + f' ({len(images)} PNG)', [
                (str(i + 1), rgba.crop((0, 0, rgba.width, min(rgba.width, rgba.height))))
                for i, (_, (_, rgba)) in enumerate(example)], 1))
    write(output / 'F3_TEMPLATE_38_FOLLOWUP.csv', summary)
    write(output / 'F3_CHILD_PNG_EVIDENCE.csv', evidence)
    for start in range(0, len(sections), 12):
        make_sheet(preview / f'children_{start // 12:02d}.png', sections[start:start+12], 10, 68)
    return Counter(row['status'] for row in summary), len(evidence)


def audit_animation(jar, output, preview):
    baseline = [row for row in rows(DATA / 'F3_PNG_FIRST_FRAME_332.csv')
                if row['full_dimensions'] != row['first_frame_dimensions']]
    summaries, raw_frames, playback, sections = [], [], [], []
    for row in baseline:
        path = Path(row['original_PNG_path'])
        data, rgba = decode(jar, path)
        if blob(data) != row['original_PNG_git_sha'] or digest(rgba.tobytes()) != row['original_RGBA_SHA256']:
            raise ValueError(f'Original F3 PNG digest mismatch: {path}')
        raw_meta = matching(jar, Path(str(path) + '.mcmeta'))
        animation = json.loads(raw_meta)['animation']
        w, h = animation.get('width'), animation.get('height')
        if w is None and h is None:
            w = h = min(rgba.size)
        else:
            w, h = w or rgba.width, h or rgba.height
        cols, col_remainder = divmod(rgba.width, w)
        row_count, row_remainder = divmod(rgba.height, h)
        if col_remainder or row_remainder:
            raise ValueError(f'Inconsistent frame bounds: {path}')
        frames = [rgba.crop((x*w, y*h, (x+1)*w, (y+1)*h))
                  for y in range(row_count) for x in range(cols)]
        hashes = [digest(frame.tobytes()) for frame in frames]
        if hashes[0] != row['first_frame_RGBA_SHA256']:
            raise ValueError(f'Original F3 first-frame digest mismatch: {path}')
        for index, frame in enumerate(frames):
            alpha = frame.getchannel('A').histogram()
            raw_frames.append(dict(png=path, frame=index, x=index%cols*w, y=index//cols*h,
                                   width=w, height=h, rgba_sha256=hashes[index],
                                   visible=w*h-alpha[0], partial_alpha=sum(alpha[1:255])))
        base_ticks = animation.get('frametime', 1)
        declared = animation.get('frames', [])
        order = [(entry, base_ticks) if isinstance(entry, int)
                 else (entry['index'], entry.get('time', base_ticks))
                 for entry in declared] if declared else [(i, base_ticks) for i in range(len(frames))]
        tick = 0
        changes = []
        last = order[-1][0]
        for step, (index, duration) in enumerate(order):
            if not 0 <= index < len(frames) or duration < 1:
                raise ValueError(f'Invalid animation schedule: {path}')
            changed = sum(a != b for a, b in zip(frames[last].get_flattened_data(), frames[index].get_flattened_data()))
            playback.append(dict(png=path, step=step, source_frame=index, tick_start=tick,
                                 duration_ticks=duration, rgba_changed_pixels=changed))
            changes.append(changed)
            tick += duration
            last = index
        summaries.append(dict(png=path, png_git_sha=blob(data), mcmeta_git_sha=blob(raw_meta), raw_cells=len(frames),
                              unique_rgba=len(set(hashes)), playback_steps=len(order),
                              played_cells=len(set(i for i, _ in order)), first_played_cell=order[0][0],
                              cycle_ticks=tick, interpolate=animation.get('interpolate', False),
                              changed_pixels_min=min(changes), changed_pixels_max=max(changes)))
        sections.append((basename(path) + f' (cells={len(frames)})',
                         [(str(i), frame) for i, frame in enumerate(frames)], (len(frames)+15)//16))
    write(output / 'F3_ANIMATION_16.csv', summaries)
    write(output / 'F3_RAW_FRAMES.csv', raw_frames)
    write(output / 'F3_PLAYBACK_SCHEDULE.csv', playback)
    for start in range(0, len(sections), 4):
        make_sheet(preview / f'frames_{start//4:02d}.png', sections[start:start+4], 16, 53)
    return len(baseline), len(raw_frames), len(playback)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jar', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--preview', type=Path, required=True)
    args = parser.parse_args()
    with args.jar.open('rb') as file:
        if hashlib.file_digest(file, 'sha1').hexdigest() != JAR_SHA1:
            raise ValueError('Unexpected 1.21.11 client SHA-1')
    args.output.mkdir(parents=True, exist_ok=True)
    args.preview.mkdir(parents=True, exist_ok=True)
    with ZipFile(args.jar) as jar:
        templates, child_png_links = audit_templates(jar, args.output, args.preview)
        animations, frames, playback = audit_animation(jar, args.output, args.preview)
    result = dict(template_status=templates, child_png_links=child_png_links, animation_textures=animations,
                  source_frame_cells=frames, playback_steps=playback, client_jar_sha1=JAR_SHA1)
    (args.output / 'F3_FOLLOWUP_SUMMARY.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
