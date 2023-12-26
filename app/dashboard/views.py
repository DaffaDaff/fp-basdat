from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import EditBiodataForm, PendaftaranForm, NilaiForm
from .models import Biodata, Praktikan, Kelompok, Jadwal, Asisten, NilaiPraktikan

# Create your views here.
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    bio = Biodata.objects.filter(username=request.user.username)
    
    if bio:
        return render(request, 'dashboard.html',
            {
            'nama' : bio.get().nama
            }
        )
    else:
        return render(request, 'dashboard.html')
    
def edit(request):
    bio = Biodata.objects.filter(username=request.user.username)

    if request.method == 'POST':
        if bio:
            form = EditBiodataForm(request.POST, instance=bio.get())
        else:
            form = EditBiodataForm(request.POST)

        if form.is_valid():
            bio = form.save(commit=False)
            bio.username = request.user
            bio.save()
            return redirect('/dashboard/')
    else:
        if bio:
            form = EditBiodataForm(instance=bio.get())
        else:
            form = EditBiodataForm()

    return render(request, 'edit.html', {
        'form': form,
    })

def ambil(request):
    if request.method == 'POST':
        form = PendaftaranForm(request.POST)

        if form.is_valid():
            praktikum = form.cleaned_data['id_praktikum']
            already_taken = Praktikan.objects.filter(username=request.user, id_praktikum=praktikum)
            if not already_taken:
                praktikan = form.save(commit=False)
                praktikan.username = request.user

                kelompoks = Kelompok.objects.filter(id_praktikum=praktikum)

                if kelompoks:
                    kelompok = kelompoks.reverse()[0]
                    

                    anggota = Praktikan.objects.filter(id_kelompok=kelompok)
                    if len(anggota) >= 3:
                        kelompok = Kelompok(nama_kelompok=kelompok.nama_kelompok + 1, id_praktikum=praktikum)
                else:
                    kelompok = Kelompok(nama_kelompok=1, id_praktikum=praktikum)
                
                kelompok.save()
                praktikan.id_kelompok = kelompok

                praktikan.save()
                return redirect('/dashboard/')
            else:
                pass
    else:
        form = PendaftaranForm()

    return render(request, 'ambil.html',
    {
        'form': form,
    })

def jadwal(request):
    return render(request, 'jadwal.html',
    {
        'jadwals' : Jadwal.objects.filter(id_kelompok=kel.id_kelompok) for kel in Praktikan.objects.filter(username = request.user)
    })

def kelompok(request):
    kels = {}
    for kel in Praktikan.objects.filter(username = request.user):
        kelompok = kel.id_kelompok 
        kels[kelompok.id_praktikum] = Praktikan.objects.filter(id_kelompok=kelompok.id_kelompok)

    print(kels)
    
    return render(request, 'kelompok.html',
    {
        'kels' : kels
    })

def nilai(request):
    return render(request, 'nilai.html',
    {
        'nilais' : NilaiPraktikan.objects.filter(id_praktikan=user) for user in Praktikan.objects.filter(username = request.user)
    })

def inputnilai(request):
    jadwals = [Jadwal.objects.filter(id_asisten=kel) for kel in Asisten.objects.filter(user = request.user)]
    next = False
    next2 = False

    if request.method == 'POST':
        form = NilaiForm(None, request.POST)
        
        if form.is_valid():
            if form.cleaned_data['id_jadwal'] and form.cleaned_data['id_praktikan'] and form.cleaned_data['nilai']:
                nilai = NilaiPraktikan.objects.filter(id_jadwal=form.cleaned_data['id_jadwal'], id_praktikan=form.cleaned_data['id_praktikan'])
                
                if nilai:
                    form = NilaiForm(form.cleaned_data['id_jadwal'], request.POST, instance=nilai.get())

                form.save()
                redirect('/input-nilai/')
            elif form.cleaned_data['id_jadwal'] and form.cleaned_data['id_praktikan']:
                nilai = NilaiPraktikan.objects.filter(id_jadwal=form.cleaned_data['id_jadwal'], id_praktikan=form.cleaned_data['id_praktikan'])
                
                if nilai:
                    form = NilaiForm(form.cleaned_data['id_jadwal'], instance=nilai.get())
                next2 = True
                next = True
            elif form.cleaned_data['id_jadwal']:
                form = NilaiForm(form.cleaned_data['id_jadwal'], request.POST)
                next = True

    else:
        form = NilaiForm()

    return render(request, 'input-nilai.html',{
        'form' : form,
        'jadwals' : jadwals,
        'praktikan' : next,
        'nilai' : next2,
    })

def jadwalasisten(request):
    return render(request, 'jadwal-asisten.html',
    {
        'jadwals' : Jadwal.objects.filter(id_asisten=kel) for kel in Asisten.objects.filter(user = request.user)
    })