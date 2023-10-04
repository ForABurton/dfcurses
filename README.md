
# DataFrame Curses Explorer (dfcurses)

## Overview

dfcurses is a compact, terminal-based tool designed to offer an uncomplicated and speedy mechanism for primary exploration of Pandas DataFrames. Available under the MIT License, it serves as a quick-and-dirty solution for users requiring a straightforward method to inspect data within the terminal, without engaging in the setup or navigation of more complex data inspection tools.

## Why dfcurses?

In scenarios where rapid, minimalistic data exploration is essential, DFCurses provides a convenient solution that allows users to swiftly peek into their data without the overhead of extensive setup or navigation through larger, more comprehensive tools. Particularly valuable for SSH sessions, constrained environments, or for those who need a quick, in-line data exploration functionality during interactive Python sessions, dfcurses offers a pragmatic and barebones approach to basic data peeking.

## What dfcurses Is Not

dfcurses is tailored for simple, immediate data exploration, and thus lacks several functionalities that users might anticipate in a more comprehensive data exploration tool:

- **No Data Manipulation**: It does not allow editing or manipulating the data.
- **No Advanced Filtering or Sorting**: No capabilities to filter or sort data based on conditions or queries.
- **No Visualization**: Does not offer data visualization, charts, or graphs.
- **No Data Export**: Lacks functionality to export modified data or save exploration sessions.

It is essential to note that dfcurses is not a substitute for a full-fledged data analysis or visualization tool but serves as a quick, one-function utility to embed in interactive data analysis sessions for immediate data inspection. One function to paste!

## Features

- **Versatile Input**: Capable of handling DataFrames, 2D NumPy arrays, and CSV file paths.
- **Interactive Navigation**: Facilitates easy navigation through data using arrow keys.
- **Data Inspection**: Enables a quick inspection of data points and basic statistics.
- **Clipboard Interaction**: Allows copying of data to the clipboard (conditional on `pyperclip` availability).
- **Dynamic UI**: Adjusts column widths to optimize screen space usage.
- **Color Customization**: Allows adjustments to UI colors.

## How to Use

### Basic Usage

```python
import dfcurses

# Directly using a DataFrame
dfcurses.idf(my_dataframe)

# Specifying a path to a CSV file
dfcurses.idf('path_to_my_file.csv')
```

### Keyboard Shortcuts

- **Navigation**: Arrow keys to navigate through the DataFrame.
- **Selection Mode**: 's' toggles selection mode.
- **Information**: 'i' displays quick information.
- **Statistics**: 'd' displays basic statistics.
- **Copy Data**: 'R', 'C', and 'V' copy the row, column, and value, respectively, of the selected cell to the clipboard. Lowercase variants ('r', 'c', 'v') perform the same actions but keep the UI active.
- **Quit**: 'q' exits the interface.

### Customization

Customize UI colors as per preference:

```python
custom_colors = {
    'bg': 'black',
    'fga': [
        ('green', 'black'),
        ('black', 'green'),
        ('black', 'white')
    ]
}

dfcurses.idf(my_dataframe, cm=custom_colors)
```

## Alternatives

For functionalities beyond dfcurses, a CURSORY search around uncovered various alternative tools that cater to different and more expanded requirements (sorting, visualization, editing):

- **GUI-Based Tools**:
  - **[D-Tale](https://github.com/man-group/dtale)**
  - **[pandasgui](https://github.com/adamerose/pandasgui)**
  
- **TUI-Based Tools**:
  - **[VisiData](https://www.visidata.org/)**
  - **[tabview](https://github.com/TabViewer/tabview)**
  
- **IDE Feature**:
  - **VSCode's Variable Explorer**
  - **RStudio's View()**

Explore these alternatives based on your specific needs and working environment.

## Dependencies

DFCurses relies on a few (obvious) Python libraries to provide its functionalities. Ensure the following packages are installed in your Python environment:

- **[Pandas](https://pandas.pydata.org/)**: For data manipulation and analysis.
- **[NumPy](https://numpy.org/)**: For numerical operations.
- **[Curses](https://docs.python.org/3/library/curses.html)**: For creating the text-based user interface.

Optional:
- **[pyperclip](https://pypi.org/project/pyperclip/)**: Enables clipboard interaction for copying data from DFCurses. Without this, the copy-to-clipboard functionality will be unavailable.

You can install the dependencies (excluding Curses, which is part of the Python standard library) using pip:

```bash
pip install pandas numpy pyperclip
```
## License

DFCurses is under the MIT License.

## Acknowledgements

Thanks to Borland Turbo C, for instilling in me a fondness for junky old UIs.
