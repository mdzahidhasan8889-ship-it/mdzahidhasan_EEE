# Limitations and validation plan

This script is an **educational single-phase, single-bus voltage-drop approximation**, not a validated EV charging controller.

It omits line reactance and reactive power, detailed feeder topology, transformer and cable thermal constraints, upper-voltage limits, unbalanced three-phase effects, inverter controls, calibrated PV forecast uncertainty, charging schedules and numerical validation against full AC power flow.

Its data are **synthetic**, and its assumed PV uncertainty bound is not statistically calibrated. Do not apply the calculated limits to real power systems.

## Possible research extensions

- Use a suitably licensed, realistic low-voltage feeder model.
- Compare approximated voltages against unbalanced AC power flow.
- Add upper/lower voltage and thermal limits.
- Calibrate PV forecast uncertainty from real data.
- Compare fixed, forecast-based and uncertainty-aware charging limits.
- Report voltage violations, energy delivered and reproducible assumptions.