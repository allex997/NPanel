import bpy
from .. import utils

def get_panels():
    prefs,name_prefs = utils.addon.prefs()
    names = utils.sidebar.tabs()

    
    if utils.hops.get_module():
        names.add(utils.hops.get_default())

    if utils.bc.get_module():
        names.add(utils.bc.get_default())

    for tab in prefs.tab_items[:]:
        
        if tab.name not in names:
            index = prefs.tab_items.find(tab.name)
            #print(f'index {index}, tab.name {tab.name}')
            prefs.tab_items.remove(index)

    for name in names:
        if name not in prefs.tab_items:
            tab = prefs.tab_items.add()
            tab.name = name

            if name == utils.hops.get_default():
                tab.rename = utils.hops.get_tab()

            elif name == utils.bc.get_default():
                tab.rename = utils.bc.get_tab()

            else:
                tab.rename = name
    return [n.name for n in prefs.tab_items[:]]
