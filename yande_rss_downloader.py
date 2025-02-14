#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yande.re RSS下载器
用于从Yande.re下载图片的工具

作者: Evan
日期: 2025-02-09
"""

import re
import os
import time
import json
import logging
import urllib.parse
from pathlib import Path
from typing import Dict, Optional, List, Tuple

import numpy as np
import pandas as pd
import feedparser
import requests
from tqdm import tqdm
from requests.exceptions import RequestException
from utils import setup_logger



class YandeDownloader:
    """Yande.re图片下载器"""
    
    # 定义下载选项模式
    DOWNLOAD_PATTERNS: List[Tuple[str, str]] = [
        (r'<li><a class="original-file-unchanged" id="png"[^>]*>', '下载PNG'),
        (r'<li><a class="original-file-changed" id="highres"[^>]*>', '下载大图'), 
        (r'<li><a class="original-file-changed highres-show"[^>]*>', '查看大图')
    ]
    
    HREF_PATTERN = r'href="([^"]*)"'
    REQUEST_TIMEOUT = 30
    
    def __init__(self, save_folder: str, config_folder: str):
        """
        初始化下载器
        
        Args:
            save_folder: 图片保存目录
            config_folder: 配置文件保存目录
        """
        self.save_folder = Path(save_folder)
        self.config_folder = Path(config_folder)
        self.name = Path(__file__).name

        self.logger = setup_logger(self.name, config_folder)
        
        self._init_folders()
        
    def _init_folders(self) -> None:
        """初始化保存目录"""
        self.save_folder.mkdir(parents=True, exist_ok=True)
        self.config_folder.mkdir(parents=True, exist_ok=True)
            
    def download_image(self, yande_url: str) -> Optional[Dict]:
        """
        下载单张图片
        
        Args:
            yande_url: Yande.re图片页面URL
            
        Returns:
            包含图片信息的字典,下载失败返回None
            
        Raises:
            RequestException: 请求失败时抛出
        """
        try:
            self.logger.info('开始下载: ' + yande_url)
            response = requests.get(yande_url, timeout=self.REQUEST_TIMEOUT)
            response.raise_for_status()
        except RequestException as e:
            self.logger.error(f'访问yande链接失败: {str(e)}')
            return None

        for pattern, img_type in self.DOWNLOAD_PATTERNS:
            if match := re.search(pattern, response.text):
                if href_match := re.search(self.HREF_PATTERN, match.group(0)):
                    img_url = href_match.group(1)
                    img_name = urllib.parse.unquote(img_url.split('/')[-1])
                    
                    try:
                        img_response = requests.get(img_url, timeout=self.REQUEST_TIMEOUT)
                        img_response.raise_for_status()
                        
                        img_path = self.save_folder / img_name
                        img_path.write_bytes(img_response.content)
                            
                        return {
                            'img_url': img_url,
                            'img_name': img_name,
                            'img_type': img_type
                        }
                    except RequestException as e:
                        self.logger.error(f'下载图片失败: {str(e)}')
                        continue
                        
        self.logger.warning('未找到可用的下载链接')
        return None

    def download_rss(self, rss_url: str) -> None:
        """
        下载RSS中的所有图片
        
        Args:
            rss_url: Yande.re RSS URL
            
        Raises:
            feedparser.FeedParserError: RSS解析失败时抛出
        """
        index_path = self.config_folder / 'index.csv'
        
        # 读取或创建索引文件
        if index_path.exists():
            index = pd.read_csv(index_path)
        else:
            index = pd.DataFrame({
                'from': [], 'url': [], 'rss': [],
                'img_url': [], 'img_name': []
            })

        try:
            self.logger.info('开始读取RSS: ' + rss_url)
            feed = feedparser.parse(rss_url)
        except Exception as e:
            self.logger.error(f'读取RSS失败: {str(e)}')
            return

        for entry in tqdm(feed.entries, desc="下载进度"):
            if entry.link in index['url'].tolist():
                self.logger.info('跳过已下载: ' + entry.link)
                continue
                
            if img_info := self.download_image(entry.link):
                new_index = pd.DataFrame([{
                    'from': 'yande.re',
                    'url': entry.link,
                    'rss': rss_url,
                    'img_url': img_info['img_url'],
                    'img_name': img_info['img_name'],
                    'download_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                }])
                new_index.to_csv(index_path, mode='a', header=not index_path.exists(), index=False)

def main():
    """主函数"""
    import argparse
    parser = argparse.ArgumentParser(description='Yande.re RSS下载器')
    parser.add_argument('-u', '--rss_url', type=str, required=True, help='RSS订阅链接')
    parser.add_argument('-d', '--save_folder', type=str, required=True, help='保存文件夹路径')
    parser.add_argument('-c', '--config_folder', type=str, help='配置文件目录，默认为图片保存目录')
    args = parser.parse_args()
    
    config_folder = args.config_folder or args.save_folder
    
    try:
        downloader = YandeDownloader(args.save_folder, config_folder)
        downloader.download_rss(args.rss_url)
    except Exception as e:
        logging.error(f"程序执行出错: {str(e)}")
        raise

if __name__ == '__main__':
    main()
