class IssueStep:

    def __init__(self, sid, iid, date_of_step, step_desc, hwguid):
        self.step_id = sid
        self.issue_id = iid
        self.date_of_step = date_of_step
        self.step_desc = step_desc
        self.team_member_guid = hwguid
        
    def write_datagram(self, dg):
        dg.add_uint32(self.step_id)
        dg.add_uint32(self.issue_id)
        dg.add_string(self.date_of_step)
        dg.add_string(self.step_desc)
        dg.add_string(self.team_member_guid)
        
    @staticmethod
    def from_datagram(dg):
        sid             = dgi.get_uint32()
        iid             = dgi.get_uint32()
        date_of_step    = dgi.get_string()
        step_desc       = dgi.get_string()
        hwguid          = dgi.get_string()
        return TabletIssueStep(sid, iid, date_of_step, step_desc, hwguid)