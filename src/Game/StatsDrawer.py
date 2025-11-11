import matplotlib.pyplot as plt


class StatsDrawer:
    def __init__(self):
        plt.ion()  # Turn on interactive mode

        fig, ax = plt.subplots()
        self.line, = ax.plot([], [], lw=2)
        ax.set_ylim(0, 50)
        ax.set_xlabel('Time')
        ax.set_ylabel('Score')
        ax.set_title('Game Score Progression')

        self.ax = ax
        self.fig = fig
        self.score = []
        self.nb_games = []

    def update(self, score: int):
        self.score.append(score)
        self.nb_games.append(len(self.score))

        self.line.set_xdata(self.nb_games[-100:])
        self.line.set_ydata(self.score[-100:])
        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        plt.pause(0.01)

        return self.line,
