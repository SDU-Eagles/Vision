import csv
import datetime

# Create log-file with uniqe name in write mode
time = str(datetime.datetime.now())[11:19]
dateid = time.replace(':', '')
log = open('logs/log_' + dateid + '.csv', 'w', newline='')
logger = csv.writer(log, dialect='excel')
logger.writerow(['Character', 'Color', 'Score',' Time'])

def Logging(ch, color, score):
    row = [ch, color, int(score)]
    logger.writerow(row + [datetime.datetime.now()])


