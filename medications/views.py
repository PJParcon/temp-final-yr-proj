from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import MedicationEntryForm


@login_required
@require_http_methods(['GET', 'POST'])
def medication_add(request):
    form = MedicationEntryForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        medication = form.save(commit=False)
        medication.user = request.user
        medication.save()
        messages.success(request, 'Medication saved successfully.')
        return redirect('medications:add')
    return render(request, 'medications/medication_form.html', {
        'form': form,
        'active_page': 'medications',
    })
