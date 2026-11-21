"""Collect the IDs that actually exist in this modpack, by scanning the mod jars and the
vanilla client jar. Used to reject typos / removed mods at build time.

Cached in questgen/.cache/registry.json; the cache is rebuilt whenever the set of jars
(name + size + mtime) changes.
"""
import io
import json
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
INSTANCE = os.path.dirname(HERE)
MODS = os.path.join(INSTANCE, 'minecraft', 'mods')
VANILLA = os.path.expanduser(
    '~/.local/share/PrismLauncher/libraries/net/minecraft/client/1.21.1-20240808.144430/'
    'client-1.21.1-20240808.144430-extra.jar')
CACHE = os.path.join(HERE, '.cache', 'registry.json')

KINDS = ('item', 'entity', 'structure', 'biome', 'advancement', 'dimension')

_PATTERNS = [
    ('item', re.compile(r'^assets/([^/]+)/models/item/(.+)\.json$')),
    ('structure', re.compile(r'^data/([^/]+)/worldgen/structure/(.+)\.json$')),
    ('biome', re.compile(r'^data/([^/]+)/worldgen/biome/(.+)\.json$')),
    ('advancement', re.compile(r'^data/([^/]+)/advancement/(.+)\.json$')),
    ('dimension', re.compile(r'^data/([^/]+)/dimension/(.+)\.json$')),
]
_LANG = re.compile(r'^assets/([^/]+)/lang/en_us\.json$')
_LANG_KEY = re.compile(r'^(item|block|entity|biome)\.([a-z0-9_-]+)\.([a-z0-9_/-]+)$')  # no '.' in path: skips .desc/.tooltip keys


def _scan_zip(zf, out, names):
    for n in zf.namelist():
        for kind, pat in _PATTERNS:
            m = pat.match(n)
            if m:
                out[kind].add(f'{m.group(1)}:{m.group(2)}')
        m = _LANG.match(n)
        if m:
            try:
                data = json.loads(zf.read(n).decode('utf-8', 'ignore'))
            except ValueError:
                continue
            for k, v in data.items():
                lm = _LANG_KEY.match(k)
                if not lm:
                    continue
                kind, ns, path = lm.groups()
                rid = f'{ns}:{path}'
                if kind in ('item', 'block'):
                    names.setdefault(rid, v)
                    out['item'].add(rid)  # most blocks have block items; models cover the rest
                elif kind == 'entity':
                    out['entity'].add(rid)
                    names.setdefault('entity:' + rid, v)
                elif kind == 'biome':
                    names.setdefault('biome:' + rid, v)
        if n.startswith('META-INF/jarjar/') and n.endswith('.jar') or n.startswith('META-INF/jars/') and n.endswith('.jar'):
            try:
                _scan_zip(zipfile.ZipFile(io.BytesIO(zf.read(n))), out, names)
            except zipfile.BadZipFile:
                pass


def _fingerprint(jars):
    return [[os.path.basename(j), os.path.getsize(j), int(os.path.getmtime(j))] for j in jars]


def load():
    jars = sorted(os.path.join(MODS, f) for f in os.listdir(MODS) if f.endswith('.jar'))
    if os.path.exists(VANILLA):
        jars.append(VANILLA)
    fp = _fingerprint(jars)
    if os.path.exists(CACHE):
        with open(CACHE) as f:
            cached = json.load(f)
        if cached.get('fingerprint') == fp:
            return Registry({k: set(v) for k, v in cached['ids'].items()}, cached['names'])
    out = {k: set() for k in KINDS}
    names = {}
    for j in jars:
        try:
            _scan_zip(zipfile.ZipFile(j), out, names)
        except zipfile.BadZipFile:
            print(f'warning: unreadable jar {j}')
    out['dimension'] |= {'minecraft:overworld', 'minecraft:the_nether', 'minecraft:the_end'}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, 'w') as f:
        json.dump({'fingerprint': fp, 'ids': {k: sorted(v) for k, v in out.items()}, 'names': names}, f)
    return Registry(out, names)


class Registry:
    def __init__(self, ids, names):
        self.ids = ids
        self.names = names

    def has(self, kind, rid):
        if rid.startswith('#'):  # tags aren't validated
            return True
        return rid in self.ids[kind]

    def name(self, rid, kind='item'):
        key = rid if kind == 'item' else f'{kind}:{rid}'
        return self.names.get(key)

    def find(self, kind, pattern):
        """Sorted IDs of `kind` whose full id matches the regex `pattern`."""
        rx = re.compile(pattern)
        return sorted(i for i in self.ids[kind] if rx.search(i))
