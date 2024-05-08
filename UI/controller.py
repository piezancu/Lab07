import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        umidita_media_mese = self._model.get_umidita_media_mese(self._mese)
        self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è:"))
        for citta in umidita_media_mese:
            self._view.lst_result.controls.append(ft.Text(f"{citta}: {umidita_media_mese[citta]}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese")
            return
        sequenza, costo = self._model.trova_sequenza_citta(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Il costo della sequenza è {costo}"))
        for fermata in sequenza:
            self._view.lst_result.controls.append(ft.Text(fermata))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

