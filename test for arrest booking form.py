doc = list(string.split(""))

blockl_list = ["Report Date", "Booking Status", "Printed By", "District", "UCR Code", "OBTN", "Court of Appearance", "Master Name", "Age", "Location of Arrest",
            "Booking Name", "Alias", "Address", "Charges", "Booking#", "Incident#", "CR Number", "Booking Date", "Arrest Date", "RA Number", "Sex", "Height", "Occupation",
            "Race", "Weight", "Employer/School", "Date of Birth", "Build, Emp/School Addr", "Place of birth", "Eyes color", "Social Sec. Number", "Marital Status", 
            "Hair color", "Operators License", "Mother's Name", "Complexion", "State", "Father's Name","Phone Used", "Scars/Marks/Tattos", "Examined at Hospital",
            "Clothing Desc", "Breathalyzer Used", "Examined by EMS", "Arresting Officer", "Cell Number", "Booking Officer", "Partner's","Informed of Rights", "Unit#",
            "Placed in Cell By", "Trans Unit#", "Searched By", "Cautions", "Booking Comments","Visible Injuries", "Person Notified", "Relationship","Phone","Address",
            "Juv.Prob.Officer","Notified By","Notified Date/Time","Bail Set By", "I Selected the Bail Comm.","Bailed By","Amount","BOP Check",
            "Suicide Check","BOP Warrant", "BOP Court"]

for s in doc:
    for word in block_list:
        s = s.replace(word, "")

content = dict(zip(blockl_list, doc))