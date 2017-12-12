import os, sys, json, requests, time, getpass
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class managerNode():
    def __init__(self):
        self.workerCount = input("Enter the number of worker nodes : ")
        self.workerCount = int(self.workerCount)
        self.currWorkerCount = 0    #Number connected to the managerNode
        self.timeStart = 0.0
        self.CClist = []

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

class repoGet(Resource):
    def __init__(self):
        super(repoGet, self).__init__()
        global managerServer
        self.reqparser = reqparse.RequestParser()
        self.server = managerServer

        self.reqparser.add_argument('pullState', type=int, location = 'json')
        self.reqparser.add_argument('complexity', type=float, location='json')

    def get(self):
        args = self.reqparser.parse_args()
        if args['pullState'] == False:
            return {'repo': "https://github.com/kaushal0/ChatServer"}
        if args['pullState'] == True:
            self.server.currWorkerCount += 1
            if self.server.currWorkerCount == self.server.workerCount:
                self.server.timeStart = time.time()  # Starting timer
            print("Worker :",self.server.currWorkerCount)

api.add_resource(repoGet, "/repo", endpoint="repo")

class cycloAPI(Resource):
    def __init__(self):
        global managerServer
        self.server = managerServer
        super(cycloAPI, self).__init__()
        self.reqparser = reqparse.RequestParser()

        self.reqparser.add_argument('commits', type=str, location = 'json')
        self.reqparser.add_argument('complexity', type=float, location='json')

    def get(self):
        if self.server.currWorkerCount < self.server.workerCount:
            time.sleep(0.1)
            return {'sha': -2}
        if len(self.server.commitTotal) == 0:
            return {'sha': -1}
        Value = self.server.commitTotal[0]
        del self.server.commitTotal[0]
        print("Sent: {}".format(Value))
        return {'sha':Value}

    def post(self):
        args = self.reqparser.parse_args()
        print("Received sha {}".format(args['commits']))
        print("Received complexity {}".format(args['cc']))
        self.server.CClist.append({'sha':args['commits'], 'complexity':args['complexity']})
        print(self.server.CClist)
        print(self.server.commitTotal)
        if len(self.server.CClist) == self.server.totalNumberOfCommits:
            timeEnd = time.time() - self.server.timeStart
            print("Time Taken (seconds) : ", timeEnd)
            print(len(self.server.CClist))
            averageCC = 0
            for x in self.server.CClist:
                if x['complexity'] > 0:
                    averageCC += x['complexity']
                else:
                    print("Commit {} has no computable files".format(x['sha']))
            averageCC = averageCC / len(self.server.CClist)
            print("Cyclometric Complexity of the Repository: ",averageCC)
        return {'success':True}

api.add_resource(cycloAPI, "/cyclomatic", endpoint="cyclomatic")


if __name__ == "__main__":
    managerServer = managerNode()  # initializing an instance of managerNode()
    app.run()
