#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yande.re RSS订阅管理器
用于管理Yande.re RSS订阅的关键词

作者: Evan
日期: 2025-02-09
"""

import time
import os
import json
from utils import setup_logger
from yande_rss_downloader import YandeDownloader

class YandeRSSManager:
    def __init__(self, save_folder: str, config_folder: str):
        """
        初始化RSS管理器
        Args:
            save_folder: 图片保存路径
            config_folder: 配置文件保存路径
        """
        self.save_folder = save_folder
        self.config_folder = config_folder
        
        # 如果保存路径不存在则创建
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)
            
        self.config_file = os.path.join(config_folder, 'config.json')
        self.interval = 3600  # 默认间隔时间1小时
        self.config = self._load_config()
        self.keywords = self.config.get('keywords', [])
        self.downloader = YandeDownloader(save_folder, config_folder)
        self.logger = setup_logger(os.path.basename(__file__), config_folder)
        
    def _load_config(self):
        """从配置文件加载配置"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.interval = config.get('interval', 3600)
                return config
        return {'keywords': [], 'interval': self.interval}
    
    def _save_config(self):
        """保存配置到配置文件"""
        config = {
            'name': 'yande_rss_manager',
            'keywords': self.keywords,
            'interval': self.interval,
            'save_folder': self.save_folder,
            'config_folder': self.config_folder,
            'update_time': time.strftime('%Y-%m-%d %H:%M:%S')  
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
            
    def add_keywords(self, new_keywords):
        """
        添加新的关键词
        :param new_keywords: 关键词列表
        """
        for keyword in new_keywords:
            if keyword not in self.keywords:
                self.keywords.append(keyword)
        self._save_config()
        self.logger.info(f'添加关键词：{new_keywords}')
        
    def remove_keywords(self, keywords_to_remove):
        """
        删除关键词
        :param keywords_to_remove: 要删除的关键词列表
        """
        self.keywords = [k for k in self.keywords if k not in keywords_to_remove]
        self._save_config()
        self.logger.info(f'删除关键词：{keywords_to_remove}')
        
    def get_rss_url(self, keyword):
        """
        生成RSS URL
        :param keyword: 关键词
        :return: RSS URL
        """
        return f'https://yande.re/post/piclens?tags={keyword}'
    
    def run_once(self):
        """执行一次下载任务"""
        self.logger.info('开始执行下载任务')
        for keyword in self.keywords:
            rss_url = self.get_rss_url(keyword)
            try:
                self.downloader.download_rss(rss_url)
            except Exception as e:
                self.logger.error(f'下载关键词 {keyword} 的RSS失败：{str(e)}')
        self.logger.info('下载任务完成')
    
    def run_forever(self, interval=3600):
        """
        持续运行下载任务
        :param interval: 间隔时间（秒），默认3600秒（1小时）
        """
        self.interval = interval
        self._save_config()
        self.logger.info('启动RSS管理器')
        while True:
            try:
                self.run_once()
                time.sleep(interval)
            except KeyboardInterrupt:
                self.logger.info('程序被用户中断')
                break
            except Exception as e:
                self.logger.error(f'发生错误：{str(e)}')
                time.sleep(60)  # 发生错误时等待1分钟后继续 