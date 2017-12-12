import os,sys,requests,json
import subprocess

if __name__ == '__main__':

    ip = input('Enter managerNode IP : ')
    port = input('Enter the port : ')
    reqURL = 'http://' + ip + ':' + port
    repoURL = reqURL + '/repo'
    cycloURL = reqURL + '/cyclomatic'
    commitsDone= 0

    commits = requests.get(repoURL,json = {'pullState' : False})
    commitData = json.loads(commits.text)
    URL = commitData['repo']

    subprocess.call(["bash", "initScript.sh", URL])
    print("Initialization Complete..")

    commits = requests.get(repoURL,json = {'pullState' : True})         #Notify managerNode for success

    while True:
        cyclo = requests.get(cycloURL)
        print("Got Cyclo")
        json_data = json.loads(cyclo.text)
        print(json_data)
        print("Received: ",json_data['sha'])
        if json_data['sha'] == -2:       # Polling for manager to give commits
            print("Polling")
        else:
            subprocess.call(["bash", "getCommit.sh", json_data['sha']])
