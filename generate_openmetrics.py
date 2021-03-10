import random
import numpy as np
import datetime
import time

# https://medium.com/tlvince/prometheus-backfilling-a92573eb712c

"""
# HELP pcf_ticket_closed_total total number of PCF tickets openend
# TYPE pcf_ticket_closed gauge
pcf_ticket_closed 2.0 1609954636
# HELP pcf_ticket_opened number of PCF tickets openend
#TYPE pcf_ticket_opened gauge
pcf_ticket_closed 2.0 1609954636
# EOF
"""

number_of_days_to_generate = 30
max_number_of_opened_tickets = 10

opened_tickets = np.random.randint(low=max_number_of_opened_tickets, size=number_of_days_to_generate)
closed_tickets = []
for n in opened_tickets:
    closed_tickets.append(random.randint(0, n))

def format_metric(name, value, timestamp):
    labels = 'instance="10.213.49.168:9090"'
    return "%s{%s} %f %d" % (name, labels, value, timestamp)

today = datetime.date.fromtimestamp(time.time())
start_date = today - datetime.timedelta(days=number_of_days_to_generate)

opened_output = []
onboarded_team_output = []
closed_output = []
total_opened = 0
total_closed = 0
unixtime = time.mktime(start_date.timetuple())
resolution_sec = 60
team_onboaded_data = [3, 3, 3, 3, 3, 3, 3, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9]

for i in range(number_of_days_to_generate):
    total_opened += opened_tickets[i]
    total_closed += closed_tickets[i]
    for n in range(int(86400/resolution_sec)):
        opened_output.append(format_metric("pcf_ticket_opened_total", float(total_opened), unixtime))
        closed_output.append(format_metric("pcf_ticket_closed_total", float(total_closed), unixtime))
        onboarded_team_output.append(format_metric("onboarded_team", float(team_onboaded_data[i]), unixtime))
        unixtime += resolution_sec



output = []
output.append("# HELP pcf_ticket_opened_total total number of PCF tickets opened")
output.append("# TYPE pcf_ticket_opened_total counter")
output = output + opened_output
output.append("# HELP pcf_ticket_closed_total total number of PCF tickets closed")
output.append("# TYPE pcf_ticket_closed counter")
output = output + closed_output
output.append("# HELP onboarded_team number of dev team on-boarded on PCF")
output.append("# TYPE onboarded_team counter")
output = output + onboarded_team_output
output.append("# EOF")

print('\n'.join(output))
