import cv2
import face_recognition
import os
from .models import Student
from Home.models import Attendance, Time_Table
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

def generate_embedding(path):
    if os.path.exists(path):
        face_image = face_recognition.load_image_file(path)
        face_encodings = face_recognition.face_encodings(face_image)
        if face_encodings:
            return face_encodings  # Assuming only one face in the image
    return None

def recognize_faces():
    cap = cv2.VideoCapture(0)
    try:
        if not cap.isOpened():
            print("Error: Unable to open camera.")
            return []

        res = [] 
        students = Student.objects.all()

        embeddings = []
        for student in students:
            if student.user.picture:
                path = student.user.picture.path
                embed = generate_embedding(path)
                name = student.user.get_full_name()
                embeddings.append((student.roll_number, embed, name))
            else:
                embeddings.append((student.roll_number, None, "Unknown"))

        iteration = 0  # Counter for number of iterations
        while iteration < (settings.FACE_RECOGNITION_ITERATIONS or 10):
            print(res)
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture frame.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for roll_number, embed, name in embeddings:
                if embed is None:
                    for x in res:
                        if x['roll_no'] == roll_number:
                            x['status'] = False
                            break
                    else:
                        res.append({'roll_no': roll_number, 'name': name, 'status': False})
                    continue
                
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(embed, face_encoding)
                    if any(matches):
                        for x in res:
                            if x['roll_no'] == roll_number:
                                x['status'] = True
                                break
                        else:
                            res.append({'roll_no': roll_number, 'name': name, 'status': True})
                        break
                else:
                    for x in res:
                        if x['roll_no'] == roll_number:
                            x['status'] = False
                            break
                    else:
                        res.append({'roll_no': roll_number, 'name': name, 'status': False})

                iteration += 1
            # for (top, right, bottom, left), re in zip(face_locations, res):
            #     status = None
            #     for student_info, embd in zip(res, embeddings):
            #         if embd[0] == student_info['roll_no']:
            #             status = student_info['status']
            #             name = student_info['name']
            #             break
                    
            #     if status is not None:
            #         if status:
            #             cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            #             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            #             font = cv2.FONT_HERSHEY_DUPLEX
            #             cv2.putText(frame, name or 'Unknown', (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            #         else:
            #             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            #             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            #             font = cv2.FONT_HERSHEY_DUPLEX
            #             cv2.putText(frame, name or 'Unknown', (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            #     else:
            #         cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            #         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
            #         font = cv2.FONT_HERSHEY_DUPLEX
            #         cv2.putText(frame, 'Unknown', (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow("IntelliTeach Face Recognition", frame)
            if cv2.waitKey(1) == ord('q'):
                break

        return res
    finally:
        cap.release()
        cv2.destroyAllWindows()


def set_attendance(force=False):
    day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    current_day_index = timezone.now().weekday()
    current_day = day[current_day_index] if settings.TEST_ATTENDANCE else day[0]

    tm = Time_Table.objects.filter(day=current_day)
    current_time = timezone.localtime().time()

    for t in tm:
        time_from_plus_10 = (datetime.combine(datetime.now().date(), t.time_from) + timedelta(minutes=10)).time()
        if t.time_from <= current_time <= t.time_to and current_time >= time_from_plus_10 :
            attendance_date = datetime.now().date()
            attendance_entries = Attendance.objects.filter(time=t, created_at__date=attendance_date)
            for attendance_entry in attendance_entries:
                if attendance_entry.created_at < timezone.now() - timedelta(minutes=10):
                    return attendance_entries
            if attendance_entries.exists() and not force:
                data = recognize_faces()
                for d in data:
                    student = Student.objects.get(roll_number=d['roll_no'])
                    attendance_entry = attendance_entries.filter(student=student).first()
                    if attendance_entry:
                        attendance_entry.status = d['status']
                        attendance_entry.save()
            else:
                data = recognize_faces()
                for d in data:
                    student = Student.objects.get(roll_number=d['roll_no'])
                    Attendance.objects.create(
                        teacher=None,
                        student=student,
                        time=t,
                        status=d['status']
                    )
            return Attendance.objects.filter(time=t, created_at__date=attendance_date)

    print("No classes scheduled for today.")
    return None