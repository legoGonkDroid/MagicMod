"""Minimal SNBT writer matching the style FTB Quests 2101.x writes (tabs, no commas)."""
import re

_BARE_KEY = re.compile(r'^[A-Za-z0-9_.+-]+$')


class Long(int):
    """Written with an L suffix (e.g. kill task `value: 1L`)."""


class Double(float):
    """Written with a d suffix (e.g. `x: -4.0d`)."""


def _str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def _key(k):
    return k if _BARE_KEY.match(k) else _str(k)


def _val(v, indent):
    pad = '\t' * indent
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, Long):
        return f'{int(v)}L'
    if isinstance(v, Double):
        return f'{float(v)}d'
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f'{v}d'
    if isinstance(v, str):
        return _str(v)
    if isinstance(v, dict):
        if not v:
            return '{ }'
        inner = '\n'.join(f'{pad}\t{_key(k)}: {_val(v[k], indent + 1)}' for k in sorted(v))
        return '{\n' + inner + '\n' + pad + '}'
    if isinstance(v, (list, tuple)):
        if not v:
            return '[ ]'
        if all(isinstance(x, str) for x in v) and sum(len(x) for x in v) < 80:
            return '[' + ', '.join(_str(x) for x in v) + ']'
        inner = '\n'.join(f'{pad}\t{_val(x, indent + 1)}' for x in v)
        return '[\n' + inner + '\n' + pad + ']'
    raise TypeError(f'cannot write {type(v)}: {v!r}')


def dumps(obj):
    return _val(obj, 0) + '\n'
