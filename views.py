from django.http import HttpResponse
from matplotlib.markers import MarkerStyle
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from .models import Student, Result
from .forms import StudentForm
import json


def search_result(request):

    roll_no = request.GET.get("roll_no")
    student = None
    result = None
    total = 0
    percentage = 0
    status = ""
    grade = ""
    marks=""

    subjects =[]
    marks =[]

   
    if roll_no:   # roll number empty nahi hona chahiye

        student = Student.objects.filter(roll_no=roll_no).first()

        if student:
            result = Result.objects.filter(student=student)
            for r in result:
                subjects.append(r.subject)
                marks.append(r.marks) # type: ignore

            total = sum([r.marks for r in result])
            subject_count = result.count()

            if subject_count > 0:
                percentage = total / subject_count
            else:
                percentage = 0

            if percentage >= 40:
                status = "PASS"
            else:
                status = "FAIL"


            if percentage >= 90:
                grade = "A+"
            elif percentage >= 80:
                grade = "A"
            elif percentage >= 70:
                grade = "B"
            elif percentage >= 60:
                grade = "C"
            elif percentage >= 40:
                grade = "D"
            else:
                grade = "F"


    context = {
        "student": student,
        "result": result,
        "total": total,
        "percentage": percentage,
        "status": status,
        "grade" :grade,
        "subjects" :subjects,
        "marks":marks,
    }

    return render(request, "search.html", context)


def add_student(request):

    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/result/')

    else:
        form = StudentForm()

    return render(request, "add_student.html", {"form": form})


def result_list(request):

    results = Result.objects.all()

    subjects = []
    marks = []

    for r in results:
        subjects.append(r.subject)
        marks.append(r.marks)

    context = {
        "results": results,
        "subjects": subjects,
        "marks": marks
    }

    return render(request, "result_list.html", context)


def download_result(request, roll_no):

    student = Student.objects.filter(roll_no=roll_no).first()
    results = Result.objects.filter(student=student)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="result.pdf"'

    p = canvas.Canvas(response)

    y = 800
    p.drawString(100, y, "Student Result")
    y -= 40

    p.drawString(100, y, f"Name: {student.name}")
    y -= 20
    p.drawString(100, y, f"Roll No: {student.roll_no}")
    y -= 40

    total = 0

    for r in results:
        p.drawString(100, y, f"{r.subject} : {r.marks}")
        total += r.marks
        y -= 20

    subjects = results.count()

    if subjects > 0:
        percentage = total / subjects
    else:
        percentage = 0

    y -= 20
    p.drawString(100, y, f"Total Marks: {total}")
    y -= 20
    p.drawString(100, y, f"Percentage: {percentage}%")

    p.save()

    return response


def student_login(request):

    if request.method == "POST":

        roll_no = request.POST.get("roll_no")

        return redirect(f'/dashboard/?roll_no={roll_no}')

    return render(request,"login.html")

def dashboard(request):

    roll_no = request.GET.get("roll_no")

    student = Student.objects.filter(roll_no=roll_no).first()

    return render(request,"dashboard.html",{"student":student})