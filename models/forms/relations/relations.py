from neo4j import GraphDatabase


def relationAdvisorPT(driver, advisor, PT):
    with driver.session() as session:
        session.run(
            """
            MATCH (a:advisor {fullName: $fullNameAdvisor}), (p:PT {fullName: $fullNamePT})
            MERGE (a)-[:HAS_PT]->(p)
            """,
            fullNameAdvisor=advisor['fullName'],
            fullNamePT=PT['fullName']
        )

def relationAdvisorStudent(driver, advisor, student):
    with driver.session() as session:
        session.run(
            """
            MATCH (a:advisor {fullName: $fullNameAdvisor}), (s:student {publicIdentifier: $publicIdentifierStudent})
            MERGE (a)-[:HAS_STUDENT]->(s)
            """,
            fullNameAdvisor=advisor['fullName'],
            publicIdentifierStudent=student['publicIdentifier']
        )

def relationPTArea(driver, PT, area):
    with driver.session() as session:
        session.run(
            """
            MATCH (p:PT {fullName: $fullNamePT}), (a:area {fullName: $fullNameArea})
            MERGE (p)-[:HAS_AREA]->(a)
            """,
            fullNamePT=PT['fullName'],
            fullNameArea=area['fullName']
        )

def relationSocialServiceArea(driver, socialService, area):
    with driver.session() as session:
        session.run(
            """
            MATCH (s:socialService {name: $name}), (a:area {fullName: $fullName})
            MERGE (s)-[:HAS_AREA]->(a)
            """,
            name=socialService,
            fullName=area
        )

def relationStudentCurricularActivity(driver, student, activity, help):
    help = True if help == "Sí" else False
    with driver.session() as session:
        session.run(
            """
            MATCH (s:student {publicIdentifier: $publicIdentifier}), (a:curricularActivity {name: $name})
            MERGE (s)-[:HAS_CURRICULAR_ACTIVITY{help: $help}]->(a)
            """,
            publicIdentifier=student['publicIdentifier'],
            name=activity['name'],
            help=help
        )

def relationStudentLanguage(driver, student, language, level, levelGraduation):
    with driver.session() as session:
        session.run(
            """
            MATCH (s:student {publicIdentifier: $publicIdentifier}), (l:language {name: $name})
            MERGE (s)-[:HAS_LANGUAGE{level: $level, levelGraduation: $levelGraduation}]->(l)
            """,
            publicIdentifier=student['publicIdentifier'],
            name=language,
            level=level,
            levelGraduation=levelGraduation
        )

def relationStudentOptativeCourse(driver, student, course, help):
    with driver.session() as session:
        session.run(
            """
            MATCH (s:student {publicIdentifier: $publicIdentifier}), (c:optativeCourse {fullName: $fullName})
            MERGE (s)-[:HAS_OPTATIVE_COURSE{help: $help}]->(c)
            """,
            publicIdentifier=student['publicIdentifier'],
            fullName=course['fullName'],
            help=help
        )

def relationStudentPT(driver, student, PT, help, type):
    help = True if help == "Sí" else False
    with driver.session() as session:
        session.run(
            """
            MATCH (s:student {publicIdentifier: $publicIdentifier}), (p:PT {fullName: $fullName})
            MERGE (s)-[:HAS_PT{help: $help, type: $type}]->(p)
            """,
            publicIdentifier=student['publicIdentifier'],
            fullName=PT['fullName'],
            help=help,
            type=type
        )

def relationStudentSkill(driver, student, skill, type, help):
    with driver.session() as session:
        session.run(
            """
            MATCH (s:student {publicIdentifier: $publicIdentifier}), (sk:skill {name: $name})
            MERGE (s)-[:HAS_SKILL{type: $type, help: $help}]->(sk)
            """,
            publicIdentifier=student['publicIdentifier'],
            name=skill['name'],
            type=type,
            help=help
        )

def relationStudentSocialService(driver, student, socialService, help, internalexternal):
    help = True if help == "Sí" else False
    with driver.session() as session:
        session.run(
            """
            MATCH (s:student {publicIdentifier: $publicIdentifier}), (a:socialService {name: $name})
            MERGE (s)-[:HAS_SOCIAL_SERVICE{help: $help, internalexternal: $internalexternal}]->(a)
            """,
            publicIdentifier=student['publicIdentifier'],
            name=socialService,
            help=help,
            internalexternal=internalexternal
        )