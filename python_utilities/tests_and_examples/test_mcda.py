from python_utilities.decision.mcda import DecisionMatrix

# Define geometries to compare
srad_parachute_design_options = [
    'Flat Ribbon',
    'Conical Ribbon',
    'Extended Skirt - 14.3%',
    'Ringsail',
    'DGB'
]

# Define selection variables
srad_parachute_variables = [
    'Average CD',
    'Opening Load Factor',
    'Inflated Shape (Dp/Do)',
    'Average Oscillation',
]

# Associate a percentage to each variable
srad_parachute_variables_percentages = [40, 30, 15, 15]
# Associate a unit to each variable
srad_parachute_units = ["[-]", "[-]", "[-]", "[°]"]
# Indicate if each variable must be maximized (True) or minimized (False)
srad_parachute_max_or_min_parameters = ['Max', 'Min', 'Max', 'Min']

# Create selection matrix with the information above
srad_parachute_matrix = DecisionMatrix(
    srad_parachute_design_options,
    srad_parachute_variables,
    srad_parachute_units,
    srad_parachute_variables_percentages,
    srad_parachute_max_or_min_parameters
)

# Add performance information to each geometry (CD, Cx, Dp/Do & AoA)
srad_parachute_matrix.add_value_per_option('Flat Ribbon', [0.475, 1.321, 0.67, 1.5])
srad_parachute_matrix.add_value_per_option('Conical Ribbon', [0.525, 1.31, 0.7, 1.5])
srad_parachute_matrix.add_value_per_option('Extended Skirt - 14.3%', [0.825, 1.292, 0.68, 12.5])
srad_parachute_matrix.add_value_per_option('Ringsail', [0.825, 1.292, 0.69, 7.5])
srad_parachute_matrix.add_value_per_option('DGB', [0.55, 1.315, 0.65, 12.5])

mat = srad_parachute_matrix.get_matrix()
norm_mat = srad_parachute_matrix.get_normalized_matrix()

print("Original Matrix:")
print(mat)
print("\nNormalized Matrix:")
print(norm_mat)
srad_parachute_matrix.show_matrix()
srad_parachute_matrix.show_normalized_matrix()
srad_parachute_matrix.best_option()
srad_parachute_matrix.to_csv("srad_parachute_decision_matrix.csv")
srad_parachute_matrix.to_csv("srad_parachute_decision_matrix_normalized.csv", normalized=True)
srad_parachute_matrix.to_markdown()
srad_parachute_matrix.to_markdown("srad_parachute_decision_matrix.md")
srad_parachute_matrix.to_markdown("srad_parachute_decision_matrix_normalized.md", normalized=True)