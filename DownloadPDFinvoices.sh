#!/bin/bash

LOG_FILE="result.log"

while read -r ID
do
  [ -z "$ID" ] && continue

  echo "Requete pour ID : $ID" | tee -a "$LOG_FILE"

  RESPONSE=$(curl -s -w "%{http_code}" -o response.txt \
    -X GET "url/api/invoice/${ID}/pdf?id=${ID}" \
    -H "Authorization: Bearer ${TOKEN}")

  HTTP_CODE="$RESPONSE"

  if [ "$HTTP_CODE" -eq 200 ]; then
    echo "Succes pour ID $ID" | tee -a "$LOG_FILE"
  else
    echo "Erreur pour ID $ID (code $HTTP_CODE)" | tee -a "$LOG_FILE"
  fi

  echo "----------------------" | tee -a "$LOG_FILE"

done < ids.csv

#### creer le fichier ids.txt pour lister les ids des invoices récupérer en DB
