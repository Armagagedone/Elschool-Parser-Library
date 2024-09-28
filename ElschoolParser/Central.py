import requests
import bs4 as bs
import datetime


class App:
	def __init__(self, username, password, session=requests.Session()):
		if not isinstance(session, requests.Session):
			raise TypeError("Session type is not a requests session!")
		self.__session = session
		self._username = username
		self._password = password
		self.login(self._username, self._password)
		data = self.get_self_data()
		self.__id = data[2]
		self.__instituteID = data[6]
		self.__departmentID = data[7]
		self.__rootID = data[8]

	def login(self, username, password):
		r = self.__session.post("https://elschool.ru/logon/index", {"login": str(username), "password": str(password)})
		return (r.status_code == 200, r)

	def exit(self):
		r = self.__session.post('https://elschool.ru/users/diaries/Exit')
		self.__session.cookies.clear_session_cookies()
		self.__session.close()

	def get_self_data(self):
		r = self.__session.get("https://elschool.ru/users/privateoffice")
		if r.status_code == 200:
			soup = bs.BeautifulSoup(r.text, "html.parser")
			name = soup.findAll('h3', class_='personal-data__name')[0].text
			id = soup.findAll('td', class_='personal-data__info-value personal-data__info-value_bold')[0].text
			login = soup.findAll('td', class_='personal-data__info-value personal-data__info-value_bold')[1].text
			birthday = soup.findAll('td', class_='personal-data__info-value')[2].text
			email = soup.findAll('td', class_='personal-data__info-value')[5].text
			role = soup.findAll('div', class_="border-block p-3 mb-3 flex-grow-1")
			data = soup.findAll('a', class_='d-block')[0].get('href').split('/')
			departmentID = data[-1]
			instituteID = data[-3]
			rootID = data[-5]
			return (r.status_code == 200, name, id, login, birthday, email, instituteID, departmentID, rootID)
		return (False, "Error")

	def get_subjects(self, week=datetime.datetime.today().isocalendar()[1], year=datetime.datetime.now().year):
		r = self.__session.get(f"https://elschool.ru/users/diaries/details?RooId={self.__rootID}&InstituteId={self.__instituteID}&DepartmentId={self.__departmentID}&PupilId={self.__id}&Year={year}&Week={week}&log=False")
		if r.status_code != 200:
			return (False, r)
		soup = bs.BeautifulSoup(r.text, "html.parser")
		subjects = {}
		lastday = 'понедельник'
		days = soup.findAll('div', class_="col-6")
		for i in days:
			lessons = i.findAll('tr', 'diary__lesson')
			for j in lessons:
				try:
					day = j.findAll('td', class_="diary__dayweek")
					lastday = day[0].find('p').text.replace(u'\xa0', u' ').split(' ')[0] if len(day) > 0 else lastday
					lessonname = j.findAll('div', class_="flex-grow-1")[0].text
					if lastday in subjects:
						subjects[lastday].append(lessonname)
					else:
						subjects[lastday] = [lessonname]
				except Exception as e:
					pass
		return subjects

	def get_homework(self, week=datetime.datetime.today().isocalendar()[1], year=datetime.datetime.now().year):
		r = self.__session.get(f"https://elschool.ru/users/diaries/details?rooId={self.__rootID}&instituteId={self.__instituteID}&departmentId={self.__departmentID}&pupilId={self.__id}&Year={year}&Week={week}&log=False")
		if r.status_code != 200:
			return (False, r)
		soup = bs.BeautifulSoup(r.text, "html.parser")
		days = soup.findAll('div', class_="col-6")
		lastday = 'понедельник'
		hw = {}
		for i in days:
			lessons = i.findAll('tr', 'diary__lesson')
			for j in lessons:
				try:
					day = j.findAll('td', class_="diary__dayweek")
					lastday = day[0].find('p').text.replace(u'\xa0', u' ').split(' ')[0] if len(day) > 0 else lastday
					lessonname = j.findAll('div', class_="flex-grow-1")[0].text
					homework = j.findAll('div', class_='diary__homework-text')[0].text
					if lastday in hw:
						hw[lastday].append((lessonname, homework))
					else:
						hw[lastday] = [(lessonname, homework)]
				except Exception as e:
					pass
		return hw

	def get_marks(self, class_):
		r = self.__session.get(f'https://elschool.ru/users/diaries/grades?rooId={self.__rootID}&instituteId={self.__instituteID}&departmentId={self.__departmentID}&pupilId={self.__id}')
		if r.status_code != 200:
			return (False, r)
		soup = bs.BeautifulSoup(r.text, 'html.parser')
		classes = soup.findAll('a', class_='dropdown-item')
		grades = {}
		for i in classes:
			if str(class_) in i.text:
				depid = i['model-department-id']
				r = self.__session.get(f'https://elschool.ru/users/diaries/grades?rooId={self.__rootID}&instituteId={self.__instituteID}&departmentId={depid}&pupilId={self.__id}')
				if r.status_code != 200:
					return (False, r)
				soup = bs.BeautifulSoup(r.text, 'html.parser')
		subjs = soup.findAll('tbody')
		for j in subjs:
			for k in j:
				if isinstance(k, bs.Tag):
					try:
						name = k.findAll(class_='grades-lesson')[0].text
						average = k.findAll(class_='grades-average')
						average = [i.text for i in average]
						marks = k.findAll(class_='grades-marks')
						marks = [i.text.replace('\n', '') for i in marks]
						grades[name] = (average, marks)
					except Exception as e:
						pass
		return grades