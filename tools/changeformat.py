
import os



length=500
path_original='./dataset_original/'
value=[]
#test
with open(path_original+"15.csv", 'r+') as f:
    d = f.read()
    t = d.replace('trace', 'rtt')
    f.seek(0, 0)
    f.write(t)
#change format
for (path_original, dirs, files) in os.walk(path_original):
    print(files)
    for filename in files:
        print(filename)
        with open(path_original+filename, 'r+') as f:
            d = f.read()
            t = d.replace('trace', 'rtt')
            f.seek(0, 0)
            f.write(t)
        with open(path_original+filename, 'r+') as f:
            d = f.read()
            t = d.replace('cpt', 'cp')
            f.seek(0, 0)
            f.write(t)
        with open(path_original+filename, 'r+') as f:
            d = f.read()
            t = d.replace(',', ';')
            f.seek(0, 0)
            f.write(t)
        with open(path_original+filename, 'r+') as f:
            d = f.read()
            t = d.replace(' " ', ' ')
            f.seek(0, 0)
            f.write(t)




