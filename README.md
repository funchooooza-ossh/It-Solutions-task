# It-Solutions-task
Тестовое для It-solutions
Перед началом разъяснения как и что ставить на свой хост, чтобы все заработало хотелось бы прокомментировать те моменты, которые вызывали у меня вопросы.
1. Какой подход к обработке моделей выбрать? ORM или API и сериализаторы. API удобнее с точки зрения разработки back и front независимо, API лучше масштабируется, а также как ни крути
его проще тестировать. ORM в свою очередь крайне прост в реализации, производительнее, легко отлаживается, но при этом тесно привязывает front к back'y.
Так как в ТЗ я не увидел четких требований к реализации данного момента, я выбрал API.
2.Так как в тз четко не было указано какие меры аутентификации нужно реализовать, то я решил использовать JWT. Реализовал middleware для проверки сессионных куки на наличие access и refresh токенов, также реализовал middleware для авто рефреш access token, иначе говоря, middleware перехватывает запрос раньше сервера, проверяет валидность access токена, если он истек, то проверяет рефреш токен и в зависимости от его валидности рефрешит access токен.
3.В models.py приложения main и в шаблоне menu.html хранится то, что я реализовал, но не стал использовать, так как это бессмысленно усложняет написание документации. Суть в том, я написал templatetag и шаблон для меню, благодаря чему можно очень 
удобно с помощью создания меню в админке и добавления {% draw_menu 'название меню из админки' %} отображать древовидные менюшки там где мы хотим, ну и создавать их сколько захочется. Оставил их просто, чтобы были.


Теперь немного про установку.
1. git clone <ссылка на этот репозиторий>
2. Нужно установить докер, идем сюда https://docs.docker.com/engine/install/ и выбираем вариант для своей os.
3. Переходим в папку проекта, после чего в терминале пишем 'docker-compose up --build -d) //возможно у вас будет docker compose без дефиса.
4. Пишем в терминале: 
    docker-compose exec web python makemigrations users
    docker-compose exec web python manage.py migrate
5.Создаем суперюзера: docker-compose exec web python manage.py createsuperuser
6. После создания заходим в браузер или постман хост по умолчанию localhost
ПРИМЕЧАНИЕ: файл .env включает в себя настройки данных для postgres и settings.py проекта, то есть вносить изменения можно в этом файле и они автоматически применятся и к поднимаемой базе, и к проекту.
Описание, пойдем по тз:
1.Реализован список автомобилей, реализована возможность посмотреть конкретный авто, добавлять новые можно только зарегестрированным пользователям. Для апи написан новый permission IsAdminOrOwner.
2.У зарегестрированных пользователей есть возможность оставлять комментарии, комментарии привязаны к конкретному автомобилю.
3. REST API для получения,создания, редактирования и удаления авто реализован, аналогично с комментариями.
4.Регистрация и авторизация реализованы на базе Djoser, путем переписывания сериализаторов, а также view для получения и обновления токена.
5.В панели администратора есть все необходимое, модели авто и комментариев, также список пользователей, ну и менюшки, которые я отбросил, но они работают и даже хорошо.
Все поля моделей Car и Comment реализованы строго по ТЗ, для сериализаторов же я имел смелость немножечко дописать отсебятины, так как модели обрабатываются API.
Views и шаблоны реализованы в полной мере, /(root) это список автомобилей, всю визуальную информацию пользователи могут получить без регистрации(конечно же в рамках здравого смысла, без явок и паролей).
CSS я использовал лениво, просто подключил simplecss ко всем шаблонам, каюсь.
Endpoint'ы API соответствуют ТЗ, хоть я и поленился используя viewset вместо более гибких(на мой взгляд) APIView.





