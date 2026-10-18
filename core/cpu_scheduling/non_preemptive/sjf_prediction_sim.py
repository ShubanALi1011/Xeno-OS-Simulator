import time


class SJFPredictionSimulator:

    def __init__(self, num_processes=4):
        self.reset(num_processes)

    def reset(self, num_processes=4):
        # Initial processes with actual burst and initial estimated (predicted) burst tau_0
        default_data = [
            {"pid": 1, "name": "P1", "arrival": 0, "burst": 6, "tau": 5.0},
            {"pid": 2, "name": "P2", "arrival": 1, "burst": 2, "tau": 3.0},
            {"pid": 3, "name": "P3", "arrival": 2, "burst": 8, "tau": 6.0},
            {"pid": 4, "name": "P4", "arrival": 3, "burst": 3, "tau": 3.0},
            {"pid": 5, "name": "P5", "arrival": 4, "burst": 5, "tau": 4.5},
            {"pid": 6, "name": "P6", "arrival": 6, "burst": 7, "tau": 5.5},
            {"pid": 7, "name": "P7", "arrival": 8, "burst": 3, "tau": 3.5},
            {"pid": 8, "name": "P8", "arrival": 10, "burst": 4, "tau": 4.0},
            {"pid": 9, "name": "P9", "arrival": 12, "burst": 6, "tau": 5.0},
            {"pid": 10, "name": "P10", "arrival": 14, "burst": 2, "tau": 3.0},
        ]

        self.processes = []
        if num_processes <= len(default_data):
            self.processes = [p.copy() for p in default_data[:num_processes]]
        else:
            self.processes = [p.copy() for p in default_data]
            for i in range(len(default_data) + 1, num_processes + 1):
                burst = 3 + (i % 5)
                arrival = default_data[-1]["arrival"] + (i - len(default_data)) * 2
                tau = float(3 + (i % 4))
                self.processes.append({
                    "pid": i,
                    "name": f"P{i}",
                    "arrival": arrival,
                    "burst": burst,
                    "tau": tau
                })

        self.alpha = 0.5
        self.gantt_chart = []
        self.metrics = []
        self.history = []
        self.add_log(
            "SYSTEM",
            f"SJF with Burst Prediction simulator initialized with {num_processes} processes.",
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

    def run_simulation(self, alpha_val, num_processes=None):
        if num_processes is not None and len(self.processes) != num_processes:
            self.reset(num_processes)

        self.alpha = alpha_val
        procs = [p.copy() for p in self.processes]
        n = len(procs)
        for p in procs:
            p["completed"] = False
            p["completion"] = 0
            p["waiting"] = 0
            p["turnaround"] = 0
            # Keep track of prediction history
            p["predicted_tau"] = p["tau"]

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

            # Pick available process with the shortest PREDICTED burst time (tau)
            idx = min(available, key=lambda x: (procs[x]["predicted_tau"], procs[x]["arrival"]))
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

            # Calculate next prediction using exponential smoothing: tau_n+1 = alpha * actual + (1 - alpha) * tau_n
            old_tau = p["predicted_tau"]
            new_tau = round(self.alpha * p["burst"] + (1 - self.alpha) * old_tau, 2)
            p["next_tau"] = new_tau

            self.add_log(
                f"PREDICTOR ({p['name']})",
                f"Actual Burst: {p['burst']}, Previous Tau: {old_tau}, New Predicted Tau: {new_tau} (α={self.alpha})",
            )

            completed_count += 1
            self.metrics.append(p)

        self.add_log(
            "KERNEL",
            f"SJF Burst Prediction simulation executed successfully for {n} processes.",
        )
        return True, "SJF Prediction simulation completed successfully."