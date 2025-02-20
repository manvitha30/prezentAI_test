import os
import logging
from datetime import datetime

class Logger:
    """
    Singleton Logger class to manage logging for test execution.
    
    - Creates a single log file per execution under the 'logs' directory.
    - Uses a timestamp in the filename for uniqueness.
    - Ensures all logs are written to the same file.
    """
    _instance = None  # Singleton instance
    _log_file = None  # Store log file path

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)

            # Ensure logs directory exists
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)

            # Create a single log file for the entire execution
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cls._log_file = os.path.join(log_dir, f"execution_{timestamp}.log")

            print(f"Logger initialized, log file should be at: {cls._log_file}")

            # Configure logging properly with a file handler
            cls._instance.logger = logging.getLogger("TestExecutionLogger")
            cls._instance.logger.setLevel(logging.INFO)

            file_handler = logging.FileHandler(cls._log_file, mode="w")
            file_handler.setLevel(logging.INFO)

            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)

            cls._instance.logger.addHandler(file_handler)

            # Ensure log messages are flushed immediately
            cls._instance.logger.info("Logging setup complete.")
            file_handler.flush()

        return cls._instance

    def get_logger(self):
        """
        Returns the logger instance for writing logs.
        
        :return: Logger object
        """
        return self.logger
