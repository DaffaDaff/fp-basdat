from django import forms

from .models import Biodata, Praktikan, NilaiPraktikan

INPUT_CLASSES = 'py-1 rounded-2'

class EditBiodataForm(forms.ModelForm):
    class Meta:
        model = Biodata
        fields = ('nama', 'nrp', 'ttl')
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'size': '40px'
            }),
            'nrp': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'size': '15px'
            }),
            'ttl': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'size': '30px'
            }),
        }

class PendaftaranForm(forms.ModelForm):
    class Meta:
        model = Praktikan
        fields = ('id_praktikum', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_praktikum'].widget.attrs.update({"class": "form-control"})
        # or iterate over field to add class for each field
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':"form-control"})

class NilaiForm(forms.ModelForm):
    class Meta:
        model = NilaiPraktikan
        fields = ('id_jadwal', 'id_praktikan', 'nilai' )
    
    def __init__(self, jadwal=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nilai'].widget.attrs.update({'min' : '0'})
        self.fields['nilai'].widget.attrs.update({'max' : '100'})

        for field in self.fields:
            if field == 'id_praktikan':
                if jadwal:
                    self.fields[field].queryset = Praktikan.objects.all()
            self.fields[field].widget.attrs.update({'class':"form-control"})