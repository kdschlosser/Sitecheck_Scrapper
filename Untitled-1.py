from collections import namedtuple
from types import SimpleNamespace as Namespace

import json
import jsonpickle

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

def loadProjects(self, user):
    with open('env/projects.json', 'r') as userdata:
        data=userdata.read()
        # projectlist = json.loads(data)
        # for project in projectlist:
        #     x = json2obj(project)
        #     print(X)
        # # data = StringIO(projectlist)
        return data

projects = loadProjects('butts', 'dan edens')
# for project in projects:
x = json.loads(projects, object_hook=lambda d: Namespace(**d))
    # print(x)
    # print(x)
# f = [('skip', 'false'), ('group', 'true'), ('name', 'capitolcomplex'), ('proj', ['null']), ('planarray', ['143', '124', '127']), ('hassite', 'amp')]
# rint(project['name'])
# x = tuple(project.items())





# d = { 'a': 1, 'b': 2, 'c': 3 }
# a = zip(d.keys(), d.values())
# # [('a', 1), ('c', 3), ('b', 2)]
# b = zip(d.values(), d.keys())
# # [(1, 'a'), (3, 'c'), (2, 'b')]
# print(a)