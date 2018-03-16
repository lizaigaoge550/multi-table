
def get_table():
    t_name = 'shark_attack'
    Table = {"country":'string', 'gender':'string', 'fatality':'string','activity':'string','attack':'number','year':'date', 'count(t)':'number'}
    # t_name = 'job'
    # Table = {'field': 'string', 'title': 'string', 'posting_date': 'date', 'desired_year_experience': 'number',
    #          'required_academic_qualification': 'string', 'company': 'string', 'area': 'string',
    #          'city': 'string', 'country': 'string', 'programming_language': 'string', 'salary': 'number',
    #          'plantform': 'string', 'count(t)': 'number'
    #          }
    # t_name = '鲨鱼'
    # Table = {"国家":'string', '性别':'string', '致命性':'string','活动':'string',
    # '攻击':'number','年':'date', 'count(t)':'number'}

    # t_name = '汽车'
    # Table = {"年": "date", "品牌": "string", "类别": "string", "型号": "string", "销量": "number",
    #          "count(t)": "number"
    #          }
    return t_name, Table