import csv
import os
import json
import datetime

# ===========================
# 1. 配置读取 (自动识别 VPN 或 eSIM)
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
        "year": "2026",
        "contact_email": "hello@ii-x.com"
    }
    
    # 优先读取 config.json
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                config.update(loaded)
        except Exception as e:
            print(f"⚠️ Config Error: {e}")
            
    # 智能修正：确保 data 目录存在
    if not os.path.exists('data'):
        os.makedirs('data')
        
    return config

CONFIG = load_config()

# ===========================
# 2. 核心页面生成器
# ===========================
def generate_site():
    print(f"🔄 Building V3.0 Site: {CONFIG['site_name']}...")
    
    # --- 读取数据 ---
    file_path = os.path.join('data', CONFIG.get('data_file', 'data.csv'))
    rows = []
    headers = []
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                headers = [h.strip() for h in next(reader)]
                rows = list(reader)
            except StopIteration:
                pass
    else:
        print(f"⚠️ Warning: Data file {file_path} not found. Generating empty template.")

    # --- 准备 HTML 组件 ---
    nav_html = f"""
    <nav style="background:rgba(15,23,42,0.95); backdrop-filter:blur(10px); padding:15px; text-align:center; border-bottom:1px solid #334155; position:sticky; top:0; z-index:100;">
        <a href="https://compare.ii-x.com" style="color:#e2e8f0; text-decoration:none; margin:0 10px; font-weight:600;">🤖 AI Tools</a>
        <span style="color:#475569">|</span>
        <a href="https://vpn.ii-x.com" style="color:{'#3b82f6' if 'VPN' in CONFIG['site_name'] else '#e2e8f0'}; text-decoration:none; margin:0 10px; font-weight:600;">🛡️ VPN</a>
        <span style="color:#475569">|</span>
        <a href="https://esim.ii-x.com" style="color:{'#10b981' if 'eSIM' in CONFIG['site_name'] else '#e2e8f0'}; text-decoration:none; margin:0 10px; font-weight:600;">📲 eSIM</a>
    </nav>
    """

    footer_html = f"""
    <footer style="background:#020617; border-top:1px solid #1e293b; padding:40px 0; margin-top:60px; text-align:center; color:#64748b; font-family:sans-serif; font-size:0.9rem;">
        <div style="max-width:800px; margin:0 auto; padding:0 20px;">
            <p>&copy; {CONFIG['year']} {CONFIG['site_name']}. All rights reserved.</p>
            <div style="margin:20px 0;">
                <a href="index.html" style="color:#94a3b8; text-decoration:none; margin:0 10px;">Home</a>
                <a href="privacy.html" style="color:#94a3b8; text-decoration:none; margin:0 10px;">Privacy Policy</a>
                <a href="terms.html" style="color:#94a3b8; text-decoration:none; margin:0 10px;">Terms of Use</a>
            </div>
            <p style="font-size:0.75rem; opacity:0.6; line-height:1.5;">
                <strong>Disclosure:</strong> We are reader-supported. When you buy through links on our site, we may earn an affiliate commission.
            </p>
        </div>
    </footer>
    """

    # --- 生成主页 index.html ---
    # (此处省略部分 CSS 样式以节省空间，保持 V2.0 的样式逻辑，重点在功能)
    css = f"""<style>
        :root {{ --primary: {CONFIG['primary_color']}; --bg: #0f172a; --text: #f8fafc; }}
        body {{ font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); margin: 0; }}
        .btn {{ background: var(--primary); color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: bold; display:inline-block; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #1e293b; }}
        th, td {{ padding: 15px; border-bottom: 1px solid #334155; text-align: left; }}
        th {{ background: #020617; color: #94a3b8; text-transform: uppercase; font-size: 0.75rem; }}
    </style>"""
    
    table_html = "<table><thead><tr>"
    hidden_cols = ['Affiliate_Link', 'Description', 'Badge', 'Link']
    valid_headers = [h for h in headers if h not in hidden_cols]
    
    for h in valid_headers: table_html += f"<th>{h.replace('_', ' ')}</th>"
    table_html += "<th>Action</th></tr></thead><tbody>"
    
    for row in rows:
        if not row: continue
        table_html += "<tr>"
        link = "#"
        if 'Affiliate_Link' in headers:
            try: link = row[headers.index('Affiliate_Link')]
            except: pass
        
        for idx, h in enumerate(headers):
            if h in hidden_cols: continue
            cell = row[idx] if idx < len(row) else ""
            table_html += f"<td>{cell}</td>"
        table_html += f'<td><a href="{link}" target="_blank" rel="nofollow sponsored" class="btn">Check Price</a></td></tr>'
    table_html += "</tbody></table>"

    index_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{CONFIG['site_name']} | Best of {CONFIG['year']}</title>
    <meta name="description" content="Compare the best {CONFIG['niche_keywords']} options. Unbiased reviews and pricing tables.">
    <link rel="canonical" href="{CONFIG['domain']}">
    {css}
</head>
<body>
    {nav_html}
    <div style="max-width:1200px; margin:40px auto; padding:20px;">
        <h1 style="text-align:center; font-size:2.5rem; margin-bottom:10px;">{CONFIG['hero_title']}</h1>
        <p style="text-align:center; color:#94a3b8; margin-bottom:40px;">Last updated: {datetime.datetime.now().strftime('%B %Y')}</p>
        <div style="overflow-x:auto; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.3); border:1px solid #334155;">
            {table_html}
        </div>
    </div>
    {footer_html}
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)

    # --- 生成 Sitemap.xml (Google 亲爹) ---
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>{CONFIG['domain']}/</loc>
      <lastmod>{datetime.datetime.now().strftime('%Y-%m-%d')}</lastmod>
      <changefreq>weekly</changefreq>
      <priority>1.0</priority>
   </url>
   <url>
      <loc>{CONFIG['domain']}/privacy.html</loc>
      <priority>0.5</priority>
   </url>
   <url>
      <loc>{CONFIG['domain']}/terms.html</loc>
      <priority>0.5</priority>
   </url>
</urlset>"""
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    # --- 生成 Robots.txt (爬虫指引) ---
    robots_content = f"""User-agent: *
Allow: /
Sitemap: {CONFIG['domain']}/sitemap.xml"""
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots_content)

    # --- 生成 Privacy Policy (通用模板) ---
    privacy_content = f"""<!DOCTYPE html><html><head><title>Privacy Policy - {CONFIG['site_name']}</title>{css}</head><body>{nav_html}<div style="max-width:800px; margin:40px auto; padding:20px;"><h1>Privacy Policy</h1><p>Last updated: {datetime.datetime.now().strftime('%B %d, %Y')}</p><p>Welcome to {CONFIG['site_name']}. We respect your privacy.</p><h2>Information We Collect</h2><p>We do not collect personal data directly. We use generic analytics tools.</p><h2>Affiliate Disclosure</h2><p>We participate in affiliate programs and may earn commissions.</p></div>{footer_html}</body></html>"""
    with open('privacy.html', 'w', encoding='utf-8') as f:
        f.write(privacy_content)

    # --- 生成 Terms of Use (通用模板) ---
    terms_content = f"""<!DOCTYPE html><html><head><title>Terms of Use - {CONFIG['site_name']}</title>{css}</head><body>{nav_html}<div style="max-width:800px; margin:40px auto; padding:20px;"><h1>Terms of Use</h1><p>By using {CONFIG['site_name']}, you agree to these terms.</p><h2>Content</h2><p>Our content is for informational purposes only. Prices may change.</p><h2>Liability</h2><p>We are not liable for any decisions made based on this data.</p></div>{footer_html}</body></html>"""
    with open('terms.html', 'w', encoding='utf-8') as f:
        f.write(terms_content)

    print("✅ All Files Generated: index.html, sitemap.xml, privacy.html, terms.html")

if __name__ == "__main__":
    generate_site()
