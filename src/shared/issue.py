class Issue:

    def __init__(self, iid, tablet_guid, incident_desc,
                 problems_desc, date_of_incident, parts_ordered,
                 parts_ordered_date, parts_expected_date,
                 insurance_or_warranty, fixed_desc, tablet_returned,
                 team_member_guid, return_date, resolved, temp_tablet_assigned = 0, temp_tablet_pcsb = ""):
                 
        self.issue_id = iid
        self.tablet_guid = tablet_guid
        self.incident_desc = incident_desc
        self.problems_desc = problems_desc
        self.date_of_incident = date_of_incident
        self.parts_ordered = parts_ordered
        self.parts_ordered_date = parts_ordered_date
        self.parts_expected_date = parts_expected_date
        self.insurance_or_warranty = insurance_or_warranty
        self.fixed_desc = fixed_desc
        self.tablet_returned = tablet_returned
        self.team_member_guid = team_member_guid
        self.return_date = return_date
        self.resolved = resolved

        self.temp_tablet_assigned = temp_tablet_assigned
        self.temp_tablet_pcsb = temp_tablet_pcsb
        if self.temp_tablet_assigned is None:
            self.temp_tablet_assigned = 0
        if self.temp_tablet_pcsb is None:
            self.temp_tablet_pcsb = ""
        
    def __eq__(self, other):
        return self.issue_id == other.issue_id
        
    def write_database(self, c):
        c.execute("SELECT * FROM TabletIssue WHERE ID = ?", (self.issue_id,))
        existing = c.fetchone()
        if not existing or self.issue_id < 0:
        
            c.execute("SELECT * FROM TabletIssue")
            issues = c.fetchall()
            self.issue_id = len(issues)
            
            c.execute("INSERT INTO TabletIssue VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (self.tablet_guid, self.incident_desc, self.problems_desc,
                 self.date_of_incident, self.parts_ordered, self.parts_ordered_date,
                 self.parts_expected_date, self.insurance_or_warranty, self.fixed_desc,
                 self.tablet_returned, self.team_member_guid, self.return_date,
                 self.resolved, self.temp_tablet_assigned, self.temp_tablet_pcsb))
        else:
            # Only a select set of properties can be changed on an issue once already
            # submitted.
            c.execute(
            """UPDATE TabletIssue SET IncidentDescription = ?, ProblemsDescription = ?, DateOfIncident = ?, PartsOrdered = ?, PartsOrderedDate = ?, PartsExpectedDate = ?,
            InsuranceOrWarranty = ?, FixedDescription = ?, TabletReturned = ?, ReturnDate = ?,
            Resolved = ?, TempTabletAssigned = ?, TempTabletPCSBTag = ? WHERE ID = ?""",
            (self.incident_desc, self.problems_desc, self.date_of_incident, self.parts_ordered,
            self.parts_ordered_date, self.parts_expected_date,
            self.insurance_or_warranty, self.fixed_desc, self.tablet_returned,
            self.return_date, self.resolved, self.temp_tablet_assigned, self.temp_tablet_pcsb, self.issue_id))
        
    def write_datagram(self, dg):
        dg.add_int32(self.issue_id)
        dg.add_string(self.tablet_guid)
        dg.add_string(self.incident_desc)
        dg.add_string(self.problems_desc)
        dg.add_string(self.date_of_incident)
        dg.add_uint8(self.parts_ordered)
        dg.add_string(self.parts_ordered_date)
        dg.add_string(self.parts_expected_date)
        dg.add_uint8(self.insurance_or_warranty)
        dg.add_string(self.fixed_desc)
        dg.add_uint8(self.tablet_returned)
        dg.add_string(self.team_member_guid)
        dg.add_string(self.return_date)
        dg.add_uint8(self.resolved)
        dg.add_uint8(self.temp_tablet_assigned)
        dg.add_string(self.temp_tablet_pcsb)
        
    @staticmethod
    def from_datagram(dgi):
        iid                 = dgi.get_int32()
        tablet_guid         = dgi.get_string()
        incident_desc       = dgi.get_string()
        problems_desc       = dgi.get_string()
        doi                 = dgi.get_string()
        parts_ordered       = dgi.get_uint8()
        parts_ordered_date  = dgi.get_string()
        parts_expected_date = dgi.get_string()
        iow                 = dgi.get_uint8()
        fixed_desc          = dgi.get_string()
        returned            = dgi.get_uint8()
        hwguid              = dgi.get_string()
        return_date         = dgi.get_string()
        resolved            = dgi.get_uint8()
        temp_tablet         = dgi.get_uint8()
        temp_pcsb           = dgi.get_string()
        
        return Issue(iid, tablet_guid, incident_desc, problems_desc, doi,
                     parts_ordered, parts_ordered_date, parts_expected_date,
                     iow, fixed_desc, returned, hwguid, return_date, resolved,
                     temp_tablet, temp_pcsb)
                     