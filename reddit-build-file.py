import csv
import re
import os

file = open("redditSubmissions.csv")
data = csv.DictReader(file, delimiter=',', quotechar='"', dialect='excel')

authors = []
count = 0

data_out = []

for row in data:
    count += 1
    if count % 1000 == 0:
        print str(count) + " loaded so far..."

    if row['username'] not in authors:
        i = len(authors)
        authors.append(row['username'])

    img = row['#image_id']
    auth = authors.index(row['username'])

    data_out.append((img,auth))

file.close()
print "++++++ Moving onto writing the out file..."
count = 0

write_file = open("reddit-data-out.csv", "a+")
csv_writer = csv.writer(write_file, delimiter=',',
                                lineterminator='\r\n')

for d in data_out:
    count += 1
    if count % 1000 == 0:
        print str(count) + " loaded so far..."

    csv_writer.writerow(d)

write_file.close()