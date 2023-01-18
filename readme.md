## MiniU3 Python port
[Видео](https://www.youtube.com/watch?v=O3rqMsH2ggE)
### Запуск примера
Для запуска примера необходимо собрать модуль ```pythree```, выполнив следующие команды:
```bash
$ cd pythree
$ python3 setup.py install 
```
Теперь, получившийся *.so/.pyd* в папке ```build``` нужно перенести в корневую папку с проектом.

**Уже собранные файлы вы также можете найти на диске: https://disk.yandex.ru/d/nDpPyelHyVfnOw**

Также необходимо установить следующие модули:
```bash
$ python3 -m pip install pyopengl
$ python3 -m pip install pyglm  # важно не спутать с просто glm
```

Для запуска игры нужно обязательно запустить сервер и клиент.
##### Сервер
Сервер запускается следующей командой:
```bash
$ python3 main.py --server <ваш ip>:27520
```

##### Клиент
Клиент запускается через пункт меню "Сетевая игра":
```bash
$ python3 main.py
```
Однако, можно сразу подключиться к серверу, минуя меню:
```bash
$ python3 main.py --client <ip сервера>:27520
```

*Note: свой IP можно узнать через команду ```ipconfig``` ( Windows ) или ```ifconfig``` ( \*NIX )*

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