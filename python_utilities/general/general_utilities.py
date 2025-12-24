def center_text(text: str, total_chars: int = 120, fill_char: str = "=") -> str:
    if text is not "":
        if len(fill_char) != 1:
            raise ValueError("fill_char must be a single character")

        text_len = len(text)

        if text_len >= total_chars:
            return text[:total_chars]

        remaining = total_chars - text_len
        left = remaining // 2
        right = remaining - left

        return f"{fill_char * left}{text}{fill_char * right}"
    else:
        return fill_char * total_chars

def print_df_pretty(df):
    """
    Prints a pandas DataFrame centered with ASCII borders.
    """
    # Convert everything to string
    df_str = df.astype(str)

    # Column widths (consider index + columns)
    index_width = max(len(str(idx)) for idx in df_str.index)
    col_widths = {
        col: max(len(col), df_str[col].map(len).max())
        for col in df_str.columns
    }

    def hline():
        line = "+"
        line += "-" * (index_width + 2) + "+"
        for w in col_widths.values():
            line += "-" * (w + 2) + "+"
        return line

    def center(text, width):
        return f" {text.center(width)} "

    # Header
    print(hline())
    header = "|" + center("", index_width) + "|"
    for col, w in col_widths.items():
        header += center(col, w) + "|"
    print(header)
    print(hline())

    # Rows
    for idx, row in df_str.iterrows():
        line = "|" + center(str(idx), index_width) + "|"
        for col, w in col_widths.items():
            line += center(row[col], w) + "|"
        print(line)

    print(hline())

def df_to_markdown_pretty(df):
    """
    Returns a markdown-formatted table with centered content.
    """
    df_str = df.astype(str)

    index_width = max(len(str(idx)) for idx in df_str.index)
    col_widths = {
        col: max(len(col), df_str[col].map(len).max())
        for col in df_str.columns
    }

    def center(text, width):
        return f" {text.center(width)} "

    lines = []

    # Header
    header = "|" + center("", index_width) + "|"
    for col, w in col_widths.items():
        header += center(col, w) + "|"
    lines.append(header)

    # Separator
    separator = "|" + "-" * (index_width + 2) + "|"
    for w in col_widths.values():
        separator += "-" * (w + 2) + "|"
    lines.append(separator)

    # Rows
    for idx, row in df_str.iterrows():
        line = "|" + center(str(idx), index_width) + "|"
        for col, w in col_widths.items():
            line += center(row[col], w) + "|"
        lines.append(line)

    return "\n".join(lines)
