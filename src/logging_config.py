import logging
from datetime import datetime


class CustomFilter(logging.Filter):
    def __init__(self, is_execute):
        super().__init__()
        self.is_execute = is_execute

    def filter(self, record):
        if not self.is_execute and 'Deleting' in record.msg:
            record.msg = record.msg.replace('Deleting', 'Planning to delete')
        if not self.is_execute and 'Terminating' in record.msg:
            record.msg = record.msg.replace(
                'Terminating', 'Planning to Terminate')
        return True


def get_logger(is_execute: bool):
    if is_execute:
        format_str = '[EXECUTE] %(levelname)s - %(message)s'
    else:
        format_str = '[PLAN] %(levelname)s - %(message)s'

    timestamp = '%Y-%m-%d_%H:%M:%S'
    date = datetime.now().strftime(timestamp)

    handlers = [
        logging.StreamHandler()
    ]

    if is_execute:
        handlers.append(logging.FileHandler(f'{date}_service_deletion.log'))

    logging.basicConfig(
        level=logging.INFO,
        format=format_str,
        handlers=handlers
    )

    logger = logging.getLogger('aws_service_deleter')
    logger.addFilter(CustomFilter(is_execute))

    return logger
