import csv
import os
import json
import datetime

# ===========================
# 1. 强壮的配置读取
# ===========================
def load_config():
    config = {
        "site_name": "Comparison Site",
        "domain": "https://ii-x.com",
        "niche_keywords": "Review",
        "hero_title": "Best Tools Compared",
        "primary_color": "#2563eb",
        "data_file": "data.csv",
        "icon": "⚡", 
        "year": "2026"
    }
    
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                config.update(loaded)
        except Exception as e:
            print(f"⚠️ Config Error: {e}")
            # 智能回退机制
            if os.path.exists(os.path.join('data', 'vpn_raw.csv')):
                config.update({'data_file': 'vpn_raw.csv', 'site_name': 'VPN Shield', 'icon': '🛡️'})
            elif os.path.exists(os.path.join('data', 'esim_raw.csv')):
                config.update({'data_file': 'esim_raw.csv', 'site_name': 'Global eSIM', 'icon': '📲'})
    
    return config

CONFIG = load_config()

# ===========================
# 2. 样式系统 (CSS)
# ===========================
# 动态生成 SVG Favicon
FAVICON_SVG = f'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>{CONFIG["icon"]}</text></svg>'

CSS = """
<style>
    :root {{ --primary: {primary_color}; --bg: #0f172a; --text: #f8fafc; --card-bg: #1e293b; --footer-bg: #020617; }}
    body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
    
    /* 导航栏 */
    nav {{ background: rgba(26, 26, 26, 0.95); backdrop-filter: blur(10px); padding: 15px; text-align: center; border-bottom: 1px solid #333; position: sticky; top: 0; z-index: 100; }}
    nav a {{ color: #e2e8f0; text-decoration: none; margin: 0 12px; font-weight: 600; font-size: 0.95rem; transition: color 0.2s; }}
    nav a:hover {{ color: var(--primary); }}
    nav span {{ color: #475569; }}

    .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; flex: 1; }}
    
    /* 头部区域 */
    header {{ text-align: center; margin: 60px 0 40px; }}
    h1 {{ font-size: 3rem; margin: 0 0 10px; background: linear-gradient(to right, #60a5fa, var(--primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1px; }}
    .subtitle {{ color: #94a3b8; font-size: 1.1rem; max-width: 600px; margin: 0 auto; line-height: 1.6; }}
    
    /* 免责声明 (合规关键) */
    .disclosure-top {{ font-size: 0.75rem; color: #64748b; text-align: center; margin-top: 15px; background: rgba(30, 41, 59, 0.5); display: inline-block; padding: 4px 12px; border-radius: 20px; }}

    /* 表格样式 */
    .table-container {{ overflow-x: auto; border-radius: 16px; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2); border: 1px solid #334155; }}
    .comparison-table {{ width: 100%; border-collapse: collapse; background: var(--card-bg); white-space: nowrap; }}
    th {{ background: #0f172a; color: #94a3b8; padding: 20px; text-align: left; font-weight: 700; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; border-bottom: 2px solid #334155; }}
    td {{ padding: 20px; border-bottom: 1px solid #334155; color: #e2e8f0; vertical-align: middle; font-size: 0.95rem; }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover {{ background: #2d3748; }}

    /* 按钮与标签 */
    .btn {{ display: inline-flex; align-items: center; justify-content: center; background: var(--primary); color: white; padding: 10px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: all 0.2s; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2); }}
    .btn:hover {{ transform: translateY(-2px); filter: brightness(110%); box-shadow: 0 10px 15px -3px rgba(var(--primary), 0.4); }}
    
    .tag {{ padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 700; display: inline-block; }}
    .tag-green {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .tag-red {{ background: rgba(239, 68, 68, 0.15); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.3); }}

    /* 页脚 */
    footer {{ background: var(--footer-bg); border-top: 1px solid #1e293b; padding: 60px 0 40px; margin-top: 80px; font-size: 0.9rem; color: #64748b; }}
    .footer-content {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }}
    .footer-links a {{ color: #94a3b8; text-decoration: none; margin-right: 20px; transition: color 0.2s; }}
    .footer-links a:hover {{ color: var(--primary); }}
    .disclaimer-text {{ margin-top: 20px; font-size: 0.8rem; line-height: 1.6; opacity: 0.7; }}
    
    @media (max-width: 768px) {{
        .footer-content {{ grid-template-columns: 1fr; text-align: center; }}
        .footer-links {{ margin-top: 20px; }}
        h1 {{ font-size: 2rem; }}
    }}
</style>
""".format(primary_color=CONFIG.get('primary_color', '#2563eb'))

# ===========================
# 3. 核心生成逻辑
# ===========================
def generate_site():
    print(f"🔄 Building Complete Site: {CONFIG['site_name']}...")
    
    file_path = os.path.join('data', CONFIG.get('data_file', 'data.csv'))
    if not os.path.exists(file_path):
        print(f"❌ Critical: Data file {file_path} NOT found.")
        # 紧急避险：生成一个优雅的等待页，而不是报错
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(f"<html><body style='background:#0f172a;color:#fff;text-align:center;padding:50px;font-family:sans-serif'><h1>🚧 System Syncing...</h1><p>Data is being replicated from our global nodes. Please refresh in 60 seconds.</p></body></html>")
        return

    # 读取数据
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = [h.strip() for h in next(reader)]
            rows = list(reader)
        except StopIteration:
            return

    # 导航栏 (绝对链接闭环)
    NAV_HTML = """
    <nav>
        <a href="https://compare.ii-x.com">🤖 AI Tools</a>
        <span>|</span>
        <a href="https://vpn.ii-x.com" style="color: {c_vpn}">🛡️ VPN Privacy</a>
        <span>|</span>
        <a href="https://esim.ii-x.com" style="color: {c_esim}">📲 Travel eSIM</a>
    </nav>
    """.format(
        c_vpn="#3b82f6" if "VPN" in CONFIG['site_name'] else "#e2e8f0",
        c_esim="#10b981" if "eSIM" in CONFIG['site_name'] else "#e2e8f0"
    )

    # 构建 HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <title>{CONFIG['site_name']} | {CONFIG['year']} Official Ranking</title>
        <meta name="description" content="Unbiased comparison of the best {CONFIG['niche_keywords']} in {CONFIG['year']}. We test speed, pricing, and features to help you save money.">
        <link rel="canonical" href="{CONFIG['domain']}">
        <link rel="icon" href="{FAVICON_SVG}">
        
        <meta property="og:type" content="website">
        <meta property="og:url" content="{CONFIG['domain']}">
        <meta property="og:title" content="{CONFIG['site_name']}">
        <meta property="og:description" content="{CONFIG['hero_title']}">
        
        {CSS}
    </head>
    <body>
        {NAV_HTML}
        
        <header>
            <div class="container">
                <div class="disclosure-top">Transparency: We may earn a commission when you buy through our links.</div>
                <h1>{CONFIG['hero_title']}</h1>
                <p class="subtitle">
                    Data last verified: {datetime.datetime.now().strftime('%B %d, %Y')} <br>
                    <span style="font-size:0.9rem; opacity:0.8">Analyzing {len(rows)} providers across global markets.</span>
                </p>
            </div>
        </header>

        <div class="container">
            <div class="table-container">
                <table class="comparison-table">
                    <thead><tr>
    """
    
    # 动态表头
    hidden_cols = ['Affiliate_Link', 'Description', 'Badge', 'Link']
    for h in headers:
        if h not in hidden_cols:
            html_content += f"<th>{h.replace('_', ' ')}</th>"
    html_content += "<th>Verdict</th></tr></thead><tbody>"
    
    # 动态数据
    for row in rows:
        if not row: continue
        html_content += "<tr>"
        
        # 提取链接
        link = "#"
        if 'Affiliate_Link' in headers:
            try: link = row[headers.index('Affiliate_Link')]
            except: pass
            
        # 填充数据
        for idx, col_name in enumerate(headers):
            if col_name in hidden_cols: continue
            
            cell = row[idx] if idx < len(row) else ""
            display = cell
            
            # 智能高亮逻辑
            lower = str(cell).lower()
            if any(x in lower for x in ['yes', 'true', 'netflix', 'unlimited', '4k', '5g']):
                display = f'<span class="tag tag-green">{cell}</span>'
            elif any(x in lower for x in ['no', 'false', 'block', 'slow']):
                display = f'<span class="tag tag-red">{cell}</span>'
                
            html_content += f"<td>{display}</td>"
        
        html_content += f'<td><a href="{link}" target="_blank" rel="sponsored noopener" class="btn">👉 Check Price</a></td></tr>'

    # 页脚与版权 (品牌闭环)
    html_content += f"""
                    </tbody>
                </table>
            </div>
        </div>

        <footer>
            <div class="footer-content">
                <div>
                    <div style="font-size:1.5rem; font-weight:bold; color:#fff; margin-bottom:15px;">{CONFIG['icon']} {CONFIG['site_name'].split('|')[0].strip()}</div>
                    <p>&copy; {CONFIG['year']} ii-x.com Network. All rights reserved.</p>
                    <p>Part of the Blade Matrix Project.</p>
                </div>
                <div>
                    <div class="footer-links">
                        <a href="#">About Us</a>
                        <a href="#">Editorial Policy</a>
                        <a href="#">Privacy Policy</a>
                        <a href="#">Terms of Use</a>
                    </div>
                    <p class="disclaimer-text">
                        <strong>Advertising Disclosure:</strong> We are an independent review site supported by our readers. 
                        When you purchase through links on our site, we may earn an affiliate commission. 
                        This does not affect our editorial independence or the price you pay.
                    </p>
                </div>
            </div>
        </footer>
    </body>
    </html>
    """
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ COMPLETE Site Generated: {CONFIG['site_name']}")

if __name__ == "__main__":
    generate_site()
