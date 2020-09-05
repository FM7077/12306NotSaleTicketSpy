import requests
import json
def spyTicket(spyInfo):
    result = {
        'status': '',
        'data': {}
    }
    headers = {
        'Cookie': '_jc_save_toDate=2050-09-09'
    }
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=' +\
        spyInfo['date'] + '&leftTicketDTO.from_station=' +\
        spyInfo['depTeleCode'] + '&leftTicketDTO.to_station=' +\
        spyInfo['desTeleCode'] + '&purpose_codes=ADULT'
    ticketsStr = requests.get(url, headers = headers).text
    tickets = json.loads(ticketsStr)['data']['result']
    for index, ticket in enumerate(tickets):
        ticket = ticket.split('|')
        tickets[index] = {
            'tno': ticket[3],
            'depStation': ticket[6],
            'desStation': ticket[7],
            'depTime': ticket[8],
            'desTime': ticket[9],
            'takeTime': ticket[10],
            'topSeat': ticket[32],
            'firstSeat': ticket[31],
            'secondSeat': ticket[30],
            'standTicket': 0,
            'topBerth': ticket[21],
            'softBerth': ticket[23],
            'dynaBerth': ticket[33],
            'hardBerth': ticket[28],
            'remark': ticket[1]
        }
    try:
        ticket = next(t for t in tickets if t['tno'] == spyInfo['tno'])
        if ticket['remark'] == '预订':
            result['status'] = True
            result['data'] = ticket
        else:
            result['status'] = False
            result['data'] = 'notSale'
    except:
        result['status'] = False
        result['data'] = 'unfound'
    return result