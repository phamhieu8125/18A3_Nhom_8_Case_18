import pandas as pd

d1 = pd.read_csv('student_profile.csv')
d1['student_id'] = d1['student_id'].str.strip().str.upper()
d1['full_name'] = d1['full_name'].str.strip().str.replace('  ', ' ') .str.replace('  ', ' ').str.lower().str.title()
d1['class_cohort'] = d1['class_cohort'].str.strip().str.upper().replace(' ', '', regex= True)

d2 = pd.read_csv('club_registration.csv')
d2['join_count'] = d2['join_count'].replace({'two': 2, '-1': 1})
d2['join_count'] = d2['join_count'].astype('int64')
d2['club_id'] = d2['club_id'].str.strip().str.lower()
d2['club_id'] = d2['club_id'].replace({'clb_amnhac': 'clb am nhac',
                                       'clb_kn_mem': 'clb ky nang mem',
                                       'clb_the_thao': 'clb the thao',
                                       'clb_tn': 'clb tot nghiep'}).str.title()
d2['student_id'] = d2['student_id'].str.strip()

d3 = pd.read_csv('event_attendance.csv', index_col= 'event_id')
d3['attendance_status'] = d3['attendance_status'].replace({'Vắng': 'Absent', 'Vang': 'Absent', 'vang ': 'Absent',
                                                           'Có mặt': 'Present', 'co  mat': 'Present', 'Co mat': 'Present',
                                                           'Muon': 'Late', 'Muộn': 'Late'})
d3['student_id'] = d3['student_id'].str.strip().str.upper()
d3['event_name'] = d3['event_name'].str.strip()
d3['club_id'] = d3['club_id'].str.strip().str.lower().str.capitalize()
d3['club_id'] = d3['club_id'].replace({'Clb_amnhac': 'Clb am nhac',
                                       'Clb_kn_mem': 'Clb ky nang mem',
                                       'Clb_the_thao': 'Clb the thao'})

a1 = pd.merge(d1, d3, on= 'student_id', how= 'outer')
a2 = a1.merge(d2, on= 'student_id', how= 'outer')
a2 = a2.drop_duplicates(['student_id', 'club_id_x', 'club_id_y']).dropna()
p1 = a2.pivot(index= ['student_id', 'club_id_x', 'club_id_y'],columns= 'attendance_status', values= 'join_count')
#print(p1.to_string())

a3 = d1.merge(d2, on= 'student_id', how= 'outer').drop_duplicates(['class_cohort', 'student_id']).dropna()
#print(a3.to_string())

p2 = a3.pivot(index= 'student_id', columns= 'class_cohort', values= 'join_count')
print(p2.to_string())
print(p1.stack().to_string())
print(p1.unstack().to_string())
print(p2.stack().to_string())
print(p2.unstack().to_string())
print(d3['club_id'].value_counts().max())
print(d3['club_id'].value_counts().min())

pp = d3.merge(d1, on= 'student_id', how= 'outer')
present_count = pp.groupby(['club_id', 'class_cohort', 'attendance_status']).size().reset_index()
print(present_count[present_count['attendance_status'] == 'Present'].value_counts())