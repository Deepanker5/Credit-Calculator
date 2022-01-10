def calculatecreditminutes(totaltime, dailyworkminutes):
    creditminutes = totaltime - dailyworkminutes
    return creditminutes


def calculatetotaltime(timehours, timeminutes):
    totaltimeminutes = timehours * 60 + timeminutes
    return totaltimeminutes


def main():
    totalcreditminutes = 0
    dailyworkhours = input("Enter your daily working hours. Separate the hours and minutes by a comma (h,min):\n")
    while True:
        hours_list = dailyworkhours.split(",")
        try:
            if len(hours_list) == 2:
                hours_list[0] = int(hours_list[0])
                hours_list[1] = int(hours_list[1])
                break
            else:
                dailyworkhours = input("Invalid input! Enter the hours and minutes separated by a comma:\n")
        except ValueError:
            dailyworkhours = input("Invalid input! Enter integers separated by a comma:\n")

    maxlimit = int(input("What are the maximum hours to be in credit?\n"))
    minlimit = int(input("What are the maximum hours to be in deficit?\n"))
    filename = input("Enter the name of the file containing the working hours:\n")
    try:
        file = open(filename, 'r')
        linelist = file.readlines()
        partslist = []
        print("")
        print("Day        | Working time    | Gained credit hours")
        print("--------------------------------------------------")
        for line in linelist:
            if linelist.index(line) == 0:
                continue
            else:
                line = line.rstrip()
                parts = line.split(",")
                partslist.append(parts)
        file.close()
        for i in range(len(partslist)):
            if len(partslist[i]) >= 4:
                timestart = partslist[i][1].split(':')
                timefinish = partslist[i][2].split(':')
                try:
                    lunchtime = int(partslist[i][3])
                    for j in range(len(timestart)):
                        timestart[j] = int(timestart[j])
                    for k in range(len(timefinish)):
                        timefinish[k] = int(timefinish[k])
                except ValueError:
                    print(f"Invalid time in line: {','.join(partslist[i])}")
                    continue
                if len(timestart) != 2 or len(timefinish) != 2:
                    print(f"Invalid time in line: {','.join(partslist[i])}")
                    continue
                totaltimehours = timefinish[0]-timestart[0]
                timeminutes = timefinish[1]-timestart[1]
                timeminutes = timeminutes - int(partslist[i][3])
                while timeminutes <= 0:
                    totaltimehours -= 1
                    timeminutes += 60
                dailyworkminutes = hours_list[0]*60+hours_list[1]
                totaltimeminutes = calculatetotaltime(totaltimehours, timeminutes)
                if timeminutes == 60:
                    timeminutes = 0
                    totaltimehours += 1

                if dailyworkminutes < totaltimeminutes:
                    creditminutes = calculatecreditminutes(totaltimeminutes, dailyworkminutes)
                    totalcreditminutes+=creditminutes
                    print(f"{partslist[i][0]} |{totaltimehours:>3d} h {timeminutes:>2d} min     | +{creditminutes} min")
                else:
                    creditminutes = calculatecreditminutes(totaltimeminutes, dailyworkminutes)
                    totalcreditminutes += creditminutes
                    print(f"{partslist[i][0]} |{totaltimehours:>3d} h {timeminutes:>2d} min     | {creditminutes} min")
            elif partslist[i] == ['']:
                continue
            elif 4 > len(partslist[i]) > 0:
                print(f"Invalid line: {','.join(partslist[i])}")

        print("")
        totalcredithours = totalcreditminutes//60
        hours = totalcreditminutes/60
        #leftovercreditminutes = (totalcredithours-(totalcreditminutes/60))*60
        if totalcreditminutes<0:
            totalcreditminutes=totalcreditminutes*-1
        leftovercreditminutes = totalcreditminutes % 60
        if hours>0:
            print(f"You have earned {totalcredithours} h and {leftovercreditminutes:.0f} minutes of credit hours.")
            if totalcreditminutes / 60 > maxlimit:
                print(f"You have exceeded the maximum credit level of {maxlimit} hours.")
        elif hours<0:
            print(f"You have {totalcredithours*-1-1} h and {leftovercreditminutes:.0f} min of deficit hours.")
            if hours*-1 >minlimit:
                print(f"You have exceeded the maximum deficit level of {minlimit} hours.")
        else:
            print("You have not gained any credits/deficit.")
    except OSError:
        print(f"Error in reading the file '{filename}'. The program ends.")
main()
