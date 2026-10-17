import time


class ProcessNode:

    def __init__(
        self, pid, name, parent_id=None, memory_allocated=64, priority="Normal"
    ):
        self.pid = pid
        self.name = name
        self.parent_id = parent_id
        self.children = []
        self.memory_allocated = memory_allocated  # in MB
        self.priority = priority
        self.status = "Ready"
        self.created_at = time.strftime("%H:%M:%S")

    def to_dict(self):
        return {
            "PID": self.pid,
            "Name": self.name,
            "Parent PID": self.parent_id if self.parent_id else "None (Init)",
            "Memory": f"{self.memory_allocated} MB",
            "Priority": self.priority,
            "Status": self.status,
            "Created At": self.created_at,
        }


class ProcessCreationSimulator:

    def __init__(self):
        self.reset()

    def reset(self):
        self.next_pid = 100
        # Root process (Init / Systemd)
        self.root = ProcessNode(
            pid=1,
            name="systemd (Init)",
            parent_id=None,
            memory_allocated=128,
            priority="High",
        )
        self.processes = {1: self.root}
        self.history = [
            {
                "action": "SYSTEM INIT",
                "pid": 1,
                "description": "Kernel initialized root process systemd (PID: 1).",
                "time": time.strftime("%H:%M:%S"),
            }
        ]

    def fork_process(
        self, parent_pid, child_name, memory_mb=64, priority="Normal"
    ):
        if parent_pid not in self.processes:
            return False, f"Parent PID {parent_pid} not found."

        parent = self.processes[parent_pid]
        new_pid = self.next_pid
        self.next_pid += 1

        child = ProcessNode(
            pid=new_pid,
            name=child_name,
            parent_id=parent_pid,
            memory_allocated=memory_mb,
            priority=priority,
        )

        parent.children.append(child)
        self.processes[new_pid] = child

        self.history.append(
            {
                "action": "FORK",
                "pid": new_pid,
                "description": f"sys_fork(): Process '{child_name}' (PID: {new_pid}) spawned by Parent (PID: {parent_pid}).",
                "time": time.strftime("%H:%M:%S"),
            }
        )
        return True, f"Process {child_name} (PID: {new_pid}) created."

    def terminate_process(self, pid):
        if pid == 1:
            return False, "Cannot terminate root process (Init)."

        if pid not in self.processes:
            return False, f"PID {pid} not found."

        proc = self.processes[pid]

        # Recursively collect all descendants
        to_remove = []

        def collect_descendants(node):
            to_remove.append(node.pid)
            for child in node.children:
                collect_descendants(child)

        collect_descendants(proc)

        # Remove from parent's children list
        if proc.parent_id in self.processes:
            parent = self.processes[proc.parent_id]
            parent.children = [c for c in parent.children if c.pid != pid]

        # Remove all collected PIDs
        for p_id in to_remove:
            if p_id in self.processes:
                del self.processes[p_id]

        self.history.append(
            {
                "action": "EXIT",
                "pid": pid,
                "description": f"sys_exit(): Terminated PID {pid} and cleared {len(to_remove)} associated process node(s).",
                "time": time.strftime("%H:%M:%S"),
            }
        )
        return True, f"Terminated PID {pid}."

    def get_process_list(self):
        return [p.to_dict() for p in self.processes.values()]