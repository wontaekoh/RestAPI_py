import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 10, "name": "RestAPI", "views": 100},
        {"likes": 20, "name": "Python Basics", "views": 200},
        {"likes": 30, "name": "Python Intermediate", "views": 300},
        {"likes": 40, "name": "Java Basics", "views": 400},
        {"likes": 50, "name": "Database", "views": 500}]

# Writing data
for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

# Retrive data
input()
response = requests.get(BASE + "video/1")
print(response.json())

# input()
# response = requests.get(BASE + "video/")
# print(response.json())

# Update data
input()
response = requests.patch(BASE + "video/1", {"views": 999, "likes": 60})
print(response.json())

# Delete data
input()
response = requests.delete(BASE + "video/1")
print(response)
