from pprint import pprint
import requests
import json

def check_repos(name, filename):
    responce = requests.get('https://api.github.com/users/' + name + '/repos')
    data = {}

    for i in range(len(responce.json())):
        repo_name = responce.json()[i]['name']
        data[f'name{i + 1}'] = repo_name

    with open(filename, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    check_repos('rtrtr3773', 'rtr_repos.txt')