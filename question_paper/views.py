import csv
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import TestBatch, Question, StudentAttempt
from .forms import ExamUploadForm

def upload_exam(request):
    if request.method == 'POST':
        form = ExamUploadForm(request.POST, request.FILES)
        if form.is_valid():
            exam_name = form.cleaned_data['exam_name']
            duration_hours = form.cleaned_data['duration_hours']
            tsv_file = request.FILES['tsv_file']
            
            expires_at = timezone.now() + timedelta(hours=duration_hours)
            batch = TestBatch.objects.create(exam_name=exam_name, expires_at=expires_at)
            
            decoded_file = tsv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter='\t')
            next(reader, None) # Skip header row
            
            for row in reader:
                if len(row) >= 6:
                    Question.objects.create(
                        batch=batch,
                        question_text=row[0].strip(),
                        option_1=row[1].strip(),
                        option_2=row[2].strip(),
                        option_3=row[3].strip(),
                        option_4=row[4].strip(),
                        correct_answer=row[5].strip()
                    )
            return render(request, 'upload_success.html', {'batch': batch})
    else:
        form = ExamUploadForm()
    return render(request, 'upload.html', {'form': form})

def take_test(request, pk):
    batch = get_object_or_404(TestBatch, pk=pk)
    if batch.is_expired():
        return render(request, 'error.html', {'message': 'This assessment link has expired.'})
        
    questions = Question.objects.filter(batch=batch)
    results = []
    score = 0
    is_submitted = False
    student_id = request.POST.get('student_id', 'ST-999').strip()

    if request.method == 'POST' and 'student_id' in request.POST:
        is_submitted = True
        answers_data = {}
        
        for q in questions:
            selected_option = request.POST.get(f'question_{q.pk}', '').strip()
            answers_data[str(q.pk)] = selected_option
            is_correct = (selected_option == q.correct_answer)
            if is_correct:
                score += 1
            results.append({
                'question': q,
                'selected': selected_option,
                'is_correct': is_correct
            })
            
        StudentAttempt.objects.create(
            batch=batch,
            student_id=student_id,
            score=score,
            answers_data=answers_data
        )

    return render(request, 'take_test.html', {
        'batch': batch,
        'questions': questions,
        'results': results if is_submitted else None,
        'score': score,
        'student_id': student_id
    })