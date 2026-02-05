"""
工具函数模块
"""

import os
import re
from datetime import datetime
from typing import Optional


def to_kebab_case(text: str) -> str:
    """
    将文本转换为kebab-case格式

    Examples:
        "用户登录" -> "user-login"
        "User Login" -> "user-login"
        "userLogin" -> "user-login"
    """
    # 处理中文：简单替换为拼音或保留
    # 这里简化处理，只处理英文
    text = re.sub(r'([a-z])([A-Z])', r'\1-\2', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'[^\w\-]', '', text)
    return text.lower().strip('-')


def generate_feature_name(title: str) -> str:
    """根据标题生成功能名称"""
    # 移除常见前缀
    prefixes = ["实现", "添加", "新增", "开发", "创建", "implement", "add", "create"]
    lower_title = title.lower()

    for prefix in prefixes:
        if lower_title.startswith(prefix):
            title = title[len(prefix):].strip()
            break

    return to_kebab_case(title) or f"feature-{datetime.now().strftime('%Y%m%d%H%M%S')}"


def get_timestamp() -> str:
    """获取当前时间戳字符串"""
    return datetime.now().strftime("%Y%m%d")


def get_iso_timestamp() -> str:
    """获取ISO格式时间戳"""
    return datetime.now().isoformat()


def ensure_dir(path: str) -> None:
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)


def read_file(path: str) -> Optional[str]:
    """读取文件内容"""
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    """写入文件"""
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def parse_bug_list(test_report: str) -> list:
    """
    从测试报告中解析Bug列表

    Returns:
        Bug列表，每个Bug包含 id, description, severity
    """
    bugs = []
    in_bug_section = False

    for line in test_report.split("\n"):
        if "Bug列表" in line or "Bug List" in line:
            in_bug_section = True
            continue

        if in_bug_section:
            # 匹配表格行: | BUG-001 | 描述 | 严重程度 | 状态 |
            match = re.match(r'\|\s*(BUG-\d+)\s*\|\s*(.+?)\s*\|\s*(\w+)\s*\|', line)
            if match:
                bugs.append({
                    "id": match.group(1),
                    "description": match.group(2).strip(),
                    "severity": match.group(3).strip(),
                })

            # 遇到下一个章节标题时停止
            if line.startswith("##") and "Bug" not in line:
                break

    return bugs


def parse_test_results(test_report: str) -> dict:
    """
    从测试报告中解析测试结果

    Returns:
        包含 total, passed, failed, pass_rate 的字典
    """
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "blocked": 0,
        "pass_rate": 0.0,
    }

    for line in test_report.split("\n"):
        if "总用例" in line or "Total" in line:
            match = re.search(r'(\d+)', line)
            if match:
                results["total"] = int(match.group(1))
        elif "通过数" in line or "Passed" in line:
            match = re.search(r'(\d+)', line)
            if match:
                results["passed"] = int(match.group(1))
        elif "失败数" in line or "Failed" in line:
            match = re.search(r'(\d+)', line)
            if match:
                results["failed"] = int(match.group(1))
        elif "通过率" in line or "Pass Rate" in line:
            match = re.search(r'([\d.]+)%?', line)
            if match:
                results["pass_rate"] = float(match.group(1))

    # 如果没有解析到通过率，计算它
    if results["pass_rate"] == 0 and results["total"] > 0:
        results["pass_rate"] = round(results["passed"] / results["total"] * 100, 1)

    return results
