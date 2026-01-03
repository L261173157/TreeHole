"""
IP地理位置查询工具

使用免费的IP地理位置API查询IP地址的地理位置信息
"""

import requests
from typing import Optional
from logger import setupLogger, logError, logInfo

logger = setupLogger("ip_utils")


def get_client_ip(request) -> str:
    """
    从请求中获取客户端真实IP地址

    Args:
        request: FastAPI请求对象

    Returns:
        str: 客户端IP地址
    """
    # 尝试从各种可能的头部获取IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # X-Forwarded-For可能包含多个IP，取第一个
        return forwarded.split(",")[0].strip()

    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # 如果没有代理，直接从客户端地址获取
    if hasattr(request, "client") and request.client:
        return request.client.host

    return "未知"


def get_ip_location(ip_address: str) -> Optional[str]:
    """
    查询IP地址的地理位置

    使用免费的IP地理位置API
    失败时返回None

    Args:
        ip_address (str): IP地址

    Returns:
        Optional[str]: 地理位置，如 "北京市" 或 "中国 北京市"
    """
    if not ip_address or ip_address == "未知":
        return None

    try:
        # 使用免费的IP地理位置API
        # 这里使用 ip-api.com 的免费API（无需API key）
        url = f"http://ip-api.com/json/{ip_address}?lang=zh-CN"

        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()

            if data.get("status") == "success":
                # 组合地理位置信息
                country = data.get("country", "")
                region_name = data.get("regionName", "")
                city = data.get("city", "")

                # 构建位置字符串
                location_parts = []
                if country and country != "中国":
                    location_parts.append(country)
                if region_name:
                    location_parts.append(region_name)
                if city and city != region_name:
                    location_parts.append(city)

                location = " ".join(location_parts) if location_parts else None

                if location:
                    logInfo(logger, f"IP {ip_address} 位置: {location}")
                    return location

        logInfo(logger, f"无法获取IP {ip_address} 的位置信息")
        return None

    except Exception as e:
        logError(logger, e, f"查询IP位置失败: {ip_address}")
        return None
