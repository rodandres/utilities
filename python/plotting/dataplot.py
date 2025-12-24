import pandas as pd
import matplotlib.pyplot as plt
from collections.abc import Iterable

from general_utilities import _center_text

DEFAULT_LINE_STYLE = {
    "markers": "",
    "line_styles": "-",
    "colors": None,
    "line_widths": 2,
    "marker_sizes": 6,
    "labels": None,
}

DEFAULT_TITLE_STYLE = {
    "fontsize": 18,
    "fontweight": "bold",
    "fontstyle": "italic",
    "fontfamily": "Arial",
    "loc": "center",
    "pad": 10,
}

DEFAULT_GRAPH_STYLE = {
    "figsize": (10, 6),
    "dpi": 100,
    "facecolor": "white",
    "grid": True,
    "legend": True,
}

DEFAULT_AXES_LABEL_STYLE = {
    "fontsize": 8,
    "fontweight": "bold",
    "fontstyle": "normal",
    "fontfamily": "Arial",
}

DEFAULT_AXES_STYLE = {
    "xlim": None,
    "ylim": None,
    "xscale": "linear",
    "yscale": "linear",
    "invert_x": False,
    "invert_y": False,
}

DEFAULT_TICKS_STYLE = {
    "labelsize": 8,
    "rotation": 0,
    "direction": "out",
    "length": 4,
    "width": 1,
}

DEFAULT_LEGEND_STYLE = {
    "loc": "best",
    "fontsize": 9,
    "frameon": True,
    "ncol": 1,
}

DEFAULT_GRID_STYLE = {
    "axis": "both",
    "linestyle": "--",
    "alpha": 0.5,
}

DEFAULT_EXTRA_STYLE = {
    "vline": {
        "color": "black",
        "linewidth": 1,
        "linestyle": "--",
        "alpha": 0.7,
        "label": None,
    },
    "hline": {
        "color": "black",
        "linewidth": 1,
        "linestyle": "--",
        "alpha": 0.7,
        "label": None,
    },
    "marker": {
        "marker": "o",
        "color": "black",
        "size": 60,
        "alpha": 0.8,
        "label": None,
    },
}

DEFAULT_SAVE_STYLE = { # NOTE: Not yet implemented
    "path": None,
    "dpi": 300,
    "bbox_inches": "tight",
}

# ---------------------------------------------------------------------------------
def _normalize_list(user_list, default_value, n):
    if user_list is None:
        return [default_value] * n

    if isinstance(user_list, set):
        raise TypeError("set is not supported; use list or tuple")

    if not isinstance(user_list, Iterable):
        raise TypeError("Expected iterable")

    user_list = list(user_list)

    return [
        user_list[i] if i < len(user_list) else default_value
        for i in range(n)
    ]

def _normalize_style_dict(style_dict, y_col_names):
    n = len(y_col_names)

    if style_dict is None:
        style_dict = {}

    if not isinstance(style_dict, dict):
        raise TypeError("style must be a dict")

    normalized = {}

    for key, default_value in DEFAULT_LINE_STYLE.items():
        user_value = style_dict.get(key)

        # Labels requieren tratamiento especial
        if key == "labels":
            values = _normalize_list(user_value, None, n)
            values = [
                v if v is not None else y_col_names[i]
                for i, v in enumerate(values)
            ]
            normalized[key] = values
            continue

        normalized[key] = _normalize_list(user_value, default_value, n)

    return normalized

def _merge_style(user_style, default_style):
    if user_style is None:
        return default_style.copy()

    if not isinstance(user_style, dict):
        raise TypeError("Style must be a dict")

    invalid_keys = set(user_style) - set(default_style)
    if invalid_keys:
        raise KeyError(f"Invalid style keys: {invalid_keys}")

    merged = default_style.copy()
    merged.update(user_style)
    return merged

def _apply_extras(ax, extras):
    if extras is None:
        return

    if not isinstance(extras, list):
        raise TypeError("extras must be a list of dicts")

    for item in extras:
        if not isinstance(item, dict):
            raise TypeError("Each extra must be a dict")

        if "type" not in item:
            raise KeyError("Extra item must have a 'type' key")

        etype = item["type"]

        if etype not in DEFAULT_EXTRA_STYLE:
            raise ValueError(f"Unsupported extra type: {etype}")

        style = DEFAULT_EXTRA_STYLE[etype].copy()
        style.update({k: v for k, v in item.items() if k != "type"})

        if etype == "vline":
            if "x" not in style:
                raise KeyError("vline requires 'x'")
            ax.axvline(
                x=style["x"],
                color=style["color"],
                linewidth=style["linewidth"],
                linestyle=style["linestyle"],
                alpha=style["alpha"],
                label=style["label"],
            )

        elif etype == "hline":
            if "y" not in style:
                raise KeyError("hline requires 'y'")
            ax.axhline(
                y=style["y"],
                color=style["color"],
                linewidth=style["linewidth"],
                linestyle=style["linestyle"],
                alpha=style["alpha"],
                label=style["label"],
            )

        elif etype == "marker":
            if "x" not in style or "y" not in style:
                raise KeyError("marker requires 'x' and 'y'")
            ax.scatter(
                style["x"],
                style["y"],
                marker=style["marker"],
                c=style["color"],
                s=style["size"],
                alpha=style["alpha"],
                label=style["label"],
            )

# ---------------------------------------------------------------------------------
class DataPlotter:
    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame.")
        if data.empty:
            raise ValueError("DataFrame is empty")
        
        self._data = data.copy()
        self.data_original = data

    def show_info(self):
        """Display basic information about the DataFrame."""

        print(_center_text(" INFORMATION SECTION "))        
        print(_center_text("DataFrame Information", fill_char=" "))        
        print(self._data.info())
        print(_center_text("", fill_char="-"))
        print(_center_text("DataFrame Description", fill_char=" "))
        print(self._data.describe())
        print(_center_text(""))

    def general_plot(self, x_col_name, y_col_names,
                     title="General Data Plot",
                     xlabel="",
                     ylabel="",
                     line_style=None,
                     title_style=None,
                     graph_style=None,
                     axes_label_style=None,
                     axes_style=None,
                     ticks_style=None,
                     legend_style=None,
                     grid_style=None,
                     extras=None
                     ):
        
        # Verification
        if x_col_name not in self._data.columns:
            raise KeyError(f"x_col_name '{x_col_name}' not in DataFrame")

        for col in y_col_names:
            if col not in self._data.columns:
                raise KeyError(f"y column '{col}' not in DataFrame")

        # Style normalization
        line_style = _normalize_style_dict(line_style, y_col_names)
        title_style = _merge_style(title_style, DEFAULT_TITLE_STYLE)
        graph_style = _merge_style(graph_style, DEFAULT_GRAPH_STYLE)
        axes_label_style = _merge_style(axes_label_style, DEFAULT_AXES_LABEL_STYLE)
        axes_style = _merge_style(axes_style, DEFAULT_AXES_STYLE)
        ticks_style = _merge_style(ticks_style, DEFAULT_TICKS_STYLE)
        legend_style = _merge_style(legend_style, DEFAULT_LEGEND_STYLE)
        grid_style = _merge_style(grid_style, DEFAULT_GRID_STYLE)

        # Figure setup
        plt.figure(figsize=graph_style["figsize"],
                   dpi=graph_style["dpi"],
                   facecolor=graph_style["facecolor"])

        # Plotting
        for i, y_col_name in enumerate(y_col_names):
            plt.plot(
                self._data[x_col_name],
                self._data[y_col_name], 
                marker=line_style["markers"][i], 
                linestyle=line_style["line_styles"][i], 
                color=line_style["colors"][i], 
                label=line_style["labels"][i], 
                linewidth=line_style["line_widths"][i], 
                markersize=line_style["marker_sizes"][i])


        # Title and labels    
        plt.title(title, **title_style)

        # Axis
        plt.xlabel(xlabel, **axes_label_style)
        plt.ylabel(ylabel, **axes_label_style)

        ax = plt.gca()

        if axes_style["xlim"]:
            ax.set_xlim(axes_style["xlim"])
        if axes_style["ylim"]:
            ax.set_ylim(axes_style["ylim"])

        ax.set_xscale(axes_style["xscale"])
        ax.set_yscale(axes_style["yscale"])

        if axes_style["invert_x"]:
            ax.invert_xaxis()
        if axes_style["invert_y"]:
            ax.invert_yaxis()

        ax.tick_params(axis="both", **ticks_style)

        ax.grid(
            True,
            axis=grid_style["axis"],
            linestyle=grid_style["linestyle"],
            alpha=grid_style["alpha"],
        )
        # Extras
        _apply_extras(ax, extras)

        # Graph style
        if grid_style is not None:
            ax.grid(True, **grid_style)

        if graph_style["legend"]:
            plt.legend(**legend_style)
                
        plt.show()