from pprint import pprint
from bs4 import BeautifulSoup
import requests
import json
import re

token = "31c0bd7c42ac286e2a28afc502819d77af0204dea39fc65fd6ac173e081e2a6f"
secret = "Hjg3m7P0blFdslG8NgCFbxORpcqjuwX34C5ns0KFi5OLJXeog185P7VgrmVIXkwD"
url_ori = "https://auth.indeed.com/resumes?client_id="

def return_fields(pos_code, pages, string, options):
	resume_json_fields = []
	for i in range(pages):
		url = url_ori + token + "&v=1&l=" + str(pos_code) + "&pretty=1" + "&start=" + str((i - 1) * 50)
		response = requests.get(url)
		resume = response.json()["data"]["resumes"]
		for j in resume:
			resume_dict = {}
			if options["firstName"]:
				resume_dict["firstName"] = j["firstName"]
			if options["lastName"]:
				resume_dict["lastName"] = j["lastName"]
			if options["summary"]:
				resume_dict["summary"] = j["summary"]
			if options["workExperiences"]:
				resume_dict["workExperiences"] = j["workExperiences"]
			if options["educations"]:
				resume_dict["educations"] = j["educations"]
			if options["skills"]:
				resume_dict["skills"] = j["skills"]
			if options["awards"]:
				resume_dict["awards"] = j["awards"]
			if options["militaryBackground"]:
				resume_dict["militaryBackground"] = j["militaryBackground"]
			if string == True:
				resume_json_fields.append(resume_dict)
			else:
				resume_json_fields.append(json.dumps(resume_dict))
	return resume, resume_json_fields

def return_all(pos_code, pages, string, options):
	resume_json_fields = []
	resume_json = []
	resume = []
	for i in range(pages):
		url = url_ori + token + "&v=1&l=" + str(pos_code) + "&pretty=1" + "&start=" + str((i - 1) * 50)
		response = requests.get(url)
		resume += response.json()["data"]["resumes"]
		resume1 = response.json()["data"]["resumes"]
		if string == True:
			for j in response.json()["data"]["resumes"]:
				str_resume = ""
				for val in j.values():
					str_resume += re.sub(r'[^\w\s]','',json.dumps(val))
				resume_json.append(str_resume)
		else:
			resume_json += response.json()["data"]["resumes"]

		for j in resume1:
			resume_dict = {}
			if options["firstName"]:
				resume_dict["firstName"] = j["firstName"]
			if options["lastName"]:
				resume_dict["lastName"] = j["lastName"]
			if options["summary"]:
				resume_dict["summary"] = j["summary"]
			if options["workExperiences"]:
				resume_dict["workExperiences"] = j["workExperiences"]
			if options["educations"]:
				resume_dict["educations"] = j["educations"]
			if options["skills"]:
				resume_dict["skills"] = j["skills"]
			if options["awards"]:
				resume_dict["awards"] = j["awards"]
			if options["militaryBackground"]:
				resume_dict["militaryBackground"] = j["militaryBackground"]
			if string == True:
				resume_json_fields.append(resume_dict)
			else:
				resume_json_fields.append(json.dumps(resume_dict))

	return resume, resume_json, resume_json_fields


# if __name__ == '__main__':
	# resume is a list of dict
	# resume = return_all(48105, 1, True)
	# print(resume)
	# options = {
	# 	"firstName": 1,
	# 	"lastName": 1,
	# 	"summary": 1,
	# 	"workExperiences": 1,
	# 	"educations": 1,
	# 	"skills": 1,
	# 	"awards": 1,
	# 	"militaryBackground": 1
	# }
	# resume = return_fields(94108, 1, True, options)
	# print(resume)