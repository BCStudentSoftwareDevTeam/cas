class timeline:
    def __init__(self, scheduleInfo, scheduleList):
        self.schedule_info     = scheduleInfo
        self.schedule_list     = scheduleList
        self.current_index     = 0
        self.previous_index    = []
        self.course_number     = 0
        self.google_chart      = self.start_chart()
        
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
        #schedule A = The current schedule 
        #schedule B = The previous schedule       
        A_course_info   = self.schedule_info[self.schedule_list[self.current_index]]
        A_start_time    = A_course_info[1]
        A_course_number = A_course_info[0]
        self.course_number = self.course_number + A_course_number
        self.previous_index.append(self.current_index) 
        self.append_google_chart(A_start_time)
        for index in self.previous_index:
            B_course_info = self.schedule_info[self.schedule_list[index]]
            B_end_time = B_course_info[2]
            if B_end_time > A_start_time:
                B_course_number = B_course_info[0]
                self.course_number = self.course_number - B_course_number
                #self.append_google_chart(B_end_time)
                self.previous_index.remove(index)                
        self.current_index += 1
     
    def reorganize_chart_data(self):
        dict_details = dict()
        for SID in schedule_list:
            schedule_details = schedule_info[SID]
            schedule_number  = schedule_details[0]
            schedule_start   = tuple(schedule_details[1])
            schedule_end     = tuple(schedule_details[2])
            if schedule_start in dict_details.keys:
                
        
        
        chart_copy = self.google_chart        
        new_list = []
        val_dict = dict()
        for data in chart_copy:
            if data[0] in new_list:
                new_list.index(data[0])
                # update dictionary
            else:
                new_list.append(data[0])
                key = li.index(data[0])
                val_dict[key] = 
            
            
        
    def check_schedules(self):
        for schedule in self.schedule_list:
            self.check_course()
        #self.reorganize_chart_data()
        
    def google_chart_data(self):
        return self.google_chart
        
    def debug_prints(self):
        #print "schedule_info: {}\n".format(self.schedule_info)
        #print "start list: {}\n".format(self.start_list)
        #print "end list: {}\n".format(self.end_list)
        #print "course number: {}\n".format(self.course_number)
        print "google chart: {}\n".format(self.google_chart)
        