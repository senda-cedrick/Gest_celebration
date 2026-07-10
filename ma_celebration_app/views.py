from io import BytesIO
import os
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Image

from .forms import WeddingCelebrationForm
from .models import WeddingCelebration


def generate_report_pdf(celebrations):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    # include logo (prefer transparent PNG); try PNG/JPG first, SVG as fallback
    logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo.png')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo.jpg')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo-transparent.svg')

    if os.path.exists(logo_path):
        try:
            if logo_path.lower().endswith('.svg'):
                from svglib.svglib import svg2rlg
                drawing = svg2rlg(logo_path)
                story.append(drawing)
            else:
                img = Image(logo_path, width=4*cm, height=4*cm)
                story.append(img)
            story.append(Spacer(1, 8))
        except Exception:
            pass

    story.append(Paragraph("Rapport des célébrations - L’église prince de paix", styles['Title']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Mariages par mois", styles['Heading2']))
    story.append(Spacer(1, 8))
    months = []
    summary = {}
    for celebration in celebrations.order_by('wedding_date'):
        month = celebration.wedding_date.strftime('%B %Y')
        summary[month] = summary.get(month, 0) + 1
    if summary:
        month_rows = [["Mois", "Nombre de mariages"]]
        for month, count in summary.items():
            month_rows.append([month, str(count)])
        month_table = Table(month_rows, hAlign='LEFT', colWidths=[9*cm, 5*cm])
        month_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        story.append(month_table)
    else:
        story.append(Paragraph("Aucun mariage enregistré.", styles['Normal']))

    story.append(Spacer(1, 16))
    story.append(Paragraph("Liste des événements", styles['Heading2']))
    story.append(Spacer(1, 8))
    if celebrations:
        event_rows = [["Marié", "Mariée", "Date", "Lieu"]]
        for celebration in celebrations.order_by('wedding_date'):
            event_rows.append([
                celebration.groom_name,
                celebration.bride_name,
                celebration.wedding_date.strftime('%d/%m/%Y'),
                celebration.church_name,
            ])
        event_table = Table(event_rows, hAlign='LEFT', colWidths=[4*cm, 4*cm, 3*cm, 3*cm])
        event_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        story.append(event_table)
    else:
        story.append(Paragraph("Aucun événement enregistré.", styles['Normal']))

    story.append(Spacer(1, 16))
    story.append(Paragraph("Certificat de mariage", styles['Heading2']))
    story.append(Spacer(1, 8))
    if celebrations:
        certificate = celebrations.order_by('-wedding_date').first()
        certificate_text = (
            f"Ce certificat atteste que {certificate.groom_name} et {certificate.bride_name} "
            f"se sont unis par les liens du mariage le {certificate.wedding_date.strftime('%d/%m/%Y')} "
            f"à {certificate.church_name}. Cette cérémonie a été célébrée par {certificate.priest_name or 'le prêtre de la paroisse'}."
        )
    else:
        certificate_text = (
            "Ce certificat de mariage est préparé pour l'Église Prince de Paix. "
            "Il atteste que les futurs mariés sont unis devant Dieu et la communauté."
        )
    story.append(Paragraph(certificate_text, styles['BodyText']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Nous déclarons solennellement que ce mariage est célébré avec respect, foi et engagement mutuel.",
        styles['BodyText']
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_monthly_report_pdf(celebrations):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo.png')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo.jpg')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo-transparent.svg')
    if os.path.exists(logo_path):
        try:
            if logo_path.lower().endswith('.svg'):
                from svglib.svglib import svg2rlg
                drawing = svg2rlg(logo_path)
                story.append(drawing)
            else:
                img = Image(logo_path, width=4*cm, height=4*cm)
                story.append(img)
            story.append(Spacer(1, 8))
        except Exception:
            pass

    story.append(Paragraph("Rapport des mariages par mois - L’église prince de paix", styles['Title']))
    story.append(Spacer(1, 12))

    summary = {}
    for celebration in celebrations.order_by('wedding_date'):
        month = celebration.wedding_date.strftime('%B %Y')
        summary[month] = summary.get(month, 0) + 1

    if summary:
        month_rows = [["Mois", "Nombre de mariages"]]
        for month, count in summary.items():
            month_rows.append([month, str(count)])
        month_table = Table(month_rows, hAlign='LEFT', colWidths=[10*cm, 4*cm])
        month_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        story.append(month_table)
    else:
        story.append(Paragraph("Aucun mariage enregistré.", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_events_report_pdf(celebrations):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo.png')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo.jpg')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo-transparent.svg')
    if os.path.exists(logo_path):
        try:
            if logo_path.lower().endswith('.svg'):
                from svglib.svglib import svg2rlg
                drawing = svg2rlg(logo_path)
                story.append(drawing)
            else:
                img = Image(logo_path, width=4*cm, height=4*cm)
                story.append(img)
            story.append(Spacer(1, 8))
        except Exception:
            pass

    story.append(Paragraph("Liste des événements - L’église prince de paix", styles['Title']))
    story.append(Spacer(1, 12))

    if celebrations:
        event_rows = [["Marié", "Mariée", "Date", "Lieu"]]
        for celebration in celebrations.order_by('wedding_date'):
            event_rows.append([
                celebration.groom_name,
                celebration.bride_name,
                celebration.wedding_date.strftime('%d/%m/%Y'),
                celebration.church_name,
            ])
        event_table = Table(event_rows, hAlign='LEFT', colWidths=[4*cm, 4*cm, 3*cm, 4*cm])
        event_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        story.append(event_table)
    else:
        story.append(Paragraph("Aucun événement enregistré.", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_certificate_report_pdf(celebrations):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo.png')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo.jpg')
    if not os.path.exists(logo_path):
        logo_path = os.path.join(settings.BASE_DIR, 'ma_celebration_app', 'static', 'assets', 'images', 'brand', 'logo', 'logo-transparent.svg')
    if os.path.exists(logo_path):
        try:
            if logo_path.lower().endswith('.svg'):
                from svglib.svglib import svg2rlg
                drawing = svg2rlg(logo_path)
                story.append(drawing)
            else:
                img = Image(logo_path, width=6*cm, height=6*cm)
                story.append(img)
            story.append(Spacer(1, 8))
        except Exception:
            pass

    story.append(Paragraph("Certificat de mariage - Église intercommunautaire Prince de Paix (EIPP)", styles['Title']))
    story.append(Spacer(1, 12))

    if celebrations:
        certificate = celebrations.order_by('-wedding_date').first()
        certificate_text = (
            f"Nous certifions que Monsieur {certificate.groom_name}, résidant sur la paroisse, "
            f"et Madame {certificate.bride_name}, résidant sur la paroisse, ont été unis par le mariage "
            f"selon le rite évangélique à l'Église intercommunautaire Prince de Paix (EIPP) dans la paroisse."
        )
        celebration_line = (
            f"Cette cérémonie a été célébrée le {certificate.wedding_date.strftime('%d/%m/%Y')} "
            f"à {certificate.church_name} par {certificate.priest_name or 'le pasteur titulaire de la paroisse'}."
        )
        report_date = certificate.wedding_date.strftime('%d/%m/%Y')
    else:
        certificate_text = (
            "Nous certifions que les futurs mariés ont été unis par le mariage selon le rite évangélique "
            "à l'Église intercommunautaire Prince de Paix (EIPP) dans la paroisse."
        )
        celebration_line = (
            "Ce certificat de mariage est préparé pour attester l'union solennelle devant Dieu et la communauté."
        )
        report_date = timezone.localdate().strftime('%d/%m/%Y')

    story.append(Paragraph(certificate_text, styles['BodyText']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(celebration_line, styles['BodyText']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Ainsi ils ne sont plus deux, mais une seule chair ; que donc l'homme ne sépare pas.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        f"Fait à l'Église intercommunautaire Prince de Paix (EIPP), le {report_date}.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 24))
    story.append(Paragraph("Pasteur titulaire de la paroisse", styles['BodyText']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Signature : ____________________________", styles['BodyText']))

    doc.build(story)
    buffer.seek(0)
    return buffer


@login_required
def home(request):
    today = timezone.localdate()
    celebrations_count = WeddingCelebration.objects.count()
    marriages_count = celebrations_count
    ongoing_events_count = WeddingCelebration.objects.filter(wedding_date=today).count()
    brides_count = WeddingCelebration.objects.count()
    next_celebration = WeddingCelebration.objects.filter(wedding_date__gte=today).order_by('wedding_date').first()
    recent_brides = WeddingCelebration.objects.order_by('-wedding_date')[:5]
    User = get_user_model()
    recent_users = User.objects.order_by('-date_joined')[:5]

    return render(request, 'ma_celebration_app/home.html', {
        'celebrations_count': celebrations_count,
        'marriages_count': marriages_count,
        'ongoing_events_count': ongoing_events_count,
        'brides_count': brides_count,
        'next_celebration': next_celebration,
        'recent_brides': recent_brides,
        'recent_users': recent_users,
    })


@login_required
def celebrations_list(request):
    if request.method == 'POST':
        form = WeddingCelebrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Célébration ajoutée avec succès.')
            return redirect('celebrations_list')
    else:
        form = WeddingCelebrationForm()

    celebrations = WeddingCelebration.objects.order_by('wedding_date')
    return render(request, 'ma_celebration_app/celebrations_list.html', {
        'celebrations': celebrations,
        'form': form,
    })


@login_required
def reports(request):
    celebrations = WeddingCelebration.objects.order_by('wedding_date')
    return render(request, 'ma_celebration_app/reports.html', {
        'celebrations': celebrations,
    })


@login_required
def reports_pdf(request):
    celebrations = WeddingCelebration.objects.order_by('wedding_date')
    buffer = generate_report_pdf(celebrations)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_complet_mariages.pdf"'
    return response


@login_required
def reports_monthly_pdf(request):
    celebrations = WeddingCelebration.objects.order_by('wedding_date')
    buffer = generate_monthly_report_pdf(celebrations)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_mariages_par_mois.pdf"'
    return response


@login_required
def reports_events_pdf(request):
    celebrations = WeddingCelebration.objects.order_by('wedding_date')
    buffer = generate_events_report_pdf(celebrations)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rapport_evenements.pdf"'
    return response


@login_required
def reports_certificate_pdf(request):
    celebrations = WeddingCelebration.objects.order_by('wedding_date')
    buffer = generate_certificate_report_pdf(celebrations)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificat_mariage.pdf"'
    return response


@login_required
def celebration_delete(request, celebration_id):
    celebration = get_object_or_404(WeddingCelebration, id=celebration_id)
    if request.method == 'POST':
        celebration.delete()
        messages.success(request, 'Célébration supprimée avec succès.')
        return redirect('celebrations_list')
    return render(request, 'ma_celebration_app/celebration_confirm_delete.html', {
        'celebration': celebration,
    })


@login_required
def celebration_detail(request, celebration_id):
    celebration = WeddingCelebration.objects.filter(id=celebration_id).first()
    return render(request, 'ma_celebration_app/celebration_detail.html', {
        'celebration': celebration,
    })
