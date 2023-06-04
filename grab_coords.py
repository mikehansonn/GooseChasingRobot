import SparkfungpsClass41


compass = SparkfungpsClass41.GpsClass()

i = 0

new_list = []

while i <= 16:
    list = compass.get_coordinates()
    new_list.append(''.join([str(list[0]), ",", str(list[1])]))
    check = input("L")



for i in new_list:
    print(i)