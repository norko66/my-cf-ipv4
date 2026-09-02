import re
import urllib.request
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# -------------------------------------------------------------------
# 1. 抓取 wetest.vip 网页上的 IPv6
# -------------------------------------------------------------------
wetest_url = "https://www.wetest.vip/page/cloudflare/address_v6.html"
wetest_ipv6_list = []

try:
    req = urllib.request.Request(wetest_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
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
                wetest_ipv6_list.append(f"[{ip}]:443#IPV6-{isp}-{dc}")

    print(f"成功抓取 wetest.vip {len(wetest_ipv6_list)} 条 IPv6 记录")
except Exception as e:
    print(f"wetest.vip 抓取失败: {e}")

# -------------------------------------------------------------------
# 2. 抓取 ipdb.030101.xyz/bestcfv6/ 网页上的 IPv6
# -------------------------------------------------------------------
ipdb_url = "https://ipdb.030101.xyz/bestcfv6/"
ipdb_ipv6_list = []

# 正则表达式：识别标准 IPv6 地址
ipv6_pattern = re.compile(r'(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}')

try:
    req = urllib.request.Request(ipdb_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode("utf-8")

    # 在页面源码中正则查找所有匹配的 IPv6 地址
    found_ips = ipv6_pattern.findall(html)
    
    # 过滤去重并格式化
    seen_ips = set()
    for idx, ip in enumerate(found_ips, start=1):
        if ip not in seen_ips and ":" in ip:
            seen_ips.add(ip)
            ipdb_ipv6_list.append(f"[{ip}]:443#IPV6-IPDB优选-{idx}")

    print(f"成功抓取 ipdb.030101.xyz {len(ipdb_ipv6_list)} 条 IPv6 记录")
except Exception as e:
    print(f"ipdb.030101.xyz 抓取失败: {e}")

# -------------------------------------------------------------------
# 3. 读取本地 IPv4 列表
# -------------------------------------------------------------------
combined_results = []

try:
    with open("best-cf-ipv4.txt", "r", encoding="utf-8") as f:
        for line in f:
            ip = line.strip()
            if ip:
                combined_results.append(ip)
except Exception as e:
    print(f"读取 IPv4 文件失败: {e}")

# -------------------------------------------------------------------
# 4. 合并所有数据 (IPv4 -> wetest IPv6 -> ipdb IPv6 -> 自定义域名)
# -------------------------------------------------------------------
combined_results.extend(wetest_ipv6_list)
combined_results.extend(ipdb_ipv6_list)

domain_list = [
    "123.cf.090227.xyz:443#CMLIU优选域名",
    "www.visa.cn:443#VISA官方优选域名",
    "mfa.gov.ua:443#乌克兰优选域名",
    "www.shopify.com:443#shopify优选域名",
    "store.ubi.com:443#育碧优选域名",
    "staticdelivery.nexusmods.com:443#MOD优选域名",
    "cloudflare-dl.byoip.top:443#NB优选域名",
    "cf.877774.xyz:443#秋名山优选域名",
    "saas.sin.fan:443#MIYU优选域名",
    "bestcf.030101.xyz:443#MINGYU移动优选域名",
    "cf.cloudflare.182682.xyz:443#WETEST优选域名",
]

combined_results.extend(domain_list)

# -------------------------------------------------------------------
# 5. 输出合并后的文件 best-cf-ip.txt
# -------------------------------------------------------------------
with open("best-cf-ip.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(combined_results) + "\n")

print(f"合并完成！总计写入 {len(combined_results)} 条记录至 best-cf-ip.txt")
