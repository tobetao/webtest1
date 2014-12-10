import csv

with open('songs.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(100):
        writer.writerow([i, '%.02f' % (i / 100.0), '%d' % (i%10), 'song %d' % i, 'writer %d' % (i % 20), 'status %d' % (i%4 + 1)])
