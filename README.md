## <a id="title1">Часть 1. Стек технологий</a>

**Используемый стек технологий:**
* FastAPI
* Telegram Bot API
* Docker (в будущем)

В качестве модели для классификации объектов на фото используется **YOLOv8n**. Скачать используемую модель можно <a href="https://drive.google.com/uc?export=download&id=1i9LToKKEFjepcfEmSrCHSQC5L0wG-jdF">здесь</a>,
затем необходимо поместить ее в директорию ```models``` 

## <a id="title2">Часть 2. Запуск приложения</a>

Для того, чтобы запустить приложение, необходимо скачать все зависимости из файла ```requirements.txt```.
```
$ pip install -r requirements.txt
```

После того, как все библиотеки будут установлены, необходимо настроить ssh-протокол, при помощи которого бот будет взаимодействовать с FastAPI.
```
$ ssh -R 80:localhost:8080 nokey@localhost.run
```

Затем запустите файл main.py. Убедитесь в том, что вы <a href="https://drive.google.com/uc?export=download&id=1i9LToKKEFjepcfEmSrCHSQC5L0wG-jdF">скачали</a> модель и поместили ее в нужную директорию.
```
$ python main.py
```

## <a id="title3">Часть 3. Демонстрация работы</a>
