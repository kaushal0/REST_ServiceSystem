Dependencies - Python3, Flask, Flask-RESTful, requests, radon
The following dependencies need to be installed using the command - pip install
Flask==0.12.2
Flask-RESTful==0.3.6
radon==2.1.1

Repository used: https://github.com/kaushal0/ChatServer

The project is used to find the cyclomatic complexity of a Github Repository
A manager node is used distribute commits from the repository to worker nodes.
The worker nodes request the SHA for a commit whenever they are free to do work and compute the complexity.

Starting the System:
Start manager node (ManagerNode.py) by running "python ManagerNode.py". Once the server has started, user needs to input the number of nodes that it will use.
The worker node (WorkerNode.py) is then started using "python WorkerNode.py" command. WorkerNodes are to be kept in separate directories.

The worker starts polling the manager until the required Worker Nodes are matched. If they match a timer is started and the workers request for commits, compute the average cyclomatic complexity for that commit and respond to the manager node with the results. After all commits have been computed. After all commits are completed, timer is stopped to calculate the total time and the Average complexity.

The benifit of such a system is that the time taken to return results is shorter as resources are shared across the worker nodes connected.

Kaushal C Gadhia - 17310654
