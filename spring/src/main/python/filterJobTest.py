import filterJob

settings = filterJob.setFilter
settings[0] = True
settings[1] = "Python Developer"

check = filterJob.filter(settings)

for i in check:
    print(i)

print("\nThen\n")

settings[8] = True
settings[9] = "0"

check = filterJob.filter(settings)

for i in check:
    print(i)

print("\nThen\n")

settings[9] = "1"

check = filterJob.filter(settings)

for i in check:
    print(i)