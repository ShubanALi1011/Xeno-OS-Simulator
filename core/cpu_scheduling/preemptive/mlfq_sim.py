import time


class MLFQSimulator:

    def __init__(self, num_processes=3):
        self.reset(num_processes)

    def reset(self, num_processes=3):
        default_data = [
            {"pid": 1, "name": "P1", "arrival": 0, "burst": 10},
            {"pid": 2, "name": "P2", "arrival": 1, "burst": 5},
            {"pid": 3, "name": "P3", "arrival": 2, "burst": 8},
            {"pid": 4, "name": "P4", "arrival": 3, "burst": 6},
            {"pid": 5, "name": "P5", "arrival": 5, "burst": 7},
            {"pid": 6, "name": "P6", "arrival": 7, "burst": 4},
            {"pid": 7, "name": "P7", "arrival": 9, "burst": 9},
            {"pid": 8, "name": "P8", "arrival": 11, "burst": 5},
        ]
        
        self.processes = []
        if num_processes <= len(default_data):
            for p in default_data[:num_processes]:
                proc = p.copy()
                proc["remaining"] = proc["burst"]
                proc["current_queue"] = 0
                self.processes.append(proc)
        else:
            for p in default_data:
                proc = p.copy()
                proc["remaining"] = proc["burst"]
                proc["current_queue"] = 0
                self.processes.append(proc)
            for i in range(len(default_data) + 1, num_processes + 1):
                burst = 4 + (i % 5)
                arrival = default_data[-1]["arrival"] + (i - len(default_data)) * 2
                self.processes.append({
                    "pid": i,
                    "name": f"P{i}",
                    "arrival": arrival,
                    "burst": burst,
                    "remaining": burst,
                    "current_queue": 0
                })

        self.gantt_chart = []
        self.metrics = []
        self.history = []
        self.add_log(
            "SYSTEM",
            f"Multilevel Feedback Queue (MLFQ) simulator initialized with {num_processes} processes and 3 priority queues.",
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
            p["current_queue"] = 0

        time_cursor = 0
        completed = 0
        self.gantt_chart = []

        # Define time quanta for 3 queues
        quanta = {0: 3, 1: 6, 2: 9}

        # Ready queues storage
        q0, q1, q2 = [], [], []
        visited = [False] * n

        procs.sort(key=lambda x: x["arrival"])

        def enqueue_arriving(t):
            for i in range(n):
                if not visited[i] and procs[i]["arrival"] <= t:
                    q0.append(i)
                    visited[i] = True
                    self.add_log("SCHEDULER", f"Process {procs[i]['name']} arrived and entered Queue 0.")

        enqueue_arriving(time_cursor)

        if not q0 and not q1 and not q2 and n > 0:
            time_cursor = procs[0]["arrival"]
            enqueue_arriving(time_cursor)

        while completed < n:
            # Check queues in priority order: Q0 > Q1 > Q2
            active_queue = None
            q_level = -1
            if q0:
                active_queue = q0
                q_level = 0
            elif q1:
                active_queue = q1
                q_level = 1
            elif q2:
                active_queue = q2
                q_level = 2
            else:
                # CPU idle, jump to next arrival
                uncompleted = [i for i in range(n) if procs[i]["remaining"] > 0]
                if uncompleted:
                    next_arr = min(uncompleted, key=lambda x: procs[x]["arrival"])
                    time_cursor = procs[next_arr]["arrival"]
                    enqueue_arriving(time_cursor)
                    continue
                else:
                    break

            idx = active_queue.pop(0)
            p = procs[idx]
            q_time = quanta[q_level]

            exec_time = min(q_time, p["remaining"])
            start_t = time_cursor
            time_cursor += exec_time
            p["remaining"] -= exec_time

            # Enqueue newly arrived processes during execution window
            enqueue_arriving(time_cursor)

            self.gantt_chart.append(
                {"name": f"{p['name']} (Q{q_level})", "start": start_t, "end": time_cursor}
            )

            if p["remaining"] == 0:
                completed += 1
                p["completion"] = time_cursor
                p["turnaround"] = p["completion"] - p["arrival"]
                p["waiting"] = p["turnaround"] - p["burst"]
                self.add_log("KERNEL", f"Process {p['name']} completed execution at time {time_cursor}.")
            else:
                # Demote to lower priority queue if time quantum exhausted
                if q_level == 0:
                    q1.append(idx)
                    self.add_log("MLFQ", f"Process {p['name']} demoted from Queue 0 to Queue 1.")
                else:
                    q2.append(idx)
                    self.add_log("MLFQ", f"Process {p['name']} demoted to Queue 2.")

        self.metrics = procs
        self.add_log("KERNEL", f"Multilevel Feedback Queue simulation executed successfully for {n} processes.")
        return True, "MLFQ simulation completed successfully."