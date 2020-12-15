import codecs
import sys

class Report:

    def __read_file(self,path):
        with codecs.open(path, encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            return lines

    def __calculate_inside_time(self):
        inside_time_report = []
        file = self.__read_file(f"reports/{sys.argv[1]}/pasajes.txt")
        for line in file:
            unit = line.split('\t')[0].replace("Virtual fleet for JAMES\\","")
            platform = line.split('\t')[1].upper()
            inside_time = line.split('\t')[3].upper().rstrip()
            #if platform.find('CAMPO') == -1 or platform != 'PUERTO TALARA':
            if inside_time.upper() == '1D 0M':
                inside_time = '24H 00M'
            hindex = None
            mindex = None
            for i in range(len(inside_time)):
                if inside_time[i] == 'H':
                    hindex = i
                if inside_time[i] == 'M':
                    mindex = i
            hour = None
            if hindex == None:
                hour = 0
                hindex = -1
            else:
                hour = int(inside_time[0:hindex])
            minute = int(inside_time[hindex+1:mindex])
            if hour == 0 and minute == 0:
                minute = 1
            inside_time = hour*60+minute
            inside_time_report.append({
                'unit':unit,
                'platform':platform,
                'inside_time':inside_time
            })
        return inside_time_report

    def __calculate_area_inside_time(self):
        inside_time_report = []
        file = self.__read_file(f"reports/{sys.argv[1]}/pasajes.txt")
        for line in file:
            unit = line.split('\t')[0].replace("Virtual fleet for JAMES\\","")
            platform = line.split('\t')[1].upper()
            inside_time = line.split('\t')[3].upper().rstrip()
            if platform.find('CAMPO') != -1 or platform == 'PUERTO TALARA':
                if inside_time.upper() == '1D 0M':
                    inside_time = '24H 00M'
                hindex = None
                mindex = None
                for i in range(len(inside_time)):
                    if inside_time[i] == 'H':
                        hindex = i
                    if inside_time[i] == 'M':
                        mindex = i
                hour = None
                if hindex == None:
                    hour = 0
                    hindex = -1
                else:
                    hour = int(inside_time[0:hindex])
                minute = int(inside_time[hindex+1:mindex])
                if hour == 0 and minute == 0:
                    minute = 1
                inside_time = hour*60+minute
                inside_time_report.append({
                    'unit':unit,
                    'platform':platform,
                    'inside_time':inside_time
                })
        return inside_time_report

    def __calculate_inside_time_operation_area(self):
        inside_time_report = self.__calculate_inside_time()
        area_inside_time_report = self.__calculate_area_inside_time()
        unit_area = []
        unit_area2 = []
        '''
        for r in inside_time_report:
            for key in self.platform_area.keys():
                if r['platform'] == key:
                    unit_area.append({
                        'unit': r['unit'],
                        'area': self.platform_area[key],
                        'outside_time': r['inside_time']
                    })
        for ua in unit_area:
            index = -1
            for i in range(len(unit_area2)):
                if ua['unit'] == unit_area2[i]['unit'] and ua['area'] == unit_area2[i]['area']:
                    index = i
                    unit_area2[i]['outside_time'] = unit_area2[i]['outside_time'] + ua['outside_time']
            if index == -1:
                unit_area2.append(ua)
        for fua in unit_area2:
            print(fua)
        print(len(unit_area2))
        print('++++++++++++++++++++++++++++++++++')
        for ar in area_inside_time_report:
            print(ar)
        print('++++++++++++++++++++++++++++++++++')
        for a in area_inside_time_report:
            for u in unit_area2:
                if a['unit'] == u['unit'] and a['platform'] == u['area']:
                    a['inside_time'] = a['inside_time'] - u['outside_time']
        '''
        for ar in area_inside_time_report:
            print(ar)
        print('++++++++++++++++++++++++++++++++++')
        return area_inside_time_report


    def __clean_stopped_time(self):
        clean_data = []
        file = self.__read_file(f"reports/{sys.argv[1]}/paradas.txt")
        for line in file:
            unit = line.split('\t')[1].upper()
            platform = line.split('\t')[8].upper()
            stopped_time = line.split('\t')[4].upper()
            if stopped_time == '1D 0M':
                stopped_time = 1440
            else:
                hindex = None
                mindex = None
                for i in range(len(stopped_time)):
                    if stopped_time[i] == 'H':
                        hindex = i
                    if stopped_time[i] == 'M':
                        mindex = i
                hour = None
                if hindex == None:
                    hour = 0
                    hindex = -1
                else:
                    hour = int(stopped_time[0:hindex])
                minute = int(stopped_time[hindex+1:mindex])
                if hour == 0 and minute == 0:
                    minute = 1
                stopped_time = hour*60+minute
            clean_data.append({
                'unit':unit,
                'platform':platform,
                'stopped_time':stopped_time
            })
        return clean_data

    def __calculate_stopped_time(self):
        clean_data = self.__clean_stopped_time()
        stopped_time_report = []
        for c in clean_data:
            if len(stopped_time_report) == 0:
                stopped_time_report.append({
                    'unit':c['unit'],
                    'platform':c['platform'],
                    'stopped_time':c['stopped_time']
                })
            else:
                index = -1
                for i in range(len(stopped_time_report)):
                    if c['unit'] == stopped_time_report[i]['unit'] and c['platform'] == stopped_time_report[i]['platform']:
                        index = i
                        break
                if index == -1:
                    stopped_time_report.append({
                        'unit':c['unit'],
                        'platform':c['platform'],
                        'stopped_time':c['stopped_time']
                    })
                else:
                    stopped_time_report[index]['stopped_time'] += c['stopped_time']
        return stopped_time_report

    def mix_reports(self):
        inside_time_report = self.__calculate_inside_time()
        outside_time_report = []
        stopped_time_report = self.__calculate_stopped_time()
        #inside_time_operation_area_report = self.__calculate_inside_time_operation_area()
        report1 = []
        report2 = []
        complete_report = []
        munits = []
        units = []
        final_report = []

        for s in stopped_time_report:
            print(s)

        for r1 in inside_time_report:
            for r2 in stopped_time_report:
                if r1['unit'] == r2['unit'] and r1['platform'] == r2['platform']:
                    if r1['inside_time'] < r2['stopped_time']:
                        r2['stopped_time'] = r1['inside_time']
                    #standby_time = r1['inside_time'] - r2['stopped_time']
                    standby_time = r2['stopped_time']
                    report1.append({
                        'unit':r1['unit'],
                        'platform':r1['platform'],
                        'inside_time':r1['inside_time'],
                        'stopped_time':r2['stopped_time'],
                        'standby_time':standby_time
                    })

        for x in inside_time_report:
            munits.append(x['unit'])
        for x in stopped_time_report:
            munits.append(x['unit'])

        munits = list(dict.fromkeys(munits))
        for f1 in report1:
            for u in range(len(munits)):
                if f1['unit'] == munits[u]:
                    del munits[u]
                    break
        munits.sort()

        for munit in munits:
            for r1 in inside_time_report:
                if r1['unit'] == munit:
                    inside_time = r1['inside_time']
                    item = {
                        'unit': r1['unit'],
                        'platform': r1['platform'],
                        'inside_time': inside_time,
                        'stopped_time': 0,
                        'standby_time': inside_time
                    }
                    report2.append(item)

        for f2 in report2:
            for u in range(len(munits)):
                if f2['unit'] == munits[u]:
                    del munits[u]
                    break

        for unit in munits:
            item = {
                'unit': unit,
                'platform': 'NONE',
                'inside_time': 0,
                'stopped_time': 0,
                'standby_time': 0,
                'outside_time': 1440
            }
            report2.append(item)

        for r1 in report1:
            complete_report.append(r1)
        for r2 in report2:
            complete_report.append(r2)

        '''
        for r3 in inside_time_operation_area_report:
            item = {
                'unit': r3['unit'],
                'platform': r3['platform'],
                'inside_time': r3['inside_time'],
                'stopped_time': 0,
                'standby_time': 0
            }
            complete_report.append(item)
        '''

        for c in complete_report:
            units.append(c['unit'])
        units = list(dict.fromkeys(units))
        units.sort()

        missing_inside_time_report = inside_time_report

        for c in complete_report:
            for i in range(len(missing_inside_time_report)):
                if missing_inside_time_report[i]['unit'] == c['unit'] and missing_inside_time_report[i]['platform'] == c['platform']:
                    del missing_inside_time_report[i]
                    break

        for m in missing_inside_time_report:
            m['stopped_time'] = 0
            m['standby_time'] = m['inside_time'] - m['stopped_time']
            complete_report.append(m)

        for unit in units:
            for c in complete_report:
                if unit == c['unit']:
                    final_report.append(c)

        # calcute outside time

        for unit in units:
            outside_time = {
                'unit':unit,
                'inside_time':0
            }
            for i in range(len(final_report)):
                if unit == final_report[i]['unit']:
                    inside_time = final_report[i]['inside_time']
                    outside_time['inside_time'] = outside_time['inside_time'] + inside_time
            outside_time['outside_time'] = 1440 - outside_time['inside_time']
            outside_time_report.append(outside_time)

        for o in outside_time_report:
            check = True
            for c in complete_report:
                if c['unit'] == o['unit']:
                    if check:
                        c['outside_time'] = o['outside_time']
                        check = False
                    else:
                        c['outside_time'] = '--'

        # Formatting text

        for f in final_report:
            inside_time = f['inside_time']
            inside_time = inside_time * 60
            seconds = inside_time % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            if seconds < 10:
                seconds = f'0{seconds}'
            if minutes < 10:
                minutes = f'0{minutes}'
            if hour < 10:
                hour = f'0{hour}'
            f['inside_time'] = f"{hour}:{minutes}:{seconds}"

            stopped_time = f['stopped_time']
            stopped_time = stopped_time * 60
            seconds = stopped_time % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            if seconds < 10:
                seconds = f'0{seconds}'
            if minutes < 10:
                minutes = f'0{minutes}'
            if hour < 10:
                hour = f'0{hour}'
            f['stopped_time'] = f"{hour}:{minutes}:{seconds}"

            standby_time = f['standby_time']
            standby_time = standby_time * 60
            seconds = standby_time % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            if seconds < 10:
                seconds = f'0{seconds}'
            if minutes < 10:
                minutes = f'0{minutes}'
            if hour < 10:
                hour = f'0{hour}'
            f['standby_time'] = f"{hour}:{minutes}:{seconds}"

            try:
                outside_time = f['outside_time']
                if outside_time != 1440:
                    outside_time = outside_time * 60
                    seconds = outside_time % (24 * 3600)
                    hour = seconds // 3600
                    seconds %= 3600
                    minutes = seconds // 60
                    seconds %= 60
                    if seconds < 10:
                        seconds = f'0{seconds}'
                    if minutes < 10:
                        minutes = f'0{minutes}'
                    if hour < 10:
                        hour = f'0{hour}'
                    f['outside_time'] = f"{hour}:{minutes}:{seconds}"
                else:
                    f['outside_time'] = '24:00:00'
            except:
                pass

        print('===============================================================')

        file1 = open(f"reports/{sys.argv[1]}/GPS{sys.argv[1]}.txt", "w")
        file2 = open(f"reports/{sys.argv[1]}/GPS{sys.argv[1]}.csv", "w")
        file1.write(f"VEHICLE\tPLATFORM\tSTART_DATETIME\tSTOP_DATETIME\tSTANDBY_TIME\tINSIDE_TIME\tOUTSIDE_TIME\n")
        file2.write(f"VEHICLE;PLATFORM;START_DATETIME;STOP_DATETIME;STANDBY_TIME;INSIDE_TIME;OUTSIDE_TIME\n")
        file1.close()
        file2.close()

        day = sys.argv[1][0:2]
        month = sys.argv[1][2:4]
        year = sys.argv[1][4:8]

        file1 = open(f"reports/{sys.argv[1]}/GPS{sys.argv[1]}.txt", "a")
        file2 = open(f"reports/{sys.argv[1]}/GPS{sys.argv[1]}.csv", "a")
        for f in final_report:
            unit = f['unit']
            if unit == 'PARIAS': unit = 'PARINAS'
            platform = f['platform']
            if platform == 'CAMPO PEA NEGRA': platform = 'CAMPO PENA NEGRA'
            file1.write(f"{unit}\t{platform}\t{year}-{month}-{day} 00:00:00\t{year}-{month}-{day} 23:59:59\t{f['standby_time']}\t{f['inside_time']}\t{f['outside_time']}\n")
            file2.write(f"{unit};{platform};{year}-{month}-{day} 00:00:00;{year}-{month}-{day} 23:59:59;{f['standby_time']};{f['inside_time']};{f['outside_time']}\n")
        file1.close()
        file2.close()
        print('===============================================================')


report = Report()
report.mix_reports()
