# EV Charging Import Limits Under Solar PV Forecast Uncertainty

**Educational Python demonstration — not validated research.**

This project illustrates EV charging import limits using a simplified single-phase, single-bus resistive feeder voltage approximation. It compares forecast-based limits against conservative limits that assume lower-than-forecast PV output.

The prototype was drafted as a portfolio learning example; it is **not** a full AC power-flow solver, a validated dynamic operating envelope, or a real-world charging controller.

## Model

```text
P_net = P_base + P_EV - P_PV
V_est = V0 - (R * P_net) / V0
P_EV,max = ((V0 - V_min) * V0 / R) - P_base + P_PV
```

Powers in the voltage equation are in watts; resistance in ohms. The computed EV limit is clipped to the range from zero to the charger rating. A conservative calculation uses `max(0, PV_forecast - PV_error_bound)`, with a **user-assumed, not calibrated** error bound.

## Run

Python 3.10+; standard library only.

```bash
python -m unittest discover -s tests -v
python src/feeder_demo.py --output results/example_24h.csv
```

The CSV contains **24 synthetic hourly scenarios**, not field data. The nine Python unit tests passed in local testing; this does not validate physical accuracy.

## Limitations

The model omits reactance, reactive power, unbalanced phases, topology, upper-voltage constraints, thermal limits and calibrated uncertainty. **Do not use its limits to control real electrical equipment.**

See [limitations and validation plan](docs/limitations.md).