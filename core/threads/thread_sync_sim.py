import time


class ThreadSyncSimulator:

    def __init__(self):
        self.reset()

    def reset(self):
        self.shared_counter = 0
        self.mutex_locked = False
        self.active_lock_owner = None
        self.history = []
        self.add_log(
            "SYSTEM",
            "Thread Synchronization subsystem (Mutex & Critical Section) initialized.",
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

    def acquire_mutex(self, thread_name):
        if self.mutex_locked:
            return (
                False,
                f"Mutex lock is ALREADY held by '{self.active_lock_owner}'! '{thread_name}' is blocked.",
            )

        self.mutex_locked = True
        self.active_lock_owner = thread_name
        self.add_log(
            thread_name,
            "Acquired mutex lock. Entered Critical Section safely.",
        )
        return (
            True,
            f"Mutex acquired by {thread_name}. Entering critical section.",
        )

    def release_mutex(self, thread_name):
        if not self.mutex_locked:
            return False, "Mutex is already unlocked."
        if self.active_lock_owner != thread_name:
            return (
                False,
                f"Access denied: Mutex is owned by '{self.active_lock_owner}', not by '{thread_name}'.",
            )

        owner = self.active_lock_owner
        self.mutex_locked = False
        self.active_lock_owner = None
        self.add_log(
            owner,
            "Released mutex lock. Exited Critical Section, unblocking waiting threads.",
        )
        return True, "Mutex released successfully."

    def increment_counter(self, thread_name):
        if not self.mutex_locked or self.active_lock_owner != thread_name:
            return (
                False,
                "Race Condition Warning! Thread attempted critical write without holding mutex lock.",
            )

        self.shared_counter += 1
        self.add_log(
            thread_name,
            f"Incremented shared counter inside critical section. New value = {self.shared_counter}",
        )
        return True, f"Counter incremented to {self.shared_counter}."