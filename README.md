# High-Rise Window Logistics & 4-Gate Foreman Tracker (`2,000 Sq Ft Warehouse` -> `15-Story Tower` -> `GC Turnover`)

**"Track every commercial window pallet from the flatbed truck at the sorting warehouse through floor staging, set crew, caulk/drywall-ready prep, and the foreman's 1st, 2nd, and 3rd final verification checks before handing the floor over to the General Contractor."**

Created by **James M. Doyle** (UBC Local 1781 Journeyman Carpenter — Commercial High-Rise Window Crew & Field-to-Office Bluebeam / Digital Reporting Bridge, Madison, WI).

> **Proprietary Trading & IP Notice:** No proprietary trading strategies, live market execution code, or personal trading data have been placed in this repository. All personal and algorithmic trading systems are strictly proprietary information and are intentionally excluded from public repositories.

---

## Live Interactive Tracker App

- **Live App (GitHub Pages):** [https://jimboskipe.github.io/highrise-window-tracker/](https://jimboskipe.github.io/highrise-window-tracker/)

## End-to-End Workflow Modeled in This System

### 1. 2,000 Sq Ft Off-Site Sorting Warehouse (Two Adjacent Connected Rooms)
- **Layout:** Two adjacent `1,000 sq ft` rooms (**Room A — Inbound Truck Unload & Primary Storage Rows** and **Room B — Weekly Foreman Dispatch & Load-Out Rows**) connected both by a **Main Center Machine Hallway** and a **Direct Room-A-to-Room-B Transfer Opening**.
- **Row Pitch & Center-Line Forklift Pick:** Window pallets measure `6'0"` to `6'6"` wide. Storage rows are spaced every **`9'0"` O.C. (`7'0"` pallet bay + `2'0"` clearance)** protruding inward from the outer walls toward the center machine line so a forklift/machine can pull pallets one-by-one.
- **Stack Depth:** Maximum **`8` window pallets per row** so pallets can be sorted off the delivery truck and re-staged for the upcoming week's tower sequence with minimal double-handling.

### 2. Jobsite Delivery & Pre-Planned Floor Staging (Floors 1 to 15)
- Weekly staged pallets arrive at the tower in installation order, are hoisted to their assigned floor (`Floors 1–15`, `468` total commercial window units), and are spotted in a **pre-planned floor staging bay completely out of the way** of framing, MEP, and drywall trades.

### 3. Three Checklists & Multi-Stage Foreman Verification (`Warehouse` -> `Install & Caulk` -> `Final 1st / 2nd / 3rd Verify` -> `GC Hand-In`)
1. **Checklist Area 1 — Warehouse:** Off-truck manifest check -> slot into `9'` row (`<= 8` pallets deep) -> weekly foreman pull into Room B in exact floor-setting order.
2. **Checklist Area 2 — Installation & Caulk/Finish:**
   - **Set Crew:** Sets, levels, shims, and anchors the window frame -> Foreman marks **`SET`**.
   - **Caulk & Finish Crew:** Caulks, seals, and finishes the opening so it is **`READY FOR DRYWALL`**.
3. **Checklist Area 3 — Final Foreman Verification (2 to 3 Checks Before GC Turnover):**
   - **Check 3A (`Foreman Final Verify #1`):** Foreman walks every drywall-ready window on the floor.
   - **Check 3B (`Touch-Up Verify #2`):** Punch items are touched up and re-verified by the foreman.
   - **Check 3C (`3rd Verify if Needed` -> `Handed In to GC`):** Any unit requiring a third pass stays tracked in the 3rd-verify column until clean, then gets formally turned over to the General Contractor.

---

## Run Locally

Python 3.9+ standard library only (`dataclasses`, `json`, `unittest`).

```bash
python window_pipeline.py                    # export docs/window_data.json & print reconciliation
python build_window_pwa.py                   # build interactive docs/index.html app
python -m unittest discover -s tests -v      # run 4 reconciliation & warehouse-spec unit tests
```
