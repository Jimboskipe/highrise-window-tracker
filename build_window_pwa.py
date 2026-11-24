"""Generate the mobile-phone-sized 15-Story Window Warehouse-to-GC-Turnover PWA (docs/index.html)."""
import json
import os
import window_pipeline as wp

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(ROOT, "docs", "window_data.json")
HTML_PATH = os.path.join(ROOT, "docs", "index.html")


def build_html():
    data = wp.export_window_json(JSON_PATH)
    data_js = json.dumps(data)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<meta name="theme-color" content="#0f172a">
<title>15-Story Window Tracker — Mobile Foreman App</title>
<style>
  :root {{
    --bg: #020617; --phone: #0f172a; --card: #1e293b; --border: #334155;
    --text: #f8fafc; --muted: #94a3b8; --accent: #0284c7; --green: #16a34a;
  }}
  * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
  body {{
    margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg); color: var(--text); display: flex; justify-content: center;
  }}
  .phone-shell {{
    width: 100%; max-width: 430px; min-height: 100vh; background: var(--phone);
    border-left: 1px solid #1e293b; border-right: 1px solid #1e293b;
    padding-bottom: 74px; position: relative;
  }}
  header {{
    background: #020617; border-bottom: 2px solid var(--accent);
    padding: 12px 14px; position: sticky; top: 0; z-index: 20;
    display: flex; justify-content: space-between; align-items: center;
  }}
  h1 {{ margin: 0; font-size: 15.5px; }}
  .sub {{ font-size: 11px; color: var(--muted); }}
  .content {{ padding: 12px; }}
  .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-bottom: 12px; }}
  .kpi {{ background: var(--card); border: 1px solid var(--border); border-radius: 7px; padding: 7px 9px; text-align: center; }}
  .kpi .l {{ font-size: 10px; color: var(--muted); text-transform: uppercase; }}
  .kpi .v {{ font-size: 17px; font-weight: 900; color: #38bdf8; margin-top: 2px; }}
  .fl-strip {{ display: flex; overflow-x: auto; gap: 6px; padding-bottom: 8px; margin-bottom: 10px; }}
  .fl-btn {{
    flex: 0 0 auto; padding: 8px 12px; border-radius: 8px; border: 2px solid var(--border);
    background: var(--card); color: var(--text); font-weight: 800; font-size: 12.5px; cursor: pointer;
  }}
  .fl-btn.active {{ border-color: #38bdf8; background: #020617; }}
  .m-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 9px; padding: 11px 12px; margin-bottom: 9px; font-size: 13px; }}
  .stage-row {{
    display: flex; justify-content: space-between; align-items: center;
    background: #020617; border: 1px solid var(--border); border-radius: 7px;
    padding: 8px 10px; margin-bottom: 6px;
  }}
  .stage-row .cnt {{ font-size: 18px; font-weight: 900; color: #38bdf8; }}
  .btn {{
    background: var(--accent); color: #fff; border: none; padding: 8px 11px;
    border-radius: 7px; font-weight: 700; font-size: 12px; cursor: pointer;
  }}
  .btn.grn {{ background: var(--green); }}
  .pal-wrap {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }}
  .pal {{ background: #020617; border: 1px solid #475569; padding: 3px 6px; border-radius: 4px; font-family: monospace; font-size: 11px; color: #bae6fd; }}
  .hall-banner {{
    background: #020617; border: 2px dashed #fbbf24; border-radius: 8px;
    padding: 9px 10px; text-align: center; color: #fde68a; font-weight: 800; font-size: 12px; margin: 10px 0;
  }}
  .bottom-nav {{
    position: fixed; bottom: 0; width: 100%; max-width: 430px; background: #020617;
    border-top: 2px solid var(--border); display: grid; grid-template-columns: repeat(3, 1fr);
    z-index: 30;
  }}
  .nav-btn {{
    background: none; border: none; color: var(--muted); padding: 11px 4px;
    font-size: 11.5px; font-weight: 700; cursor: pointer; text-align: center;
  }}
  .nav-btn.active {{ color: #fff; background: var(--accent); }}
</style>
</head>
<body>
<div class="phone-shell">
  <header>
    <div>
      <h1>15-STORY WINDOW TRACKER</h1>
      <div class="sub">2,000 SF Warehouse &rarr; Install/Caulk &rarr; GC Hand-In</div>
    </div>
    <button class="btn" onclick="window.print()">Print</button>
  </header>

  <div class="content">
    <div class="kpi-grid" id="kpiBar"></div>

    <div id="tab-tower">
      <div class="fl-strip" id="flStrip"></div>
      <div id="flCard"></div>
    </div>
    <div id="tab-warehouse" style="display:none"></div>
    <div id="tab-checklists" style="display:none"></div>
  </div>

  <nav class="bottom-nav">
    <button class="nav-btn active" onclick="showTab('tower', this)">1. Floors 1–15</button>
    <button class="nav-btn" onclick="showTab('warehouse', this)">2. 2,000 SF Whse</button>
    <button class="nav-btn" onclick="showTab('checklists', this)">3. 3 Checklists</button>
  </nav>
</div>

<script>
const DATA = {data_js};
let curFl = 6; // Default to active Floor 7 (index 6)

function showTab(name, btn) {{
  ['tower','warehouse','checklists'].forEach(t => document.getElementById('tab-' + t).style.display = (t === name) ? 'block' : 'none');
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  window.scrollTo(0, 0);
}}

function recompute() {{
  const t = {{ total_windows:0, in_warehouse:0, staged_on_floor:0, set_by_install_crew:0, caulked_ready_for_drywall:0, foreman_final_verify_1:0, touchup_verify_2_gc_handed_in:0 }};
  DATA.floors.forEach(f => {{
    t.total_windows += f.total_windows; t.in_warehouse += f.in_warehouse;
    t.staged_on_floor += f.staged_on_floor; t.set_by_install_crew += f.set_by_install_crew;
    t.caulked_ready_for_drywall += f.caulked_ready_for_drywall;
    t.foreman_final_verify_1 += f.foreman_final_verify_1;
    t.touchup_verify_2_gc_handed_in += f.touchup_verify_2_gc_handed_in;
  }});
  DATA.totals = t;
}}

function renderKpis() {{
  recompute();
  const t = DATA.totals;
  document.getElementById('kpiBar').innerHTML = `
    <div class="kpi"><div class="l">Warehouse</div><div class="v">${{t.in_warehouse}}</div></div>
    <div class="kpi"><div class="l">Floor Staged</div><div class="v">${{t.staged_on_floor}}</div></div>
    <div class="kpi"><div class="l">Set Crew</div><div class="v">${{t.set_by_install_crew}}</div></div>
    <div class="kpi"><div class="l">Caulked/DW</div><div class="v">${{t.caulked_ready_for_drywall}}</div></div>
    <div class="kpi"><div class="l">Verify #1</div><div class="v">${{t.foreman_final_verify_1}}</div></div>
    <div class="kpi"><div class="l">GC Hand-In</div><div class="v" style="color:#4ade80">${{t.touchup_verify_2_gc_handed_in}}/${{t.total_windows}}</div></div>
  `;
}}

function renderFlStrip() {{
  document.getElementById('flStrip').innerHTML = DATA.floors.map((f, i) => `
    <button class="fl-btn ${{i===curFl?'active':''}}" onclick="curFl=${{i}};renderFlStrip();renderFlCard()">
      Fl ${{f.floor}} (${{f.touchup_verify_2_gc_handed_in}}/${{f.total_windows}})
    </button>
  `).join('');
}}

function step(fromK, toK, n) {{
  const f = DATA.floors[curFl];
  const m = Math.min(n, f[fromK]);
  if (m <= 0) return;
  f[fromK] -= m; f[toK] += m;
  renderKpis(); renderFlStrip(); renderFlCard();
}}

function renderFlCard() {{
  const f = DATA.floors[curFl];
  document.getElementById('flCard').innerHTML = `
    <div class="m-card" style="border-top:4px solid #38bdf8">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <strong style="font-size:17px">Floor ${{f.floor}} (${{f.total_windows}} Windows)</strong>
        <span style="font-size:11.5px;color:#4ade80;font-weight:700">${{f.warehouse_row}}</span>
      </div>
      <div style="font-size:12px;color:var(--muted);margin:3px 0 8px">Staging Spot: ${{f.floor_staging_zone}}</div>

      <div class="stage-row">
        <div><strong>1. In 2,000 SF Warehouse</strong><div style="font-size:11px;color:var(--muted)">Sorted in 9' row (max 8 deep)</div></div>
        <div style="display:flex;align-items:center;gap:8px">
          <span class="cnt">${{f.in_warehouse}}</span>
          ${{f.in_warehouse>0 ? `<button class="btn" onclick="step('in_warehouse','staged_on_floor',4)">Deliver +4</button>` : ''}}
        </div>
      </div>

      <div class="stage-row">
        <div><strong>2. Staged on Floor (Out of Way)</strong><div style="font-size:11px;color:var(--muted)">Ready for Set Crew</div></div>
        <div style="display:flex;align-items:center;gap:8px">
          <span class="cnt">${{f.staged_on_floor}}</span>
          ${{f.staged_on_floor>0 ? `<button class="btn" onclick="step('staged_on_floor','set_by_install_crew',4)">Set +4</button>` : ''}}
        </div>
      </div>

      <div class="stage-row">
        <div><strong>3. Set by Install Crew</strong><div style="font-size:11px;color:var(--muted)">Foreman logged set; ready for Caulk Crew</div></div>
        <div style="display:flex;align-items:center;gap:8px">
          <span class="cnt">${{f.set_by_install_crew}}</span>
          ${{f.set_by_install_crew>0 ? `<button class="btn" onclick="step('set_by_install_crew','caulked_ready_for_drywall',4)">Caulk +4</button>` : ''}}
        </div>
      </div>

      <div class="stage-row">
        <div><strong>4. Caulked &amp; Ready for Drywall</strong><div style="font-size:11px;color:var(--muted)">Awaiting Foreman Final Verify #1</div></div>
        <div style="display:flex;align-items:center;gap:8px">
          <span class="cnt">${{f.caulked_ready_for_drywall}}</span>
          ${{f.caulked_ready_for_drywall>0 ? `<button class="btn" onclick="step('caulked_ready_for_drywall','foreman_final_verify_1',4)">Verify #1 +4</button>` : ''}}
        </div>
      </div>

      <div class="stage-row">
        <div><strong>5. Foreman Final Verify #1 Passed</strong><div style="font-size:11px;color:var(--muted)">Awaiting 2nd Touch-Up Verify</div></div>
        <div style="display:flex;align-items:center;gap:8px">
          <span class="cnt">${{f.foreman_final_verify_1}}</span>
          ${{f.foreman_final_verify_1>0 ? `<button class="btn grn" onclick="step('foreman_final_verify_1','touchup_verify_2_gc_handed_in',4)">Verify #2 &rarr; GC</button>` : ''}}
        </div>
      </div>

      <div class="stage-row" style="border-color:#16a34a">
        <div><strong style="color:#4ade80">6. Verify #2/#3 Done &rarr; Handed to GC</strong><div style="font-size:11px;color:var(--muted)">${{f.third_verify_required>0 ? f.third_verify_required+' unit(s) on 3rd Touch-Up Verify' : 'Signed over to General Contractor'}}</div></div>
        <span class="cnt" style="color:#4ade80">${{f.touchup_verify_2_gc_handed_in}}</span>
      </div>

      <div style="font-size:12px;color:#cbd5e1;margin-top:6px"><strong>Note:</strong> ${{f.blocker_note}}</div>
    </div>
  `;
}}

function renderWarehouse() {{
  const wh = DATA.warehouse;
  const rmHtml = (rm) => `
    <div class="m-card" style="border-top:4px solid #38bdf8">
      <div style="font-weight:900;color:#38bdf8;font-size:14.5px">${{rm.name}}</div>
      <div style="font-size:11.5px;color:var(--muted);margin:3px 0 8px">Pallets: ${{wh.pallet_width_ft}} wide &middot; Rows every ${{wh.row_spacing_ft}}' (7'+2') &middot; Max ${{wh.max_pallets_per_row}} pallets/row</div>
      ${{rm.rows.map(r => `
        <div style="background:#020617;border-left:4px solid #38bdf8;padding:8px;border-radius:6px;margin-bottom:7px">
          <div style="display:flex;justify-content:space-between;font-weight:800;font-size:12.5px">
            <span>${{r.row_id}} (${{r.wall}})</span>
            <span style="color:#4ade80">${{r.pallets_loaded}}/${{r.capacity}}</span>
          </div>
          <div style="font-size:11.5px;color:#cbd5e1;margin-top:2px">${{r.assigned_floors}}</div>
          <div class="pal-wrap">${{r.pallet_ids.map(p=>`<span class="pal">${{p}}</span>`).join('')}}</div>
        </div>
      `).join('')}}
    </div>
  `;
  document.getElementById('tab-warehouse').innerHTML =
    rmHtml(wh.rooms[0]) +
    `<div class="hall-banner">MAIN CENTER MACHINE HALLWAY &amp; DIRECT ROOM-A &harr; ROOM-B TRANSFER DOOR<br><span style="font-weight:400;font-size:11px">Rows protrude from outer walls toward center line so machine grabs pallets 1-by-1</span></div>` +
    rmHtml(wh.rooms[1]);
}}

function renderChecklists() {{
  document.getElementById('tab-checklists').innerHTML = DATA.checklists.map(c => `
    <div class="m-card">
      <div style="font-weight:900;color:#38bdf8;font-size:14px;margin-bottom:6px">${{c.title}}</div>
      ${{c.steps.map((s, i) => `
        <label style="display:flex;align-items:flex-start;gap:9px;padding:7px 0;border-top:1px solid var(--border);font-size:12.5px;cursor:pointer">
          <input type="checkbox" checked style="width:18px;height:18px;margin-top:2px">
          <span><strong>#${{i+1}}:</strong> ${{s}}</span>
        </label>
      `).join('')}}
    </div>
  `).join('');
}}

renderKpis(); renderFlStrip(); renderFlCard(); renderWarehouse(); renderChecklists();
</script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(HTML_PATH), exist_ok=True)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote mobile window app:", HTML_PATH, "bytes:", len(html))


if __name__ == "__main__":
    build_html()
