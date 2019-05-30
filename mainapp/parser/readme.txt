1.Модуль parser собирает информацию со сторонних сайтов для товаров (Items) в mainapp.models  и подтягивает её в таблицу FromWebProdFields, обновляя поля (value) таблицы списков (ItemInChecklist)

2.Конфигурация и настройки поиска сохранены в configures.json . Можно дополнять новыми адресами поиска, добавляя очередной словарь с ключами настроек "adr", "search_exp", "reg_expr" () и т.д.

3.Запуск модуля производится из командной строки python manage.py run_web_parser:
	По умолчанию данные базы будут обновляться раз в 24 часа. Чтобы изменить периодичность надо добавить --sleep [кол-во 	часов]

4. Можно удалить из бд все данные таблицы FromWebProdFields из командной строки python manage.py run_web_parser -clear_db

5. Посмотеть содержимое любой таблицы бд, добавив аргумент --show_db [tab_name], например: 
	python manage.py run_web_parser --show_db Items 