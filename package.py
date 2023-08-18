class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline_time,
                 weight, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline_time = deadline_time
        self.weight = weight
        self.notes = notes

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address,
                                                   self.city, self.state,
                                                   self.zip_code, self.deadline_time,
                                                   self.weight, self.notes)