from bs4 import BeautifulSoup
import requests
from colorama import Fore, Back, Style


# Parsing data from the UCSC catalog
def web_parse(class_num, dept_name):
    dept_link, div = '', ''
    class_num_str = str(class_num)

    # Currently considering only CSE and MATH, may add more in the future
    if dept_name == 'cse':
        dept_link = "CSE-Computer-Science-and-Engineering/"
        if type(class_num) == str:
            class_num = int(''.join(filter(str.isdigit, class_num)))
        if class_num < 100:
            div = "Lower-Division/CSE-"
        else:
            div = "Upper-Division/CSE-"

    if dept_name == 'math':
        dept_link = "MATH-Mathematics/"
        if type(class_num) == str:
            class_num = int(''.join(filter(str.isdigit, class_num)))
        if class_num < 100:
            div = "Lower-Division/MATH-"
        else:
            div = "Upper-Division/MATH-"

    url = "https://catalog.ucsc.edu/en/Current/General-Catalog/Courses/" + dept_link + div + class_num_str
    print(f"{Fore.LIGHTYELLOW_EX}[GET]{Style.RESET_ALL}", url)
    request_result = requests.get(url)
    request_result.raise_for_status()
    html = BeautifulSoup(request_result.text, 'html.parser')
    for a in html.find_all('a'):  # Removing hyperlinks in text
        a.replaceWithChildren()

    cc = str(html.find_all("span")[5].string).replace("CSE ", '')
    gen_descrip = str(html.find_all("p")[1]).replace("</p>", "").replace("<p>", "")
    quarter_offered = str(html.find_all("p")[4].string).split(", ")
    # prereq = str(html.find_all("p")[2]).replace("</p>", "").replace("<p>", "").replace("Prerequisite(s): ", "")

    return cc, gen_descrip, quarter_offered  # Returns course code, general description, and the quarters offered


# print(web_parse(20, 'cse'))

CLASSES = {
    "cse20": {
        "cc": web_parse(20, 'cse')[0],  # Class code (20)
        "availability": 4,
        # 1 = never available, 2 = sometimes available, 3 = meh, 4 = often available, 5 = always available
        "prereqs": [],
        "gen_descrip": web_parse(20, 'cse')[1],
        "difficulty": 4,
        "quarter_offered": web_parse(20, 'cse')[2],  # ['Fall', 'Winter', 'Spring']
        "syllabus": [{"zybooks_attendence": 15}, {"homework": 40}, {"midterm": 20}, {"final": 25}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 1,  # Math is 0, programming is 1, other is 2
        "time_commit": 2,  # 1= slack, 2= some work, 3= extra work
        "ge_satis": ["mf"],
        "pref_prof": ["Larrabee"],  # Based on rate my prof, can't predict "staff" tho
    },
    "cse30": {
        "cc": web_parse(30, 'cse')[0],
        "availability": 4,
        "prereqs": ["cse20", "math19a"],
        "gen_descrip": web_parse(30, 'cse')[1],
        "difficulty": 4,
        "quarter_offered": web_parse(30, 'cse')[2],
        "syllabus": [{"attendence": 10}, {"assignments": 90}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 1,
        "time_commit": 2,
        "ge_satis": [""],
        "pref_prof": ["Larrabee"],
    },
    "cse12": {
        "cc": web_parse(12, 'cse')[0],
        "availability": 6,
        "prereqs": ["cse20"],
        "gen_descrip": web_parse(12, 'cse')[1],
        "difficulty": 8,
        "quarter_offered": web_parse(12, 'cse')[2],
        "syllabus": [{"quizzes": 5}, {"assignments": 30}, {"midterm": 30}, {"final": 35}],
        "textbook": "textbook_url",
        "haslab": True,
        "ta_helpful": 6,
        "class_type": 1,
        "time_commit": 3,
        "ge_satis": [""],
        "pref_prof": ["Larrabee"],
    },
    "cse16": {
        "cc": web_parse(16, 'cse')[0],
        "availability": 7,
        "prereqs": ["math19a"],
        "gen_descrip": web_parse(16, 'cse')[1],
        "difficulty": 5,
        "quarter_offered": web_parse(16, 'cse')[2],
        "syllabus": [{"assignments": 30}, {"midterm": 35}, {"final": 35}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 0,
        "time_commit": 2,
        "ge_satis": ["mf"],
        "pref_prof": ["Larrabee"],
    },
    "math19a": {
        "cc": web_parse("19a", 'math')[0],
        "availability": 10,
        "prereqs": [],
        "gen_descrip": web_parse("19a", 'math')[1],
        "difficulty": 5,
        "quarter_offered": web_parse("19a", 'math')[2],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],  # Not sure need edit
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 0,
        "time_commit": 2,
        "ge_satis": ["mf"],
        "pref_prof": ["Larrabee"],
    },
    "math19b": {
        "cc": web_parse("19b", 'math')[0],
        "availability": 7,
        "prereqs": ["math19a"],
        "gen_descrip": web_parse("19b", 'math')[1],
        "difficulty": 5,
        "quarter_offered": web_parse("19b", 'math')[2],
        "syllabus": [{"homework": 10}, {"midterm": 20}, {"final": 70}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 0,
        "time_commit": 2,
        "ge_satis": ["mf"],
        "pref_prof": ["Larrabee"],
    },
    "math23a": {
        "cc": web_parse("23a", 'math')[0],
        "availability": 8,
        "prereqs": ["math19b"],
        "gen_descrip": web_parse("23a", 'math')[1],
        "difficulty": 5,
        "quarter_offered": web_parse("23a", 'math')[2],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],  # Not sure need edit
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 0,
        "time_commit": 2,
        "ge_satis": ["mf"],
        "pref_prof": ["Larrabee"],
    },
    "math21": {
        "cc": web_parse(21, 'math')[0],
        "availability": 7,
        "prereqs": ["math19a"],
        "gen_descrip": web_parse(21, 'math')[1],
        "difficulty": 4,
        "quarter_offered": web_parse(21, 'math')[2],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],  # Not sure need edit
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 0,
        "time_commit": 2,
        "ge_satis": [""],
        "pref_prof": ["Larrabee"],
    },
    "cse13s": {
        "cc": web_parse("13s", 'cse')[0],
        "availability": 5,
        "prereqs": ["cse12"],
        "gen_descrip": web_parse(30, 'cse')[1],
        "difficulty": 8,
        "quarter_offered": web_parse(30, 'cse')[2],
        "syllabus": [{"assignments": 50}, {"quizzes": 20}, {"final": 30}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 8,
        "class_type": 1,
        "time_commit": 3,
        "ge_satis": [""],
        "pref_prof": ["Long"],
    },
    "cse101": {
        "cc": web_parse(101, 'cse')[0],
        "availability": 4,
        "prereqs": ["cse13s", "cse16", "cse30", "math19b"],
        "gen_descrip": web_parse(101, 'cse')[1],
        "difficulty": 6,
        "quarter_offered": web_parse(101, 'cse')[2],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 1,
        "time_commit": 2,
        "ge_satis": [""],
        "pref_prof": ["Larrabee"],
    },
    "cse102": {
        "cc": web_parse(102, 'cse')[0],
        "availability": 4,
        "prereqs": ["cse101"],
        "gen_descrip": web_parse(102, 'cse')[1],
        "difficulty": 6,
        "quarter_offered": web_parse(102, 'cse')[2],
        "syllabus": [{"homework": 20}, {"programming_assignment": 10}, {"midterm": 40}, {"final": 30}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 5,
        "class_type": 0,
        "time_commit": 2,
        "ge_satis": [""],
        "pref_prof": ["Larrabee"],
    },
    "cse103": {
        "cc": web_parse(103, 'cse')[0],
        "availability": 7,
        "prereqs": ["cse101"],
        "gen_descrip": web_parse(103, 'cse')[1],
        "difficulty": 4,
        "quarter_offered": web_parse(103, 'cse')[2],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 0,
        "time_commit": 2,
        "ge_satis": [""],
        "pref_prof": ["Larrabee"],
    },
    "cse120": {
        "cc": web_parse(120, 'cse')[0],
        "availability": 7,
        "prereqs": ["cse12", "cse13s", "cse16"],
        "gen_descrip": web_parse(120, 'cse')[1],
        "difficulty": 4,
        "quarter_offered": web_parse(120, 'cse')[2],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 1,
        "time_commit": 2,
        "ge_satis": [""],
        "pref_prof": ["Larrabee"],
    },
    "cse130": {
        "cc": web_parse(130, 'cse')[0],
        "availability": 7,
        "prereqs": ["cse12", "cse101", "cse15"],
        "gen_descrip": web_parse(130, 'cse')[1],
        "difficulty": 4,
        "quarter_offered": web_parse(130, 'cse')[2],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 1,
        "time_commit": 2,
        "ge_satis": [""],
        "pref_prof": ["Larrabee"],
    },
    "cse107": {
        "cc": web_parse(107, 'cse')[0],
        "availability": 7,
        "prereqs": ["cse16", "math23a"],
        "gen_descrip": web_parse(107, 'cse')[1],
        "difficulty": 4,
        "quarter_offered": web_parse(107, 'cse')[2],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 1,
        "time_commit": 2,
        "ge_satis": ["sr"],
        "pref_prof": ["Larrabee"],
    },
    "cse112": {
        "cc": web_parse(112, 'cse')[0],
        "availability": 7,
        "prereqs": ["cse101"],
        "gen_descrip": web_parse(112, 'cse')[1],
        "difficulty": 4,
        "quarter_offered": web_parse(112, 'cse')[2],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 6,
        "class_type": 1,
        "time_commit": 2,
        "ge_satis": [""],
        "pref_prof": ["Larrabee"],
    },
    "core": {
        "cc": None,
        "availability": 10,
        "prereqs": [],
        "gen_descrip": "Depending on your affiliated college",
        "difficulty": 3,
        "quarter_offered": ['Fall'],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 10,
        "class_type": 2,
        "time_commit": 1,
        "ge_satis": [""],
        "pref_prof": ["Larrabee"],
    },
    "ge": {
        "cc": None,
        "availability": 10,
        "prereqs": [],
        "gen_descrip": "GE Description Varies",
        "difficulty": 3,
        "quarter_offered": ['Spring', 'Summer', 'Fall', 'Winter'],
        "syllabus": [{"quiz": 30}, {"midterm": 30}, {"final": 30}],
        "textbook": "textbook_url",
        "haslab": False,
        "ta_helpful": 10,
        "class_type": 2,
        "time_commit": 1,
        "ge_satis": ["mf"],
        "pref_prof": ["Larrabee"],
    },
}
# print(CLASSES.get("cse30").get("cc"))
# print(CLASSES.get("cse30"))
# print(CLASSES.keys())


# Currently unable to directly imply satisfied courses (ex: Took cse 101 -> satisify all prereqs)
# Include other minors and majors if the user wants to take it
# No database yet to store individual user data
