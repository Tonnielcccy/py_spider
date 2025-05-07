import logging


def get_logger(log_path):
    # 创建 logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建控制台输出 handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 控制台显示日志级别

    # 创建文件输出 handler
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)  # 文件记录日志级别

    # 创建日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 将 handler 添加到 logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
