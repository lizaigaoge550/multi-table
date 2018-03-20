from operation_class.modify import Modify
from operation_class.filter import In
from operation_class.project import Project
from type_raising import extract_opt


#c,T-->T(Project). T(connect), s,F-->s. c.F-->c. c,v-->Filter_
def composition(node1,node2,option):
    option = extract_opt(option)
    if option == 'Project':
        return Project(node1, node2)

    if option == 'modify':
        return Modify(node1,node2)
    if option == 'In':
        return In(node1,node2)


