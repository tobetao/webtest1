import csv

with open('publisher.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(20):
        writer.writerow(['%d' % (i%10), 'publisher %d' %i, '%.02f' % (i/100.0), 'writer %d'%i, 'note %d' %i, 'publisher status %d' %(i%5+1)])
