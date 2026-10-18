import time


class MultilevelQueueSimulator:

    def __init__(self, num_system=2, num_user=2):
        self.reset(num_system, num_user)

    def reset(self, num_system=2, num_user=2):
        default_sys = [
            {"pid": 101, "name": "Sys_P1", "arrival": 0, "burst": 4, "queue": "System"},
            {"pid": 102, "name": "Sys_P2", "arrival": 2, "burst": 3, "queue": "System"},
            {"pid": 103, "name": "Sys_P3", "arrival": 4, "burst": 5, "queue": "System"},
            {"pid": 104, "name": "Sys_P4", "arrival": 6, "burst": 2, "queue": "System"},
            {"pid": 105, "name": "Sys_P5", "arrival": 8, "burst": 4, "queue": "System"},
        ]
        default_user = [
            {"pid": 201, "name": "User_P1", "arrival": 1, "burst": 6, "queue": "User"},
            {"pid": 202, "name": "User_P2", "arrival": 3, "burst": 5, "queue": "User"},
            {"pid": 203, "name": "User_P3", "arrival": 5, "burst": 7, "queue": "User"},
            {"pid": 204, "name": "User_P4", "arrival": 7, "burst": 4, "queue": "User"},
            {"pid": 205, "name": "User_P5", "arrival": 9, "burst": 6, "queue": "User"},
        ]

        # Generate System Processes
        self.system_processes = []
        if num_system <= len(default_sys):
            self.system_processes = [p.copy() for p in default_sys[:num_system]]
        else:
            self.system_processes = [p.copy() for p in default_sys]
            for i in range(len(default_sys) + 1, num_system + 1):
                self.system_processes.append({
                    "pid": 100 + i,
                    "name": f"Sys_P{i}",
                    "arrival": (i - 1) * 2,
                    "burst": 3 + (i % 4),
                    "queue": "System"
                })

        # Generate User Processes
        self.user_processes = []
        if num_user <= len(default_user):
            self.user_processes = [p.copy() for p in default_user[:num_user]]
        else:
            self.user_processes = [p.copy() for p in default_user]
            for i in range(len(default_user) + 1, num_user + 1):
                self.user_processes.append({
                    "pid": 200 + i,
                    "name": f"User_P{i}",
                    "arrival": 1 + (i - 1) * 2,
                    "burst": 4 + (i % 4),
                    "queue": "User"
                })

        self.gantt_chart = []
        self.metrics = []
        self.history = []
        self.add_log(
            "SYSTEM",
            f"Multilevel Queue Scheduling simulator initialized with {len(self.system_processes)} System and {len(self.user_processes)} User processes.",
        )

    def add_log(self, sender, message):
        timestamp = time.strftime("%H:%M:%S")
        self.history.insert(
            0,
            {
                "time": timestamp,
                "sender": sender,
                "message": message,
            },
        )

    def run_simulation(self, num_system=None, num_user=None):
        if num_system is not None and num_user is not None:
            if len(self.system_processes) != num_system or len(self.user_processes) != num_user:
                self.reset(num_system, num_user)

        sys_procs = [p.copy() for p in self.system_processes]
        user_procs = [p.copy() for p in self.user_processes]

        for p in sys_procs + user_procs:
            p["completed"] = False
            p["completion"] = 0
            p["waiting"] = 0
            p["turnaround"] = 0

        time_cursor = 0
        self.gantt_chart = []
        self.metrics = []

        all_procs = sys_procs + user_procs
        n = len(all_procs)
        completed_count = 0

        while completed_count < n:
            sys_available = [
                p for p in sys_procs if p["arrival"] <= time_cursor and not p["completed"]
            ]

            if sys_available:
                p = min(sys_available, key=lambda x: x["arrival"])
                start_t = time_cursor
                time_cursor += p["burst"]
                end_t = time_cursor

                self.gantt_chart.append(
                    {"name": f"{p['name']} (Sys)", "start": start_t, "end": end_t}
                )
                p["completion"] = end_t
                p["turnaround"] = p["completion"] - p["arrival"]
                p["waiting"] = p["turnaround"] - p["burst"]
                p["completed"] = True
                completed_count += 1
                self.metrics.append(p)
                self.add_log("SCHEDULER", f"Executed System Queue process {p['name']}.")
                continue

            user_available = [
                p for p in user_procs if p["arrival"] <= time_cursor and not p["completed"]
            ]

            if user_available:
                p = min(user_available, key=lambda x: x["arrival"])
                start_t = time_cursor
                time_cursor += p["burst"]
                end_t = time_cursor

                self.gantt_chart.append(
                    {"name": f"{p['name']} (User)", "start": start_t, "end": end_t}
                )
                p["completion"] = end_t
                p["turnaround"] = p["completion"] - p["arrival"]
                p["waiting"] = p["turnaround"] - p["burst"]
                p["completed"] = True
                completed_count += 1
                self.metrics.append(p)
                self.add_log("SCHEDULER", f"Executed User Queue process {p['name']}.")
                continue

            uncompleted = [p for p in all_procs if not p["completed"]]
            if uncompleted:
                next_arr = min(uncompleted, key=lambda x: x["arrival"])
                time_cursor = next_arr["arrival"]
            else:
                break

        self.add_log("KERNEL", f"Multilevel Queue simulation executed successfully for {n} processes.")
        return True, "Multilevel Queue simulation completed successfully."