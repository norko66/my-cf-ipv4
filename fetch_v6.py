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

            dc_match = re.search(r"([A-Z]{3})", dc_raw)
            dc = dc_match.group(1) if dc_match else dc_raw

            if ":" in ip:
                # 关键修改：用 [] 包裹 IPv6 地址
                ipv6_list.append(f"[{ip}]:443#IPV6-{isp}-{dc}")

    print(f"成功抓取 {len(ipv6_list)} 条 IPv6 记录")
except Exception as e:
    print(f"IPv6 抓取失败: {e}")

# 2. 读取之前抓取好的 IPv4 文本并合并
combined_results = []

try:
    with open("best-cf-ipv4.txt", "r", encoding="utf-8") as f:
        for line in f:
            ip = line.strip()
            if ip:
                combined_results.append(ip)
except Exception as e:
    print(f"读取 IPv4 文件失败: {e}")

combined_results.extend(ipv6_list)

# 3. 输出合并后的文件
with open("best-cf-ip.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(combined_results) + "\n")

print("更新完成！")
