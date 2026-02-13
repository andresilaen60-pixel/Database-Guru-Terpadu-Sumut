import pandas as pd
import json

# ambil data eksel
df = pd.read_excel("data.xlsx")
df.fillna("", inplace=True)
DATA_JSON = json.dumps(df.to_dict(orient="records"), ensure_ascii=False)

html = """
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Dashboard ABK Guru Sumatera Utara</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" rel="stylesheet">
<link href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css" rel="stylesheet">

<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

<style>
body{
    background:linear-gradient(135deg,#081a3a,#0f2c70);
    color:white;
    font-family:'Segoe UI',sans-serif;
}
header{
    padding:15px 25px;
    font-size:26px;
    font-weight:bold;
    background:linear-gradient(90deg,#081a3a,#133a8a);
}
.glass{
    backdrop-filter:blur(16px);
    background:rgba(255,255,255,0.12);
    border-radius:22px;
    padding:15px;
}
.menu{
    cursor:pointer;
    padding:12px;
    border-radius:12px;
    margin-bottom:6px;
}
.menu:hover{background:rgba(255,255,255,0.25);}

#map{height:520px;border-radius:18px;}
.table-container{display:none;margin-top:15px;}

/* tabel gaya liquid glass */
table.dataTable,
table.dataTable td,
table.dataTable th{
    background:rgba(255,255,255,0.08)!important;
    color:white!important;
}
table.dataTable thead th{
    background:rgba(255,255,255,0.3)!important;
}
table.dataTable tbody tr:hover td{
    background:rgba(255,255,255,0.18)!important;
}

/* highlight merah jika lebih guru */
table.dataTable tbody tr.lebh,
table.dataTable tbody tr.lebh td{
    background:rgba(255,0,0,0.65)!important;
    color:#fff!important;
    font-weight:600;
}

/* rapikan pagination */
.dataTables_wrapper .dataTables_paginate{
    display:flex!important;
    justify-content:end;
    gap:6px;
    margin-top:12px;
}
.dataTables_wrapper .paginate_button{
    background:rgba(255,255,255,0.18)!important;
    color:white!important;
    border-radius:8px!important;
    border:none!important;
}
.dataTables_wrapper .paginate_button.current{
    background:rgba(0,123,255,0.85)!important;
}
/* pengkotakan pagination */
.dataTables_wrapper .dataTables_paginate {
    display: flex !important;
    justify-content: end;
    align-items: center;
    gap: 6px;
    margin-top: 12px;
}

/*  Tombol */
.dataTables_wrapper .dataTables_paginate .paginate_button {
    background: rgba(255,255,255,0.15) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.35) !important;
    border-radius: 8px !important;
    padding: 4px 12px !important;
    min-width: 36px;
    text-align: center;
}

/* HOVER */
.dataTables_wrapper .dataTables_paginate .paginate_button:hover {
    background: rgba(255,255,255,0.35) !important;
    color: white !important;
}

/* HALAMAN AKTIF */
.dataTables_wrapper .dataTables_paginate .paginate_button.current {
    background: rgba(0,123,255,0.9) !important;
    border-color: rgba(0,123,255,1) !important;
    color: white !important;
    font-weight: 600;
}

/* DISABLED (PREV / NEXT) */
.dataTables_wrapper .dataTables_paginate .paginate_button.disabled {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.15) !important;
    color: rgba(255,255,255,0.5) !important;
    cursor: not-allowed !important;
}

</style>
</head>

<body>

<header>Dashboard ABK Guru Provinsi Sumatera Utara</header>

<div class="container-fluid mt-3">
<div class="row">

<!-- SIDEBAR -->
<div class="col-lg-2">
<div class="glass">
<div class="menu" onclick="setMode('ALL')">Peta Geografis Sumatera Utara</div>
<div class="menu" onclick="setMode('Sesuai')">Jumlah Guru Sesuai</div>
<div class="menu" onclick="setMode('Kurang Guru')">Jumlah Guru Kurang</div>
<div class="menu" onclick="setMode('Lebih Guru')">Jumlah Guru Lebih</div>
<div class="menu" onclick="showAll()">Data Keseluruhan</div>
</div>
</div>

<!-- CONTENT -->
<div class="col-lg-10">
<div class="glass">

<!-- BACK BUTTON -->
<div id="navBack" style="display:none;margin-bottom:10px;">
<button class="btn btn-outline-light btn-sm" onclick="goBack()">⬅ Kembali</button>
</div>

<div id="mapBox"><div id="map"></div></div>

<!-- TABLE LEVEL 1 -->
<div class="table-container" id="tableKabBox">
<table id="tableKab" class="table w-100">
<thead>
<tr><th>NPSN</th><th>Nama Sekolah</th><th>Kab/Kota</th></tr>
</thead>
<tbody></tbody>
</table>
</div>

<!-- TABLE LEVEL 2 -->
<div class="table-container" id="tableDetailBox">
<table id="tableDetail" class="table w-100">
<thead>
<tr>
<th>NPSN</th><th>Nama Sekolah</th><th>Kab/Kota</th>
<th>Jabatan</th><th>Jml Guru</th><th>Kurang Guru</th><th>Keterangan</th>
</tr>
</thead>
<tbody></tbody>
</table>
</div>

</div>
</div>
</div>
</div>

<footer class="text-center mt-3">
© Bidang Pembinaan Ketenagaan Dinas Pendidikan Provinsi Sumatera Utara 2026
</footer>

<script>
const data = __DATA_JSON__;
let mode = "ALL";
let viewState = "MAP";

/* ===== MAP ===== */
const map = L.map('map').setView([2.5,99],7);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

/* ===== TABLE ===== */
const tableKab = $('#tableKab').DataTable({
    pageLength:15,
    columns:[
        {data:"NPSN"},
        {data:"Nama Sekolah"},
        {data:"Kab/Kota"}
    ]
});

const tableDetail = $('#tableDetail').DataTable({
    pageLength:20,
    columns:[
        {data:"NPSN"},
        {data:"Nama Sekolah"},
        {data:"Kab/Kota"},
        {data:"Jabatan"},
        {data:"Jml Guru"},
        {data:"Kurang Guru"},
        {data:"Keterangan"}
    ],
    createdRow:(row,d)=>{
        if(d["Keterangan"]==="Lebih Guru") $(row).addClass("lebh");
    }
});

/* ===== BACK ===== */
function goBack(){
    if(viewState==="DETAIL"){
        $("#tableDetailBox").hide();
        $("#tableKabBox").show();
        viewState="KAB";
    }else if(viewState==="KAB"){
        $("#tableKabBox").hide();
        $("#mapBox").show();
        $("#navBack").hide();
        viewState="MAP";
    }
}

/* klik sekolah */
$('#tableKab tbody').on('click','tr',function(){
    const d = tableKab.row(this).data();
    let f = data.filter(x=>x["NPSN"]===d["NPSN"]);
    if(mode!=="ALL") f=f.filter(x=>x["Keterangan"]===mode);

    tableDetail.clear().rows.add(f).draw();
    $("#tableKabBox").hide();
    $("#tableDetailBox").show();
    $("#navBack").show();
    viewState="DETAIL";
});

/* ===== ALERT ===== */
$('#tableDetail tbody').on('click','tr',function(){
    const d = tableDetail.row(this).data();
    if(d["Keterangan"]==="Lebih Guru"){
        Swal.fire("Peringatan",
        "Kuota Guru "+d["Jabatan"]+" pada "+d["Nama Sekolah"]+" sudah penuh",
        "warning");
    }
});

/* koordinat kab kota */
const kab = ["Kab. Asahan","Kab. Batu Bara","Kab. Dairi","Kab. Deli Serdang","Kab. Humbang Hasundutan",
"Kab. Karo","Kab. Labuhanbatu","Kab. Labuhanbatu Selatan","Kab. Labuhanbatu Utara",
"Kab. Langkat","Kab. Mandailing Natal","Kab. Nias","Kab. Nias Barat","Kab. Nias Selatan",
"Kab. Nias Utara","Kab. Padang Lawas","Kab. Padang Lawas utara","Kab. Pakpak Bharat",
"Kab. Samosir","Kab. Serdang Bedagai","Kab. Simalungun","Kab. Tapanuli Selatan",
"Kab. Tapanuli Tengah","Kab. Tapanuli Utara","Kab. Toba","Kota Binjai","Kota Gunungsitoli",
"Kota Medan","Kota Padang Sidempuan","Kota Pematangsiantar","Kota Sibolga",
"Kota Tebing Tinggi","Kota Tanjung Balai"];

const coords = [[2.8,99.6],[3.17,99.51],[2.74,98.31],[3.42,98.7],[2.26,98.5],[3.11,98.26],
[2.34,100.17],[1.93,100.09],[2.44,99.9],[3.72,98.27],[0.9,99.57],[1.07,97.72],
[1.01,97.49],[0.59,97.8],[1.33,97.35],[1.27,99.86],[1.48,99.93],[2.57,98.29],
[2.6,98.67],[3.36,99.05],[2.9,99.05],[1.53,99.27],[1.8,98.78],[2.02,99.11],
[2.35,99.1],[3.59,98.48],[1.28,97.61],[3.59,98.67],[1.37,99.27],[2.95,99.06],
[1.74,98.78],[3.32,99.15],[2.96,99.8]];

kab.forEach((k,i)=>{
    const icon = L.divIcon({
        html:`<svg width="24" height="24"><circle cx="12" cy="12" r="10" fill="hsl(${i*11},70%,50%)"/></svg>`,
        iconSize:[24,24]
    });

    L.marker(coords[i],{icon}).addTo(map).on("click",()=>{
        let f=data.filter(d=>d["Kab/Kota"]===k);
        if(mode!=="ALL") f=f.filter(d=>d["Keterangan"]===mode);

        const u=Object.values(Object.fromEntries(f.map(x=>[x.NPSN,x])));
        tableKab.clear().rows.add(u).draw();

        $("#mapBox").hide();
        $("#tableKabBox").show();
        $("#navBack").show();
        viewState="KAB";
    });
});

/* ===== MENU ===== */
function setMode(m){
    mode=m;
    viewState="MAP";
    $("#mapBox").show();
    $("#tableKabBox,#tableDetailBox,#navBack").hide();
}
function showAll(){
    viewState="DETAIL";
    $("#mapBox,#tableKabBox,#navBack").hide();
    $("#tableDetailBox").show();
    tableDetail.clear().rows.add(data).draw();
}
</script>

</body>
</html>
"""

html = html.replace("__DATA_JSON__", DATA_JSON)

with open("dashboard.html","w",encoding="utf-8") as f:
    f.write(html)

print("dashboard.html BERHASIL dibuat")
