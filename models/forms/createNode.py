from neo4j import GraphDatabase


def nodeStudent(driver, student):
    with driver.session() as session:
        session.run(
            """
            MERGE (o:student {publicIdentifier: $publicIdentifier, fullName: $fullName, studentId: $studentId, admissionDate: $admissionDate, linkedinProfile: $linkedinProfile, contactPermission: $contactPermission, yearsToGraduate: $yearsToGraduate})
            """,
            publicIdentifier=student['publicIdentifier'],
            fullName=student['fullName'],
            studentId=student['studentId'],
            admissionDate=student['admissionDate'],
            linkedinProfile=student['linkedinProfile'],
            contactPermission=student['contactPermission'],
            yearsToGraduate=student['yearsToGraduate'],
        )


def nodeAdvisor(driver, advisor):
    with driver.session() as session:
        session.run(
            """
            MERGE (o:advisor {fullName: $fullName})
            """,
            fullName=advisor['fullName'],
        )


def nodeArea(driver, area):
    with driver.session() as session:
        session.run(
            """
            MERGE (o:area {fullName: $fullName})
            """,
            fullName=area['fullName'],
        )


def nodeExtracurricularActivity(driver, activity):
    with driver.session() as session:
        session.run(
            """
            MERGE (o:curricularActivity {name: $name})
            """,
            name=activity['name'],
        )


def nodeLenguage(driver):
    with driver.session() as session:
        session.run(
            """
            MERGE (o:language {name: $name})
            """,
            name='Inglés',
        )


def nodeOptativeCourse(driver, course):
    with driver.session() as session:
        session.run(
            """
            MERGE (o:optativeCourse {fullName: $fullName})
            """,
            fullName=course['fullName'],
        )


def nodePT(driver, PT):
    with driver.session() as session:
        session.run(
            """
            MERGE (o:PT {fullName: $fullName})
            """,
            fullName=PT['fullName'],
        )


def nodeSkill(driver, skill):
    with driver.session() as session:
        session.run(
            """
            MERGE (o:skill {name: $name})
            """,
            name=skill['name'],
        )


def nodeSocialService(driver, name):
    with driver.session() as session:
        session.run(
            """
            MERGE (o:socialService {name: $name})
            """,
            name=name,
        )


def nodeSocialService(driver, name):
    with driver.session() as session:
        session.run(
            """
            MERGE (o:socialService {name: $name})
            """,
            name=name,
        )
