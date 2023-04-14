

class Timer():
    def __init__(self):
        self.current_lap = 0
        self.laps = []

    def dnf(self):
        if self.current_lap > 0:
            self.laps.append(-1)
        self.current_lap = 0

    def complete(self):
        if self.current_lap > 0:
            self.laps.append(self.current_lap)
        self.current_lap = 0

    def tick(self, dt: float):
        self.current_lap += (dt * 1000)

    def format(self, time: int):
        return f"{int((time / 1000) / 60)}:{int((time / 1000) % 60):02}:{int(time % 1000):03}"
