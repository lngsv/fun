# print lines from 10 to 20 (21q not to read file tail)
sed -n '10,20p; 21q' filename
