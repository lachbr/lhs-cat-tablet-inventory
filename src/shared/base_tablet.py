class BaseTablet:

    def __init__(self, ad_tablet, pcsb_tag, serial = None, devicemodel = None, student_guid = None):
        self.ad_tablet = ad_tablet
        self.guid = ad_tablet.guid_str
        self.pcsb_tag = pcsb_tag
        self.serial = serial
        self.device_model = devicemodel
        self.student_guid = student_guid
        
    def write_datagram(self, dg):
        dg.add_string(self.pcsb_tag)
        dg.add_string(self.serial)
        dg.add_string(self.device_model)
        #dg.add_string(
        
    def __str__(self):
        return (
            """GUID: %s\n\tPCSB Tag: %s\n\tSerial No: %s\n\tDevice Model: %s\n\tStudent GUID: %s""" % (self.guid, self.pcsb_tag, self.serial, self.device_model, self.student_guid)
        )