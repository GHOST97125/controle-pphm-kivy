# main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.utils import platform
from plyer import gps, camera
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

class PPHMForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.chantier = TextInput(hint_text="Nom du chantier")
        self.entreprise = TextInput(hint_text="Nom de l'entreprise")
        self.date = TextInput(hint_text="Date du contrôle")
        self.localisation = TextInput(hint_text="Coordonnées GPS")
        self.code_pphm = TextInput(hint_text="Code PPHM")
        self.dimension = TextInput(hint_text="Dimensions")
        self.message = TextInput(hint_text="Type de message")
        self.etat = TextInput(hint_text="État du matériel")
        self.resultat = TextInput(hint_text="Conforme / Non conforme")
        self.observation = TextInput(hint_text="Observations")

        self.add_widget(Label(text="Formulaire de contrôle PPHM", size_hint=(1, 0.1)))
        for champ in [self.chantier, self.entreprise, self.date, self.localisation,
                      self.code_pphm, self.dimension, self.message,
                      self.etat, self.resultat, self.observation]:
            self.add_widget(champ)

        bouton_gps = Button(text="Géolocaliser")
        bouton_gps.bind(on_press=self.get_gps)
        self.add_widget(bouton_gps)

        bouton_photo = Button(text="Prendre une photo")
        bouton_photo.bind(on_press=self.take_photo)
        self.add_widget(bouton_photo)

        bouton_pdf = Button(text="Générer le PDF")
        bouton_pdf.bind(on_press=self.export_pdf)
        self.add_widget(bouton_pdf)

    def get_gps(self, instance):
        if platform == 'android':
            try:
                gps.configure(on_location=self.on_location)
                gps.start(minTime=1000, minDistance=0)
            except NotImplementedError:
                self.localisation.text = "GPS non supporté"

    def on_location(self, **kwargs):
        self.localisation.text = f"{kwargs['lat']}, {kwargs['lon']}"

    def take_photo(self, instance):
        filepath = os.path.join(App.get_running_app().user_data_dir, "photo_pphm.jpg")
        camera.take_picture(filename=filepath, on_complete=self.photo_taken)

    def photo_taken(self, filepath):
        if filepath and os.path.exists(filepath):
            popup = Popup(title="Photo enregistrée", content=Label(text=filepath), size_hint=(0.8, 0.3))
            popup.open()

    def export_pdf(self, instance):
        fichier_pdf = os.path.join(App.get_running_app().user_data_dir, "controle_pphm.pdf")
        doc = SimpleDocTemplate(fichier_pdf, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Fiche de Contrôle PPHM", styles['Title']))
        elements.append(Spacer(1, 12))

        donnees = [
            ["Champ", "Valeur"],
            ["Chantier", self.chantier.text],
            ["Entreprise", self.entreprise.text],
            ["Date", self.date.text],
            ["Coordonnées GPS", self.localisation.text],
            ["Code PPHM", self.code_pphm.text],
            ["Dimensions", self.dimension.text],
            ["Message", self.message.text],
            ["État", self.etat.text],
            ["Résultat", self.resultat.text],
            ["Observation", self.observation.text]
        ]

        tableau = Table(donnees, hAlign='LEFT')
        tableau.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(tableau)
        doc.build(elements)

        popup = Popup(title="PDF généré", content=Label(text=fichier_pdf), size_hint=(0.8, 0.3))
        popup.open()

class PPHMApp(App):
    def build(self):
        return ScrollView(size_hint=(1, None), size=(800, 1000), do_scroll_x=False, do_scroll_y=True,
                          scroll_type=['bars', 'content'], bar_width=10,
                          content=PPHMForm())

if __name__ == '__main__':
    PPHMApp().run()
