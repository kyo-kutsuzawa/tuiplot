import curses


class Figure:
    def __init__(self):
        self.plots = []
        self.labels = []
        self.markers = ['x', '+', '*', '#', '@', 'o']
        self.colors =  [ 2,   7,   3,   4,   6,   5 ]

    def plot(self, x, y, label=''):
        self.plots.append((x, y))
        self.labels.append(label)

    def show(self):
        curses.wrapper(self._show)

    def _show(self, stdscr):
        # Initialize colors
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        # Get canvas size
        canvas_height, canvas_width = stdscr.getmaxyx()

        # Compute ticks-area size
        val_range = self._get_range()
        xtick_size = 9  # length of "-1.1e-111"
        ytick_size = 1

        # Compute label-size area
        label_size = len(self.plots)

        # Compute plot-area size
        plot_height = canvas_height - ytick_size - (label_size+1)
        plot_width  = canvas_width  - (xtick_size+1)

        # Draw a plot frame
        stdscr.addstr(0, xtick_size+1, '+' + '-'*(plot_width-2) + '+')
        for i in range(1, plot_height-2):
            stdscr.addstr(i, xtick_size+1, '|' + ' '*(plot_width-2) + '|')
        stdscr.addstr(plot_height-2, xtick_size+1, '+' + '-'*(plot_width-2) + '+')

        # Draw ticks
        stdscr.addstr(0,             0,                       '{num:>{size}.1e}'.format(num=val_range[3], size=xtick_size))  # y_max
        stdscr.addstr(plot_height-2, 0,                       '{num:>{size}.1e}'.format(num=val_range[2], size=xtick_size))  # y_min
        stdscr.addstr(plot_height-1, xtick_size+1,            '{num:.1e}'.format(num=val_range[0]))                          # x_min
        stdscr.addstr(plot_height-1, canvas_width-xtick_size, '{num:>{size}.1e}'.format(num=val_range[1], size=xtick_size))  # x_max

        # Draw plots
        descrete_plots = self._discretize_plots(plot_height-4, plot_width-3, *val_range)
        for k, p in enumerate(descrete_plots):
            for xi, yi in p:
                stdscr.addstr(yi+1, xi+xtick_size+1+1, self.markers[k], curses.color_pair(self.colors[k]))

        # Draw labels
        for i, label in enumerate(self.labels):
            stdscr.addstr(plot_height+1+i, xtick_size+1, self.markers[i], curses.color_pair(self.colors[i]))
            stdscr.addstr(plot_height+1+i, xtick_size+5, label)

        stdscr.refresh()
        stdscr.getkey()

    def _discretize_plots(self, height, width, x_min, x_max, y_min, y_max):
        discrete_plots = []

        for p in self.plots:
            pd = []
            for xi, yi in zip(p[0], p[1]):
                # Normalize points
                xi = (xi - x_min) / (x_max - x_min)
                yi = (y_max - yi) / (y_max - y_min)

                if not (0<=xi<=1 and 0<=yi<=1):
                    continue

                xi = int(xi * width)
                yi = int(yi * height)

                pd.append((xi, yi))
            discrete_plots.append(pd)
        discrete_plots.append([(0, 0), (0, height), (width, 0), (width, height)])  # Debug plots

        return discrete_plots

    def _get_range(self, margin=0.0):
        x_min = min([min(x) for x, _ in self.plots])
        x_max = max([max(x) for x, _ in self.plots])
        y_min = min([min(y) for _, y in self.plots])
        y_max = max([max(y) for _, y in self.plots])

        x_size = x_max - x_min
        y_size = y_max - y_min

        x_min = x_min - x_size * margin
        x_max = x_max + x_size * margin
        y_min = y_min - y_size * margin
        y_max = y_max + y_size * margin

        return x_min, x_max, y_min, y_max

    def _get_ticks_str(self, x_min, x_max, y_min, y_max, xtick_size):
        xtick_min = str(x_min)
        xtick_max = str(x_max)
        ytick_min = str(y_min)
        ytick_max = str(y_max)

        xtick_size = max(len(ytick_max), len(ytick_max))
        ytick_size = max(len(xtick_max), len(xtick_max))
        ytick_size = 1

        return xtick_size, ytick_size
