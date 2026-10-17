# core/process_management/state_transition.py

class ProcessSimulator:
    def __init__(self, process_id="P1", process_name="Sample Process"):
        self.process_id = process_id
        self.process_name = process_name
        self.current_state = "New"
        self.history = [{"state": "New", "description": "Process created in memory (New state)."}]

    def transition(self, action):
        """
        Handles state transitions based on OS rules.
        Returns (success: bool, message: str)
        """
        state = self.current_state
        
        if state == "New":
            if action == "Admit":
                self._update_state("Ready", "Process admitted to Ready queue by Long-Term Scheduler.")
                return True, "Process moved to Ready state."
                
        elif state == "Ready":
            if action == "Dispatch":
                self._update_state("Running", "Process selected by Short-Term Scheduler (Dispatcher) and assigned to CPU.")
                return True, "Process is now Running."
                
        elif state == "Running":
            if action == "Interrupt":
                self._update_state("Ready", "CPU time slice expired (Timer Interrupt). Process moved back to Ready queue.")
                return True, "Process interrupted, moved to Ready."
            elif action == "I/O Request":
                self._update_state("Waiting", "Process requested I/O operation and moved to Waiting/Blocked state.")
                return True, "Process waiting for I/O."
            elif action == "Exit":
                self._update_state("Terminated", "Process finished execution. All resources released.")
                return True, "Process Terminated successfully."
                
        elif state == "Waiting":
            if action == "I/O Complete":
                self._update_state("Ready", "I/O operation finished. Process returned to Ready queue.")
                return True, "I/O completed, process back to Ready."
                
        return False, f"Invalid transition! Cannot perform '{action}' from '{state}' state."

    def _update_state(self, new_state, description):
        self.current_state = new_state
        self.history.append({"state": new_state, "description": description})

    def reset(self):
        self.current_state = "New"
        self.history = [{"state": "New", "description": "Process reset to New state."}]