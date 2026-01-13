import csv
import os
import json
import datetime
import shutil
import sys
import base64

# Tiandao eSIM Generator V2.0 (Final Stable)
# 核心特性：智能弹窗逻辑(防骚扰)、Sticky Top Bar、Base64图标、零依赖

class ESIMGenerator:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_dir, 'data', 'esim_raw.csv')
        self.config_path = os.path.join(self.base_dir, 'config.json')
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.static_dir = os.path.join(self.base_dir, 'static')
        self.generated_urls = []
        self.config = self.load_config()

        # eSIM 域名修正字典 (确保 Logo 能抓取到)
        self.domain_map = {
            "Airalo": "airalo.com",
            "Holafly": "holafly.com",
            "Nomad": "getnomad.app",
            "AloSIM": "alosim.com",
            "Instabridge": "instabridge.com",
            "BNESIM": "bnesim.com",
            "SimOptions": "simoptions.com",
            "Maya Mobile": "maya.net",
            "Ubigi": "ubigi.com",
            "GigSky": "gigsky.com"
        }

    def log(self, message):
        print(f"[ESIM-GEN] {message}")

    def load_config(self):
        config = {
            "site_name": "Global eSIM Finder",
            "domain": "https://esim.ii-x.com",
            "year": "2026",
            "google_analytics_id": "",
            "affiliate_map": {}, 
            "top_bar": {"enabled": True, "text": "✈️ Traveling? Get 15% OFF eSIMs!", "link": "#"},
            "legal": {"disclosure": "Advertiser Disclosure: We are reader-supported."}
        }
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    config.update(loaded)
                self.log("✅ Config loaded.")
            except: pass
        return config

    def load_data(self):
        self.log(f"📂 Loading data from {self.data_path}...")
        if not os.path.exists(self.data_path): return []
        data = []
        try:
            with open(self.data_path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('Provider'): data.append(row)
            self.log(f"✅ Loaded {len(data)} eSIMs.")
            return data
        except Exception as e:
            self.log(f"❌ CSV Error: {e}")
            return []

    def get_affiliate_link(self, provider, original_link):
        clean_name = str(provider).strip().lower()
        mapping = self.config.get('affiliate_map', {})
        for key, link in mapping.items():
            if key.lower() in clean_name and link: return link
        return original_link
    
    def get_real_domain(self, provider_name):
        clean = str(provider_name).strip()
        if clean in self.domain_map: return self.domain_map[clean]
        return f"{clean.lower().replace(' ', '')}.com"

    # --- 统一的 JS 脚本 (核心修复点) ---
    def get_common_script(self):
        return """
        <script>
            // 智能弹窗逻辑：统一处理入口
            function safePopup() {
                // 核心判断：如果 localStorage 里没有记录，才弹窗
                if (!localStorage.getItem('popupShown')) {
                    var popup = document.getElementById('exitPopup');
                    if(popup) {
                        popup.style.display = 'flex';
                        // 标记已显示，防止刷新或重复触发骚扰用户
                        localStorage.setItem('popupShown', 'true');
                    }
                }
            }

            // 1. Exit Intent (鼠标快速移出浏览器顶部)
            document.addEventListener('mouseleave', (e) => {
                if (e.clientY < 0) {
                    safePopup();
                }
            });
            
            // 2. 绑定关闭按钮事件
            function closePopup() {
                document.getElementById('exitPopup').style.display = 'none';
            }
        </script>
        """

    def generate_css(self):
        # 配色：使用旅游绿 (#059669) 和 活力橙 (#f59e0b)
        css_content = """
        :root { --primary: #059669; --secondary: #047857; --accent: #f59e0b; --bg: #f0fdf4; --text: #064e3b; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); margin: 0; line-height: 1.6; display: flex; flex-direction: column; min-height: 100vh; }
        .container { max-width: 1100px; margin: 0 auto; padding: 20px; width: 100%; box-sizing: border-box; flex: 1; }
        
        /* Top Bar - 冻结 + 吸顶 */
        .top-bar { 
            position: sticky; 
            top: 0; 
            z-index: 9999; 
            background: var(--accent); 
            color: white; 
            text-align: center; 
            padding: 12px; 
            font-weight: 700; 
            font-size: 14px; 
            cursor: pointer; 
            transition: background 0.2s; 
            user-select: none; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        }
        .top-bar:hover { background: #d97706; text-decoration: underline; }
        
        /* Headers - 绿色渐变 */
        header { text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #064e3b 0%, #065f46 100%); color: white; border-radius: 0 0 20px 20px; margin-bottom: 40px; }
        h1 { font-size: 2.5rem; margin: 0 0 15px 0; letter-spacing: -1px; }
        .subtitle { font-size: 1.2rem; color: #a7f3d0; max-width: 600px; margin: 0 auto; }
        
        /* Cards */
        .champion-card { background: white; border: 2px solid var(--primary); border-radius: 16px; padding: 30px; margin-bottom: 40px; box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.2); position: relative; overflow: hidden; }
        .ribbon { position: absolute; top: 0; right: 0; background: var(--primary); color: white; padding: 8px 15px; border-bottom-left-radius: 12px; font-weight: bold; font-size: 0.9rem; }
        .card { background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #d1fae5; overflow: hidden; margin-bottom: 20px; }
        
        /* Tables */
        table { width: 100%; border-collapse: collapse; }
        th { text-align: left; padding: 18px; background: #ecfdf5; color: #047857; font-size: 0.85rem; text-transform: uppercase; border-bottom: 1px solid #d1fae5; }
        td { padding: 20px 18px; border-bottom: 1px solid #e2e8f0; vertical-align: middle; }
        tr:hover { background-color: #f0fdf9; }
        
        /* Buttons */
        .btn { display: inline-block; background: var(--primary); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 700; transition: 0.2s; white-space: nowrap; text-align: center; cursor: pointer; }
        .btn:hover { background: var(--secondary); transform: translateY(-1px); box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3); }
        .btn-outline { color: #047857; text-decoration: none; font-size: 0.9rem; margin-top: 10px; display: inline-block; border: 1px solid #6ee7b7; padding: 8px 16px; border-radius: 6px; transition: 0.2s; background: white; cursor: pointer; }
        .btn-outline:hover { border-color: var(--primary); color: var(--primary); background: #ecfdf5; }

        /* Elements */
        .rank-circle { width: 32px; height: 32px; background: #ecfdf5; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; color: #059669; }
        .rank-1 { background: #fef3c7; color: #d97706; border: 2px solid #fcd34d; }
        .badge { background: #d1fae5; color: var(--primary); padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; white-space: nowrap; }
        .breadcrumbs { font-size: 0.9rem; color: #64748b; margin-bottom: 20px; }
        .breadcrumbs a { color: var(--primary); text-decoration: none; }
        .breadcrumbs span { margin: 0 8px; color: #cbd5e1; }
        
        /* Mobile */
        @media (max-width: 768px) {
            header { padding: 30px 20px; }
            h1 { font-size: 1.8rem; }
            thead { display: none; }
            tr { display: flex; flex-direction: column; padding: 20px; border-bottom: 8px solid #f8fafc; }
            td { padding: 5px 0; border: none; }
            .btn, .btn-outline { display: block; width: 100%; margin-top: 10px; box-sizing: border-box; }
        }

        footer { text-align: center; margin-top: auto; color: #64748b; font-size: 0.9rem; padding: 40px 0; background: #fff; border-top: 1px solid #f1f5f9; }
        .disclosure { background: #ecfdf5; color: #065f46; padding: 15px; font-size: 0.85rem; border: 1px solid #6ee7b7; border-radius: 8px; display: inline-block; margin-top: 20px; max-width: 800px; line-height: 1.5; }
        
        /* Popup */
        .exit-popup { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 9999; justify-content: center; align-items: center; backdrop-filter: blur(5px); }
        .popup-box { background: white; padding: 40px; border-radius: 16px; text-align: center; max-width: 400px; position: relative; animation: popIn 0.3s ease; }
        @keyframes popIn { from {transform: scale(0.9); opacity: 0;} to {transform: scale(1); opacity: 1;} }
        .close-btn { position: absolute; top: 15px; right: 20px; cursor: pointer; font-size: 24px; color: #cbd5e1; }
        """
        static_out = os.path.join(self.output_dir, 'static')
        if not os.path.exists(static_out): os.makedirs(static_out)
        with open(os.path.join(static_out, 'style.css'), 'w', encoding='utf-8') as f: f.write(css_content)

    def get_head_html(self, title, description, schema_json=None):
        ga_script = ""
        if self.config.get('google_analytics_id') and self.config['google_analytics_id'].startswith("G-"):
            ga_script = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={self.config['google_analytics_id']}"></script>
            <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{self.config['google_analytics_id']}');</script>"""
        
        schema_html = f'<script type="application/ld+json">{schema_json}</script>' if schema_json else ""

        # Favicon: 飞机 Emoji (SVG + 字体兼容)
        favicon_base64 = "data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><style>text{font-family:system-ui,sans-serif}</style><text y=%22.9em%22 font-size=%2290%22>✈️</text></svg>"

        return f"""<head>
            <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title><meta name="description" content="{description}">
            <link rel="icon" href="{favicon_base64}">
            <link rel="stylesheet" href="/static/style.css">
            {ga_script}{schema_html}
        </head>"""

    def generate_index(self, esims):
        self.log("🏆 Generating Index Page...")
        champion = esims[0] if esims else None
        champion_html = ""
        if champion:
            aff_link = self.get_affiliate_link(champion['Provider'], champion.get('Affiliate_Link', '#'))
            slug = f"{str(champion['Provider']).lower().replace(' ', '-')}-review.html"
            real_domain = self.get_real_domain(champion['Provider'])
            logo_url = f"https://www.google.com/s2/favicons?domain={real_domain}&sz=128"
            
            champion_html = f"""
            <div class="champion-card">
                <div class="ribbon">🏆 BEST FOR TRAVEL</div>
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
                    <div style="flex:1;">
                        <div style="display:flex; align-items:center; gap:15px; margin-bottom:10px;">
                            <img src="{logo_url}" style="width:48px; height:48px; border-radius:50%; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                            <h2 style="margin:0; font-size:1.8rem;">{champion['Provider']}</h2>
                        </div>
                        <p style="margin:0; color:#047857;">Top rated eSIM for seamless global connectivity.</p>
                        <div style="margin-top:15px;">
                            <span class="badge">🌐 {champion.get('Coverage', 'Global')}</span>
                            <span class="badge">⚡ {champion.get('Speed', '5G')}</span>
                        </div>
                    </div>
                    <div style="text-align:center; min-width:150px;">
                        <div class="price" style="font-size:1.5rem; font-weight:800; color:#059669;">{champion.get('Price_1GB', 'N/A')}</div>
                        <div class="period">per GB</div>
                        <a href="{aff_link}" class="btn" style="width:100%; box-sizing:border-box; margin-top:10px;">Get eSIM &rarr;</a>
                        <a href="{slug}" class="btn-outline">📖 Read Review</a>
                    </div>
                </div>
            </div>"""

        rows_html = ""
        for index, esim in enumerate(esims):
            aff_link = self.get_affiliate_link(esim['Provider'], esim.get('Affiliate_Link', '#'))
            detail_slug = f"{str(esim['Provider']).lower().replace(' ', '-')}-review.html"
            real_domain = self.get_real_domain(esim['Provider'])
            logo_url = f"https://www.google.com/s2/favicons?domain={real_domain}&sz=64"
            rank_class = "rank-1" if index == 0 else ""
            
            rows_html += f"""
            <tr onclick="window.location='{detail_slug}'" style="cursor:pointer;">
                <td width="5%"><div class="rank-circle {rank_class}">#{index + 1}</div></td>
                <td width="30%">
                    <div style="display:flex; align-items:center; gap:12px;">
                        <img src="{logo_url}" style="width:24px; height:24px; border-radius:4px;">
                        <span style="font-weight:bold; color:#064e3b;">{esim['Provider']}</span>
                    </div>
                </td>
                <td><ul style="margin:0; padding-left:15px; font-size:0.85rem; color:#047857;">
                    <li>Coverage: {esim.get('Coverage', 'N/A')}</li>
                    <li>Plans: {esim.get('Data_Plans', 'N/A')}</li>
                </ul></td>
                <td width="15%"><div style="font-weight:800; font-size:1.1rem; color:#059669;">{esim.get('Price_1GB', 'N/A')}</div></td>
                <td width="20%">
                    <a href="{aff_link}" class="btn" onclick="event.stopPropagation();" target="_blank" rel="nofollow">Get Deal</a>
                    <a href="{detail_slug}" class="btn-outline" onclick="event.stopPropagation();">📖 Review</a>
                </td>
            </tr>"""

        # 【核心修复】Top Bar 使用 onmouseenter 调用 safePopup (防止乱弹)
        top_bar_html = f'''<div class="top-bar" onmouseenter="safePopup()">{self.config["top_bar"]["text"]}</div>''' if self.config['top_bar']['enabled'] else ""

        html = f"""<!DOCTYPE html><html lang="en">
        {self.get_head_html(f"Best Travel eSIMs {self.config.get('year', '2026')}", "Compare top eSIMs.")}
        <body>
            {top_bar_html}
            <header>
                <div class="container">
                    <h1>✈️ {self.config['site_name']}</h1>
                    <p class="subtitle">Stay connected in 200+ countries. No expensive roaming fees.</p>
                </div>
            </header>
            <div class="container" style="margin-top:-60px;">
                {champion_html}
                <div class="card">
                    <table>
                        <thead><tr><th>Rank</th><th>Provider</th><th>Coverage</th><th>Price/GB</th><th>Action</th></tr></thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                </div>
                <footer>
                    <p>&copy; {self.config.get('year', '2026')} {self.config['site_name']}.</p>
                    <div class="disclosure">{self.config.get('legal', {}).get('disclosure', '')}</div>
                    <p style="margin-top:20px;"><a href="privacy.html">Privacy Policy</a> • <a href="terms.html">Terms</a></p>
                </footer>
            </div>
            <div class="exit-popup" id="exitPopup">
                <div class="popup-box">
                    <span class="close-btn" onclick="closePopup()">&times;</span>
                    <div style="font-size:3rem; margin-bottom:10px;">🎁</div>
                    <h2>Travel Smart!</h2>
                    <p>Don't pay roaming fees. Get <strong>15% OFF</strong> your first eSIM.</p>
                    <a href="#ranking" class="btn" onclick="closePopup()" style="width:100%; box-sizing:border-box; margin-top:15px;">Claim Discount</a>
                </div>
            </div>
            {self.get_common_script()}
        </body></html>"""
        with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f: f.write(html)

    def generate_details(self, esims):
        self.log("📝 Generating Detail Pages...")
        for esim in esims:
            provider = esim['Provider']
            aff_link = self.get_affiliate_link(provider, esim.get('Affiliate_Link', '#'))
            slug = f"{str(provider).lower().replace(' ', '-')}-review.html"
            real_domain = self.get_real_domain(provider)
            logo_url = f"https://www.google.com/s2/favicons?domain={real_domain}&sz=128"
            long_review = esim.get('Long_Review', '')
            if not long_review or len(long_review) < 50:
                long_review = f"<h3>Why choose {provider}?</h3><p>Detailed review coming soon...</p>"

            top_bar_html = f'''<div class="top-bar" onmouseenter="safePopup()">✈️ Traveling? Get 15% OFF eSIMs!</div>'''
            disclaimer = self.config.get('legal', {}).get('disclosure', '')

            html = f"""<!DOCTYPE html><html lang="en">
            {self.get_head_html(f"{provider} eSIM Review", f"Review of {provider}.")}
            <body>
                {top_bar_html}
                <div class="container" style="margin-top:20px;">
                    <div class="breadcrumbs"><a href="index.html">Home</a> <span>/</span> Reviews <span>/</span> {provider}</div>
                    <div class="card" style="padding:40px; text-align:center;">
                        <img src="{logo_url}" style="width:64px; height:64px; border-radius:50%; margin-bottom:20px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
                        <h1 style="margin:0;">{provider} Review</h1>
                        <a href="{aff_link}" class="btn" style="margin-top:20px; font-size:1.1rem; padding:15px 30px;" target="_blank" rel="nofollow">Get {provider} Deal &rarr;</a>
                    </div>
                    <div class="card" style="margin-top:20px; padding:40px;">
                        <div style="max-width:800px; margin:0 auto; line-height:1.8;">{long_review}</div>
                    </div>
                    <footer>
                        <p>&copy; {self.config.get('year', '2026')} {self.config['site_name']}.</p>
                        <div class="disclosure">{disclaimer}</div>
                        <p style="margin-top:20px;"><a href="privacy.html">Privacy</a> • <a href="terms.html">Terms</a></p>
                    </footer>
                </div>
                <div class="exit-popup" id="exitPopup">
                    <div class="popup-box">
                        <span class="close-btn" onclick="closePopup()">&times;</span>
                        <div style="font-size:3rem; margin-bottom:10px;">🎁</div>
                        <h2>Travel Smart!</h2>
                        <p>Get <strong>15% OFF</strong> {provider}.</p>
                        <a href="{aff_link}" class="btn" style="width:100%; box-sizing:border-box; margin-top:15px;">Claim Discount</a>
                    </div>
                </div>
                {self.get_common_script()}
            </body></html>"""
            with open(os.path.join(self.output_dir, slug), 'w', encoding='utf-8') as f: f.write(html)

    def generate_legal(self):
        for page in ['privacy', 'terms']:
            title = f"{page.capitalize()} Policy"
            content = "<p>Standard legal text...</p>"
            html = f"""<!DOCTYPE html><html lang="en">{self.get_head_html(title, title)}<body><div class="container"><header style="padding:40px;"><h1>{title}</h1></header><div class="card" style="padding:40px;">{content}</div><footer><p><a href="index.html">Back to Home</a></p></footer></div></body></html>"""
            with open(os.path.join(self.output_dir, f'{page}.html'), 'w', encoding='utf-8') as f: f.write(html)

    def generate_sitemap(self):
        base_url = self.config.get('domain', 'https://esim.ii-x.com')
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml += f'<url><loc>{base_url}/</loc><priority>1.0</priority></url>\n'
        for url in self.generated_urls: xml += f'<url><loc>{base_url}/{url}</loc><priority>0.8</priority></url>\n'
        xml += '</urlset>'
        with open(os.path.join(self.output_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f: f.write(xml)
        with open(os.path.join(self.output_dir, 'robots.txt'), 'w') as f: f.write(f"User-agent: *\nAllow: /\nSitemap: {base_url}/sitemap.xml")

    def run(self):
        self.log("🚀 Starting eSIM Generator V2.0...")
        if os.path.exists(self.output_dir): 
            try: shutil.rmtree(self.output_dir)
            except: pass
        os.makedirs(self.output_dir)
        self.generate_css()
        esims = self.load_data()
        if not esims:
            with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f: f.write("<h1>Coming Soon</h1>")
            return
        try:
            self.generate_index(esims)
            self.generate_details(esims)
            self.generate_legal()
            self.generate_sitemap()
            self.log("✅ Build Complete.")
        except Exception as e: self.log(f"❌ BUILD FAILED: {e}")

if __name__ == "__main__":
    gen = ESIMGenerator()
    gen.run()
