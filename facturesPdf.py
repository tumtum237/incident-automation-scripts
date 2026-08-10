import requests
import os
import csv

BEARER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjE5NyIsIm5hbWVpZCI6IjE5NyIsInR5cGUiOiJVU0VSIiwibmJmIjoxNzg2MzU1MjA4LCJleHAiOjE3ODYzNTU1MDgsImlhdCI6MTc4NjM1NTIwOCwiaXNzIjoiaHR0cHM6Ly9hdXRoLWFwaS5jaXRpei5mciIsImF1ZCI6Imh0dHBzOi8vcG9ydGFpbC5jaXRpei5mci9iYWNrb2ZmaWNlIn0.25JdsCCg7M5k2XmtiwBli0YKqogsrB_4ryL_oO7P5Jw" 

def telecharger_facture(invoice_id, dossier_destination="factures"):
    """Télécharge une facture PDF à partir de l'API."""
    url = f"https://backend.citiz.fr/api/invoice/{invoice_id}/pdf"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        nom_fichier = os.path.join(dossier_destination, f"facture_{invoice_id}.pdf")
        with open(nom_fichier, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)
        print(f"Facture {invoice_id} téléchargée avec succès dans {nom_fichier}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de la facture {invoice_id}: {e}")
        return False

def lire_ids_depuis_csv(chemin_csv):
    ids = []
    with open(chemin_csv, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return ids

    # Détecte si la première ligne est un en-tête (non numérique)
    premiere_ligne = rows[0]
    header = None
    start_index = 0
    if premiere_ligne and not premiere_ligne[0].strip().isdigit():
        header = [h.strip().lower() for h in premiere_ligne]
        start_index = 1

    col_index = 0
    if header and "invoice_id" in header:
        col_index = header.index("invoice_id")

    for row in rows[start_index:]:
        if not row:
            continue
        valeur = row[col_index].strip()
        if valeur:
            ids.append(int(valeur))

    return ids

def telecharger_factures_en_masse(liste_invoice_ids):
    """Télécharge en masse les factures PDF pour la liste d'identifiants fournie."""
    dossier_destination = "factures"
    os.makedirs(dossier_destination, exist_ok=True)
    print(f"Début du téléchargement des factures vers le dossier '{dossier_destination}'...")
    for invoice_id in liste_invoice_ids:
        telecharger_facture(invoice_id, dossier_destination)
    print("Téléchargement des factures terminé.")

if __name__ == "__main__":
    chemin_csv = "invoiceIds.csv"  # chemin vers votre fichier CSV
    liste_ids_a_telecharger = lire_ids_depuis_csv(chemin_csv)
    print(f"{len(liste_ids_a_telecharger)} identifiants trouvés dans {chemin_csv}")
    telecharger_factures_en_masse(liste_ids_a_telecharger)