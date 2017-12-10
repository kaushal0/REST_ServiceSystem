import os,sys,requests,json

if __name__ == '__main__':

    ip = input('Enter managerNode IP : ')
    port = input('Enter the port : ')
    reqURL = 'http://' + ip + '/' + port
    repoURL = reqURL + '/repo'

    commits = requests.get(repoURL,json = {'pullState' : False})
    commitData = json.loads(commits.text)
    URL = commitData['repo']

    commits = requests.get(repoURL,json = {'pullState' : True})          #Notify managerNode for success
