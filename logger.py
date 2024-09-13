
import logging
import sys
import os


class BasicLogger:
    def __init__(self, log_dir: str = None):
        if not log_dir:
            log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        suppressed_packages = ['mysql.connector', 'httpx', 'httpcore.connection', 'openai']
        for package in suppressed_packages:
            logging.getLogger(package).setLevel(logging.CRITICAL)
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)  # Capture all levels of logs
        self.info_log_file = os.path.join(log_dir, 'info.log')
        self.error_log_file = os.path.join(log_dir, 'error.log')
        self.debug_log_file = os.path.join(log_dir, 'debug.log')

        # Remove all handlers associated with the root logger object
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Create handlers
        self._add_file_handler(self.info_log_file, logging.INFO)
        self._add_file_handler(self.error_log_file, logging.ERROR)
        self._add_file_handler(self.debug_log_file, logging.DEBUG)
        self._add_console_handler(logging.INFO)
        

    def _add_file_handler(self, file_name, level):
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(level)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)

    def _add_console_handler(self, level):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

    def get_logger(self, name):
        return logging.getLogger(name)

# Create our logger object
logger = BasicLogger().get_logger(__name__)

def extract_response_content(input: str) -> str:
    """Getting parsable data string from LLM response
    Args:
        input (str): _description_
    Returns:
        str: _description_
    """
    logger.debug(f"[extract_response_content] Input: {input}")
    datablock = ""
    if "```" not in input:
        datablock = input
    else:
        pattern = r"```(.*?)```"
        match = re.search(pattern, input, re.DOTALL)
        if match:
            datablock = match.group(1)
    datablock = datablock.strip()
    if "[" in datablock and "]" in datablock:
        # remove anything before starting of the list [
        d = datablock.split("[")[1]
        # remove anything after ending of the list ]
        e = d.split("]")[0]
        data = f"[{e}]"
        return data
    elif datablock[0] == "{" and datablock[-1] == "}":
        return f"[{datablock}]"
    elif input[0] == "[" and input[-1] == "]":
        return input
    else:
        logger.error(f"[extract_response_content] No parsable data found in response: {input}")