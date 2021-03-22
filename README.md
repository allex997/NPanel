### NPanel 

Аддон добавляющий возможность прокрутки N-panel в Blender

![image](https://user-images.githubusercontent.com/31005234/112046126-aff12280-8b5c-11eb-80cf-f9f752fd7bf9.png)

Аддон работает только для **windows** системы😢

Для работы аддона необходимо установить **python 3.x.x** (желательно  3.7.7 (default, Jun 13 2020, 11:11:23))😒

Аддон использует uncompyle6 для декомпиляции pyc файлов. Если у вас есть установленный python, аддон сам попробуем выполнить команду 'pip3 install uncompyle6'.

1) Аддон пытаеться связать n-панель и установленные аддоны внутри blender

2) Аддон пытаеться связать n-панель и установленные аддоны проходя по путям аддонов и парсит их

### О том как он работает вкратце🤷‍♂️🤷‍♀️

1) Проверяет установлен ли uncompyle6 ()(install_uncompyle6()), если нет то попытаеться установить 

2) Проходиться по внутренним аддонам и ищет их в blender (get_name_panel())

3) Пробигаеться по файлам, а точнее по папкам в которых есть '__init__.py' (get_other_addons())

4) Перед декомпиляцией в папке blender создает файл uncompl.bat (являеться посредником чтобы у blender был доступ к файлам windows) (create_bat())

5) Проходиться по файлам если он не проходил по ним

6) Сохраняет результат в файл NPanel.data, который создаеться если его нет в папке blender (save())

7) Даёт доступ интерфейсу взаимодествовать с полученными данными, отключая и включая аддоны.


_**P.S. Может кто знает как улучшить ?**_🧙‍♀️🧙‍♂️🧐

### Установка
Если вы хотите просто установить его то вам нужно выбрать архив - NPanel.zip. Можно также скачать я яндекса https://disk.yandex.ru/d/G-XoQ-2I_jKmYg?w=1


Моя почта: alex997@list.ru
