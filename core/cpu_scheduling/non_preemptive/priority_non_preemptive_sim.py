import time


class PriorityNonPreemptiveSimulator:

    def __init__(self, num_processes=4):
        self.reset(num_processes)

    def reset(self, num_processes=4):
        # Default processes with priority (Lower number = Higher priority)
        default_data = [
            {"pid": 1, "name": "P1", "arrival": 0, "burst": 5, "priority": 2},
            {"pid": 2, "name": "P2", "arrival": 1, "burst": 3, "priority": 1},
            {"pid": 3, "name": "P3", "arrival": 2, "burst": 7, "priority": 3},
            {"pid": 4, "name": "P4", "arrival": 3, "burst": 4, "priority": 2},
            {"pid": 5, "name": "P5", "arrival": 4, "burst": 6, "priority": 1},
            {"pid": 6, "name": "P6", "arrival": 6, "burst": 5, "priority": 4},
            {"pid": 7, "name": "P7", "arrival": 8, "burst": 3, "priority": 2},
            {"pid": 8, "name": "P8", "arrival": 10, "burst": 4, "priority": 3},
            {"pid": 9, "name": "P9", "arrival": 12, "burst": 5, "priority": 1},
            {"pid": 10, "name": "P10", "arrival": 14, "burst": 3, "priority": 4},
        ]
        
        self.processes = []
        if num_processes <= len(default_data):
            self.processes = [p.copy() for p in default_data[:num_processes]]
        else:
            self.processes = [p.copy() for p in default_data]
            for i in range(len(default_data) + 1, num_processes + 1):
                burst = 3 + (i % 5)
                arrival = default_data[-1]["arrival"] + (i - len(default_data)) * 2
                priority = (i % 4) + 1
                self.processes.append({
                    "pid": i,
                    "name": f"P{i}",
                    "arrival": arrival,
                    "burst": burst,
                    "priority": priority
                })

        self.gantt_chart = []
        self.metrics = []
        self.history = []
        self.add_log(
            "SYSTEM",
            f"Priority (Non-Preemptive) CPU Scheduling simulator initialized with {num_processes} processes.",
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

    def run_simulation(self, num_processes=None):
        if num_processes is not None and len(self.processes) != num_processes:
            self.reset(num_processes)

        procs = [p.copy() for p in self.processes]
        n = len(procs)
        for p in procs:
            p["completed"] = False
            p["completion"] = 0
            p["waiting"] = 0
            p["turnaround"] = 0

        time_cursor = 0
        completed_count = 0
        self.gantt_chart = []
        self.metrics = []

        while completed_count < n:
            available = [
                i
                for i in range(n)
                if procs[i]["arrival"] <= time_cursor and not procs[i]["completed"]
            ]

            if not available:
                uncompleted = [i for i in range(n) if not procs[i]["completed"]]
                if uncompleted:
                    next_arr = min(uncompleted, key=lambda x: procs[x]["arrival"])
                    time_cursor = procs[next_arr]["arrival"]
                    continue
                else:
                    break

            # Pick available process with highest priority (lowest priority number)
            idx = min(available, key=lambda x: (procs[x]["priority"], procs[x]["arrival"]))
            p = procs[idx]

            start_t = time_cursor
            time_cursor += p["burst"]
            end_t = time_cursor

            self.gantt_chart.append(
                {"name": p["name"], "start": start_t, "end": end_t}
            )

            p["completion"] = end_t
            p["turnaround"] = p["completion"] - p["arrival"]
            p["waiting"] = p["turnaround"] - p["burst"]
            p["completed"] = True

            completed_count += 1
            self.metrics.append(p)

        self.add_log(
            "KERNEL",
            f"Non-Preemptive Priority simulation executed successfully for {n} processes.",
        )
        return True, "Priority simulation completed successfully."