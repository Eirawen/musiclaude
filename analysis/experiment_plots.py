"""Generate analysis plots for the Rachmaniclaude report.

Covers the experimental arc from 005 through 011.
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

plt.style.use('seaborn-v0_8-whitegrid')
PLOT_DIR = "analysis/plots"
os.makedirs(PLOT_DIR, exist_ok=True)


# =============================================================================
# Plot 09: Experiment Score Trajectory
# =============================================================================

experiments = {
    "005\nProfile\nFeedback": {"scores": [93, 84, 70], "avg": 82.3, "type": "baseline"},
    "007\nCanonical\nTargets": {"scores": [], "avg": None, "type": "failure"},
    "008\nCanonical\nWisdom": {"scores": [], "avg": None, "type": "failure"},
    "009\nMinimal\nClarinet": {"scores": [83, 78, 73, 50], "avg": 71.0, "type": "mixed"},
    "010\nMinimal\nCello": {"scores": [90, 88, 86, 85], "avg": 87.3, "type": "success"},
    "011\nJRPG\nOrchestra": {"scores": [73, 70, 68, 60], "avg": 67.8, "type": "failure"},
}

fig, ax = plt.subplots(figsize=(12, 6))

colors = {"baseline": "#2196F3", "failure": "#F44336", "mixed": "#FF9800", "success": "#4CAF50"}
x_positions = range(len(experiments))

for i, (label, data) in enumerate(experiments.items()):
    color = colors[data["type"]]
    scores = data["scores"]
    if scores:
        ax.scatter([i] * len(scores), scores, color=color, alpha=0.5, s=80, zorder=3)
    if data["avg"] is not None:
        ax.plot(i, data["avg"], 'D', color=color, markersize=12, zorder=4,
                markeredgecolor='white', markeredgewidth=2)
    else:
        # No numeric scores — show a marker with "qualitative" label
        ax.plot(i, 50, 'X', color=color, markersize=14, zorder=4, alpha=0.6)
        ax.annotate("qualitative\nonly", (i, 44), ha='center', fontsize=7, fontstyle='italic', alpha=0.5)

# Connect averages (skip None)
valid = [(x, d["avg"]) for x, d in zip(x_positions, experiments.values()) if d["avg"] is not None]
if valid:
    ax.plot([v[0] for v in valid], [v[1] for v in valid], '--', color='gray', alpha=0.5, linewidth=1.5, zorder=2)

ax.set_xticks(list(x_positions))
ax.set_xticklabels(experiments.keys(), fontsize=9)
ax.set_ylabel("Listener Score", fontsize=12)
ax.set_title("Experimental Arc: From Feature Targets to Minimal Prompting", fontsize=14, fontweight='bold')
ax.set_ylim(20, 100)
ax.axhline(y=80, color='green', linestyle=':', alpha=0.3, label='Good threshold')

# Note: 007/008 had qualitative feedback only, no numeric scores
ax.text(1.5, 30, "007/008 had qualitative\nfeedback only (no scores)",
        fontsize=8, fontstyle='italic', alpha=0.6, ha='center')

legend_elements = [
    mpatches.Patch(color=colors["baseline"], label="Baseline (profile feedback validated)"),
    mpatches.Patch(color=colors["failure"], label="Failed experiments"),
    mpatches.Patch(color=colors["mixed"], label="Mixed results"),
    mpatches.Patch(color=colors["success"], label="Best results"),
    plt.Line2D([0], [0], marker='D', color='gray', markersize=8, linestyle='None', label="Average score"),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)

plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/09_experiment_trajectory.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved 09_experiment_trajectory.png")


# =============================================================================
# Plot 10: v1 vs v3 Profile Comparison
# =============================================================================

features = [
    "dynamics_count", "hairpin_count", "staccato_count", "expression_count",
    "articulation_count", "accent_count", "voice_crossing", "pitch_class_entropy",
    "num_parts", "total_duration"
]
v1_values = [8, 1, 0, 4, 23, 0, 1, 3.00, 2, 253]
v3_values = [15, 10, 9, 10, 30, 1, 6, 3.12, 3, 192]

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(features))
width = 0.35

bars1 = ax.bar(x - width/2, v1_values, width, label='v1 (PDMX, 5,894 pieces)', color='#2196F3', alpha=0.8)
bars2 = ax.bar(x + width/2, v3_values, width, label='v3 (Canonical, 2,871 pieces)', color='#FF5722', alpha=0.8)

ax.set_xlabel('Feature', fontsize=11)
ax.set_ylabel('Median Target Value', fontsize=11)
ax.set_title('Feature Profile Comparison: PDMX Community vs Canonical Masterworks', fontsize=13, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(features, rotation=45, ha='right', fontsize=9)
ax.legend(fontsize=10)

# Annotate the dramatic differences
for i, (v1, v3) in enumerate(zip(v1_values, v3_values)):
    if v3 > v1 * 2 and v1 > 0:
        pct = int((v3 - v1) / v1 * 100)
        ax.annotate(f'+{pct}%', xy=(i + width/2, v3), xytext=(0, 5),
                   textcoords='offset points', ha='center', fontsize=8, fontweight='bold', color='#D32F2F')

plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/10_profile_comparison.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved 10_profile_comparison.png")


# =============================================================================
# Plot 11: Experiment 009 vs 010 — 2x2 Heatmaps
# =============================================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Exp 009 (clarinet)
data_009 = np.array([[83, 78], [50, 73]])  # rows: exp5/exp9, cols: v1/v3
im1 = ax1.imshow(data_009, cmap='RdYlGn', vmin=40, vmax=95, aspect='auto')
ax1.set_xticks([0, 1])
ax1.set_xticklabels(['v1 (PDMX)', 'v3 (Canonical)'])
ax1.set_yticks([0, 1])
ax1.set_yticklabels(['exp5\n(revise)', 'exp9\n(autonomous)'])
ax1.set_title('Exp 009: Clarinet + Piano\n(French village)', fontsize=12, fontweight='bold')
for i in range(2):
    for j in range(2):
        ax1.text(j, i, str(data_009[i, j]), ha='center', va='center', fontsize=18, fontweight='bold')

# Exp 010 (cello)
data_010 = np.array([[85, 90], [86, 88]])  # rows: exp5/exp9, cols: v1/v3
im2 = ax2.imshow(data_010, cmap='RdYlGn', vmin=40, vmax=95, aspect='auto')
ax2.set_xticks([0, 1])
ax2.set_xticklabels(['v1 (PDMX)', 'v3 (Canonical)'])
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['exp5\n(revise)', 'exp9\n(autonomous)'])
ax2.set_title('Exp 010: Cello + Piano\n(Chess game)', fontsize=12, fontweight='bold')
for i in range(2):
    for j in range(2):
        ax2.text(j, i, str(data_010[i, j]), ha='center', va='center', fontsize=18, fontweight='bold')

fig.colorbar(im2, ax=[ax1, ax2], label='Listener Score', shrink=0.8)
fig.suptitle('Effect of Instrumentation on Profile × Workflow Interaction', fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/11_instrumentation_heatmap.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved 11_instrumentation_heatmap.png")


# =============================================================================
# Plot 12: The Competence Ceiling — Feature Scores vs Listener Scores
# =============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

# Data points: (features above median fraction, listener score, label)
points = [
    # Exp 009
    (33/42, 83, "009: v1-exp5 (D)", "#4CAF50"),
    (39/42, 50, "009: v1-exp9 (B)", "#FF9800"),
    (38/42, 78, "009: v3-exp9 (C)", "#FF9800"),
    (40/42, 73, "009: v3-exp5 (A)", "#FF9800"),
    # Exp 010
    (33/41, 90, "010: v3-exp5 (A)", "#4CAF50"),
    (37/42, 85, "010: v1-exp5 (B)", "#4CAF50"),
    (36/42, 86, "010: v1-exp9 (C)", "#4CAF50"),
]

for feat_frac, score, label, color in points:
    ax.scatter(feat_frac * 100, score, color=color, s=100, zorder=3, alpha=0.8)
    ax.annotate(label, (feat_frac * 100, score), textcoords="offset points",
               xytext=(8, 4), fontsize=7, alpha=0.7)

ax.set_xlabel("% Features Above Profile Median", fontsize=12)
ax.set_ylabel("Listener Score", fontsize=12)
ax.set_title("The Competence Ceiling: Feature Compliance ≠ Musical Quality", fontsize=13, fontweight='bold')
ax.set_xlim(70, 102)
ax.set_ylim(25, 100)

# Annotations
ax.annotate("Best music has\nFEWER features above median",
           xy=(77, 91), fontsize=9, fontstyle='italic', color='#2E7D32',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9', alpha=0.8))

ax.annotate("More features ≠ better music",
           xy=(92, 52), fontsize=9, fontstyle='italic', color='#D32F2F',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFEBEE', alpha=0.8))

plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/12_competence_ceiling.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved 12_competence_ceiling.png")


# =============================================================================
# Plot 13: Intervention Timeline
# =============================================================================

fig, ax = plt.subplots(figsize=(14, 4))

interventions = [
    (1, "001\nBaseline", "XGBoost + IF\n60.2% acc", "#9E9E9E"),
    (2, "002\nDedup", "+PDMX meta\n63.5% acc", "#9E9E9E"),
    (3, "003\nDirectives", "Disagg. perf.\nR²+41%", "#9E9E9E"),
    (4, "004\nSelf-compute", "Drop PDMX meta\nportable", "#9E9E9E"),
    (5, "005\nBlind A/B/C", "Profile wins\n+7 over baseline", "#2196F3"),
    (6, "006\nCanonical", "2,871 masterworks\nv3 profile", "#9C27B0"),
    (7, "007\nBlind v1/v3", "v3 REJECTED\ncompetence ceiling", "#F44336"),
    (8, "008\nTeacher", "Wisdom REJECTED\nsame problem", "#F44336"),
    (9, "009\nMinimal", "No pipeline\nclarinet weak", "#FF9800"),
    (10, "010\nCello", "90/100!\nv3 rehabilitated", "#4CAF50"),
    (11, "011\nJRPG", "Full orchestra\ncan't orchestrate", "#F44336"),
]

for x, label, detail, color in interventions:
    ax.plot(x, 0, 'o', color=color, markersize=20, zorder=3, markeredgecolor='white', markeredgewidth=2)
    ax.annotate(label, (x, 0), xytext=(0, 25), textcoords='offset points',
               ha='center', fontsize=8, fontweight='bold')
    ax.annotate(detail, (x, 0), xytext=(0, -30), textcoords='offset points',
               ha='center', fontsize=7, fontstyle='italic', color='#555')

ax.plot([1, 11], [0, 0], '-', color='#BDBDBD', linewidth=2, zorder=1)
ax.set_xlim(0.3, 11.7)
ax.set_ylim(-0.8, 0.8)
ax.axis('off')
ax.set_title("The Experimental Arc: 11 Experiments, 5 Hypotheses Rejected",
            fontsize=13, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/13_intervention_timeline.png", dpi=150, bbox_inches='tight')
plt.close()
print("Saved 13_intervention_timeline.png")

print("\nAll experiment plots generated.")
