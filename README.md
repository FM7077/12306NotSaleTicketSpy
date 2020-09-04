# What is this bot?

A bot that can automatically spy those un-sale ticket.

Once the ticket is onsale, it will inform user.

# data source

[Stations info all around China Mainland](https://kyfw.12306.cn/otn/resources/js/framework/station_name.js)

[A example train info page](https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=广州南,IZQ&ts=潮汕,CBQ&date=2020-09-29&flag=N,N,Y)

and in this page, can easily find out: use the following [url](https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2020-09-29&leftTicketDTO.from_station=IZQ&leftTicketDTO.to_station=CBQ&purpose_codes=ADULT) to get the trains info from 广州南 to 潮汕 on 2020-09-29
