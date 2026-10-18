import time


class PipeSimulator:

    def __init__(self):
        self.reset()

    def reset(self):
        self.pipe_id = 501
        self.read_fd = "fd[0] (Read End)"
        self.write_fd = "fd[1] (Write End)"
        self.buffer = []
        self.capacity = 4  # Maximum buffer blocks in pipe
        self.history = []
        self.add_log(
            "SYSTEM",
            f"Anonymous Pipe created. Read Descriptor: {self.read_fd}, Write Descriptor: {self.write_fd}.",
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

    def write_to_pipe(self, writer_pid, data_chunk):
        if len(self.buffer) >= self.capacity:
            return False, "Pipe buffer is FULL! (Writer blocked)"

        self.buffer.append(data_chunk)
        self.add_log(
            f"Process {writer_pid} (Writer)",
            f"Wrote data chunk '{data_chunk}' into pipe write-end.",
        )
        return True, "Data successfully pushed into pipe buffer."

    def read_from_pipe(self, reader_pid):
        if not self.buffer:
            return False, "Pipe buffer is EMPTY! (Reader blocked / EOF)"

        data_chunk = self.buffer.pop(0)  # FIFO queue behavior
        self.add_log(
            f"Process {reader_pid} (Reader)",
            f"Read data chunk '{data_chunk}' from pipe read-end.",
        )
        return True, f"Read chunk: '{data_chunk}'."