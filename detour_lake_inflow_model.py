"""
Detour Lake Open Pit — Steady-State Groundwater Inflow Model
Author: Isaiah Ephraim

Description:
    Analytical steady-state radial flow model estimating groundwater inflow
    to the Detour Lake open pit. Parameters are derived from hydrogeological
    data reported in NI 43-101 technical disclosures for the site.

    The governing equation is Darcy's Law applied to confined radial flow:

        Q = (2 * pi * K * b * (h2 - h1)) / ln(r2 / r1)

    where Q is discharge (m3/s), K is hydraulic conductivity (m/s),
    b is saturated thickness (m), h2-h1 is the hydraulic head difference (m),
    r1 is the pit radius (m), and r2 is the radius of influence (m).

    A sensitivity analysis is run across the full reported bedrock
    conductivity range (1e-8 to 1e-5 m/s) to show how inflow scales
    with structural permeability variation.
"""

import numpy as np
import matplotlib.pyplot as plt
import math

# -----------------------------------------------------------------------
# 1. Model Parameters — Detour Lake Mine
# -----------------------------------------------------------------------
# Source: Detour Gold Corporation, 2018. Detour Lake Operation,
# Ontario, Canada: NI 43-101 Technical Report.
# Effective date: 27 June 2018. Report date: 26 November 2018.

b      = 200    # Saturated thickness (m)
h_diff = 100    # Hydraulic head difference, h2 - h1 (m)
r1     = 1200   # Equivalent pit radius (m)
r2     = 5000   # Radius of influence (m)

ln_ratio = math.log(r2 / r1)   # ln(5000/1200) = 1.4271

# -----------------------------------------------------------------------
# 2. Sensitivity — hydraulic conductivity range from NI 43-101 data
# -----------------------------------------------------------------------
K_values = np.logspace(-8, -5, 200)   # 1e-8 to 1e-5 m/s, 200 points

Q_values = [
    (2 * math.pi * K * b * h_diff) / ln_ratio * 86400   # convert m3/s -> m3/day
    for K in K_values
]

# -----------------------------------------------------------------------
# 3. Reference Scenarios
# -----------------------------------------------------------------------
K_conservative = 1e-7   # Low-permeability fractured bedrock
K_fractured    = 1e-5   # Shear zone / fracture-enhanced conductivity

Q_conservative = (2 * math.pi * K_conservative * b * h_diff) / ln_ratio * 86400
Q_fractured    = (2 * math.pi * K_fractured    * b * h_diff) / ln_ratio * 86400

print("\n--- Detour Lake Reference Scenarios ---")
print(f"  Conservative case  (K = 1e-7 m/s):  Q = {Q_conservative:,.1f} m\u00b3/day")
print(f"  Fracture-enhanced  (K = 1e-5 m/s):  Q = {Q_fractured:,.1f} m\u00b3/day")
print(f"\n  ln(r2/r1) = {ln_ratio:.6f}")

# -----------------------------------------------------------------------
# 4. Plot
# -----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6.5))
fig.patch.set_facecolor('#FAFAFA')
ax.set_facecolor('#FAFAFA')

ax.plot(K_values, Q_values, color='#1a3a5c', linewidth=2.8, zorder=3,
        label='Predicted steady-state inflow')

# Permeability zone shading
ax.axvspan(1e-8, 1e-7, alpha=0.10, color='#2980b9', label='Low-permeability bedrock')
ax.axvspan(1e-7, 1e-6, alpha=0.10, color='#f39c12', label='Moderate fractured rock')
ax.axvspan(1e-6, 1e-5, alpha=0.10, color='#c0392b', label='Shear zone / fracture-enhanced')

# Reference lines
ax.axvline(x=K_conservative, color='#e67e22', linestyle='--', linewidth=1.8, zorder=4)
ax.axvline(x=K_fractured,    color='#c0392b', linestyle='--', linewidth=1.8, zorder=4)

# Callout annotations
ax.annotate(
    f'Conservative case\nK = 1\u00d710\u207b\u2077 m/s\nQ = {Q_conservative:,.0f} m\u00b3/day',
    xy=(K_conservative, Q_conservative),
    xytext=(2.5e-8, 3500),
    fontsize=9, color='#e67e22',
    arrowprops=dict(arrowstyle='->', color='#e67e22', lw=1.4),
    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#e67e22', alpha=0.85)
)
ax.annotate(
    f'Fracture-enhanced\nK = 1\u00d710\u207b\u2075 m/s\nQ = {Q_fractured:,.0f} m\u00b3/day',
    xy=(K_fractured, Q_fractured),
    xytext=(3e-6, 8000),
    fontsize=9, color='#c0392b',
    arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.4),
    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#c0392b', alpha=0.85)
)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Hydraulic Conductivity, K  (m/s)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('Groundwater Inflow, Q  (m\u00b3/day)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title(
    'Figure 1 \u2014 Detour Lake Open Pit: Steady-State Groundwater Inflow Sensitivity\n'
    'Analytical Radial Flow Model  |  b = 200 m,  \u0394h = 100 m,  '
    'r\u2081 = 1,200 m,  r\u2082 = 5,000 m',
    fontsize=11, fontweight='bold', pad=14
)
ax.grid(True, which='both', linestyle=':', linewidth=0.6, alpha=0.7, color='#aaaaaa')
ax.tick_params(axis='both', labelsize=10)
ax.legend(fontsize=9.5, loc='upper left', framealpha=0.92, edgecolor='#cccccc')

fig.text(
    0.5, -0.04,
    'Author: Isaiah Ephraim  |  Model: Darcy steady-state radial flow, confined aquifer'
    '  |  Parameters: Detour Lake Mine NI 43-101',
    ha='center', fontsize=8.5, color='#555555', style='italic'
)

plt.tight_layout()
plt.savefig('detour_lake_inflow_sensitivity.png', dpi=220, bbox_inches='tight',
            facecolor='#FAFAFA')
print("\nFigure saved: detour_lake_inflow_sensitivity.png")
