#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON文件条数统计工具
统计指定目录下所有JSON文件中的条目数量
"""

import json
import os
import glob
from pathlib import Path
from typing import Dict, List, Tuple


def count_json_entries(file_path: str) -> Tuple[int, str]:
    """
    统计单个JSON文件中的条目数

    Args:
        file_path: JSON文件路径

    Returns:
        (条目数, 错误信息)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return len(data), ""
        elif isinstance(data, dict):
            # 如果是字典，尝试找到包含数据的键
            if "data" in data and isinstance(data["data"], list):
                return len(data["data"]), ""
            elif "items" in data and isinstance(data["items"], list):
                return len(data["items"]), ""
            elif "results" in data and isinstance(data["results"], list):
                return len(data["results"]), ""
            else:
                return 1, ""  # 单个对象算作1条
        else:
            return 1, ""

    except json.JSONDecodeError as e:
        return 0, f"JSON解析错误: {e}"
    except Exception as e:
        return 0, f"文件读取错误: {e}"


def scan_json_files(directory: str = ".") -> List[str]:
    """
    扫描目录下的所有JSON文件

    Args:
        directory: 要扫描的目录

    Returns:
        JSON文件路径列表
    """
    json_files = []

    # 递归查找所有.json文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))

    return sorted(json_files)


def main():
    """主函数"""
    print("=" * 60)
    print("JSON文件条数统计工具")
    print("=" * 60)

    # 只扫描data目录下的JSON文件
    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"错误: {data_dir} 目录不存在")
        return

    json_files = scan_json_files(data_dir)

    if not json_files:
        print(f"在 {data_dir} 目录下未找到任何JSON文件")
        return

    print(f"在 {data_dir} 目录下找到 {len(json_files)} 个JSON文件:")
    print("-" * 60)

    total_entries = 0
    file_stats = []

    for file_path in json_files:
        relative_path = os.path.relpath(file_path)
        entries, error = count_json_entries(file_path)

        if error:
            print(f"❌ {relative_path}: {error}")
        else:
            print(f"✅ {relative_path}: {entries:,} 条")
            total_entries += entries
            file_stats.append((relative_path, entries))

    print("-" * 60)
    print(f"总计: {total_entries:,} 条数据")

    # 按条数排序显示
    if file_stats:
        print("\n按条数排序:")
        print("-" * 60)
        sorted_stats = sorted(file_stats, key=lambda x: x[1], reverse=True)
        for file_path, entries in sorted_stats:
            print(f"{entries:>8,} 条 - {file_path}")

    # 保存统计结果到文件
    output_file = "data_json_statistics.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Data目录JSON文件条数统计报告\n")
        f.write("=" * 40 + "\n")
        f.write(f"统计时间: {os.popen('date').read().strip()}\n")
        f.write(f"统计目录: {data_dir}\n")
        f.write(f"总文件数: {len(json_files)}\n")
        f.write(f"总条数: {total_entries:,}\n\n")

        f.write("详细统计:\n")
        f.write("-" * 40 + "\n")
        for file_path, entries in sorted_stats:
            f.write(f"{entries:>8,} 条 - {file_path}\n")

    print(f"\n统计结果已保存到: {output_file}")


if __name__ == "__main__":
    main()
