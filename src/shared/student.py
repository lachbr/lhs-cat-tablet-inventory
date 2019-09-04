class Student:

    @staticmethod
    def from_datagram(dgi):
        student = Student()
        student.guid = dgi.get_string()
        student.name = dgi.get_string()
        student.grade = dgi.get_string()
        student.email = dgi.get_string()
        student.pcsb_agreement = dgi.get_uint8()
        student.cat_agreement = dgi.get_uint8()
        student.insurance_paid = dgi.get_uint8()
        student.insurance_amount = dgi.get_string()
        student.cat_student = dgi.get_uint8()
        student.tablet_guid = dgi.get_string()
        return student
        
    def __eq__(self, other):
        return self.guid == other.guid
        