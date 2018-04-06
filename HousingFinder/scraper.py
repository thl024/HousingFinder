import time

from models import CAPE, GradeDist, BasicDetails

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from db import get_db

URL = 'http://cape.ucsd.edu/responses/Results.aspx'

class Scraper():

	def __init__(self, start_dept=None, end_dept=None, count=None):
		self.url = URL
		self.count = count
		self.start_dept = start_dept
		self.end_dept = end_dept

	def begin(self):
		self.scrape_page(self.url)

	def create_driver(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--disable-extensions')
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
		options.add_argument('--no-sandbox')
		return webdriver.Chrome(options=options)

	def scrape_page(self, url):
		# Initialize driver
		driver = self.create_driver()
		driver.get(url)

		# Get list of department elements
		dept_list = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddlDepartments"]')
		time.sleep(4)
		dept_elements = [x for x in dept_list.find_elements_by_tag_name("option")][1:]
		dept_elements_text = [str(x.text.split(' ')[0] )for x in dept_elements]

		# Apply start dept and end dept filtering
		lowerb = 0
		upperb = len(dept_elements)
		if self.start_dept:
			try:
				lowerb = dept_elements_text.index(self.start_dept)
			except ValueError as e:
				print(e)
				print("No such department: {}".format(self.start_dept))

		if self.end_dept:
			try:
				upperb = dept_elements_text.index(self.end_dept) + 1
			except ValueError as e:
				print(e)
				print("No such department: {}".format(self.end_dept))

		dept_elements = dept_elements[lowerb:upperb]

		i = 0
		for dept in dept_elements:

			course_links = []
			try:
				# Select and search for department
				dept.click()
				time.sleep(4)
				search_button = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_btnSubmit"]')
				search_button.click()
				time.sleep(7)
			
				# Receive results and get links to each course CAPE page
				table = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_gvCAPEs"]')
				table_body = table.find_element_by_tag_name("tbody")
				rows = table_body.find_elements_by_tag_name('tr')
				course_links = [row.find_elements_by_tag_name('td')[1] for row in rows]
			except Exception as e:
				print(e)
				print("Failed Initial Search for Dept: {}".format(dept))

			for course in course_links:
				try:
					# Select link
					link = course.find_element_by_tag_name("a")
					link.click()
					time.sleep(4)
	    
					# Switch driver to focus on new tab
					driver.switch_to.window(driver.window_handles[1])

					# Scrape and store CAPE
					self.findElementsAndStoreCAPE(driver)
					time.sleep(5)

				except Exception as e:
					print("Exception with course: {}".format(course))
					print(e)

				# Close tab if it was opened
				if len(driver.window_handles) > 1:
					driver.close()
					time.sleep(8)
					driver.switch_to.window(driver.window_handles[0])
					time.sleep(4)

				if self.count is not None and i == self.count:
					driver.quit()
					return
				i += 1

	def getElement(self, root, xpath, label):
		try:
			return root.find_element_by_xpath(xpath)
		except NoSuchElementException as e:
			print("No such element: {}".format(label))
			return None

	def cast(self, text):
		if text == "N/A":
			return None
		try:
			return int(text)
		except ValueError as e:
			print(e)
			return None

	def castFloat(self, text):
		if text == "N/A":
			return None
		try:
			return float(text)
		except ValueError as e:
			print(e)
			return None

	def findElementsAndStoreCAPE(self, root):

		course = self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_lblCourseDescription"]', 'course').text
		instructor = self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_lblInstructorName"]', 'instructor').text
		term = self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_lblTermCode"]', 'term').text
		enrollment = self.cast(self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_lblEnrollment"]', 'enrollment').text)
		capes_returned = self.cast(self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_lblEvaluationsSubmitted"]', 'capes_returned').text)

		rec_inst = self.cast(self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_lblRecommendInstructor"]', 'rec_inst').text.split('\n')[0])
		rec_course = self.cast(self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_lblRecommendCourse"]', 'rec_course').text.split('\n')[0])
		exam_rep = self.castFloat(self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_lblExamsRepresentCourseMaterial"]', 'exam_rep').text.split(' ')[0])
		clear_audible = self.castFloat(self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_lblInstructorClearAndAudible"]', 'clear_audible').text.split(' ')[0])

		exp_grade_counts = []

		exp_grades_table = self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_tblExpectedGrades"]', 'exp_grades_table')
		
		if exp_grades_table is not None:
			exp_grades_count = exp_grades_table.find_element_by_tag_name('tbody')
			exp_grades = exp_grades_count.find_elements_by_tag_name('td')
			for i in range(0, 7):
				exp_grade_counts.append(exp_grades[i].text)

		# Get received grades
		grade_counts = []

		grades_table = self.getElement(root, '//*[@id="ctl00_ContentPlaceHolder1_tblGradesReceived"]', 'grades_table')
		if grades_table is not None:
			grades_count = grades_table.find_element_by_tag_name('tbody')
			grades = grades_count.find_elements_by_tag_name('td')
			for i in range(0, 7):
				grade_counts.append(grades[i].text)

		# Received grades
		received_grades = None
		if len(grade_counts) != 0:
			received_grades = {
				"a_count": grade_counts[0],
				"b_count": grade_counts[1],
				"c_count": grade_counts[2],
				"d_count": grade_counts[3],
				"f_count": grade_counts[4],
				"p_count": grade_counts[5],
				"np_count": grade_counts[6]
			}

		data = {
			"course": course,
			"instructor": instructor,
			"term": term,
			"enrollment": enrollment,
			"capes_returned": capes_returned,
			"expected_grades": {
				"a_count": exp_grade_counts[0],
				"b_count": exp_grade_counts[1],
				"c_count": exp_grade_counts[2],
				"d_count": exp_grade_counts[3],
				"f_count": exp_grade_counts[4],
				"p_count": exp_grade_counts[5],
				"np_count": exp_grade_counts[6]
			},
			"received_grades": received_grades,
			"details": {
				"rec_inst": rec_inst,
				"rec_course": rec_course,
				"exam_rep": exam_rep,
				"clear_audible": clear_audible
			}
		}

		# Unique identifier for a CAPE
		filter = {
			"course": course,
			"instructor": instructor,
			"term": term,
		}

		# Perform Pymongo's upsert operaion for combined updating/insertion
		cape_collection = get_db()
		try:
			cape_collection.replace_one(filter, data, upsert=True)
			print("Saved new element: {}".format(course + ";" + instructor + ";" + term))
		except Exception as e:
			print("Failed to save cape: {}".format(course + ";" + instructor + ";" + term))
			print(e)



