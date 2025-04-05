#!/bin/bash

mkdir -p manuais_weg
cd manuais_weg

user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
referer="https://www.weg.net/"

urls=(
"https://static.weg.net/medias/downloadcenter/h0c/hfd/WEG-WMO-iom-installation-operation-and-maintenance-manual-of-electric-motors-50033244-manual-pt-en-es-web.pdf"
"https://static.weg.net/medias/downloadcenter/h32/h6d/manual_transformador_seco_10000647758_portugues.pdf"
"https://static.weg.net/medias/downloadcenter/h51/h9c/WEG-CFW300-programming-manual-10007849716-en.pdf"
"https://static.weg.net/medias/downloadcenter/h0b/h15/WEG-enterprise-manual-de-instalacao-e-operacao-0502132-manual-portugues-br.pdf"
"https://static.weg.net/medias/downloadcenter/hb7/h52/WEG-CFW500-programming-manual-10006739425-en.pdf"
"https://static.weg.net/medias/downloadcenter/h9c/h19/WEG-tintas-manutencao-industrial-50021433-catalogo-pt.pdf"
"https://static.weg.net/medias/downloadcenter/h7c/h6c/WEG-w50-three-phase-electric-motor-technical-catalogue-50044241-brochure-english-web.pdf"
"https://static.weg.net/medias/downloadcenter/h3c/hb5/WEG-SSW7000-users-manual-10001461783-en.pdf"
"https://static.weg.net/medias/downloadcenter/hcb/h36/WEG-professional-manual-de-instalacao-e-operacao-0502139-manual-portugues-br.pdf"
"https://static.weg.net/medias/downloadcenter/ha7/h48/WEG-synchronou-motor-brushless-11866576-manual-english-dc.pdf"
"https://static.weg.net/medias/downloadcenter/hae/h83/WEG-10004699316-13871637-r00-CFW11-W-users-manual-en.pdf"
"https://static.weg.net/medias/downloadcenter/h52/h74/WEG-PLC410-user-manual-10010696216-pt.pdf"
"https://static.weg.net/medias/downloadcenter/h5f/h9d/WEG-WMO-manual-safe-area-india-16267648-english-web.pdf"
"https://static.weg.net/medias/downloadcenter/h35/h1c/WEG-CFW320-users-manual-10008951923-en.pdf"
"https://static.weg.net/medias/downloadcenter/h29/h41/WEG-manual-transformador-a-oleo-de-distribuicao-ate-300-kva-10003898721-1-manual-portugues-br.pdf"
"https://static.weg.net/medias/downloadcenter/he3/he6/WEG-three-phase-induction-motors-used-in-explosive-atmospheres-low-and-high-voltage-m-line-squirrel-cage-rotor-horizontal-12352463-manual-english-dc.pdf"
"https://static.weg.net/medias/downloadcenter/h03/hd3/WEG-CFW900-users-manual-10008985516-en.pdf"
"https://static.weg.net/medias/downloadcenter/h2b/h91/WEG-cfw11-manual-de-programacao-0899.5654-2.0x-manual-portugues-br.pdf"
"https://static.weg.net/medias/downloadcenter/haa/h3e/WEG-w22xd-flameproof-motors-installation-operation-and-maintenance-manual-13564560-manual-english-web.pdf"
"https://static.weg.net/medias/downloadcenter/h56/hc5/WEG-CESTARI-manual-iom-coroa-e-rosca-50111526-english-web.pdf"
)

for url in "${urls[@]}"; do
    file=$(basename "$url")
    echo "🔽 Baixando $file..."
    curl -L -O -H "User-Agent: $user_agent" -H "Referer: $referer" -H "Connection: keep-alive" "$url"
    if [[ $? -ne 0 ]]; then
        echo "❌ Falha ao baixar: $url"
    else
        echo "✅ Sucesso: $file"
    fi
done

echo "🎉 Downloads com curl finalizados!"
