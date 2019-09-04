class StudentTabletLink:

    def __init__(self, student_guid = None, tablet_guid = None):
        self.tablet_guid = tablet_guid
        self.student_guid = student_guid

    @staticmethod
    def from_datagram(dgi):
        link = StudentTabletLink()
        link.student_guid = dgi.get_string()
        link.tablet_guid = dgi.get_string()
        return link
        
    def write_datagram(self, dg):
        dg.add_string(self.student_guid)
        dg.add_string(self.tablet_guid)
        