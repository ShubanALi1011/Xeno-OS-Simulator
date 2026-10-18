import time


class SRTFSimulator:

    def __init__(self, num_processes=4):
        self.reset(num_processes)

    def reset(self, num_processes=4):
        default_data = [
            {"pid": 1, "name": "P1", "arrival": 0, "burst": 7},
            {"pid": 2, "name": "P2", "arrival": 2, "burst": 4},
            {"pid": 3, "name": "P3", "arrival": 4, "burst": 1},
            {"pid": 4, "name": "P4", "arrival": 5, "burst": 4},
            {"pid": 5, "name": "P5", "arrival": 6, "burst": 3},
            {"pid": 6, "name": "P6", "arrival": 8, "burst": 6},
            {"pid": 7, "name": "P7", "arrival": 10, "burst": 2},
            {"pid": 8, "name": "P8", "arrival": 12, "burst": 5},
            {"pid": 9, "name": "P9", "arrival": 14, "burst": 4},
            {"pid": 10, "name": "P10", "arrival": 15, "burst": 3},
        ]
        
        self.processes = []
        if num_processes <= len(default_data):
            for p in default_data[:num_processes]:
                proc = p.copy()
                proc["remaining"] = proc["burst"]
                self.processes.append(proc)
        else:
            for p in default_data:
                proc = p.copy()
                proc["remaining"] = proc["burst"]
                self.processes.append(proc)
            for i in range(len(default_data) + 1, num_processes + 1):
                burst = 3 + (i % 5)
                arrival = default_data[-1]["arrival"] + (i - len(default_data)) * 2
                self.processes.append({
                    "pid": i,
                    "name": f"P{i}",
                    "arrival": arrival,
                    "burst": burst,
                    "remaining": burst
                })

        self.gantt_chart = []
        self.metrics = []
        self.history = []
        self.add_log(
            "SYSTEM",
            f"SRTF (Shortest Remaining Time First) CPU Scheduling simulator initialized with {num_processes} processes.",
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
            p["remaining"] = p["burst"]
            p["completion"] = 0
            p["waiting"] = 0
            p["turnaround"] = 0

        time_cursor = 0
        completed = 0
        self.gantt_chart = []

        # Simulate tick by tick until all complete
        while completed < n:
            available = [
                i
                for i in range(n)
                if procs[i]["arrival"] <= time_cursor and procs[i]["remaining"] > 0
            ]

            if not available:
                uncompleted = [i for i in range(n) if procs[i]["remaining"] > 0]
                if uncompleted:
                    next_arr = min(
                        uncompleted, key=lambda x: procs[x]["arrival"]
                    )
                    time_cursor = procs[next_arr]["arrival"]
                    continue
                else:
                    break

            # Pick the process with the shortest remaining time
            idx = min(available, key=lambda x: (procs[x]["remaining"], procs[x]["arrival"]))
            p = procs[idx]

            # Execute for 1 time unit (preemptive check at each unit)
            p["remaining"] -= 1
            time_cursor += 1

            # Consolidate Gantt chart blocks
            if self.gantt_chart and self.gantt_chart[-1]["name"] == p["name"]:
                self.gantt_chart[-1]["end"] = time_cursor
            else:
                self.gantt_chart.append(
                    {"name": p["name"], "start": time_cursor - 1, "end": time_cursor}
                )

            if p["remaining"] == 0:
                completed += 1
                p["completion"] = time_cursor
                p["turnaround"] = p["completion"] - p["arrival"]
                p["waiting"] = p["turnaround"] - p["burst"]

        self.metrics = procs
        self.add_log(
            "KERNEL",
            f"SRTF preemptive simulation executed successfully across timeline for {n} processes.",
        )
        return True, "SRTF simulation completed successfully."