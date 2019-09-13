class IssueStep:

    def __init__(self, sid, iid, date_of_step, step_desc, hwguid):
        self.step_id = sid
        self.issue_id = iid
        self.date_of_step = date_of_step
        self.step_desc = step_desc
        self.team_member_guid = hwguid
        
    def write_datagram(self, dg):
        dg.add_int32(self.step_id)
        dg.add_uint32(self.issue_id)
        dg.add_string(self.date_of_step)
        dg.add_string(self.step_desc)
        dg.add_string(self.team_member_guid)
        
    def write_database(self, c):
        c.execute("SELECT * FROM TabletIssueStep WHERE ID = ?", (self.step_id,))
        existing = c.fetchone()
        if not existing or self.step_id < 0:
        
            c.execute("SELECT * FROM TabletIssueStep")
            steps = c.fetchall()
            self.step_id = len(steps)
            
            c.execute("INSERT INTO TabletIssueStep VALUES (NULL,?,?,?,?)",
                (self.issue_id, self.date_of_step, self.step_desc, self.team_member_guid))
        else:
            print("Tried to write an already existing TabletIssueStep to database (TabletIssueSteps are not mutable)")
        
    def __eq__(self, other):
        return self.step_id == other.step_id
        
    def __str__(self):
        return """IssueStep(%s, %s, %s, %s, %s)""" % (self.step_id, self.issue_id, self.date_of_step, self.step_desc, self.team_member_guid)
        
    @staticmethod
    def from_datagram(dgi):
        sid             = dgi.get_int32()
        iid             = dgi.get_uint32()
        date_of_step    = dgi.get_string()
        step_desc       = dgi.get_string()
        hwguid          = dgi.get_string()
        return IssueStep(sid, iid, date_of_step, step_desc, hwguid)