# Elschool Parser Library #

## Что это за библиотека? ##
Elschool Parser Library - библиотека для работы с Elschool, на данный момент она может:
1. Получать расписание 
2. Получать домашку
3. Получать Оценки
4. Получать информацию о себе
5. Входить/Выходить из аккаунта

Модуль сделан на Requests, Beatiful Soup 4 (они должны быть установлены)

## Using ##

Что ба начать работать с модулем прочитайте документацию.
Модуль работает только в синхронном режиме но планируется добавление асинхронности.
Вот пример кода:
app = App(username="ваше имя", password="ваш пароль")
data = app.get_self_data()
print(data)

Импортируйте библиотеку.
В библиотеке есть всего 1 класс:
App, он принимает в себя 3 аттрибута:
username(обязательно), password(обязательно), session(необязательно)

Вот пример создания экземпляра класса:
app = App(username="ваше имя", password="ваш пароль")

есть всего 6 функций:
1. login(username(обязательно), password(обязательно))
2. get_self_data()
3. get_subjects(week(необязательно), year(необязательно))
4. get_homework(week(необязательно), year(необязательно))
5. get_marks(class_(обязательно))
6. exit()

если вы знаете английский то уже поняли за что всё отвечает.

1. login - принимает 2 параметра: имя и пароль,
	вызывается автоматически при создании класса, о при желании можно вызвать повторно и зайти в другой аккаунт.
2. get_self_data - не принимает никаких параметров. Возвращает данные о вас в виде кортежа:
	(status_code, name, id, login, birthday, email, instituteID, departmentID, rootID)
	1 статус код запроса
	2 ваше имя
	3 ваш ID
	4 ваш логин
	5 ваше дата рождения
	6 ваш электронный адрес
	7,8,9 - это данные которые скорее всего вам будут не нужны,
	instituteID - ID школы
	departmentId - ID вашего класса.

3. get_subjects - принимает необязательные параметры: week(неделя), year(год), если их не указать автоматически будет 	 указано сегодняшняя дата. Возвращает словарь в котором ключ это день недели, а значение это список с уроками:
{'понедельник': ['1. Разговоры о важном', '1. ПДД', '1. Классный час', '3. Алгебра', '4. Русский язык', '5. География', '7. Физическая культура', '8. Функциональная грамотность', '10. Я выбираю ГТО'], 'вторник': ['4. Алгебра', '5. История', '6. Изобразительное искусство', '7. Русский язык', '8. В мире музыки'], 'среда': ['1. Литература', '2. Биология', '3. Физика', '4. Обществознание', '5. Алгебра', '6. География', '10. ВПК'], 'четверг': ['1. Русский язык', '2. Русский язык', '4. Физическая культура', '5. Физика', '6. Алгебра'], 'пятница': ['1. Геометрия', '2. Геометрия', '3. Литература', '5. История', '7. Я выбираю ГТО']}

4. get_homework - принимает необязательные параметры: week(неделя), year(год), если их не указать автоматически будет 	 указано сегодняшняя дата. Возвращает словарь с уроками и домашним заданием, ключом является день недели а значением список в котором кортеж с уроком и домашним заданием: {'понедельник': [('математика': 'Выполнить задание 993'), ('русский','выполнить задание 255')]}

5. get_marks - принимает обязательный параметр class_(класс в котором вы учитесь/учились). Возвращает словарь где ключом является урок, а значением кортеж внутри которого списки с оценками:
{'Биология': (['4,78', '4,75', '5', '4,75'], ['545555545', '5455', '55555', '5455'])}
	1. первый список это средняя оценка
		каждый элемент это четверть
	2. второй список это все оценки
		каждый элемент это четверть

6. exit - ничего не принимает, ничего не возвращает. Выходит из аккаунта.

Вот и всё пользуйтесь! :) (Это мой первый проект который я выкладываю, если нашли что код сделан как-будто новичком не удивляйтесь)
