# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    'name': 'Npanel',
    'author': 'alex997',
    'description': 'Organize the Blender sidebar',
    'blender': (2, 80, 0),
    'version': (1, 0, 0),
    'location': 'View3D',
    'wiki_url': '',
    'category': '3D View'
}

from . import addon
import bpy
import addon_utils
import os
import re
import sys,os
import pickle
import subprocess

class item_panel():
    def __init__(self,bl_name='',owner_id='',bl_category=[]):
        self.bl_name = bl_name
        self.owner_id = owner_id
        self.bl_category = bl_category
        
    def print_all(self):
        print(f'self.bl_name {self.bl_name} self.owner_id {self.owner_id} self.bl_category {self.bl_category}')
        
class Data():
    nTab = [] # Полученные вкладки
    Npanels = [] # данные([item_panel]) полученные из файлов 
    true_nTab = [] # включенные вкладки
    false_nTab = [] # выключенные вкладки
    adons = []
    
def save(ob):
        #pickle.damp(self, open('NPanel.data', 'wb')) #pkl
    with open('NPanel.data', 'wb') as fp:
        pickle.dump(ob, fp)
        
def load():
    with open('NPanel.data', 'rb') as fp:
        return pickle.load(fp)

# для чтения pyc файлов
def install_uncompyle6():
    cm = subprocess.call('uncompyle6 --help', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)#os.system('uncompyle6 --help')
    if cm:
        cm2 = subprocess.call('pip3 install uncompyle6', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)#os.system('pip3 install uncompyle6')
    #if cm2:
    #bpy.app.version_string

def get_name_cls(cls):
    try:
        name = cls.__dict__['__dict__'].__qualname__ #'TEXTFX_MT_ADDFONT.__dict__'
        return re.findall('(.*)(?=.__dict__)', name)[0] #'TEXTFX_MT_ADDFONT'
    except:
        return -1
    
def get_owner_id(bcpak):
    path = sys.modules[bcpak].__file__ #sys.modules[bpy.context.preferences.addons.keys()[0]].__file__ 'C:\\Users\\vv\\AppData\\Roaming\\Blender Foundation\\Blender\\2.90\\scripts\\addons\\TextFX.py'
    if os.path.basename(path) == '__init__.py':
        dir = os.path.dirname(path)
        _,name = os.path.split(dir)
        return name
    else:
        return '.'.join(os.path.basename(path).split('.')[:-1])

Npanels = []
def panel_item_exists(item_p):
    bl_category,owner_id,bl_name = item_p.bl_category,item_p.owner_id,item_p.bl_name
    for ipan in Npanels:
        if bl_category == ipan.bl_category or owner_id == item_p.owner_id or bl_name == item_p.bl_name:
            return False
    return True

# только textfx пытаеться получить сведения из blender
def get_name_panel():
    global Npanels
    st = []
    for p in dir(bpy.types):
        cls = getattr(bpy.types, p)
        if (issubclass(cls, bpy.types.Panel)
        and getattr(cls, "bl_space_type", "") == 'VIEW_3D'):
            if getattr(cls, "bl_category", "No Category") != "No Category" and getattr(cls, "bl_category", "No Category") != '':
                #if get_name_cls(cls) in dir(sys.modules[bpy.context.preferences.addons.keys()[0]]):
                # bl_category- getattr(cls, "bl_category", "No Category")
                # bl_name sys.modules[bpy.context.preferences.addons.keys()[0]].bl_info['name']
                # owner_id get_owner_id()
                for bcpak in bpy.context.preferences.addons.keys():
                    try:
                        if get_name_cls(cls) !=-1 and get_name_cls(cls)!=None:
                            #print(get_name_cls(cls))
                            if get_name_cls(cls) in dir(sys.modules[bcpak]): #bug
                                item_p = item_panel(bl_category=[getattr(cls, "bl_category", "No Category")],bl_name = sys.modules[bcpak].bl_info['name'], owner_id = get_owner_id(bcpak))
                                if panel_item_exists(item_p):
                                    Npanels.append(item_p)# если не существует
                    except:
                        pass                        
                
                #print(cls) #tf = sys.modules].TEXTFX_PT_UI
                #print(getattr(cls, "bl_category", "No Category"))
                st.append(getattr(cls, "bl_category", "No Category"))
                
    st = set(st)
    return st



#Npanels[0].print_all()
#print(len(Npanels))
#print(bpy.context.preferences.addons.keys())

# получаем данные из файлов
def get_other_addons():
    all_paths = []
    
    #print('get_other_addons()')
    context = bpy.context
    # get all paths
    for mod_name in context.preferences.addons.keys():
        try:
            all_path = {}
            all_path['type'] = 'None'
            all_path['path'] = 'None'
            mod = sys.modules[mod_name]
            if os.path.basename(mod.__file__) == '__init__.py':
                all_path['type'] = 'in_folder'
            else:
                all_path['type'] = 'out_folder'
            all_path['path'] = mod.__file__
            all_paths.append(all_path)
        #print(all_path['path']) # тут норм
        except:
            pass

            
    def get_bl_category_and_bl_name(path,owner_id):
        
        py,pyc = [],[]
        def decomp_file(paths):#paths - pyc
            new_py_windows,new_py = [],[]
            
            for path in paths:
                npath = os.path.dirname(path)
                new_path = path.replace('.pyc','.py')
                old_path = '\\'.join(path.split('\\'))
                new_path_windows = old_path.replace('.pyc','.py')
                name = os.path.basename(old_path).replace(".pyc",".py")
                
                command12 = str(f'uncompl.bat "{old_path}" %USERPROFILE%\\{name} "{new_path}"')
                command2 = str(f'uncompl.bat "{old_path}" "{new_path}"')

                
                err = os.system(command2)
                
                #raise 'Проверка'
                
                if err==0:
                    new_py_windows.append(new_path_windows)
                    new_py.append(new_path)
                
            return new_py_windows,new_py
        
        
        
        def delete_all_py(new_py):
            for p in new_py:
                try:
                    if os.path.isfile(p):
                        os.remove(p)#//
                    os.remove('uncompl.bat')
                except:
                    pass
            
        def read_py_file(py,new_py,owner_id):
            global Npanels
            files = py+new_py
            bl_categorys = []
            bl_name = None
            for path in files:
                with open(path) as f:#error
                    content = f.readlines()
                content = [x.strip() for x in content]
                content= ' '.join(content)
                bli = re.findall(r".*bl_info.*(?<={).*name.*?'.*?:.*?'.*?(.+?)'.*(?=})",content)#group1
                blc = re.findall(r"bl_category.+?'(.+?)(?=')",content)#group1
                if bl_name == None and len(bli)>0:
                    bl_name = bli[0]
                if len(blc)>0:
                    for name in blc:
                        if not (name in bl_categorys):
                            bl_categorys.append(name)
            #return bl_name, bl_categorys
            
            if owner_id != None:
                if not (owner_id in [x.owner_id for x in Npanels]):
                    item_p = item_panel(bl_name = bl_name, owner_id = owner_id)
                    Npanels.append(item_p)
            
            # edit categoty
            for np in Npanels:
                if owner_id == np.owner_id:
                    for cat in bl_categorys:
                        if not (cat in np.bl_category):
                            np.bl_category.append(cat)
            
        #:~,-3%
        def create_bat():
            if os.path.isfile('uncompl.bat')==False:
                code = [
                'set path1=%1\n'
                ,'uncompyle6 %1 >> %2'
                ]
                fp = open('uncompl.bat', 'w')
                fp.writelines(code)
                fp.close()
                
        #add all paths
        for directory, dirnames, filenames in os.walk(path):
            for file in filenames:
                if 'pyc' in file:
                    pyc.append(os.path.join(directory, file))
                elif 'py' in file:
                    py.append(os.path.join(directory, file))
        
        
        create_bat()
        new_py_win,new_py = decomp_file(pyc)
        #print(new_py)
        read_py_file(py,new_py,owner_id)
        
        delete_all_py(new_py)
        
    
          
    for path in all_paths: # путь на который указывает плагин
        #print(f'Путь аддона которого проверяем - {path}')
        dir = os.path.dirname(path['path']) 
        if path['type'] == 'in_folder':
            _,owner_id = os.path.split(dir)
            # NPanel ?
        #elif path['type'] == 'out_folder':
            #owner_id = os.path.basename(path['path']).split('.')[:-1]
            if not owner_id in [np.owner_id for np in Npanels] and not owner_id=='NPanel':
                #print(f'owner_id {owner_id}')
                get_bl_category_and_bl_name(dir,owner_id)
    #os.system('cls')

def main_npanel(nTab,Npan = []):

    # проверяем добавились ли Npanel
    def check_nTab(nTab,nTab2):
        '''for nt in nTab:
            if not nt in nTab2:
                return True
        for nt2 in nTab2:
            if not nt2 in nTab:
                return True'''
        if nTab != nTab2:
            return True
        return False
                

    global Npanels
    if len(Npan)!=0:
        Npanels=Npan
    nTab2 = []
    if os.path.exists('NPanel.data'):# если файл есть загрузить
        dat = load()
        Npanels = dat.Npanels
        nTab2 = dat.nTab
    else:
        dat = Data()
    
    
        
    install_uncompyle6()

    #if len(nTab)< len(nTab2): # если появился новый или уменьшилось количество, проверяем все ли остались и добавляем новые

    
    if check_nTab(nTab,nTab2): # если вкладки изменились значит пора искать
        get_name_panel()
        #print('get_name_panel()')
        get_other_addons()
        dat.Npanels = Npanels
        dat.nTab = nTab
    #print(f'dat.Npanels {Npanels} nTab {nTab}')
    dat.adons = [np for np in Npanels for bl in np.bl_category if bl in nTab]
    #print(f'dat.adons {dat.adons}')
    #print([x.owner_id for x in dat.Npanels]) # тут все правильно
    #enable and desable tab
    
    #dat.true_nTab = true_nTab
    #dat.false_nTab = false_nTab
    

    return dat#.Npanels


class DOWN_Npanel(bpy.types.Operator):
    bl_idname = 'panel.down_npanel'#'mesh.NPanel_id' #'mesh.add_cube_sample'
    bl_label = 'NPanel_DOWN'
    #bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        global Npanels

        dat = load()
        dat.true_nTab = dat.adons[:context.scene.count_npanel]
        dat.false_nTab = [np for np in Npanels if not np in dat.true_nTab]
        
        dat.false_nTab.insert(0,dat.true_nTab.pop())
        dat.true_nTab.insert(0,dat.false_nTab.pop())
        [addon_utils.disable(mod.owner_id) for mod in dat.false_nTab]
        [addon_utils.enable(mod.owner_id) for mod in dat.true_nTab]
        #os.system('cls')
        #print('two')
        #print([x.owner_id for x in Npanels])
        return {"FINISHED"}

class UP_Npanel(bpy.types.Operator):
    bl_idname = 'panel.up_npanel'#'mesh.NPanel_id' #'mesh.add_cube_sample'
    bl_label = 'NPanel_UP'
    #bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        global Npanels

        dat = load()
        dat.true_nTab = dat.adons[:context.scene.count_npanel]
        dat.false_nTab = [np for np in Npanels if not np in dat.true_nTab]

        dat.false_nTab.append(dat.true_nTab.pop(0))
        dat.true_nTab.append(dat.false_nTab.pop(0))
        addon_utils.disable(dat.true_nTab[0].owner_id)
        addon_utils.enable(dat.false_nTab[0].owner_id)
        #os.system('cls')
        #print('two')
        #print([x.owner_id for x in Npanels])
        return {"FINISHED"}

class refresh_Npanel(bpy.types.Operator):
    bl_idname = 'panel.refresh_npanel'#'mesh.NPanel_id' #'mesh.add_cube_sample'
    bl_label = 'NPanel_refresh'
    #bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        global Npanels
        #bpy.ops.npanel.refresh()
        nTab = addon.ops.refresh.get_panels()
        dat = main_npanel(nTab,Npanels)
        Npanels = dat.Npanels

        dat.true_nTab = dat.adons[:context.scene.count_npanel]
        dat.false_nTab = [np for np in Npanels if not np in dat.true_nTab]
        save(dat)
        [addon_utils.disable(mod.owner_id) for mod in dat.false_nTab]
    
        [addon_utils.enable(mod.owner_id) for mod in dat.true_nTab]
        
        #os.system('cls')
        #print('two')
        #print([x.owner_id for x in Npanels])
        return {"FINISHED"}

class panel3(bpy.types.Panel):
    bl_idname = "panel.npanel"
    bl_label = "SCROLLBAR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "scroll"
    #bl_options = {"REGISTER", "UNDO"}
    
    #total = bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)
 
    def draw(self, context):
        self.layout.operator("panel.up_npanel", icon='TRIA_UP', text="UP")
        self.layout.operator("panel.down_npanel", icon='TRIA_DOWN', text="DOWN")
        ob = context.scene
        
        spl =self.layout.column().split(factor=0.9,align =True)
        spl.prop(ob, 'count_npanel',expand=True)
        spl.operator("panel.refresh_npanel", icon='FILE_REFRESH', text="refresh")
        


def register():
    #bpy.ops.wm.addon_enable(module='blenderkit')
    global Npanels
    addon.register()
    bpy.utils.register_class(UP_Npanel)
    bpy.utils.register_class(DOWN_Npanel)
    bpy.utils.register_class(refresh_Npanel)
    bpy.utils.register_class(panel3)
    
    
    #os.system('cls')
    #print(addon.ops.refresh.get_panels())

    nTab = addon.ops.refresh.get_panels()
    
    dat= main_npanel(nTab)
    Npanels = dat.Npanels
    #dat.adons = [np for np in Npanels if np.bl_category in nTab]
    #print([x.owner_id for x in Npanels])
    #bpy.ops.npanel.refresh()
    #addon.ops.refresh.Refresh()
    #npanel.refresh()
    bpy.types.Scene.count_npanel = bpy.props.IntProperty(name="count npanel", default=int(len(dat.adons)/2), soft_min= 1,soft_max = len(dat.adons),subtype = 'FACTOR',max =len(dat.adons),min=1)#int(len(bpy.types.Scene.npanel)/2) len(bpy.types.Scene.npanel)
    

    dat.true_nTab = dat.adons[:int(len(dat.adons)/2) if len(dat.true_nTab)==0 else len(dat.true_nTab)]# сохраняем данные какие включим
    
    dat.false_nTab = [np for np in Npanels if not np in dat.true_nTab]# сохраняем данные какие выключим
    #print(dat.false_nTab)
    save(dat)
    [addon_utils.disable(mod.owner_id,default_set=False, handle_error=None) for mod in dat.false_nTab] # выключаем определенное количество(len(dat.adons)/2 либо len(dat.true_nTab)) вкладок
    
    [addon_utils.enable(mod.owner_id,default_set=False, persistent=False, handle_error=None) for mod in dat.true_nTab]# включаем оставшиеся вкладки
    



def unregister():
    addon.unregister()
    bpy.utils.unregister_class(UP_Npanel)
    bpy.utils.unregister_class(DOWN_Npanel)
    bpy.utils.unregister_class(refresh_Npanel)
    bpy.utils.unregister_class(panel3)
    del bpy.types.Scene.count_npanel

if __name__ == "__main__" :
    register()