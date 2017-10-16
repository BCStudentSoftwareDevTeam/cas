
class timeline:
    def __init__(self, scheduleInfo, scheduleList):
        self.schedule_info = scheduleInfo
        self.start_list    = scheduleList
        #self.start_index   = 0
        #self.end_index     = 0
        self.end_list      = scheduleList
        self.course_number = 0
        self.google_chart  = self.start_chart()
        
    def start_chart(self):
        return [[[8,0,0], self.course_number]]
        
    def append_google_chart(self, time):
        format_date = self.convert_time(time)
        self.google_chart.append([format_date, self.course_number])
        return True
        
    def convert_time(self,time_obj):
        str_list = str(time_obj).split(":")
        int_list = []
        for item in str_list:
            int_list.append(int(item))
        return int_list
    
    def check_course(self):
        start_index = self.start_list[0]
        course_info = self.schedule_info[start_index]
        self.course_number = self.course_number + course_info[0]
        self.append_google_chart(course_info[1])
        
    def google_chart_data(self):
        return self.google_chart
        
    def debug_prints(self):
        #print "schedule_info: {}\n".format(self.schedule_info)
        #print "start list: {}\n".format(self.start_list)
        #print "end list: {}\n".format(self.end_list)
        #print "course number: {}\n".format(self.course_number)
        print "google chart: {}\n".format(self.google_chart)
        