import os, sys, json, requests, time, getpass

class managerNode():
    def __init__(self):
        self.workerCount = input("Enter the number of worker nodes : ")
        self.workerCount = int(self.workerCount)
        self.currWorkerCount = 0    #Number connected to the managerNode
        #request repository info using the github API
        gitUsername = input("Type your Github username to use authenticated requests, or press return to use unauthenitcated requests: ")
        print(len(gitUsername))
        if len(gitUsername) != 0:
            gitPassword = getpass.getpass("Type your Github password (input is hidden): ")

        self.commitTotal = []  # List containing all commit sha values

        if len(gitUsername) == 0:
            r = requests.get("https://api.github.com/repos/kaushal0/ChatServer/commits?page={}&per_page=100")
        else:
            r = requests.get("https://api.github.com/repos/kaushal0/ChatServer/commits?page={}&per_page=100", auth=(gitUsername, gitPassword))
        jsonData = json.loads(r.text)

        for x in jsonData:
            self.commitTotal.append(x['sha'])
            print("Commits : {}".format(x['sha']))
        print("\n")
        self.totalNumberOfCommits = len(self.commitTotal)  # Total number of commits in repo
        print("Number of commits: {}".format(self.totalNumberOfCommits))


if __name__ == "__main__":
    managerServer = managerNode()  # initializing an instance of managerNode()
