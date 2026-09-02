import re
import urllib.request
from bs4 import BeautifulSoup

url = "https://www.wetest.vip/page/cloudflare/address_v6.html"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# 1. 抓取并解析网页上的 IPv6
ipv6_list = []
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")

    for row in rows:
        isp_td = row.find("td", {"data-label": "线路名称"})
        ip_td = row.find("td", {"data-label": "优选地址"})
        datacenter_td = row.find("td", {"data-label": "数据中心"})

        if isp_td and ip_td and datacenter_td:
            isp = isp_td.text.strip()
            ip = ip_td.text.strip()
            dc_raw = datacenter_td.text.strip()

            # 提取数据中心前3位大写字母（如 HKG54-P2 -> HKG）
            dc_match = re.search(r"([A-Z]{3})", dc_raw)
            dc = dc_match.group(1) if dc_match else dc_raw

            if ":" in ip:
                ipv6_list.append(f"{ip}#{isp}-{dc}")

    print(f"成功抓取 {len(ipv6_list)} 条 IPv6 记录")
except Exception as e:
    print(f"IPv6 抓取失败: {e}")

# 2. 读取之前抓取好的 IPv4 文本，加上统一备注，并与 IPv6 合并
combined_results = []

try:
    with open("best-cf-ipv4.txt", "r", encoding="utf-8") as f:
        for line in f:
            ip = line.strip()
            if ip:
                # 如果原 IPv4 已经带有 # 备注则保持原样，否则加上 #IPv4-CF 备注
                if "#" in ip:
                    combined_results.append(ip)
                else:
                    combined_results.append(f"{ip}#IPv4-CF")
except Exception as e:
    print(f"读取 IPv4 文件失败或文件不存在: {e}")

# 追加 IPv6 数据（回车拼接）
combined_results.extend(ipv6_list)

# 3. 输出合并后的单一文件 best-cf-ip.txt
with open("best-cf-ip.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(combined_results) + "\n")

print(f"合并完成！总计生成 {len(combined_results)} 条 IP 记录至 best-cf-ip.txt")
