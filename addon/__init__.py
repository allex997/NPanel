from . import utils
from . import ops
from . import props


modules = (
    utils,
    props,
    ops,
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
