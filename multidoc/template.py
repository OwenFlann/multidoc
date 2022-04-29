import os
from jinja2 import Template
import jinja2
from multidoc.utils import indent_line
from multidoc import logger
import re
import logging

log = logging.getLogger('root')
log.setLevel('DEBUG')
log.addHandler(logger.MyHandler())

__languages__ = [
    'cpp',
    'py']

# constants ------------------------------------------------------------------#
# template dir for default templates
# if source
candidate_template_dirs = [
    os.path.join(os.path.dirname(__file__), 'templates'),  # source
    os.path.join(os.path.dirname(__file__), '../../../../share/templates'),
    # unix
    os.path.join(os.path.dirname(__file__), '../../../../../share/templates'),
    # win
]

candidate_variable_dirs = [
    ('CONDA_PREFIX', 'share/templates'),  # shouldn't be needed with the
    #  above, just in case. (wont work
    #  without executing with conda env
    #  activated
    ('MULTIDOC_TEMPLATE_DIR', ''),  # if a dev wants to set a custom set
    #  of templates  (e.g. for testing)
]

for var, dir in candidate_variable_dirs:
    if var in os.environ:
        candidate_template_dirs.insert(0, os.path.join(os.environ[var], dir))

for template_dir in candidate_template_dirs:
    if os.path.isdir(template_dir):
        TEMPLATE_DIR = template_dir
        log.info('Using template dir: {}'.format(TEMPLATE_DIR))
        break
else:
    raise RuntimeError('No template directory found')

# TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

# template mapping for language docstring templates
TEMPLATE_LANGUAGE_MAP = {"cpp": os.path.join(TEMPLATE_DIR, "cpp.jinja2"),
                         "py": os.path.join(TEMPLATE_DIR, "numpydoc.jinja2")}

TEMPLATE_PROPERTY = os.path.join(TEMPLATE_DIR, "property.jinja2")
TEMPLATE_ENUM_MEMBER = os.path.join(TEMPLATE_DIR, "enum-member.jinja2")

# template mapping for generated compiled docstrings
TEMPLATE_DOCSTRING_HEADER = os.path.join(TEMPLATE_DIR, "docstring_h.jinja2")

# base globals required for template functions
_BASE_GLOBALS = {"indent_line": indent_line}

LINKFY_PATTERN = re.compile(r"([\w.]+)")


# functions ------------------------------------------------------------------#


def linkify_type(type_str):
    # You can manually specify the number of replacements by changing the 4th argument
    # result = re.sub(regex, subst, type_str, 0, re.MULTILINE)
    matches = set(list(re.findall(LINKFY_PATTERN, type_str)))
    print(matches)
    for match in matches:
        print('---', type_str)
        type_str = type_str.replace(match, f':class:`{match}`')
    type_str = type_str.replace('[', '\[')
    type_str = type_str.replace(']', '\]')
    return type_str


def get_enum_member_template(**kwargs):
    """

    Parameters
    ----------
    kwargs : dict[str, Any]
        One of the supported :ref:`multidoc.template.__languages__` must be set
        to true in the **kwargs in order to facilitate successful docstring
        deduction.

    Returns
    -------

    """
    _globals = kwargs.pop("globals", {})
    _globals.update(_BASE_GLOBALS)
    _lstrip_blocks = kwargs.pop("lstrip_blocks", True)
    _trim_blocks = kwargs.pop("trim_blocks", True)

    # iterate through supported languages, set as False if not in kwargs.
    # highly unnecessary here?
    _locals = {}
    for j in __languages__:
        _locals[j] = kwargs.pop(j, False)

    # which language is True
    aux = list(map(lambda x: x is True, [_locals[i] for i in __languages__]))

    # ensure only one language detected (e.g. cpp / py)
    assert aux.count(True) == 1

    # finally deduce lang.
    # TODO: There must be a more straightforward way.
    lang = __languages__[aux.index(True)]

    # open language template and return.
    with open(TEMPLATE_ENUM_MEMBER) as f:
        t = Template(
            f.read(),
            lstrip_blocks=_lstrip_blocks,
            trim_blocks=_trim_blocks)

        # update globals dict if globals given through kwargs
        t.globals.update(_globals)
        # if _globals else None (currently redundant)

        return t


def get_property_template(**kwargs):
    """

    Parameters
    ----------
    kwargs : dict[str, Any]
        One of the supported :ref:`multidoc.template.__languages__` must be set
        to true in the **kwargs in order to facilitate successful docstring
        deduction.

    Returns
    -------

    """
    _globals = kwargs.pop("globals", {})
    _globals.update(_BASE_GLOBALS)
    _globals["linkify_type"] = linkify_type
    _lstrip_blocks = kwargs.pop("lstrip_blocks", True)
    _trim_blocks = kwargs.pop("trim_blocks", True)

    # iterate through supported languages, set as False if not in kwargs.
    # highly unnecessary here?
    _locals = {}
    for j in __languages__:
        _locals[j] = kwargs.pop(j, False)

    # which language is True
    aux = list(map(lambda x: x is True, [_locals[i] for i in __languages__]))

    # ensure only one language detected (e.g. cpp / py)
    assert aux.count(True) == 1

    # finally deduce lang.
    # TODO: There must be a more straightforward way.
    lang = __languages__[aux.index(True)]

    # open language template and return.
    with open(TEMPLATE_PROPERTY) as f:
        t = Template(
            f.read(),
            lstrip_blocks=_lstrip_blocks,
            trim_blocks=_trim_blocks)

        # update globals dict if globals given through kwargs
        t.globals.update(_globals)
        # if _globals else None (currently redundant)

        return t


def get_docstring_template(**kwargs):
    """

    Parameters
    ----------
    kwargs : dict[str, Any]
        One of the supported :ref:`multidoc.template.__languages__` must be set
        to true in the **kwargs in order to facilitate successful docstring
        deduction.

    Returns
    -------

    """
    _globals = kwargs.pop("globals", {})
    _globals.update(_BASE_GLOBALS)
    _lstrip_blocks = kwargs.pop("lstrip_blocks", True)
    _trim_blocks = kwargs.pop("trim_blocks", True)

    # iterate through supported languages, set as False if not in kwargs.
    # highly unnecessary here?
    _locals = {}
    for j in __languages__:
        _locals[j] = kwargs.pop(j, False)

    # which language is True
    aux = list(map(lambda x: x is True, [_locals[i] for i in __languages__]))

    # ensure only one language detected (e.g. cpp / py)
    assert aux.count(True) == 1

    # finally deduce lang.
    # TODO: There must be a more straightforward way.
    lang = __languages__[aux.index(True)]

    # open language template and return.
    with open(TEMPLATE_LANGUAGE_MAP[lang]) as f:
        t = Template(
            f.read(),
            lstrip_blocks=_lstrip_blocks,
            trim_blocks=_trim_blocks)

        # update globals dict if globals given through kwargs
        t.globals.update(_globals)
        # if _globals else None (currently redundant)

        return t


# render the templates to source code
def render_cpp_docstring(args):
    t = get_docstring_template(cpp=True, py=False)
    return t.render(**args.dict())


def render_python_docstring(args):
    t = get_docstring_template(py=True, cpp=False)
    return t.render(**args.dict())


if __name__ == "__main__":
    t1 = get_docstring_template(cpp=True)
    t2 = get_docstring_template(py=True)
    try:
        t3 = get_docstring_template(py=True, cpp=True)
    except AssertionError as e:
        print("success")
