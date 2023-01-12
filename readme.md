## MiniU3 Python port
### Запуск примера
Для запуска примера необходимо собрать модуль ```pythree```, выполнив следующие команды:
```bash
$ cd pythree
$ python3 setup.py install 
```
Теперь, получившийся *.so/.pyd* нужно перенести в папку с проектом.
Также необходимо установить следующие модули:
```bash
$ python3 -m pip install pyopengl
$ python3 -m pip install pyglm  # важно не спутать с просто glm
```
Запустить ```python3 main.py``` и управлять "кораблём" с помощью клавиш WASD
### Troubleshooting
Может возникать следующая проблема:
```
AttributeError: module 'glm' has no attribute 'perspective'
```
Она может возникать, когда оба модуля ```glm``` и ```pyglm``` установленны.
Для исправления нужно удалить модуль ```glm```:
```bash
$ python3 -m pip uninstall glm
```