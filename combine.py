from operation_class.modify import Modify
from operation_class.filter import In
from operation_class.project import Project
from operation_class.project_connect import Project_Connect


#c,T-->T(Project). T(connect), s,F-->s. c.F-->c. c,v-->Filter_
def composition(node1,node2,option):
    if option == 'Project':
        return Project(node1.val,node2.val)
    if option == 'Connect':
        return Project_Connect(node1.val,node2.val)
    if option == 'modify':
        return Modify(node1.val,node2.val)
    if option == 'In':
        return In(node1.val,node2.val)


