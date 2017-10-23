import datetime

class timeline:
    def __init__(self, scheduleInfo, scheduleList):
        self.schedule_info     = scheduleInfo
        self.schedule_list     = scheduleList
        self.overall_number    = 0
        self.google_chart      = []
        self.overall_times     = []
        self.chart_data        = self.collect_chart_data()
        
    def append_google_chart(self, time):
        format_date = self.convert_time(time)
        self.google_chart.append([format_date, self.overall_number])
        return True
        
    def convert_time(self,time_obj):
        str_list = str(time_obj).split(":")
        int_list = [ int(x) for x in str_list ]        
        return int_list
    
    def organize_overall_times(self):
        self.overall_times = sorted(self.overall_times, key=lambda x: datetime.datetime.strptime(x, '%H:%M:%S'))
     
    def append_overall_time(self, time):
        if time not in self.overall_times:
            self.overall_times.append(time)
    
    def collect_chart_data(self):
        dict_details = dict()
        for SID in self.schedule_list:
            schedule_details = self.schedule_info[SID]
            number  = schedule_details[0]
            start   = str(schedule_details[1])
            end     = str(schedule_details[2])
            #Add to overall times for later use
            self.append_overall_time(start)
            self.append_overall_time(end)
            
            #Discover values for times
            if start in dict_details.keys():
                value = dict_details[start]
                dict_details[start] = dict_details[start] + number
            else:
                dict_details[start] = number
            if end in dict_details.keys():
                value = dict_details[end]
                dict_details[end] = dict_details[end] + (-number)
            else:
                dict_details[end] = -number
        self.organize_overall_times()        
        return dict_details
        
    def create_google_chart(self):
        for time in self.overall_times:
            x = self.chart_data[time]
            self.overall_number += x
            self.append_google_chart(time)
        
    def google_chart_data(self):
        self.create_google_chart()
        return self.google_chart
        
    def debug_prints(self):
        #print "schedule_info: {}\n".format(self.schedule_info)
        #print "start list: {}\n".format(self.start_list)
        #print "end list: {}\n".format(self.end_list)
        #print "course number: {}\n".format(self.course_number)
        print "google chart: {}\n".format(self.google_chart)
        