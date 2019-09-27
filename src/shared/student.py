class Student:

    @staticmethod
    def from_datagram(dgi):
        student = Student()
        student.guid = dgi.get_string()
        student.first_name = dgi.get_string()
        student.last_name = dgi.get_string()
        student.name = student.first_name + " " + student.last_name
        student.grade = dgi.get_string()
        student.email = dgi.get_string()
        student.pcsb_agreement = dgi.get_uint8()
        student.cat_agreement = dgi.get_uint8()
        student.insurance_paid = dgi.get_uint8()
        student.insurance_amount = dgi.get_string()
        student.date_of_insurance = dgi.get_string()
        student.cat_student = dgi.get_uint8()
        student.tablet_guid = dgi.get_string()
        student.net_assistant = dgi.get_uint8()
        return student
        
    def __eq__(self, other):
        return self.guid == other.guid
        