from config.database import create_neo4j_connection
from config.questions import questions
from utils.file_utils import read_json, get_random_color
from utils.hash_utils import generate_unique_id

from models.forms.createNode import nodeStudent, nodeAdvisor, nodeArea, nodeExtracurricularActivity, nodeLenguage, nodeOptativeCourse, nodePT, nodeSkill, nodeSocialService
from models.forms.relations.relations import relationAdvisorPT, relationAdvisorStudent, relationPTArea, relationSocialServiceArea, relationStudentCurricularActivity, relationStudentLanguage, relationStudentOptativeCourse, relationStudentPT, relationStudentSkill, relationStudentSocialService

from services.linkedinApi import main

import json
from colorama import Fore


def test_connection():
    driver = create_neo4j_connection()
    with driver.session() as session:
        result = session.run("RETURN 'Conexión exitosa con Neo4j'")
        for record in result:
            print(record[0])  # Debería imprimir "Conexión exitosa con Neo4j"


if __name__ == "__main__":
    test_connection()
    data = read_json("data/formsprueba.json")
    driver = create_neo4j_connection()

    nodeLenguage(driver)
    for person in data:
        randomColor = get_random_color()
        print(f"{randomColor} Datos de la persona:")
        personObject = {}
        for key, value in person.items():
            if key in questions:
                print (f"{questions[key]}: {value}")
                personObject[questions[key]] = value
            else:
                print(f"{key}: {value}")
        
        print(json.dumps(personObject, indent=4, ensure_ascii=False))
        print(Fore.RESET)

        student = {
            "publicIdentifier": personObject['publicIdentifier'],
            "fullName": personObject['fullName'],
            "studentId": personObject['studentId'],
            "admissionDate": personObject['admissionDate'],
            "linkedinProfile": personObject['linkedinProfile'],
            "contactPermission": personObject['contactPermission'],
            "yearsToGraduate": personObject['yearsToGraduate']
        }

        nodeStudent(driver, student)

        thesisAdvisor = personObject['thesisAdvisor']
        if isinstance(thesisAdvisor, list):
            for advisor in thesisAdvisor:
                nodeAdvisor(driver, {"fullName": advisor})
        else:
            nodeAdvisor(driver, {"fullName": thesisAdvisor})

        thesisArea = personObject['thesisArea']
        if isinstance(thesisArea, list):
            for area in thesisArea:
                nodeArea(driver, {"fullName": area})
        else:
            nodeArea(driver, {"fullName": thesisArea})

        nodePT(driver, {"fullName": personObject['thesisTitle']})

        relationStudentPT(driver, student, {"fullName": personObject['thesisTitle']}, personObject['thesisContribution'], personObject['thesisFocus'])
        
        if isinstance(thesisArea, list):
            for area in thesisArea:
                relationPTArea(driver, {"fullName": personObject['thesisTitle']}, {"fullName": area})
        else:
            relationPTArea(driver, {"fullName": personObject['thesisTitle']}, {"fullName": thesisArea})
        
        if isinstance(thesisAdvisor, list):
            for advisor in thesisAdvisor:
                relationAdvisorPT(driver, {"fullName": advisor}, {"fullName": personObject['thesisTitle']})
        else:
            relationAdvisorPT(driver, {"fullName": thesisAdvisor}, {"fullName": personObject['thesisTitle']})
        
        if isinstance(thesisAdvisor, list):
            for advisor in thesisAdvisor:
                relationAdvisorStudent(driver, {"fullName": advisor}, student)
        else:
            relationAdvisorStudent(driver, {"fullName": thesisAdvisor}, student)

        relationStudentLanguage(driver, student, "Inglés", personObject['englishLevel'], personObject['englishLevelGraduation'])

        optativeCourses = personObject['helpfulOptativeCourses']
        if isinstance(optativeCourses, list):
            for optativeCourse in optativeCourses:
                nodeOptativeCourse(driver, {"fullName": optativeCourse})
                relationStudentOptativeCourse(driver, student, {"fullName": optativeCourse}, True)
        else:
            nodeOptativeCourse(driver, {"fullName": optativeCourses})
            relationStudentOptativeCourse(driver, student, {"fullName": optativeCourses}, True)

        optativeCourses = personObject['missingOptativeTopics']
        if isinstance(optativeCourses, list):
            for optativeCourse in optativeCourses:
                nodeOptativeCourse(driver, {"fullName": optativeCourse})
                relationStudentOptativeCourse(driver,student, {"fullName": optativeCourse}, False)
        else:
            nodeOptativeCourse(driver, {"fullName": optativeCourses})
            relationStudentOptativeCourse(driver, student, {"fullName": optativeCourses}, False)
            
        skills = personObject['transversalSkills']
        if isinstance(skills, list):
            for skill in skills:
                nodeSkill(driver, {"name": skill})
                relationStudentSkill(driver, student, {"name": skill}, "Transversal", True)
        else:
            nodeSkill(driver, {"name": skills})
            relationStudentSkill(driver, student, {"name": skills}, "Transversal", True)

        skills = personObject['missingTransversalSkills']
        if isinstance(skills, list):
            for skill in skills:
                nodeSkill(driver, {"name": skill})
                relationStudentSkill(driver, student, {"name": skill}, "Transversal", False)
        else:
            nodeSkill(driver, {"name": skills})
            relationStudentSkill(driver, student, {"name": skills}, "Transversal", False)

        skills = personObject['disciplinarySkills']
        if isinstance(skills, list):
            for skill in skills:
                nodeSkill(driver,{"name": skill})
                relationStudentSkill(driver, student, {"name": skill}, "Disciplinaria", True)
        else:
            nodeSkill(driver, {"name": skills})
            relationStudentSkill(driver, student, {"name": skills}, "Disciplinaria", True)

        skills = personObject['missingDisciplinarySkills']
        if isinstance(skills, list):
            for skill in skills:
                print("HOLA" + skill)
                nodeSkill(driver, {"name": skill})
                relationStudentSkill(driver, student, {"name": skill}, "Disciplinaria", False)
        else:

            nodeSkill(driver, {"name": skills})
            relationStudentSkill(driver, student, {"name": skills}, "Disciplinaria", False)

        extracurricularActivities = personObject['extracurricularActivities']
        if isinstance(extracurricularActivities, list):
            for extracurricularActivitie in extracurricularActivities:
                nodeExtracurricularActivity(driver, {"name": extracurricularActivitie})
                relationStudentCurricularActivity(driver, student, {"name": extracurricularActivitie}, personObject['extracurricularContribution'])

        else:
            nodeExtracurricularActivity(driver, {"name": extracurricularActivities})
            relationStudentCurricularActivity(driver, student, {"name": extracurricularActivities}, personObject['extracurricularContribution'])

        socialService = personObject['socialServiceFocus']
        if isinstance(socialService, list):
            for socialService in socialService:
                nodeSocialService(driver, socialService)
                relationStudentSocialService(driver, student, socialService, personObject['socialServiceContribution'], personObject['socialServiceArea'])
        else:
            nodeSocialService(driver, socialService)
            relationStudentSocialService(driver, student, socialService, personObject['socialServiceContribution'], personObject['socialServiceArea'])

        socialServiceArea = personObject['socialServiceAreaInternal']
        if isinstance(socialServiceArea, list):
            for area in socialServiceArea:
                nodeArea(driver, {"fullName": area})
                relationSocialServiceArea(driver, socialService, area)
                
        else:
            nodeArea(driver, {"fullName": area})
            relationSocialServiceArea(driver, socialService, socialServiceArea)

        #Datos de LinkedIn
        main(personObject['linkedinProfile'], student, driver)
        exit()
    
    driver.close()
