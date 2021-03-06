class BaseTablet:

    def __init__(self, guid = None, pcsb_tag = None, serial = None, devicemodel = None, student_guid = None, ad_tablet = None):
        self.ad_tablet = ad_tablet
        self.guid = guid
        self.pcsb_tag = pcsb_tag
        self.serial = serial
        self.device_model = devicemodel
        self.student_guid = student_guid
        
        if serial is None:
            self.serial = "Not Specified"
        if devicemodel is None:
            self.device_model = "Not Specified"
            
    def __eq__(self, other):
        return self.guid == other.guid
        
    def write_datagram(self, dg):
        dg.add_string(self.guid)
        dg.add_string(self.pcsb_tag)
        dg.add_string(self.serial)
        dg.add_string(self.device_model)
        if self.student_guid:
            dg.add_string(self.student_guid)
        else:
            dg.add_string("")
        
    @staticmethod
    def from_datagram(dgi):
        guid = dgi.get_string()
        pcsb = dgi.get_string()
        serial = dgi.get_string()
        device = dgi.get_string()
        student_guid = dgi.get_string()
        return BaseTablet(guid, pcsb, serial, device, student_guid)
        
    def __str__(self):
        return (
            """GUID: %s\n\tPCSB Tag: %s\n\tSerial No: %s\n\tDevice Model: %s\n\tStudent GUID: %s""" % (self.guid, self.pcsb_tag, self.serial, self.device_model, self.student_guid)
        )