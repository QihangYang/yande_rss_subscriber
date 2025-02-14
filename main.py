#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from yande_rss_manager import YandeRSSManager
import os
import argparse

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='Yande.re RSS订阅管理器')
    parser.add_argument('-d', '--save_folder', type=str, default='save_folder/', help='图片保存目录')
    parser.add_argument('-c', '--config_folder', type=str, default='config_folder/', help='配置文件目录')
    parser.add_argument('-a', '--add', nargs='+', help='添加关键词')
    parser.add_argument('-r', '--remove', nargs='+', help='删除关键词')
    parser.add_argument('-l', '--list', action='store_true', help='列出所有关键词')
    parser.add_argument('-i', '--interval', type=int, default=21600, help='下载间隔（秒），默认86400秒')
    
    args = parser.parse_args()
    
    # 设置默认保存路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_folder = args.save_folder or os.path.join(base_dir, 'save_folder')
    config_folder = args.config_folder or os.path.join(base_dir, 'config_folder')
    
    # 初始化RSS管理器
    manager = YandeRSSManager(save_folder, config_folder)
    
    # 处理命令行参数
    if args.add:
        manager.add_keywords(args.add)
        
    if args.remove:
        manager.remove_keywords(args.remove)
        
    if args.list:
        print('当前关键词列表：')
        for keyword in manager.keywords:
            print(f'- {keyword}')
            
    # 如果没有其他参数，则启动下载任务
    if not (args.add or args.remove or args.list):
        manager.run_forever(args.interval)

if __name__ == '__main__':
    main() 