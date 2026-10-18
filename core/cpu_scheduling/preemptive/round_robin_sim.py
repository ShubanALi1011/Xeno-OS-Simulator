import time


class RoundRobinSimulator:

    def __init__(self, num_processes=4):
        self.reset(num_processes)

    def reset(self, num_processes=4):
        default_bursts = [8, 4, 9, 5, 6, 7, 3, 5, 4, 6]
        self.processes = []
        for i in range(1, num_processes + 1):
            burst = default_bursts[(i - 1) % len(default_bursts)]
            arrival = i - 1
            self.processes.append({
                "pid": i,
                "name": f"P{i}",
                "arrival": arrival,
                "burst": burst,
                "remaining": burst
            })

        self.time_quantum = 3
        self.gantt_chart = []
        self.metrics = []
        self.history = []
        self.add_log(
            "SYSTEM",
            f"Round Robin (Preemptive) CPU Scheduling simulator initialized with {num_processes} processes.",
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

    def run_simulation(self, quantum, num_processes=None):
        if num_processes is not None and len(self.processes) != num_processes:
            self.reset(num_processes)

        self.time_quantum = quantum
        # Deep copy for simulation state tracking
        procs = [p.copy() for p in self.processes]
        for p in procs:
            p["waiting"] = 0
            p["turnaround"] = 0
            p["completion"] = 0

        time_cursor = 0
        queue = []
        completed = 0
        n = len(procs)
        self.gantt_chart = []

        # Sort by arrival time initially
        procs.sort(key=lambda x: x["arrival"])
        visited = [False] * n

        # Enqueue first arriving process
        for i in range(n):
            if procs[i]["arrival"] <= time_cursor:
                queue.append(i)
                visited[i] = True

        if not queue and n > 0:
            # Jump time if first process arrives later
            time_cursor = procs[0]["arrival"]
            queue.append(0)
            visited[0] = True

        while queue:
            idx = queue.pop(0)
            p = procs[idx]

            exec_time = min(self.time_quantum, p["remaining"])
            start_t = time_cursor
            time_cursor += exec_time
            p["remaining"] -= exec_time

            self.gantt_chart.append(
                {"name": p["name"], "start": start_t, "end": time_cursor}
            )

            # Check newly arrived processes during this execution window
            for i in range(n):
                if (
                    not visited[i]
                    and procs[i]["arrival"] <= time_cursor
                    and procs[i]["remaining"] > 0
                ):
                    queue.append(i)
                    visited[i] = True

            # If process still has remaining burst, push back to queue
            if p["remaining"] > 0:
                queue.append(idx)
            else:
                completed += 1
                p["completion"] = time_cursor
                p["turnaround"] = p["completion"] - p["arrival"]
                p["waiting"] = p["turnaround"] - p["burst"]

            # If queue is empty but processes remain, jump to next arrival
            if not queue and completed < n:
                uncompleted = [i for i in range(n) if procs[i]["remaining"] > 0]
                if uncompleted:
                    next_i = min(uncompleted, key=lambda x: procs[x]["arrival"])
                    time_cursor = procs[next_i]["arrival"]
                    queue.append(next_i)
                    visited[next_i] = True

        self.metrics = procs
        self.add_log(
            "KERNEL",
            f"Round Robin scheduling executed successfully with Time Quantum = {quantum} for {n} processes.",
        )
        return True, "Round Robin simulation completed successfully."