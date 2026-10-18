import time


class ForkWaitSimulator:

    def __init__(self):
        self.reset()

    def reset(self):
        self.logs = []
        self.parent_pid = 201
        self.child_pid = None
        self.parent_status = "Running"
        self.child_status = "Not Created"
        self.shared_variable_x = 10
        self.execution_step = 0  # 0: Initial, 1: Forked, 2: Wait/Done
        self.add_log(
            "SYSTEM",
            f"Parent Process (PID: {self.parent_pid}) started. Variable X = {self.shared_variable_x}",
        )

    def add_log(self, sender, message):
        timestamp = time.strftime("%H:%M:%S")
        self.logs.insert(
            0,
            {
                "time": timestamp,
                "sender": sender,
                "message": message,
            },
        )

    def execute_fork(self):
        if self.execution_step > 0:
            return False, "Fork already executed."

        self.child_pid = self.parent_pid + 1
        self.child_status = "Running"
        self.execution_step = 1

        self.add_log(
            "KERNEL",
            f"sys_fork() executed by Parent (PID: {self.parent_pid}). Child (PID: {self.child_pid}) created as an exact duplicate context memory snapshot.",
        )
        self.add_log(
            "CHILD",
            f"Child process active. fork() return value = 0. Local variable X = {self.shared_variable_x}",
        )
        self.add_log(
            "PARENT",
            f"Parent process active. fork() return value = {self.child_pid}. Local variable X = {self.shared_variable_x}",
        )
        return True, "Process successfully forked into Parent and Child."

    def modify_variable(self, actor, new_value):
        if self.execution_step == 0:
            return False, "Execute fork first."

        self.shared_variable_x = new_value
        self.add_log(
            actor,
            f"{actor} modified shared/copied variable X to {new_value}. (Demonstrating Copy-on-Write / independent address space isolation).",
        )
        return True, f"Variable X updated to {new_value} by {actor}."

    def execute_wait(self):
        if self.execution_step != 1:
            return False, "Invalid state for sys_wait()."

        self.child_status = "Terminated (Zombie cleared)"
        self.execution_step = 2
        self.add_log(
            "PARENT",
            f"sys_wait() invoked. Parent blocked/waited until Child (PID: {self.child_pid}) exited safely. Reaped child exit status 0.",
        )
        self.add_log(
            "SYSTEM",
            f"Child process PID {self.child_pid} completely removed from process table.",
        )
        return True, "Parent successfully waited and reaped child process."