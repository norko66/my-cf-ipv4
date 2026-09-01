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

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")

    results = []
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

            # 过滤有效的 IPv6 地址格式
            if ":" in ip:
                results.append(f"{ip}#{isp}-{dc}")

    # 保存为 best-cf-ipv6.txt
    with open("best-cf-ipv6.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results) + "\n")

    print(f"成功抓取并生成 {len(results)} 条 IPv6 记录！")

except Exception as e:
    print(f"抓取失败: {e}")
    exit(1)
