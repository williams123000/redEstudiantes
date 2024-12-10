import requests
import json
from config.apiKeys import API_KEYS
from utils.linkedin import validateLinkedInURL, notURL
from models.linkedin.createNode import nodeStudent, nodePosition, nodeSchool, nodeSkills, nodeLanguage, nodeRecommendation, nodeCertification, nodeLocation

def petition(url):
    index_keys = 0
    while index_keys < len(API_KEYS):
        url_api = "https://api.scrapin.io/enrichment/profile"
        querystring = {"apikey": API_KEYS[index_keys], "linkedInUrl": url}
        response = requests.get(url_api, params=querystring)
        if response.status_code == 200:
            return json.loads(response.text)
        index_keys += 1
    return None

def extractData(url):
    if (validateLinkedInURL(url)):

        dataLinkedIn_ = petition(url)
        return dataLinkedIn_
    else:
        if (notURL(url)):
            print("User found")
            urlNew = f"https://www.linkedin.com/in/{url}/"
            dataLinkedIn_ = petition(urlNew)
            return dataLinkedIn_
        else:
            return None

def main(url, student, driver):
    dataLinkedIn = extractData(url)
    if dataLinkedIn is not None:
        print(json.dumps(dataLinkedIn, indent=4, ensure_ascii=False))
        nodeStudent(dataLinkedIn, student, driver)
        nodePosition(dataLinkedIn, student, driver)
        nodeSchool(dataLinkedIn, student, driver)
        nodeSkills(dataLinkedIn, student, driver)
        nodeLanguage(dataLinkedIn, student, driver)
        nodeRecommendation(dataLinkedIn, student, driver)
        nodeCertification(dataLinkedIn, student, driver)
        nodeLocation(dataLinkedIn, student, driver)