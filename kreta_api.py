import requests
import jwt

class KretaEndpoints:
	token = "/connect/token"
	notes = "/ellenorzo/V3/Sajat/Feljegyzesek"
	events = "/ellenorzo/V3/Sajat/FaliujsagElemek"
	student = "/ellenorzo/V3/Sajat/TanuloAdatlap"
	teachers = "/ellenorzo/V3/Felhasznalok/Alkalmazottak/Tanarok/Osztalyfonokok"
	evaluations = "/ellenorzo/V3/Sajat/Ertekelesek"
	absences = "/ellenorzo/V3/Sajat/Mulasztasok"
	groups = "/ellenorzo/V3/Sajat/OsztalyCsoportok"
	classAverages = "/ellenorzo/V3/Sajat/Ertekelesek/Atlagok/OsztalyAtlagok"
	timetable = "/ellenorzo/V3/Sajat/OrarendElemek"
	exams = "/ellenorzo/V3/Sajat/BejelentettSzamonkeresek"
	homework = "/ellenorzo/V3/Sajat/HaziFeladatok"
	capabilities = "/ellenorzo/V3/Sajat/Intezmenyek"
	
class KretaAPI:
	IDP_URL = 'https://idp.e-kreta.hu'

	def __init__(self, useragent):
		self.useragent = useragent

	def get_school_list(self):
		urls = requests.get('https://kretamobile.blob.core.windows.net/configuration/ConfigurationDescriptor.json').json()
		response = requests.get(urls['GlobalMobileApiUrlPROD'] + '/api/v3/Institute', headers = {
			'User-Agent': self.useragent,
			'apiKey': '7856d350-1fda-45f5-822d-e1a2f3f1acf0'
		})
		return response.json()

	def authenticate(self, username, password, institute_code):
		self.institude_code = institute_code
		self.SCHOOL_URL = f'https://{institute_code}.e-kreta.hu'

		post_data = {
			'userName': username,
			'password': password,
			'institute_code': institute_code,
			'grant_type': 'password',
			'client_id': 'kreta-ellenorzo-mobile',
		}
		headers = {
			'User-Agent': self.useragent,
			'Content-Type': 'application/x-www-form-urlencoded',
		}
		
		response = requests.post(self.IDP_URL + KretaEndpoints.token, data = post_data, headers = headers)

		if(response.status_code == 200):
			resposne_data = response.json()
			self.access_token = resposne_data['access_token']
			self.refresh_token = resposne_data['refresh_token']
			self.auth_headers = {
				'User-Agent': self.useragent,
				'Authorization': f'Bearer {self.access_token}'
			}
			return response.json()
		else:
			raise Exception(f"Error occurred, status code: {response.status_code}")

	def authenticate_token(self, refresh_token, institute_code):
		self.refresh_token = refresh_token
		self.institude_code = institute_code
		self.SCHOOL_URL = f'https://{institute_code}.e-kreta.hu'
		return self.refresh_auth()

	def set_access_token(self, access_token, refresh_token = None):
		self.access_token = access_token
		self.refresh_token = refresh_token
		jwt_data = jwt.decode(access_token, options={"verify_signature": False})
		institute_code = jwt_data['kreta:institute_code']
		self.SCHOOL_URL = f'https://{institute_code}.ekreta.hu'

	def refresh_auth(self):
		post_data = {
			'refresh_token': self.refresh_token,
			'institute_code': self.institude_code,
			'grant_type': 'refresh_token',
			'client_id': 'kreta-ellenorzo-mobile',
		}

		headers = {
			'User-Agent': self.useragent,
			'Content-Type': 'application/x-www-form-urlencoded',
		}

		response = requests.post(self.IDP_URL + KretaEndpoints.token, data = post_data, headers = headers)

		if(response.status_code == 200):
			resposne_data = response.json()
			self.access_token = resposne_data['access_token']
			self.auth_headers = {
				'User-Agent': self.useragent,
				'Authorization': f'Bearer {self.access_token}'
			}
			return response.json()
		else:
			raise Exception(f"Error occurred, status code: {response.status_code}")

	def get_timetable(self, fromDate, toDate):
		params = {
			'datumTol': fromDate,
			'datumIg': toDate,
		}
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.timetable, params = params, headers = self.auth_headers)
		return response.json()

	def get_grades(self):
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.evaluations, headers = self.auth_headers)
		return response.json()

	def get_class_averages(self, oktatasi_nevelesi_feladat_uid):
		params = {
			"oktatasiNevelesiFeladatUid": oktatasi_nevelesi_feladat_uid
		}
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.classAverages, params = params, headers = self.auth_headers)
		return response.json()

	def get_notes(self):
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.notes, headers = self.auth_headers)
		return response.json()

	def get_notice_board(self):
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.events, headers = self.auth_headers)
		return response.json()
	
	def get_homework(self, fromDate, toDate):
		params = {
			'datumTol': fromDate,
			'datumIg': toDate,
		}
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.homework, params = params, headers = self.auth_headers)
		return response.json()
	
	def get_absences(self):
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.absences, headers = self.auth_headers)
		return response.json()

	def get_exams(self):
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.exams, headers = self.auth_headers)
		return response.json()

	def get_groups(self):
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.groups, headers = self.auth_headers)
		return response.json()

	def get_user_data(self):
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.student, headers = self.auth_headers)
		return response.json()

	def get_head_teacher_data(self, teacher_id):
		params = {
			'Uids': teacher_id,
		}
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.teachers, params = params, headers = self.auth_headers)
		return response.json()

	def get_teachers(self):
		headers = self.auth_headers
		headers['X-Uzenet-Lokalizacio'] = 'hu-HU'
		response = requests.get("https://eugyintezes.e-kreta.hu/api/v1/kreta/alkalmazottak/tanar", headers = headers)
		return response.json()

	def get_school_data(self):
		response = requests.get(self.SCHOOL_URL + KretaEndpoints.capabilities, headers = self.auth_headers)
		return response.json()