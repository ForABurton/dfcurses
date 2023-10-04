def idf(df, dfi=locals(), cm=None):

    import pandas as pd
    import curses as cs
    import numpy as np

    if isinstance(df, pd.DataFrame):
        df = df
    else:
        try:
            df = pd.DataFrame(df if isinstance(df, np.ndarray) else pd.read_csv(df))
        except:
            raise ValueError("Unable to process the provided data into a DataFrame.")

    bd = cs.A_BOLD
    curcol = lambda colorname: getattr(cs, f'COLOR_{colorname.upper()}', cs.COLOR_BLACK)

    cboard = pyperclip = None
    try:
        import pyperclip
        cboard = pyperclip
    except ImportError:
        pass

    cm = cm or {
        'bg': 'black',
        'fga': [
            ('white', 'black'),  # General text: white on black
            ('black', 'white'),  # Highlighted text: black on white
            ('black', 'white')   # Inverted text: black on white
        ]
    }

    def ln(dfi, df):
        for name, var in dfi.items():
            if id(var) == id(df):
                return name
        return "???"

    global cclip
    cclip = None
    def v(s, df):
        global cclip

        # Lambda to blink the screen by inverting colors
        blink = lambda s, clr: [s.bkgd(' ', cs.color_pair(i % 2 + 1)) or clr() or cs.napms(100) for i in range(5)] + [s.bkgd(' ', cs.color_pair(1)) or clr()]

        def az(y, x, str_to_add, *args, **kwargs):
            if (
                0 <= y < h and 
                0 <= x < w and 
                0 <= x + len(str_to_add) <= w
            ):
                s.addstr(y, x, str_to_add, *args, **kwargs)
                
        cls = s.clear
        clr = s.refresh
        
        # Initialize colors and screen
        cs.start_color(); 
        [cs.init_pair(i+1, curcol(fg), curcol(bg)) for i, (fg, bg) in enumerate(cm['fga'])]
        s.bkgd(' ', cs.color_pair(1))
        cs.curs_set(0)
        
        # Initialize navigation variables
        r = c = cr = cc = 0
        sm = False  # Selection mode flag
        
        while 1:
            cls()
            h, w = s.getmaxyx()
            should_exit = False
            
            # Ensure navigation is within bounds
            r = max(0, min(r, len(df) - h + 2))
            c = max(0, min(c, len(df.columns) - 1))
            cr = max(0, min(cr, h-3))
            cc = max(0, min(cc, w-11))
            
            # Virtual DataFrame for the current view
            vdf = df.iloc[r:r+h-1, c:c+w-10]
            
            # Determine maximum width for column formatting
            if not vdf.empty:
                mw = min(w-10, max(vdf.astype(str).applymap(len).max().max(), max(map(len, map(str, vdf.columns)))))
            else:
                mw = 0
            
            # Display UI elements
            az(0, 0, "↑→ SiQ", cs.color_pair(2) | bd)
            az(0, 3, "S", cs.color_pair(1 if sm else 2) | bd)
            col_headers = ':'.join([f'{x:>{mw}}' for x in df.columns[c:c+w-10]])
            az(0, 6, col_headers[:w-6], cs.color_pair(2) | bd)
            
            # Display data
            for i in range(1, h-1):
                if r+i-1 < len(df):
                    az(i, 0, f"{df.index[r+i-1]:<5}:", cs.color_pair(2) | bd)
                    row_data = '|'.join([f'{x:>{mw}}' for x in df.iloc[r+i-1, c:c+w-10].astype(str).values])
                    az(i, 6, row_data[:w-6])
            
            # Highlight selected cell in selection mode
            if sm:
                cell_data = f"{df.iat[r+cr, c+cc]:>{mw}}"
                az(cr+1, cc * (mw+1) + 6, cell_data[:w-6], cs.color_pair(3) | bd)
            
            # Refresh screen
            clr()
            k = s.getch()
            
            # Bounded navigation and actions
            if k == cs.KEY_DOWN and (not sm and r < len(df) - h + 2 or sm and cr < min(h-3, len(vdf)-1)):
                r, cr = (r + 1, cr) if not sm else (r, cr + 1)
            elif k == cs.KEY_UP and (not sm and r > 0 or sm and cr > 0):
                r, cr = (r - 1, cr) if not sm else (r, cr - 1)
            elif k == cs.KEY_RIGHT and (not sm and c < df.shape[1] - 1 or sm and cc < min(w-11, vdf.shape[1]-1)):
                c, cc = (c + 1, cc) if not sm else (c, cc + 1)
            elif k == cs.KEY_LEFT and (not sm and c > 0 or sm and cc > 0):
                c, cc = (c - 1, cc) if not sm else (c, cc - 1)
            elif k == ord('q'):
                break
            elif k == ord('i'):
                # Information Display
                cls()
                if sm:
                    # In selection mode: display info about the selected cell
                    vl = df.iat[r+cr, c+cc]
                    vlt = type(vl).__name__
                    az(h//2-2, max(0, w//2-len(f"Pos: ({r+cr}, {c+cc})")//2), f"Pos: ({r+cr}, {c+cc})", cs.color_pair(2) | bd)
                    az(h//2-1, max(0, w//2-len(f"Val: {vl}")//2), f"Val: {vl}", cs.color_pair(2) | bd)
                    az(h//2, max(0, w//2-len(f"Type: {vlt}")//2), f"Type: {vlt}", cs.color_pair(2) | bd)
                else:
                    # Not in selection mode: display info about the dataframe
                    dfn = ln(dfi, df)
                    az(h//2-1, max(0, w//2-len(f"Shape: {df.shape}")//2), f"Shape: {df.shape}", cs.color_pair(2) | bd)
                    az(h//2, max(0, w//2-len(f"Name: {dfn}")//2), f"Name: {dfn}", cs.color_pair(2) | bd)
                clr()
                s.getch()
            elif k == ord('s'):
                sm = not sm; cr, cc = 0, 0
            elif k == ord('d'):
                # Descriptive Stats Display
                cls()
                if not sm:
                    # Not in selection mode: display stats for the whole dataframe
                    stats = df.describe().astype(str)
                else:
                    # In selection mode: display stats for the column of the selected cell
                    owning_column = df.iloc[:, c + cc]
                    stats = owning_column.describe().astype(str)
                
                # Ensure stats are displayed within the screen width
                stats_str = str(stats).split("\n")
                az(0, 0, "Col. Stats", cs.color_pair(2) | bd)
                for idx, line in enumerate(stats_str):
                    az(idx + 1, 0, line[:w], cs.color_pair(2) | bd)
                clr()
                s.getch()
            elif k in [ord('R'), ord('r')] and sm:
                cclip = df.iloc[r + cr, :].to_csv(index=False)
                blink(s, clr)
                should_exit = k == ord('R')
            elif k in [ord('C'), ord('c')] and sm:
                cclip = df.iloc[:, c + cc].to_csv(index=False)
                blink(s, clr)
                should_exit = k == ord('C')
            elif k in [ord('V'), ord('v')] and sm:
                cclip = str(df.iat[r + cr, c + cc])
                blink(s, clr)
                should_exit = k == ord('V')
            elif k in [ord('A'), ord('a')]:
                cclip = df.to_csv(index=False)
                blink(s, clr)
                should_exit = k == ord('A')

            if should_exit:
                break

    # Start the curses wrapper
    cs.wrapper(v, df)
    if cclip and cboard:
        cboard.copy(cclip)

if __name__ == "__main__":
    import seaborn as sns

    calccols = {
        'bg': 'black',
        'fga': [
            ('green', 'black'),
            ('black', 'green'),
            ('black', 'white')
        ]
    }

    try:
        datasets = sns.get_dataset_names()
    except:
        print("Could not retrieve the list of available datasets from Seaborn.")
        datasets = []

    for dataset_name in datasets:
        try:
            # Load the dataset
            locals()[dataset_name] = sns.load_dataset(name=dataset_name)
            
            # Call the idf function to inspect the DataFrame
            print(f"\n\nInspecting the dataset: {dataset_name}")
            idf(locals()[dataset_name], cm=calccols)
            
        except Exception as e:
            print(f"An error occurred while loading or inspecting the dataset {dataset_name}: {str(e)}")
