import numpy as np
import pandas as pd

from python_utilities.general import center_text, print_df_pretty, df_to_markdown_pretty

class DecisionMatrix:

    def __init__(self, 
                design_options_names, 
                variables_names, 
                variable_units, 
                variables_percentages, 
                optimization_criteria):
            
            # ---- Validations ----
            if not (
                len(variables_names)
                == len(variable_units)
                == len(variables_percentages)
                == len(optimization_criteria)
            ):
                raise ValueError("Variables, units, weights and criteria must have the same length")

            if len(design_options_names) == 0:
                raise ValueError("At least one design option is required")

            if sum(variables_percentages) != 100:
                raise ValueError("Variable percentages must sum to 100")

            # ---- Core data ----
            self.design_options_names = design_options_names
            self.variables_names = variables_names
            self.variables_units = variable_units
            self.weights = variables_percentages
            self.optimization_criteria = optimization_criteria

            self.design_options_number = len(design_options_names)
            self.variables_number = len(variables_names)

            self.original_matrix = np.zeros(
                (self.design_options_number, self.variables_number)
            )
            self.normalized_matrix = np.zeros_like(self.original_matrix)

    # ------------------------------------------------------------------
    # Data input
    # ------------------------------------------------------------------
    def add_value(self, option_name, variable_name, value):
            option_idx = self.design_options_names.index(option_name)
            variable_idx = self.variables_names.index(variable_name)
            self.original_matrix[option_idx, variable_idx] = value

    def add_value_per_option(self, option_name, values):
        if len(values) != self.variables_number:
            raise ValueError("Values length does not match number of variables")

        for variable, value in zip(self.variables_names, values):
            self.add_value(option_name, variable, value)


    # ------------------------------------------------------------------
    # Core calculations
    # ------------------------------------------------------------------
    def _calculate_normalized_matrix(self):
        self.normalized_matrix[:] = 0.0

        for i in range(self.variables_number):
            criterion = self.optimization_criteria[i]
            criterion = criterion.lower()

            if criterion not in [True, False, "max", "min"] and not isinstance(criterion, (int, float)):                
                raise ValueError(
                    f"Invalid criterion: must be True, False, 'max', 'min', or a numeric target. "
                    f"Criteria found: {criterion}"
                )

            column = self.original_matrix[:, i]

            if criterion is True or criterion == "max":  # Maximize
                max_value = np.max(column)
                if max_value != 0:
                    self.normalized_matrix[:, i] = column / max_value

            elif criterion is False or criterion == "min":  # Minimize
                min_value = np.min(column)
                for j in range(self.design_options_number):
                    if column[j] != 0:
                        self.normalized_matrix[j, i] = min_value / column[j]

            else:  # Target value
                target = float(criterion)
                distances = np.abs(column - target)
                max_dist = np.max(distances) if np.max(distances) != 0 else 1.0
                self.normalized_matrix[:, i] = 1.0 - distances / max_dist

    def _compute_final_scores(self):
        self._calculate_normalized_matrix()
        scores = np.zeros(self.design_options_number)

        for j in range(self.design_options_number):
            for i in range(self.variables_number):
                scores[j] += self.normalized_matrix[j, i] * self.weights[i]

        return scores

    # ------------------------------------------------------------------
    # Public results
    # ------------------------------------------------------------------
    def best_option(self):
        scores = self._compute_final_scores()

        print(center_text(" FINAL SCORES "))
        for option, score in zip(self.design_options_names, scores):
            txt_result = f"Final score for {option}: {round(score, 2)} points"
            print(txt_result)
        
        print(center_text("", fill_char="-"))        

        best_idx = np.argmax(scores)        
        txt_best_option = f"The best option is {self.design_options_names[best_idx]} with {round(scores[best_idx], 2)} points over 100"
        print(center_text(txt_best_option, fill_char=" "))
        print(center_text(""))

        return best_idx, scores

    # ------------------------------------------------------------------
    # Visualization helpers
    # ------------------------------------------------------------------
    def get_matrix(self):
        
        df = pd.DataFrame(
            self.original_matrix,
            index=self.design_options_names,
            columns=self.variables_names,
        )
        df.loc["Percentage per variable [%]"] = self.weights      
        return df
    
    def show_matrix(self):
        df = self.get_matrix()
        print(center_text(" ORIGINAL MATRIX "))
        print_df_pretty(df)
        print(center_text(""))

    def get_normalized_matrix(self):
        
        self._calculate_normalized_matrix()

        df = pd.DataFrame(
            self.normalized_matrix,
            index=self.design_options_names,
            columns=self.variables_names,
        )
        df.loc["Percentage per variable [%]"] = self.weights        
        return df
    
    def show_normalized_matrix(self):
        df = self.get_normalized_matrix()
        print(center_text(" NORMALIZED MATRIX "))
        print_df_pretty(df)
        print(center_text(""))

    # ------------------------------------------------------------------
    # Export functions
    # ------------------------------------------------------------------
    def to_csv(self, filename, normalized=False):
        if normalized:
            df = self.get_normalized_matrix()
        else:
            df = self.get_matrix()
        
        df.to_csv(filename)

    def to_markdown(self, filename=None, normalized=False, show=True):
        if normalized:
            df = self.get_normalized_matrix()
        else:
            df = self.get_matrix()


        markdown = df_to_markdown_pretty(df)

        if show:
            print(markdown)

        if filename:
            with open(filename, "w") as f:
                f.write(markdown)

        return markdown