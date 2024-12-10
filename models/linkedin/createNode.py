from datetime import datetime

from utils.hash_utils import generate_unique_id
from models.forms.createNode import nodeSkill
from models.forms.relations.relations import relationStudentSkill


def nodeStudent(dataLinkedIn, student, driver):
    person = dataLinkedIn['person']
    publicIdentifierLinkedin = person['publicIdentifier']
    firstName = person['firstName']
    lastName = person['lastName']
    location = person['location']
    photoUrl = person['photoUrl']
    creationDate = person['creationDate']
    followerCount = person['followerCount']
    with driver.session() as session:
        session.run(
            """
            MATCH (o:student {studentId: $studentId})
            SET o.publicIdentifierLinkedin = $publicIdentifierLinkedin,
                o.firstName = $firstName,
                o.lastName = $lastName,
                o.location = $location,
                o.photoUrl = $photoUrl,
                o.followerCount = $followerCount
            """,
            studentId=student['studentId'],
            publicIdentifierLinkedin=publicIdentifierLinkedin,
            firstName=firstName,
            lastName=lastName,
            location=location,
            photoUrl=photoUrl,
            # creationDate=creationDate,
            followerCount=followerCount
        )


def nodePosition(dataLinkedIn, student, driver):
    positions = dataLinkedIn['person']['positions']
    positions = positions['positionHistory']
    for position in positions:
        titlePosition = position['title']
        descriptionPosition = position['description']
        startEndDatePosition = position['startEndDate']
        startDatePosition = f"{
            startEndDatePosition['start']['month']} / {startEndDatePosition['start']['year']}"
        if (startEndDatePosition['end'] == None):
            endDatePosition = "Now"
        else:
            endDatePosition = f"{
                startEndDatePosition['end']['month']} / {startEndDatePosition['end']['year']}"
        if ('contractType' not in position):
            contractTypePosition = "n/a"
        else:
            contractTypePosition = position['contractType']

        with driver.session() as session:
            session.run(
                """
                    MATCH (s:student {publicIdentifierLinkedin: $publicIdentifierLinkedin})
                    MERGE (p:Position {title: $title, description: $description, startDate: $startDate, endDate: $endDate, contractType: $contractType})
                    MERGE (s)-[:HAS_POSITION]->(p)
                    """,
                publicIdentifierLinkedin=dataLinkedIn['person']['publicIdentifier'],
                title=titlePosition,
                description=descriptionPosition,
                startDate=startDatePosition,
                endDate=endDatePosition,
                contractType=contractTypePosition
            )

            session.run(
                """
                    MATCH (p:Position {title: $title})
                    MERGE (c:Company {name: $name})
                    MERGE (p)-[:WORKS_IN]->(c)
                    """,
                title=titlePosition,
                name=position['companyName']
            )

            # se agrego
            session.run(
                """
                    MATCH (p:Position {title: $title})
                    MERGE (l:Location {name: $name})
                    MERGE (p)-[:LOCATED_IN]->(l)
                    """,
                title=titlePosition,
                name=position['companyLocation']
            )

    if ('company' in dataLinkedIn):
        if (dataLinkedIn['company'] != None):
            with driver.session() as session:
                session.run(
                    """
                                MATCH (p:Company {name: $nameCompany})
                                MERGE (l:Industry {name: $nameIndustry})
                                MERGE (p)-[:BELONGS_TO]->(l)
                                """,
                    nameCompany=dataLinkedIn['company']['name'],
                    nameIndustry=dataLinkedIn['company']['industry']
                )


def nodeSchool(dataLinkedIn, student, driver):

    schools = dataLinkedIn['person']['schools']
    schools = schools['educationHistory']

    for school in schools:
        startEndDateEducation = school['startEndDate']
        startDateEducation = f"{
            startEndDateEducation['start']['month']} / {startEndDateEducation['start']['year']}"
        if (startEndDateEducation['end'] == None):
            endDateEducation = "Now"
        else:
            endDateEducation = f"{
                startEndDateEducation['end']['month']} / {startEndDateEducation['end']['year']}"

        if (school['degreeName'] == None):
            school['degreeName'] = "n/a"

        uuidSchool = generate_unique_id(
            dataLinkedIn['person']['publicIdentifier'], school['schoolName'])

        with driver.session() as session:

            session.run(
                """
                    MERGE (o:School {name: $name, uuidSchool: $uuidSchool, degree: $degree, startDate: $startDate, startDate: $startDate, endDate: $endDate})
                    """,
                name=school['schoolName'],
                uuidSchool=uuidSchool,
                degree=school['degreeName'],
                startDate=startDateEducation,
                endDate=endDateEducation,
            )

            session.run(
                """
                    MATCH (s:student {publicIdentifierLinkedin: $publicIdentifierLinkedin})
                    MATCH (sc:School {uuidSchool: $uuidSchool})
                    MERGE (s)-[:STUDIED_IN]->(sc)
                    """,
                publicIdentifierLinkedin=dataLinkedIn['person']['publicIdentifier'],
                uuidSchool=uuidSchool,
            )


def nodeSkills(dataLinkedIn, student, driver):
    skills = dataLinkedIn['person']['skills']
    for skill in skills:
        nodeSkill(driver, {"name": skill})
        type = "Transversal"  # getAISkillCategory(skill)

        relationStudentSkill(driver, student, {"name": skill}, type, True)


def nodeLanguage(dataLinkedIn, student, driver):  # Cambiar
    languages = dataLinkedIn['person']['languages']
    for language in languages:
        print(language)


def nodeRecommendation(dataLinkedIn, student, driver):  # Cambiar
    recommendations = dataLinkedIn['person']['recommendations']
    recommendations = recommendations['recommendationHistory']

    for recommendation in recommendations:
        print(recommendation)


def nodeCertification(dataLinkedIn, student, driver):

    def parse_issued_date(issued_date_str):
        # Extrae el mes y el año de la cadena
        try:
            return datetime.strptime(issued_date_str.replace("Issued ", ""), "%b %Y").date()
        except ValueError:
            # Manejo de errores si el formato es incorrecto
            print(f"Error al procesar la fecha: {issued_date_str}")
            return None

    certifications = dataLinkedIn['person']['certifications']
    certifications = certifications['certificationHistory']
    print("Certifications")
    print(certifications)

    # Crear nodos y la relación entre ellos
    with driver.session() as session:
        for certification in certifications:
            print(certification)
            # Convertir la fecha
            issued_date = parse_issued_date(certification['issuedDate'])

            # Crear nodos y relación solo si la fecha es válida
            if issued_date:
                session.run(
                    """
                        MERGE (o:OrgCertification {organizationName: $organizationName})
                        MERGE (c:Certification {name: $name})
                        MERGE (o)-[:CERTIFY]->(c)
                        """,
                    organizationName=certification['organizationName'],
                    name=certification['name'],
                )

                session.run(
                    """
                        MATCH (s:student {publicIdentifierLinkedin: $publicIdentifierLinkedin})
                        MATCH (c:Certification {name: $name})
                        MERGE (s)-[:HAS_CERTIFICATION {issuedDate: $issuedDate}]->(c)
                        """,
                    publicIdentifierLinkedin=dataLinkedIn['person']['publicIdentifier'],
                    name=certification['name'],
                    issuedDate=issued_date,
                )


def nodeLocation(dataLinkedIn, student, driver):
    location = dataLinkedIn['person']['location']
    print(location)
    with driver.session() as session:
        session.run(
            """
                MATCH (s:student {publicIdentifierLinkedin: $publicIdentifierLinkedin})
                MERGE (l:Location {name: $name})
                MERGE (s)-[:LIVES_IN]->(l)
                """,
            publicIdentifierLinkedin=dataLinkedIn['person']['publicIdentifier'],
            name=location,
        )
