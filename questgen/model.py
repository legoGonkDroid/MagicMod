"""Quest data model. Chapter files in content/ build Chapters with these helpers.

IDs are deterministic hashes of slugs, so regenerating never resets progress as long as
chapter/quest slugs don't change. Task/reward IDs hash the quest path + their own key
(default: their position), so reordering tasks inside a quest resets just those tasks.
"""
import hashlib

from snbt import Double, Long


def make_id(path):
    h = hashlib.sha1(('magicmod:' + path).encode()).hexdigest()[:16].upper()
    return '%X' % (int(h[0], 16) & 0x7) + h[1:]  # keep it a positive signed long


# ---------------------------------------------------------------- tasks
class Task:
    def __init__(self, type_, refs, title=None, key=None, **fields):
        self.type = type_
        self.refs = refs  # [(kind, id)] to validate
        self.title = title
        self.key = key
        self.fields = fields


def item(rid, count=1, title=None, consume=False, key=None):
    f = {'item': {'count': count, 'id': rid}}
    if consume:
        f['consume_items'] = True
    return Task('item', [('item', rid)], title, key, **f)


def kill(entity, count=1, title=None, key=None):
    return Task('kill', [('entity', entity)], title, key, entity=entity, value=Long(count))


def observe(entity, title=None, key=None, ticks=0):
    return Task('observation', [('entity', entity)], title, key,
                observation_type='entity_type', observe_type=5,  # ENTITY_TYPE ordinal (read wins)
                timer=Long(ticks), to_observe=entity)


def structure(rid, title=None, key=None):
    return Task('structure', [('structure', rid)], title, key, structure=rid)


def biome(rid, title=None, key=None):
    return Task('biome', [('biome', rid)], title, key, biome=rid)


def dimension(rid, title=None, key=None):
    return Task('dimension', [('dimension', rid)], title, key, dimension=rid)


def adv(rid, title=None, key=None):
    return Task('advancement', [('advancement', rid)], title, key, advancement=rid, criterion='')


def check(title=None, key=None):
    return Task('checkmark', [], title, key)


# ---------------------------------------------------------------- rewards
class Reward:
    def __init__(self, type_, refs, title=None, key=None, **fields):
        self.type = type_
        self.refs = refs
        self.title = title
        self.key = key
        self.fields = fields


def give(rid, count=1, key=None, components=None):
    it = {'count': count, 'id': rid}
    if components:
        it['components'] = components
    return Reward('item', [('item', rid)], None, key, item=it)


def potion(effect, count=1, kind='minecraft:potion', key=None):
    """A potion reward, e.g. potion('long_fire_resistance', 2)."""
    return give(kind, count, key, {'minecraft:potion_contents': {'potion': 'minecraft:' + effect}})


def xp(amount, key=None):
    return Reward('xp', [], None, key, xp=amount)


def levels(amount, key=None):
    return Reward('xp_levels', [], None, key, xp_levels=amount)


# ---------------------------------------------------------------- quests / chapters
class Quest:
    def __init__(self, chapter, slug, title, tasks, rewards, desc=(), subtitle=None, icon=None,
                 deps=(), x=None, y=None, shape=None, size=None, optional=False, min_deps=None):
        self.chapter = chapter
        self.slug = slug
        self.title = title
        self.tasks = list(tasks)
        self.rewards = list(rewards)
        self.desc = list(desc)
        self.subtitle = subtitle
        self.icon = icon
        self.deps = list(deps)  # 'slug' (same chapter) or 'chapter/slug'
        self.x, self.y = x, y
        self.shape = shape
        self.size = size
        self.optional = optional
        self.min_deps = min_deps

    @property
    def path(self):
        return f'{self.chapter.slug}/{self.slug}'

    @property
    def id(self):
        return make_id('quest/' + self.path)

    def dep_paths(self):
        return [d if '/' in d else f'{self.chapter.slug}/{d}' for d in self.deps]


class Chapter:
    def __init__(self, slug, title, group, icon, subtitle=None, order=0):
        self.slug = slug
        self.title = title
        self.group = group
        self.icon = icon
        self.subtitle = subtitle
        self.order = order
        self.quests = []

    @property
    def id(self):
        return make_id('chapter/' + self.slug)

    def quest(self, slug, title, tasks, rewards, **kw):
        q = Quest(self, slug, title, tasks, rewards, **kw)
        self.quests.append(q)
        return q


def grid(quests, cols, x0=0.0, y0=0.0, dx=1.5, dy=1.5):
    """Place quests row by row in a grid of `cols` columns starting at (x0, y0)."""
    for i, q in enumerate(quests):
        q.x = x0 + (i % cols) * dx
        q.y = y0 + (i // cols) * dy
    return quests


def layout(chapter, spacing_x=2.0, spacing_y=1.5):
    """Give quests without explicit x/y a position: columns by dependency depth (within
    the chapter), rows in declaration order, each column centred on y=0. Explicit
    positions are kept."""
    by_path = {q.path: q for q in chapter.quests}
    depth = {}

    def d(q, stack=()):
        if q.path in depth:
            return depth[q.path]
        if q.path in stack:
            raise ValueError(f'dependency cycle at {q.path}')
        local = [by_path[p] for p in q.dep_paths() if p in by_path]
        depth[q.path] = 0 if not local else 1 + max(d(x, stack + (q.path,)) for x in local)
        return depth[q.path]

    auto = [q for q in chapter.quests if q.x is None or q.y is None]
    count = {}
    for q in auto:
        count[d(q)] = count.get(d(q), 0) + 1
    rows = {}
    for q in auto:
        col = d(q)
        row = rows.get(col, 0)
        rows[col] = row + 1
        if q.x is None:
            q.x = col * spacing_x
        if q.y is None:
            q.y = (row - (count[col] - 1) / 2) * spacing_y
    return chapter


def to_snbt_dicts(q):
    """(quest dict, lang entries) for one quest."""
    lang = {f'quest.{q.id}.title': q.title}
    if q.subtitle:
        lang[f'quest.{q.id}.quest_subtitle'] = q.subtitle
    if q.desc:
        lang[f'quest.{q.id}.quest_desc'] = q.desc
    tasks = []
    for i, t in enumerate(q.tasks):
        tid = make_id(f'task/{q.path}/{t.key or i}')
        tasks.append({'id': tid, 'type': t.type, **t.fields})
        if t.title:
            lang[f'task.{tid}.title'] = t.title
    rewards = []
    for i, r in enumerate(q.rewards):
        rid = make_id(f'reward/{q.path}/{r.key or i}')
        rewards.append({'id': rid, 'type': r.type, **r.fields})
    d = {'id': q.id, 'tasks': tasks, 'x': Double(q.x), 'y': Double(q.y)}
    if rewards:
        d['rewards'] = rewards
    if q.deps:
        d['dependencies'] = [make_id('quest/' + p) for p in q.dep_paths()]
    if q.min_deps:
        d['min_required_dependencies'] = q.min_deps
    if q.icon:
        d['icon'] = {'count': 1, 'id': q.icon}
    if q.shape:
        d['shape'] = q.shape
    if q.size:
        d['size'] = Double(q.size)
    if q.optional:
        d['optional'] = True
    return d, lang
