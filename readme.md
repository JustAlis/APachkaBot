Hello, GitHub!

Асинхронный микрофреймворк для работы с API мессенджера пачка.

Меня очень озадачило отсутствие чего-то хоть немного похожего на aiogram
для мессенджера пачка, так что решил написать комфортное для меня окружение,
чтобы можно было спокойно писать себе хендлеры и не париться

Данный микро фреймворк не использует большую часть возможностей API, так как у меня была 
пара вполне конкретных целей
    
    С ботом можно переписываться только 1 на 1(в базовой реализации)

    Решил для себя, что проще всего добавить бота в беседу компании, 
    после чего каждый просто отправит боту команду /start и откроет
    личную переписку с ботом. На сообщение бот отвечает именно в личные сообщения
    человека, который тригернул бота. Это сделано намеренно.
    Можно изменить это поведение, добавив новых функций классу Message, но тогда придётся внутри server в районе 50
    строки дополнительно парсить данные из body запроса(об этом дальше), но это не проблема, так как в документации 
    api указаны все параметры body входящего запооса, нужно просто вытащить из body методом гет необходимую информацию
    (смотри API и что входит в тело запроса), добавить свойство классу Message ну и новую функцию обработчик туда же, так же
    при создании класса message передать новое свойство.

    +возможность выполнять фоновые задачи конкурентно с обработкой входящих
    запросов.

    Так что по сути тут реализована только одна возможность API, а именно,
    отсылать сообщения в ответ на входящие. Если что, можно всегда увеличить простор работы с ботом,
    добавив новых функций и свойств в класс Message в одноимённом пакете, ссылка на API в пакете.

Навигация

    Config - в этом пакете помимо бота токена, хоста и порта хранятся маршруты API, которые вы можете
    дополнить по своему усмотрению (после импортируйте новые маршруты в пакеты message и service)

    Handlers - Собственно, хендлеры. Не буду скрывать, вдохновлялся библиотеками для написания ботов
    для телеграма, когда писал дизайн хендлеров. Если вас устраивает текущий функционал, то можете 
    спокойно писать только хендлеры(не забывайте регестрировать команды внутри самой "Пачки")

    Message - пакет с 1 классом Message. Чтобы расширить свойства и функционал - вам нужно работать внутри 
    данного класса, а потом писать хендоеры, но чобы добавить данных в сообщение, придётся перейти в пакет
    Server, о чём напишу дальше

    Server - самая душная и интересная часть микрофреймворка. 
    Стоит отметить следующее(строка 19 server):

            loop = asyncio.get_event_loop()

            for service in self.services:
                loop.create_task(service())
        
        Тут формируются и запускаются все конкурентные сервисы из пакета service

    Дальше парсинг запроса(строка 51):

            # request_method, headers = header.split('\r\n', 1)
            # request_method = request_method.split('/')[0].replace(' ', '')
            user = body.get('user_id')
            content = body.get('content')
            handler, *text = content.split(' ')
            text = ' '.join(text)

            handler = self.handlers.get(handler)
            message = Message(text=text, user=user)
        
        Собственно тут арсится реквест(body создаётся раньше, но это не принципиально) и данные переходят
        в новый объект Message. Можете ознакомиться с тем, какие данные можно забрать
        из боди и добавлять их в конструктор класса Message(после чего инициализировать новые объекты уже
        с дополнительными параметрами.). На этом этапе body - dict, соответсвующий входящему json.
        Ещё тут выбирается хендлер. Не советую менять, так как нужно переписывать класс регистратора в таком случае.
        Если хендлера нет, то выбирается хендлер error, единственный без "/" в начале.

    Services - пакет, куда вы можете записывать свои дополнительные задачи, которые будут выполняться конкурентно
    с обработкой входящих сообщений. Cоветую подробнее ознакомиться с API, перед тем как писать фоновые сервисы.
    Можете посмотреть реализацию класса Message, чтобы примерно понять, как следует работать с сервисами.

    Orm - пустой пакет. Что хотите - то и пишите, хоть чистый сиквел, хоть алхимию, хоть не сиквел базы данных.
    Это всегда зависит от конкретных потребностей

    Registrator - внутри два вспомогательных класса, которые я не советую трогать. Они отлично справляются со своей задачей:
    увеличивают удобство написания хендлеров и сервисов, а так же инициализирут последних при запуске сервера

Нужно ли кому-то это творение? Не знаю, но мне удобно работать именно в таком виде.

Так же хочу отметить, что "Пачка" не подключится к локалхосту. 

    Для разработки вполне удобно использовать
    ngrok или ему подобные утилиты. А вот с продакшеном уже на нормальном домене/статическом ip можно 
    подключать всякие nginx и апач. Прямо из коробки эта библиотека не подключается к пачке! Вебхуку нужен
    домен.

Чтобы это всё запустить просто в виртуальном окружении python main.py, прокинуть через ngrok локалхост 
и подключать исходящий вебхук в "Пачке" на предложенный ngrok домен. При перезапуске ngrok домены меняются.

Так же я специально оставил несколько сервисов и хендлеров, чтобы было понятнее, как с ними работать)

Если вдруг найдёте ошибки или недочёты - я только рад о них узнать и исправить, но если критикуете, то
предагайте)

Спасибо за внимание и приятного использования)
До связи, ГитХаб! 

Буп...Бип...б.п.....