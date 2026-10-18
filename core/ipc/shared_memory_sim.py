import time


class SharedMemorySimulator:

    def __init__(self):
        self.reset()

    def reset(self):
        self.shm_id = 4096
        self.size_kb = 4
        self.attached_processes = [101, 102]
        self.shared_data = "XenoOS_IPC_Shared_Buffer_v1.0"
        self.is_locked = False
        self.history = []
        self.add_log(
            "SYSTEM",
            f"Shared Memory segment (ID: {self.shm_id}, Size: {self.size_kb}KB) initialized.",
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

    def attach_process(self, pid):
        if pid in self.attached_processes:
            return False, f"Process PID {pid} is already attached to this segment."
        self.attached_processes.append(pid)
        self.add_log(
            f"PID {pid}", f"Attached to shared memory segment ID {self.shm_id}."
        )
        return True, f"Process {pid} attached successfully."

    def detach_process(self, pid):
        if pid not in self.attached_processes:
            return False, f"Process PID {pid} is not attached."
        if len(self.attached_processes) <= 1:
            return (
                False,
                "Cannot detach last remaining process. Segment requires at least one attachment.",
            )
        self.attached_processes.remove(pid)
        self.add_log(
            f"PID {pid}", f"Detached from shared memory segment ID {self.shm_id}."
        )
        return True, f"Process {pid} detached successfully."

    def write_memory(self, pid, new_data):
        if pid not in self.attached_processes:
            return (
                False,
                f"Error: Process PID {pid} must attach to segment before writing.",
            )
        if self.is_locked:
            return (
                False,
                "Memory segment is currently LOCKED by a mutex. Write operation blocked (race condition prevention).",
            )

        old_data = self.shared_data
        self.shared_data = new_data
        self.add_log(
            f"PID {pid}",
            f"Wrote to shared memory. Content updated from '{old_data}' to '{new_data}'.",
        )
        return True, "Data successfully written to shared memory block."

    def toggle_lock(self):
        self.is_locked = not self.is_locked
        status = "LOCKED" if self.is_locked else "UNLOCKED"
        self.add_log("KERNEL", f"Mutex lock status changed to: {status}.")
        return True, f"Shared memory segment is now {status}."