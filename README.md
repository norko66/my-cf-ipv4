# Daily-updated-CF-IPV4&IPV6
为防止一次性抓取500或更多的IP导致CF封禁WORKER项目，抓取自@ethgan的项目cf-worker-bestip中更新的前45条IPV4记录。
抓取自https://www.wetest.vip/page/cloudflare/address_v6.html 中更新的IPV6记录。
每日凌晨4点自动更新一次。


#2026/9/2更新，鉴于部分CF项目只能填入一个自定义优选域名，而部分用户又同时需要IPV4&IPV6的CDN-IP，因此调整了一下代码，将45个优选IPV4及15个优选的IPV6集成至新的TXT文件。
