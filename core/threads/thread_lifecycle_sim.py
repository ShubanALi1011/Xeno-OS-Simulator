import time


class ThreadLifecycleSimulator:

    def __init__(self):
        self.reset()

    def reset(self):
        self.threads = {
            101: {
                "tid": 101,
                "name": "main_thread",
                "state": "RUNNING",
                "priority": "Normal",
            },
            102: {
                "tid": 102,
                "name": "worker_thread_1",
                "state": "READY",
                "priority": "High",
            },
        }
        self.history = []
        self.add_log(
            "SYSTEM",
            "Thread Lifecycle Management subsystem initialized. Initial threads spawned.",
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

    def create_thread(self, name, priority):
        new_tid = max(self.threads.keys()) + 1 if self.threads else 101
        self.threads[new_tid] = {
            "tid": new_tid,
            "name": name,
            "state": "READY",
            "priority": priority,
        }
        self.add_log(
            "KERNEL",
            f"pthread_create(): Thread '{name}' (TID: {new_tid}) spawned with priority {priority}. State set to READY.",
        )
        return True, f"Thread {name} created successfully with TID {new_tid}."

    def change_state(self, tid, new_state):
        if tid not in self.threads:
            return False, "Thread ID not found."

        old_state = self.threads[tid]["state"]
        self.threads[tid]["state"] = new_state
        self.add_log(
            f"TID {tid} ({self.threads[tid]['name']})",
            f"State transitioned from {old_state} to {new_state}.",
        )
        return True, f"Thread {tid} state updated to {new_state}."

    def terminate_thread(self, tid):
        if tid not in self.threads:
            return False, "Thread ID not found."
        if tid == 101:
            return (
                False,
                "Cannot terminate main thread directly while application runs.",
            )

        t_name = self.threads[tid]["name"]
        del self.threads[tid]
        self.add_log(
            "KERNEL",
            f"pthread_exit(): Thread '{t_name}' (TID: {tid}) terminated and reaped from thread table.",
        )
        return True, f"Thread {tid} terminated successfully."