#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
提供日志记录等通用功能

作者: Evan
日期: 2025-02-09
"""

import os
import logging
from pathlib import Path
from typing import Optional

def setup_logger(name: str, save_folder: str) -> logging.Logger:
    """
    配置日志记录器
    
    Args:
        name: 日志记录器名称
        save_folder: 日志文件保存目录
        
    Returns:
        配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    
    # 添加控制台处理器
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    # 添加文件处理器
    log_file = Path(save_folder) / 'logs.log'
    # 确保日志文件所在目录存在
    log_file.parent.mkdir(parents=True, exist_ok=True)
    # 如果日志文件不存在则创建
    if not log_file.exists():
        log_file.touch()
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
