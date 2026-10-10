"""Educational EV/PV import-limit example; not validated power-system research."""
from __future__ import annotations
import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Feeder:
    nominal_voltage_v: float = 230.0
    min_voltage_v: float = 216.0
    resistance_ohm: float = 0.8
    charger_rating_kw: float = 7.0

    def __post_init__(self):
        if self.nominal_voltage_v <= 0:
            raise ValueError("Nominal voltage must be positive")
        if not 0 < self.min_voltage_v < self.nominal_voltage_v:
            raise ValueError("Minimum voltage must be between 0 and nominal")
        if self.resistance_ohm <= 0:
            raise ValueError("Resistance must be positive")
        if self.charger_rating_kw < 0:
            raise ValueError("Charger rating must be non-negative")

def estimate_voltage_v(ev_kw, base_load_kw, pv_kw, feeder):
    if min(ev_kw, base_load_kw, pv_kw) < 0:
        raise ValueError("Inputs must be non-negative")
    net_power_w = 1000 * (base_load_kw + ev_kw - pv_kw)
    return feeder.nominal_voltage_v - feeder.resistance_ohm * net_power_w / feeder.nominal_voltage_v

def import_limit_kw(pv_assumed_kw, base_load_kw, feeder):
    if pv_assumed_kw < 0 or base_load_kw < 0:
        raise ValueError("Inputs must be non-negative")
    max_net_import_kw = ((feeder.nominal_voltage_v - feeder.min_voltage_v)
                         * feeder.nominal_voltage_v / feeder.resistance_ohm / 1000)
    return min(feeder.charger_rating_kw,
               max(0.0, max_net_import_kw - base_load_kw + pv_assumed_kw))

def conservative_import_limit_kw(pv_forecast_kw, pv_error_bound_kw, base_load_kw, feeder):
    if pv_forecast_kw < 0 or pv_error_bound_kw < 0:
        raise ValueError("Forecast and uncertainty bound must be non-negative")
    return import_limit_kw(max(0.0, pv_forecast_kw - pv_error_bound_kw), base_load_kw, feeder)

def synthetic_rows(feeder):
    for hour in range(24):
        solar_shape = max(0.0, math.sin(math.pi * (hour - 6) / 12))
        pv_forecast_kw = round(6.0 * solar_shape, 4)
        pv_error_bound_kw = round(0.35 * pv_forecast_kw, 4)
        base_load_kw = 3.2 if 17 <= hour <= 21 else 2.7
        worst_case_pv_kw = max(0.0, pv_forecast_kw - pv_error_bound_kw)
        forecast_limit = import_limit_kw(pv_forecast_kw, base_load_kw, feeder)
        conservative_limit = conservative_import_limit_kw(
            pv_forecast_kw, pv_error_bound_kw, base_load_kw, feeder)
        yield {
            "hour": hour,
            "base_load_kw": round(base_load_kw, 3),
            "pv_forecast_kw": pv_forecast_kw,
            "pv_error_bound_kw": pv_error_bound_kw,
            "worst_case_pv_kw": round(worst_case_pv_kw, 3),
            "fixed_ev_limit_kw": round(min(1.5, feeder.charger_rating_kw), 3),
            "forecast_ev_limit_kw": round(forecast_limit, 3),
            "conservative_ev_limit_kw": round(conservative_limit, 3),
            "voltage_with_forecast_limit_v": round(
                estimate_voltage_v(forecast_limit, base_load_kw, worst_case_pv_kw, feeder), 3),
            "voltage_with_conservative_limit_v": round(
                estimate_voltage_v(conservative_limit, base_load_kw, worst_case_pv_kw, feeder), 3),
        }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="results/example_24h.csv")
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = list(synthetic_rows(Feeder()))
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic rows to {out}")
    print("Educational voltage approximation only; not validated feeder analysis.")

if __name__ == "__main__":
    main()
