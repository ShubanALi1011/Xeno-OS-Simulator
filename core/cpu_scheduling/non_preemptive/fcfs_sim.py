import time


class FCFSSimulator:

    def __init__(self, num_processes=4):
        self.reset(num_processes)

    def reset(self, num_processes=4):
        default_data = [
            {"pid": 1, "name": "P1", "arrival": 0, "burst": 5},
            {"pid": 2, "name": "P2", "arrival": 1, "burst": 3},
            {"pid": 3, "name": "P3", "arrival": 2, "burst": 8},
            {"pid": 4, "name": "P4", "arrival": 3, "burst": 6},
            {"pid": 5, "name": "P5", "arrival": 4, "burst": 4},
            {"pid": 6, "name": "P6", "arrival": 6, "burst": 7},
            {"pid": 7, "name": "P7", "arrival": 8, "burst": 3},
            {"pid": 8, "name": "P8", "arrival": 10, "burst": 5},
            {"pid": 9, "name": "P9", "arrival": 12, "burst": 4},
            {"pid": 10, "name": "P10", "arrival": 14, "burst": 6},
        ]
        
        self.processes = []
        if num_processes <= len(default_data):
            self.processes = [p.copy() for p in default_data[:num_processes]]
        else:
            self.processes = [p.copy() for p in default_data]
            for i in range(len(default_data) + 1, num_processes + 1):
                burst = 3 + (i % 6)
                arrival = default_data[-1]["arrival"] + (i - len(default_data)) * 2
                self.processes.append({
                    "pid": i,
                    "name": f"P{i}",
                    "arrival": arrival,
                    "burst": burst
                })

        self.gantt_chart = []
        self.metrics = []
        self.history = []
        self.add_log(
            "SYSTEM",
            f"FCFS (Non-Preemptive) CPU Scheduling simulator initialized with {num_processes} processes.",
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
        # FCFS sorts processes strictly by arrival time
        procs.sort(key=lambda x: x["arrival"])

        time_cursor = 0
        self.gantt_chart = []
        self.metrics = []

        for p in procs:
            if time_cursor < p["arrival"]:
                time_cursor = p["arrival"]  # CPU idle time gap handle

            start_t = time_cursor
            time_cursor += p["burst"]
            end_t = time_cursor

            self.gantt_chart.append(
                {"name": p["name"], "start": start_t, "end": end_t}
            )

            completion = end_t
            turnaround = completion - p["arrival"]
            waiting = turnaround - p["burst"]

            p["completion"] = completion
            p["turnaround"] = turnaround
            p["waiting"] = waiting
            self.metrics.append(p)

        self.add_log(
            "KERNEL", f"FCFS non-preemptive simulation executed successfully for {len(procs)} processes."
        )
        return True, "FCFS simulation completed successfully."