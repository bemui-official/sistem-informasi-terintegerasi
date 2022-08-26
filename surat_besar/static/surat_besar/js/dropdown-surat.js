const links_surat_besar = {
    'SPK Nonprofit': 'https://docs.google.com/document/d/1Mh3sHy5L0Le_PDH78-pftdodIU1tmdAI/edit?usp=sharing&ouid=109525181806200227081&rtpof=true&sd=true',
    'SPK Profit': 'https://docs.google.com/document/d/1Q5DZQszGysgdA8TLs43Zhyv6iaJwBPAm/edit?usp=sharing&ouid=109525181806200227081&rtpof=true&sd=true',
    'MoU Lembaga Eksternal': 'https://docs.google.com/document/d/156FgHoFvcy0BHvY0q4kfbxVqa5QsgWik/edit?usp=sharing&ouid=109525181806200227081&rtpof=true&sd=true',
    'LPJ Kegiatan': 'https://docs.google.com/document/d/1tYO70rx6fRXoqQY9lyDhUUKmZdRMNQY6/edit?usp=sharing&ouid=109525181806200227081&rtpof=true&sd=true',
    'LPJ Keuangan': 'https://docs.google.com/spreadsheets/d/1HCLoLWgNLO9Gri4_Ww8_AXU4iIa0Ng2h/edit?usp=sharing&ouid=109525181806200227081&rtpof=true&sd=true',
    'Pra Proposal': 'https://docs.google.com/document/d/1PWnrKaFrEKYI_Ya2YbQgP_MPnl12EnNK/edit?usp=sharing&ouid=109525181806200227081&rtpof=true&sd=true',
    'Proposal': 'https://docs.google.com/document/d/16GpZcNSW0F6u_1F8EblTp-23o_26pi2J/edit?usp=sharing&ouid=109525181806200227081&rtpof=true&sd=true',
    'lainnya': ''
}


function showLink(s) {
    var tag = document.getElementById('link_a');
    if(s.value == "lainnya"){
        tag.style.display = "none"
    }
    else if (s.value != "none"){
        var tag = document.getElementById('link_a');
        var tag2 = document.getElementById('link');
        tag2.textContent = "Link Surat " + s.value
        tag.href = links_surat_besar[s.value]
        tag.target = "_blank"
        tag.style.display = "block"
    }
    else{
        tag.style.display = "none"
    }
}

function showInsidental(s) {
    var tag = document.getElementById('bukti_insidental');
    if (s.value == "True") {
        tag.style.display = "block"
    } else {
        tag.style.display = "none"
    }
}