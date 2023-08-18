class Truck:
    def __init__(self, packages, end_time, statuses):
        self.max_cap = 16
        self.mph = 18
        self.packages = packages
        self.end_time = end_time
        self.statuses = statuses

    def __str__(self):
        return "%s, %s, %s" % (self.packages, self.end_time, self.statuses)
