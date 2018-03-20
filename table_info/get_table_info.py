from collections import defaultdict
def get_table(tab_name):
    dic = defaultdict(dict)
    border_table = {"border_info.state_name":'string', 'border_info.border':"string"}
    dic['border_info'] = border_table

    city_table = {'city.city_name':'string','city.population':'number','city.country_name':'string','city.state_name':'string'}
    dic['city'] = city_table

    highlow_table = {'highlow.state_name':'string','highlow.highest_elevation':'number','highlow.lowest_point':'string','highlow.highest_point':'string',
                     'highlow.lowest_elevation':'number'}
    dic['highlow'] = highlow_table

    lake_table = {'lake.lake_name':'string','lake.area':'number','lake.country_name':'string','lake.state_name':'string'}
    dic['lake'] = lake_table

    mountain_table = {'mountain.mountain_name':'string','mountain.mountain_altitude':'number','mountain.country_name':'string','mountain.state_name':'string'}
    dic['mountain'] = mountain_table

    river_table = {'river.river_name':'string','river.length':'number','river.country_name':'string','river.traverse':'string'}
    dic['river'] = river_table

    state_table = {'state.state_name':'string','state.population':'number','state.area':'number','state.country_name':'string',
                   'state.capital':'string','state.density':'string'}
    dic['state'] = state_table
    return list(dic[tab_name].keys()), list(dic[tab_name].values())