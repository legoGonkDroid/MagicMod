#!/usr/bin/env python3
"""Generate MagicMod's FTB Quests files.

    python3 MagicMod/questgen/build.py          # validate + write
    python3 MagicMod/questgen/build.py --check  # validate only

Writes minecraft/config/ftbquests/quests/{chapter_groups.snbt, chapters/*.snbt,
lang/en_us.snbt}. data.snbt (book-wide settings) is left alone once it exists.
Every chapter file in chapters/ that this script doesn't generate is deleted, so edit
quests here, not in the in-game editor.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import registry  # noqa: E402
import snbt  # noqa: E402
from model import layout, make_id, to_snbt_dicts  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), 'minecraft', 'config', 'ftbquests', 'quests')

GROUPS = [
    ('journey', 'The Journey'),
    ('codex', 'Codex & Collections'),
]

DATA_DEFAULT = {
    'default_autoclaim_rewards': 'disabled', 'default_consume_items': False,
    'default_quest_disable_jei': False, 'default_quest_shape': 'circle',
    'default_reward_team': False, 'detection_delay': 20, 'disable_gui': False,
    'drop_book_on_death': False, 'drop_loot_crates': False, 'emergency_items_cooldown': 300,
    'fallback_locale': 'en_us', 'grid_scale': snbt.Double(0.5), 'hide_excluded_quests': False,
    'lock_message': '', 'loot_crate_no_drop': {'boss': 0, 'monster': 600, 'passive': 4000},
    'pause_game': False, 'presets': {}, 'progression_mode': 'linear', 'show_lock_icons': False,
    'verify_on_load': False, 'version': 13,
}


def load_chapters(reg):
    mods = sorted(f[:-3] for f in os.listdir(os.path.join(HERE, 'content'))
                  if f.startswith('c') and f.endswith('.py'))
    chapters = []
    for i, name in enumerate(mods):
        ch = importlib.import_module(f'content.{name}').build(reg)
        ch.order = i
        chapters.append(ch)
    return chapters


def validate(chapters, reg):
    errors = []
    quests = {}
    for ch in chapters:
        if ch.group not in dict(GROUPS):
            errors.append(f'{ch.slug}: unknown group {ch.group!r}')
        if not reg.has('item', ch.icon):
            errors.append(f'{ch.slug}: unknown chapter icon {ch.icon}')
        for q in ch.quests:
            if q.path in quests:
                errors.append(f'{q.path}: duplicate quest slug')
            quests[q.path] = q
            if not q.tasks:
                errors.append(f'{q.path}: no tasks')
            if not q.rewards:
                errors.append(f'{q.path}: no rewards')
            if q.icon and not reg.has('item', q.icon):
                errors.append(f'{q.path}: unknown icon {q.icon}')
            for obj in q.tasks + q.rewards:
                for kind, rid in obj.refs:
                    if not reg.has(kind, rid):
                        errors.append(f'{q.path}: unknown {kind} {rid}')
    for q in quests.values():
        for p in q.dep_paths():
            if p not in quests:
                errors.append(f'{q.path}: missing dependency {p}')
    # cycles across the whole book
    state = {}

    def visit(p, stack):
        if state.get(p) == 2 or p not in quests:
            return
        if state.get(p) == 1:
            errors.append('dependency cycle: ' + ' -> '.join(stack + [p]))
            return
        state[p] = 1
        for d in quests[p].dep_paths():
            visit(d, stack + [p])
        state[p] = 2

    for p in quests:
        visit(p, [])
    return errors


def write(chapters):
    os.makedirs(os.path.join(OUT, 'chapters'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'lang'), exist_ok=True)
    data_path = os.path.join(OUT, 'data.snbt')
    if not os.path.exists(data_path):
        with open(data_path, 'w') as f:
            f.write(snbt.dumps(DATA_DEFAULT))

    lang = {}
    groups = []
    for slug, title in GROUPS:
        gid = make_id('group/' + slug)
        groups.append({'id': gid})
        lang[f'chapter_group.{gid}.title'] = title
    with open(os.path.join(OUT, 'chapter_groups.snbt'), 'w') as f:
        f.write(snbt.dumps({'chapter_groups': groups}))

    written = set()
    for ch in chapters:
        layout(ch)
        quests = []
        for q in ch.quests:
            d, ql = to_snbt_dicts(q)
            quests.append(d)
            lang.update(ql)
        lang[f'chapter.{ch.id}.title'] = ch.title
        if ch.subtitle:
            lang[f'chapter.{ch.id}.chapter_subtitle'] = [ch.subtitle]
        doc = {
            'default_hide_dependency_lines': False, 'default_quest_shape': '',
            'filename': ch.slug, 'group': make_id('group/' + ch.group),
            'icon': {'count': 1, 'id': ch.icon}, 'id': ch.id, 'images': [],
            'order_index': ch.order, 'quest_links': [], 'quests': quests,
        }
        fname = ch.slug + '.snbt'
        with open(os.path.join(OUT, 'chapters', fname), 'w') as f:
            f.write(snbt.dumps(doc))
        written.add(fname)

    for fname in os.listdir(os.path.join(OUT, 'chapters')):
        if fname.endswith('.snbt') and fname not in written:
            os.remove(os.path.join(OUT, 'chapters', fname))
            print(f'removed stale chapter file {fname}')

    with open(os.path.join(OUT, 'lang', 'en_us.snbt'), 'w') as f:
        f.write(snbt.dumps(lang))


def main():
    reg = registry.load()
    chapters = load_chapters(reg)
    errors = validate(chapters, reg)
    total = 0
    for ch in chapters:
        total += len(ch.quests)
        print(f'  [{ch.group}] {ch.title}: {len(ch.quests)} quests')
    print(f'  total: {total} quests in {len(chapters)} chapters')
    if errors:
        print(f'\n{len(errors)} error(s):')
        for e in errors:
            print('  ' + e)
        sys.exit(1)
    if '--check' not in sys.argv:
        write(chapters)
        print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
