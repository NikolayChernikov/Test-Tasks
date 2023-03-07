class TreeStore:
    def __init__(self,items):
        self.items = items
    
    #Return the original array of elements
    def getAll(self):
        return self.items
    
    #Return an element object by id
    def getItem(self,id):
        return (next(x for x in self.items if x["id"] == id))
    
    #Takes an element id and returns an array of elements that are children for that element
    def getChildren(self,parent):
        return list(filter(lambda item: item['parent'] == parent, self.items))
    
    #Takes an element id and returns an array from the chain of parent elements
    def getAllParents(self,children):
        returned_list = []
        while children != "root":
            for i in self.items:
                if i["id"] == children:
                    children = i["parent"]
                    returned_list.append(i)
        returned_list.pop(0)
        return returned_list


items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]
ts = TreeStore(items)


ts.getAll()
ts.getItem(7)
ts.getChildren(5)
ts.getAllParents(7)
"""
#For test

print(ts.getAll())
print(ts.getItem(7))
print(ts.getChildren(5))
print(ts.getAllParents(7))
"""
