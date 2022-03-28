import csv
import copy
new_csv = []
variables = ['survey_id', 'message_id', 'duration', 'age', 'gender', 'ethnicity', 'intepersonal_emphasis', 'average_trust_score', 'subject_expertise_score', 'ai_score', 'interpersonal_score', 'trust_scale', 'computer_attitude_scale', 'ai_attitude_scale']
mapping = {"pet":["Q292", "Q296", "Q300", "Q304", "Q308"], "party":["Q268", "Q272", "Q276", "Q280", "Q284"], "inquiring":["Q85", "Q252", "Q256", "Q260", "Q264"]}
gender_mapping = {"Male":0,"Female":1,"Other":2,"Prefer not to say":3}
ethnicities_mapping = {"White":0, "Black or African American":1, "American Indian or Alaska Native":2, "Asian":3,"Native Hawaiian or Pacific Islander":4,"Other":5,"Prefer not to say":6}
scale = {"Strongly disagree": 1, "Somewhat disagree": 2, "Neither agree nor disagree":3, "Somewhat agree":4, "Strongly agree":5}
pet_scale = {"I am a long time pet owner": 5, "I am a beginner pet owner": 4, "I help look after pet(s) occasionaly":3, "I do not have a pet but often encounter one":2, "I never interact with pet(s)":1}
party_scale = {"I often invite people or receive invitations to parties": 4, "I sometimes invite people or receive invitations to parties": 3, "I rarely invite people or receive invitations to parties":2, "I never invite people or receive invitations to parties":1}
inquiring_scale = {"I know this is true": 5, "I am not sure but it seems right": 3, "I am not sure":1, "I am not sure but it seems wrong":3, "I know this is wrong":5}

with open('', newline='', encoding='gb18030', errors='ignore') as csvfile:
	reader = csv.DictReader(csvfile)

	header = next(reader)
	header = list(header.keys())
	next(reader)
	for r in reader:
		temp_dict = {}
		temp_dict['survey_id'] = r['RandomID']
		temp_dict['age'] = r['Q134']
		temp_dict['gender'] = gender_mapping[r['Q138']]
		if ',' in r['Q140']:
			temp_dict['ethnicity'] = 7
		else:
			temp_dict['ethnicity'] = ethnicities_mapping[r['Q140']]
		temp_dict['trust_scale'] = scale[r['Q178_1']]
		temp_dict['computer_attitude_scale'] = ((6-scale[r['Q178_3']])+scale[r['Q178_2']])/2
		temp_dict['ai_attitude_scale'] = ((6-scale[r['Q178_5']])+scale[r['Q178_4']])/2
		for i in range(15, len(header)-8, 7):
			if not len(r[header[i]])==0:
				result_dict = copy.deepcopy(temp_dict)
				result_dict['message_id'] = header[i]
				if header[i] in mapping['inquiring']:
					result_dict['intepersonal_emphasis']= 0
					result_dict['subject_expertise_score']= inquiring_scale[r[header[i+4]]]
				elif header[i] in mapping['party']:
					result_dict['intepersonal_emphasis']= 1
					result_dict['subject_expertise_score']= party_scale[r[header[i+4]]]/4*5
				elif header[i] in mapping['pet']:
					result_dict['intepersonal_emphasis']= 2
					result_dict['subject_expertise_score']= pet_scale[r[header[i+4]]]
				else:
					print('error')
				result_dict['average_trust_score']= (scale[r[header[i+1]]]+scale[r[header[i+2]]]+scale[r[header[i+3]]])/3
				result_dict['ai_score']= r[header[i+5]]
				result_dict['interpersonal_score']=r[header[i+6]]
				new_csv.append(result_dict)

with open('ai_soc_implication_pilot1.csv', 'w', newline='') as csvfile:
    fieldnames = variables
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for r in new_csv:
    	    writer.writerow(r)