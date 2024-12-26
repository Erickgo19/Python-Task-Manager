"Task Manager"
import datetime
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

app = ctk.CTk()
app.title("Task Manager")
app.geometry("500x500")
app.resizable(False, False)
# app.iconbitmap("TaskManager.ico")

main_container = ctk.CTkScrollableFrame(app, width=400, height=350)
main_container.place(x=40, y=50)
app_title = ctk.CTkLabel(app, text="Task Manager", font=("calibri", 30),
                         text_color="#76a2b7")
app_title.place(x=170, y=10)

class TaskTime():
    "initialize class create widgets"
    def __init__(self):
        self.status = ctk.BooleanVar()
        self.act_status = False
        self.prev_status = False
        self.start = None
        self.end = None
        self.tdt = None
        self.total_time = 0

    def task_time(self):
        "time doing the task"
        self.act_status = self.status.get()
        if self.act_status is True:
            self.start = datetime.datetime.now()

        self.prev_status = True

        if self.prev_status is True and self.act_status is False:
            self.end = datetime.datetime.now()
            self.tdt = self.end - self.start

            self.total_time += self.tdt.seconds

    def get_total_time(self):
        "return total time"
        if self.total_time != 0:
            return self.total_time


class CreateWidgets(TaskTime):
    "initialize class create widgets"
    def __init__(self, task, container, task_list):
        super().__init__()
        self.task = task
        self.container = container
        self.del_btn = None
        self.start_switch = None
        self.total_time = 0
        self.task_list =  task_list
        self.wid_container = None

    def del_elements(self):
        "delete elements and get info before"
        if self.act_status is False:
            self.total_time = self.get_total_time()
            self.task_list.remove(self)
            time_doing_task.append(self.total_time)
            self.wid_container.destroy()
        else:
            self.start_switch.configure(text="Turn Me \noff before")

    def switch_command(self):
        "switch event controler"
        if self.act_status is True:
            self.start_switch.configure(text="To Work")
        elif self.act_status is False:
            self.start_switch.configure(text="Pause/ \n End")
        start_time.append(datetime.datetime.now())
        self.task_time()

    def create_task(self):
        "create task widgetes"
        self.wid_container = ctk.CTkFrame(self.container, width=390, height=50)
        self.wid_container.pack()

        self.del_btn = ctk.CTkButton(self.wid_container, text="Delete", width=25,
                                     font=("calibri", 14), command=self.del_elements)
        self.del_btn.place(x=10, y=10)

        self.task = ctk.CTkLabel(self.wid_container, text=self.task, anchor="center",
                                 font=("calibri", 15), width=100, wraplength=130)
        self.task.place(x=125, y=10)

        self.start_switch = ctk.CTkSwitch(self.wid_container, text="To Work",
                                          font=("calibri", 14), text_color="#76a2b7",
                                          variable=self.status, command=self.switch_command)
        self.start_switch.place(x=293, y=10)


    def tasks_left(self):
        "return how many tasks are left"
        return self.task_list


tasks = []
title = ctk.StringVar()

def add_task():
    "idk maybe add new task"
    title_task = title.get()
    if title_task != "":
        new_task = CreateWidgets(title_task, main_container, tasks)
        new_task.create_task()
        tasks.append(new_task)
        task_name.append(title_task)

start_time = []
task_name = []
time_doing_task = []


lbl = ctk.CTkLabel(app, text="Task Title", text_color="#76a2b7", font=("calibri", 15))
lbl.place(x=110, y=420)
user_input = ctk.CTkEntry(app, placeholder_text="Add new task", textvariable=title)
user_input.place(x=180, y=420)
add_button =  ctk.CTkButton(app, text="Add Task", command=add_task, width=80,
                            font=("calibri", 14))
add_button.place(x= 210, y= 455)


def wnds_report():
    "generate report"
    report = ctk.CTkToplevel(app)
    report.resizable(False, False)
    if len(tasks) == 0 and len(start_time) != 0:
        end_time = datetime.datetime.now()
        delta = end_time - start_time[0]
        delta_noms = str(delta)
        report.title("Report")
        report.geometry("600x400")
        info_container = ctk.CTkScrollableFrame(report, width=130, height=310)
        info_container.place(x=440, y=40)
        ttl_infcntainer = ctk.CTkLabel(info_container, text="Resume", font=("calibri", 16),
                                       text_color="#76a2b7")
        ttl_infcntainer.pack()
        report_info = ctk.CTkLabel(report, text="Total Time Doing Tasks", font=("calibri", 20),
                                   text_color="#76a2b7")
        report_info.place(x=165, y=10)


        time_in_secs = sum(time_doing_task)
        us_totaltime = datetime.timedelta(seconds=time_in_secs)

        pause_delta = delta - us_totaltime
        pause_noms = str(pause_delta)

        ttw_lbl = ctk.CTkLabel(report, font=("calibri", 15), text_color="#76a2b7",
                               text=f"Total Time {delta_noms[:8]} || Time Off: {pause_noms[:8]}")
        ttw_lbl.place(x=80, y=365)

        fig, ax = plt.subplots(figsize=(3.9, 3.2))
        fig.patch.set_facecolor('#2e2e2e')
        ax.pie(time_doing_task, labels=task_name, autopct='%1.1f%%',
               textprops={'color': 'white', 'wrap':True})
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=report)
        canvas.draw()
        canvas.get_tk_widget().place(x=15, y=40)

        for idx, ntask in enumerate(task_name):
            ntimes =  datetime.timedelta(seconds=time_doing_task[idx])

            lbl_foret = ctk.CTkLabel(info_container, text=f"{ntask}:  {ntimes}",
                                     wraplength=130, text_color="#76a2b7")
            lbl_foret.pack()

    elif len(tasks) > 0:
        report.title("Unfinished Tasks")
        report.geometry("200x100")
        lbl_error =  ctk.CTkLabel(report, text="there are still unfinished tasks :(",
                                  font=("calibri", 14))
        lbl_error.place(x=10, y=35)

    else:
        report.title("NO TASKS")
        report.geometry("200x100")
        lbl_error =  ctk.CTkLabel(report, text="YOU HAVEN'T ADDED TASKS",
                                  font=("calibri", 14))
        lbl_error.place(x=20, y=35)



btn_report = ctk.CTkButton(app, text="Report", font=("calibri", 14), width=80,
                           command=wnds_report)
btn_report.place(x=400, y=455)

def info_for_users():
    "Info About Total Time"
    info = ctk.CTkToplevel(app)
    info.title("Info About Report")
    info.geometry("200x200")
    info.resizable(False, False)
    etiqueta = ctk.CTkLabel( info, font=("calibri", 15), text_color="#76a2b7", anchor="center",
         width=180, wraplength=180, text=(
        "Total time starts from when the first task was started until the report was generated, "
        "the total time does not vary if two or more tasks were performed at the same time"))
    etiqueta.place(x=10, y=35)

btn_info = ctk.CTkButton(app, text="?", width=20, fg_color="transparent", text_color="#76a2b7",
                         command=info_for_users)
btn_info.place(x=10, y=455)

app.mainloop()
