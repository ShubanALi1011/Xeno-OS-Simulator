import time


class MessagePassingSimulator:

    def __init__(self):
        self.reset()

    def reset(self):
        self.mailbox = []
        self.capacity = 5  # Maximum messages buffer size
        self.history = []
        self.add_log(
            "SYSTEM",
            "Message Passing IPC kernel subsystem initialized. Mailbox buffer capacity: 5 slots.",
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

    def send_message(self, sender_pid, receiver_pid, message_text):
        if len(self.mailbox) >= self.capacity:
            return False, "Mailbox buffer is FULL! (Blocking Send simulation)"

        msg = {
            "id": len(self.history) + 1,
            "sender": f"Process {sender_pid}",
            "receiver": f"Process {receiver_pid}",
            "text": message_text,
            "time": time.strftime("%H:%M:%S"),
        }
        self.mailbox.append(msg)
        self.add_log(
            f"PID {sender_pid}",
            f"Sent message to PID {receiver_pid}: '{message_text}'",
        )
        return True, f"Message successfully delivered to Mailbox buffer."

    def receive_message(self, receiver_pid):
        if not self.mailbox:
            return False, "Mailbox is EMPTY! (Blocking Receive simulation)"

        msg = self.mailbox.pop(0)  # FIFO queue behavior
        self.add_log(
            f"PID {receiver_pid}",
            f"Received message from {msg['sender']}: '{msg['text']}'",
        )
        return True, f"Processed message from mailbox."