"""Commercial Window Warehouse-to-Highrise Logistics & 4-Gate Inspection Pipeline.

Models the end-to-end commercial window package workflow used on a 15-story downtown
Madison high-rise (~100,000+ SF, 10-person window crew, 300+ trades on site):

1. 2,000 Sq Ft Off-Site Sorting Warehouse:
   - Two adjacent big rooms (Room A: Receiving & Primary Rows; Room B: Weekly Jobsite
     Staging & Overflow Rows) connected by a Main Center Machine Hallway AND a direct
     Room-to-Room Transfer Opening.
   - Window pallets are 6'0" to 6'6" wide -> rows are spaced every 9'0" (7' bay + 2' clearance)
     protruding from the outer walls toward the center machine aisle so a forklift/telehandler
     can pull pallets one-by-one.
   - Max stack depth: 8 window pallets per row.
   - Weekly staging pull: foreman pulls the upcoming week's pallets into Room B staging lanes
     in the exact installation sequence needed on the tower so deliveries arrive in setting order.

2. Jobsite Floor Delivery & Out-of-the-Way Pre-Planned Floor Staging (Floors 1 to 15):
   - Pallets arrive on site, go up the buckhoist/crane to their assigned floor, and land in the
     pre-planned Floor Staging Zone out of the way of other trades.

3. Three Checklists / Four Verification Gates (Off-Truck -> Drywall-Ready -> GC Turnover):
   - AREA 1 — WAREHOUSE CHECKLIST:
     * Gate 1 (Warehouse Off-Truck & Weekly Stage Verify): Pallet unloaded, count/glass checked
       against delivery manifest, slotted into 9' row (max 8 deep), and pulled in weekly order.
   - AREA 2 — INSTALLATION & CAULK/FINISH CHECKLIST:
     * Gate 2A (Set Crew Install Verify): Window set, shimmed, anchored by setting crew ->
       Foreman notes install complete.
     * Gate 2B (Caulk & Finish Crew — Ready for Drywall): Second crew caulks, seals, flashes,
       and finishes interior/exterior perimeter -> ready for drywallers.
   - AREA 3 — FINAL FOREMAN & TOUCH-UP VERIFICATION (2+ Checks Before GC Hand-In):
     * Gate 3A (Foreman Final Verify #1): Foreman inspects caulk, hardware, plumb/reveal, and
       drywall clearance.
     * Gate 3B (Touch-Up Verify #2 / Optional #3 -> Handed In to GC): Second verification after
       touch-ups (and 3rd if needed) before signing the opening over to the General Contractor.

Run CLI report & export JSON:  python window_pipeline.py
"""
from dataclasses import dataclass, field
import json
import os
from typing import List, Dict

WAREHOUSE_SPEC = {
    "total_sq_ft": 2000,
    "layout_description": "2,000 sq ft facility split into two adjacent rooms (Room A: 1,000 sq ft Inbound Rows; Room B: 1,000 sq ft Weekly Jobsite Dispatch & Rows) connected by a Main Center Forklift Hallway AND a direct Room-to-Room Transfer Opening.",
    "pallet_width_ft": "6' 0\" to 6' 6\"",
    "row_spacing_ft": 9,          # 7' bay + 2' clearance = 9' center-to-center row pitch
    "max_pallets_per_row": 8,     # Stacked max 8 window pallets deep protruding from wall to center aisle
    "rooms": [
        {
            "room_id": "ROOM-A",
            "name": "Room A — Inbound Truck Unload & Primary Storage Rows (1,000 Sq Ft)",
            "connections": ["Main Center Forklift Hallway", "Direct Room-A-to-Room-B Transfer Opening"],
            "rows": [
                {"row_id": "A-R1 (0'–9')",   "wall": "North Wall -> Center Line", "capacity": 8, "assigned_floors": "Floors 9–10 Window Pallets", "pallets_loaded": 8, "pallet_ids": ["PAL-09N-1","PAL-09N-2","PAL-09E-1","PAL-09S-1","PAL-09W-1","PAL-10N-1","PAL-10E-1","PAL-10S-1"]},
                {"row_id": "A-R2 (9'–18')",  "wall": "North Wall -> Center Line", "capacity": 8, "assigned_floors": "Floors 11–12 Window Pallets", "pallets_loaded": 7, "pallet_ids": ["PAL-11N-1","PAL-11E-1","PAL-11S-1","PAL-11W-1","PAL-12N-1","PAL-12E-1","PAL-12S-1"]},
                {"row_id": "A-R3 (18'–27')", "wall": "South Wall -> Center Line", "capacity": 8, "assigned_floors": "Floors 13–14 Window Pallets", "pallets_loaded": 6, "pallet_ids": ["PAL-13N-1","PAL-13E-1","PAL-13S-1","PAL-14N-1","PAL-14E-1","PAL-14S-1"]},
                {"row_id": "A-R4 (27'–36')", "wall": "South Wall -> Center Line", "capacity": 8, "assigned_floors": "Floor 15 Penthouse & Oversize 6'6\" Pallets", "pallets_loaded": 5, "pallet_ids": ["PAL-15N-1","PAL-15E-1","PAL-15S-1","PAL-15W-1","PAL-15PH-2"]},
            ],
        },
        {
            "room_id": "ROOM-B",
            "name": "Room B — Weekly Foreman Dispatch Rows & Jobsite Load-Out (1,000 Sq Ft)",
            "connections": ["Main Center Forklift Hallway (To Truck Dock)", "Direct Room-A-to-Room-B Transfer Opening"],
            "rows": [
                {"row_id": "B-R1 (0'–9')",   "wall": "North Wall -> Center Line", "capacity": 8, "assigned_floors": "THIS WEEK'S DISPATCH — Floor 7 & Floor 8 (Ordered First-Off-Truck)", "pallets_loaded": 8, "pallet_ids": ["PAL-07N-1","PAL-07E-1","PAL-07S-1","PAL-07W-1","PAL-08N-1","PAL-08E-1","PAL-08S-1","PAL-08W-1"]},
                {"row_id": "B-R2 (9'–18')",  "wall": "North Wall -> Center Line", "capacity": 8, "assigned_floors": "NEXT WEEK'S STAGING — Floor 9 Ready Pull", "pallets_loaded": 6, "pallet_ids": ["PAL-08-CRTYD","PAL-09N-STAGE","PAL-09E-STAGE","PAL-09S-STAGE","PAL-09W-STAGE","PAL-09-CRTYD"]},
                {"row_id": "B-R3 (18'–27')", "wall": "South Wall -> Center Line", "capacity": 8, "assigned_floors": "Replacement Glass / Warranty / Trim & Sill Pan Pallets", "pallets_loaded": 3, "pallet_ids": ["PAL-PAN-SILL","PAL-REPL-06W","PAL-CAULK-ROD"]},
            ],
        },
    ],
}


@dataclass
class FloorWindowPackage:
    floor: int
    total_windows: int
    warehouse_row: str
    floor_staging_zone: str
    # Stage counts across the pipeline (must reconcile to total_windows)
    in_warehouse: int
    staged_on_floor: int
    set_by_install_crew: int          # Set crew done, awaiting caulk/finish crew
    caulked_ready_for_drywall: int    # Caulk & finish crew done, awaiting Foreman Final Verify #1
    foreman_final_verify_1: int       # Foreman Final Check #1 passed, awaiting Touch-Up Verify #2
    touchup_verify_2_gc_handed_in: int  # Passed 2nd (or 3rd) touch-up verify & handed in to GC
    third_verify_required: int = 0    # Units flagged for 3rd re-verify (damaged glass / caulk redo)
    blocker_note: str = ""

    @property
    def accounted_total(self) -> int:
        return (
            self.in_warehouse
            + self.staged_on_floor
            + self.set_by_install_crew
            + self.caulked_ready_for_drywall
            + self.foreman_final_verify_1
            + self.touchup_verify_2_gc_handed_in
        )


def sample_15_story_tower() -> List[FloorWindowPackage]:
    return [
        FloorWindowPackage(1, 24, "Delivered Set", "Fl 1 North Retail Bay (Cleared)", 0, 0, 0, 0, 0, 24, 0, "100% Handed in to GC — Drywall Complete"),
        FloorWindowPackage(2, 32, "Delivered Set", "Fl 2 East Core Alcove (Cleared)", 0, 0, 0, 0, 0, 32, 0, "100% Handed in to GC — Drywall Complete"),
        FloorWindowPackage(3, 32, "Delivered Set", "Fl 3 East Core Alcove (Cleared)", 0, 0, 0, 0, 0, 32, 0, "100% Handed in to GC — Drywall Complete"),
        FloorWindowPackage(4, 32, "Delivered Set", "Fl 4 East Core Alcove (Cleared)", 0, 0, 0, 0, 0, 32, 0, "100% Handed in to GC — Drywall Complete"),
        FloorWindowPackage(5, 32, "Delivered Set", "Fl 5 Center Corridor Bay", 0, 0, 0, 0, 2, 30, 2, "30 Handed to GC; 2 units on 3rd Touch-Up Verify (exterior perimeter bead re-tool)"),
        FloorWindowPackage(6, 32, "Delivered Set", "Fl 6 Center Corridor Bay", 0, 0, 0, 4, 10, 18, 1, "18 Handed to GC; 10 at Foreman Final Verify #1; 4 Caulk Crew finishing today"),
        FloorWindowPackage(7, 32, "Room B — Row B-R1", "Fl 7 West Elevator Lobby Bay (Out of Drywallers' Way)", 0, 4, 14, 14, 0, 0, 0, "Set Crew finished 28; Caulk Crew has 14 ready for drywall; 4 staged on floor"),
        FloorWindowPackage(8, 32, "Room B — Row B-R1", "Fl 8 West Elevator Lobby Bay (Pre-Planned Staging)", 4, 12, 16, 0, 0, 0, 0, "Set Crew actively setting North & East elevations (16 set, 12 staged on floor, 4 on tomorrow's truck)"),
        FloorWindowPackage(9, 32, "Room A — Row A-R1 -> Moving to B-R2", "Fl 9 West Elevator Lobby Bay", 24, 8, 0, 0, 0, 0, 0, "First 2 pallets hoisted to Fl 9 staging zone; remaining 6 pallets staged in Room B Row B-R2 for Thursday truck"),
        FloorWindowPackage(10, 32, "Room A — Row A-R1", "Fl 10 West Elevator Lobby Bay", 32, 0, 0, 0, 0, 0, 0, "In Warehouse Room A Row A-R1 (8-pallet stack)"),
        FloorWindowPackage(11, 32, "Room A — Row A-R2", "Fl 11 West Elevator Lobby Bay", 32, 0, 0, 0, 0, 0, 0, "In Warehouse Room A Row A-R2"),
        FloorWindowPackage(12, 32, "Room A — Row A-R2", "Fl 12 West Elevator Lobby Bay", 32, 0, 0, 0, 0, 0, 0, "In Warehouse Room A Row A-R2"),
        FloorWindowPackage(13, 32, "Room A — Row A-R3", "Fl 13 West Elevator Lobby Bay", 32, 0, 0, 0, 0, 0, 0, "In Warehouse Room A Row A-R3"),
        FloorWindowPackage(14, 32, "Room A — Row A-R3", "Fl 14 West Elevator Lobby Bay", 32, 0, 0, 0, 0, 0, 0, "In Warehouse Room A Row A-R3"),
        FloorWindowPackage(15, 28, "Room A — Row A-R4", "Fl 15 Penthouse Center Bay", 28, 0, 0, 0, 0, 0, 0, "In Warehouse Room A Row A-R4 (6'6\" wide penthouse pallets)"),
    ]


CHECKLIST_AREAS = [
    {
        "area_id": "AREA-1",
        "title": "1. Warehouse Checklist (Off-Truck -> 9' Row Slot -> Weekly Dispatch Order)",
        "steps": [
            "Truck Unload & Manifest Check: Verify pallet width (6'0\" to 6'6\"), opening tags, and glass condition as pallet comes off flatbed.",
            "Row Slotting (9' Row Pitch = 7' Pallet Bay + 2' Clearance, Max 8 Pallets Deep): Slot pallet into assigned Room A row protruding from outer wall toward center machine hallway.",
            "Weekly Foreman Pull to Room B (Through Room-to-Room Transfer or Main Hallway): Restage next week's pallets into Room B in reverse load order so pallets arrive at the tower in exact floor-setting sequence."
        ],
    },
    {
        "area_id": "AREA-2",
        "title": "2. Jobsite Installation & Caulk/Finish Checklist (Staged Out of Way -> Set Crew -> Caulk Crew -> Ready for Drywall)",
        "steps": [
            "Floor Delivery & Pre-Planned Staging: Hoist pallets to assigned floor and spot in the pre-planned staging bay completely out of the path of metal-stud/MEP trades.",
            "Set Crew Installation: Set window frame into rough opening, laser level/plumb, shim, and anchor to spec -> Foreman logs opening as SET.",
            "Caulk & Finish Crew (Drywall-Ready Prep): Second crew caulks exterior/interior perimeter, installs backer rod/flashing/trim -> logs opening READY FOR DRYWALL."
        ],
    },
    {
        "area_id": "AREA-3",
        "title": "3. Final Foreman Multi-Stage Verification (Final Verify #1 -> Touch-Up Verify #2 -> 3rd Verify if Needed -> Hand In to GC)",
        "steps": [
            "Check 3A — Foreman Final Verify #1: Foreman walks every 'Ready for Drywall' window on the floor, checking caulk continuity, anchor heads, hardware lock, and drywall return clearance.",
            "Check 3B — Touch-Up Verify #2: Any punch item flagged in Check 3A gets touched up and re-walked by the foreman for 2nd sign-off.",
            "Check 3C — 3rd Verify (When Required) & GC Turnover: If a stubborn leak/glass/frame issue takes a 3rd pass, track it in the 3rd-Verify queue until clean, then sign the floor over to the General Contractor."
        ],
    },
]


def export_window_json(out_path: str) -> dict:
    floors = sample_15_story_tower()
    totals = {
        "total_windows": sum(f.total_windows for f in floors),
        "in_warehouse": sum(f.in_warehouse for f in floors),
        "staged_on_floor": sum(f.staged_on_floor for f in floors),
        "set_by_install_crew": sum(f.set_by_install_crew for f in floors),
        "caulked_ready_for_drywall": sum(f.caulked_ready_for_drywall for f in floors),
        "foreman_final_verify_1": sum(f.foreman_final_verify_1 for f in floors),
        "touchup_verify_2_gc_handed_in": sum(f.touchup_verify_2_gc_handed_in for f in floors),
        "third_verify_required": sum(f.third_verify_required for f in floors),
        "unaccounted": sum(f.total_windows - f.accounted_total for f in floors),
    }
    payload = {
        "project_name": "15-Story Commercial High-Rise Window Logistics & 4-Gate Foreman Tracker (Madison, WI Workflow)",
        "warehouse": WAREHOUSE_SPEC,
        "checklists": CHECKLIST_AREAS,
        "totals": totals,
        "floors": [
            {
                "floor": f.floor,
                "total_windows": f.total_windows,
                "warehouse_row": f.warehouse_row,
                "floor_staging_zone": f.floor_staging_zone,
                "in_warehouse": f.in_warehouse,
                "staged_on_floor": f.staged_on_floor,
                "set_by_install_crew": f.set_by_install_crew,
                "caulked_ready_for_drywall": f.caulked_ready_for_drywall,
                "foreman_final_verify_1": f.foreman_final_verify_1,
                "touchup_verify_2_gc_handed_in": f.touchup_verify_2_gc_handed_in,
                "third_verify_required": f.third_verify_required,
                "accounted_total": f.accounted_total,
                "blocker_note": f.blocker_note,
            }
            for f in floors
        ],
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return payload


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "window_data.json")
    d = export_window_json(out)
    print(d["project_name"])
    print("TOTALS:", d["totals"])


if __name__ == "__main__":
    main()
