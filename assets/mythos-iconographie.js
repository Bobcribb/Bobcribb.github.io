
/* MYTHOS — catalogue iconographique scientifique. Références Wikimedia Commons vérifiées le 2026-11-03. */
(function () {
"use strict";
const media={
achille:{
 file:"Achilles Hector Louvre G153.jpg",
 title:"Achille et le corps d’Hector",
 work:"Coupe attique à figures rouges, atelier de Macron, vers 490–480 av. J.-C. Musée du Louvre, G 153.",
 reading:"Iliade XXII–XXIV : la puissance du vainqueur se lit dans le traitement du corps de l’ennemi.",
 status:"Œuvre antique · photographie documentaire moderne · aucune génération IA.",
 credit:"Photographie : Marie-Lan Nguyen / Wikimedia Commons ; domaine public."
},
priam:{
 file:"Hektor ransom BM E75.jpg",
 title:"Priam réclame le corps d’Hector",
 work:"Kylix attique du Peintre de Briséis, vers 480 av. J.-C., British Museum, E 75 (1843,1103.54).",
 reading:"Iliade XXIV : la supplication fait émerger la compassion et la reconnaissance de la mortalité commune.",
 status:"Œuvre antique · photographie documentaire moderne · aucune génération IA.",
 credit:"Photographie : Marie-Lan Nguyen / Wikimedia Commons ; domaine public."
},
traine:{
 file:"Akhilleus Hektor Louvre CA601.jpg",
 title:"Achille traînant le corps d’Hector",
 work:"Lécythe attique à fond blanc, Peintre de Diosphos, vers 490 av. J.-C., musée du Louvre, CA 601.",
 reading:"Iliade XXII : l’outrage au corps et la limite de la vengeance héroïque.",
 status:"Œuvre antique · photographie documentaire moderne · aucune génération IA.",
 credit:"Photographie publiée sur Wikimedia Commons ; domaine public."
},
sirenes:{
 file:"Odysseus Sirens BM E440 n2.jpg",
 title:"Ulysse et les Sirènes",
 work:"Stamnos attique à figures rouges, Peintre de la Sirène, vers 480–470 av. J.-C., British Museum, E 440.",
 reading:"Odyssée XII : savoir, désir, maîtrise de soi et danger d’une expérience interdite.",
 status:"Œuvre antique · photographie documentaire moderne · aucune génération IA.",
 credit:"Photographie : Jastrow / Wikimedia Commons ; domaine public."
},
cyclope:{
 file:"Cyclops and Odysseus vase painting.svg",
 title:"Ulysse et l’aveuglement de Polyphème",
 work:"Dessin numérique contemporain (2014) dérivé d’une iconographie antique de vase à figures noires.",
 reading:"Odyssée IX : la mêtis délivre le héros, tandis que son besoin de gloire le met en péril.",
 status:"Reconstitution graphique moderne d’après l’Antiquité · non assimilable à un objet conservé · aucune génération IA.",
 credit:"Fichier Wikimedia Commons, auteur KDS444, marque de domaine public indiquée dans la notice."
},
pretendants:{
 file:"Odysseus slays the suitors of his wife Penelope (Skyphos pot).jpg",
 title:"Ulysse combattant les prétendants",
 work:"Illustration documentaire publiée d’après un skyphos attique à figures rouges, vers 440 av. J.-C. Reproduction en noir et blanc.",
 reading:"Odyssée XXII : l’autorité retrouvée a pour contrepartie une violence dont l’évaluation éthique demeure ouverte.",
 status:"Document de reproduction moderne d’un objet antique · aucune génération IA.",
 credit:"Source : planche issue de Furtwängler (1924), numérisée sur Wikimedia Commons ; licence CC0 (notice vérifiée)."
},
rhea:{
 file:"Rhea handing a swaddled stone to Cronus, Attic terracotta pelike, c. 460–450 BC, Met 06.1021.144.jpg",
 title:"Rhéa présente une pierre emmaillotée à Cronos",
 work:"Péliké attique attribuée au Peintre de Nausicaa, vers 460–450 av. J.-C., Metropolitan Museum, 06.1021.144.",
 reading:"Théogonie 453–506 : l’ordre nouveau doit d’abord échapper au mécanisme de la dévoration dynastique.",
 status:"Œuvre antique · photographie de musée · aucune génération IA.",
 credit:"Metropolitan Museum of Art / Wikimedia Commons ; licence CC0."
},
typhon:{
 file:"Zeus Typhon Staatliche Antikensammlungen 596.jpg",
 title:"Zeus contre Typhon",
 work:"Hydrie chalcidienne à figures noires, vers 550 av. J.-C., Staatliche Antikensammlungen de Munich, inv. 596.",
 reading:"Théogonie 820–880 : la dernière grande crise cosmique manifeste la conquête d’une souveraineté stable.",
 status:"Œuvre antique · photographie documentaire moderne · aucune génération IA.",
 credit:"Photographie : Bibi Saint-Pol / Wikimedia Commons ; domaine public."
},
enuma:{
 file:"Enuma Elish K.3473.jpg",
 title:"Fragment de l’Enūma eliš",
 work:"Tablette cunéiforme, bibliothèque d’Assurbanipal à Ninive, VIIe siècle av. J.-C., K.3473.",
 reading:"Comparaison prudente des récits de souveraineté : les analogies ne prouvent pas à elles seules une filiation directe.",
 status:"Artefact antique · photographie moderne · aucune génération IA.",
 credit:"Photographie : Zunkir, 2020 / Wikimedia Commons ; CC BY-SA 4.0.",
 license:"https://creativecommons.org/licenses/by-sa/4.0/"
},
hunefer:{
 file:"BD Hunefer.jpg",
 title:"Pesée du cœur du défunt Hounefer",
 work:"Papyrus du Livre des morts, Égypte, XIXe dynastie, British Museum, EA 9901.",
 reading:"Religions comparées : Maât, vérité, jugement et articulation du rituel à l’ordre cosmique.",
 status:"Document égyptien antique · reproduction photographique moderne · aucune génération IA.",
 credit:"British Museum / Wikimedia Commons ; reproduction de document dans le domaine public."
},
lascaux:{
 file:"Lascaux, replica 04.JPG",
 title:"Motifs pariétaux de Lascaux : réplique muséale",
 work:"Photographie de 2009 d’une réplique de Lascaux, musée Anthropos de Brno ; ce n’est pas une photographie de la grotte originale.",
 reading:"Origines du sacré : les images pariétales ne permettent pas, à elles seules, d’identifier un culte déterminé.",
 status:"Réplique contemporaine photographiée en musée · non assimilable à un vestige original · aucune génération IA.",
 credit:"Photographie : HTO / Wikimedia Commons ; domaine public."
},
masque:{
 file:"Greek terracotta theatre mask, Greece, 4th to 2nd century ac.JPG",
 title:"Masque de théâtre en terre cuite",
 work:"Objet grec, datation indiquée dans la notice : entre le IVe et le IIe siècle av. J.-C.",
 reading:"Théâtre : rôle, persona et représentation ; cet objet n’est pas une preuve directe des costumes des tragédies d’Eschyle.",
 status:"Objet antique · photographie moderne · aucune génération IA.",
 credit:"Photographie : Alf van Beem / Wikimedia Commons ; domaine public."
},
behistun:{file:"Darius (Behistun relief).jpg",title:"Darius Ier : relief de Behistun",work:"Relief achéménide, fin du VIe siècle av. J.-C.",reading:"Source visuelle de légitimation royale, à comparer au texte trilingue.",status:"Relief antique ; photo documentaire, non IA.",credit:"Leen van Dorp / Livius.org, Wikimedia Commons ; CC0."},
delphi:{file:"Delphi - Temple of Apollo.jpg",title:"Temple d’Apollon à Delphes",work:"Ruines du sanctuaire, Phocide ; photo de 2013.",reading:"Vestiges conservés, et non reconstitution du sanctuaire antique.",status:"Vestiges antiques ; photo moderne, non IA.",credit:"Ronny Siegel / Wikimedia Commons ; CC BY 3.0.",license:"https://creativecommons.org/licenses/by/3.0/"},
aphrodite:{file:"Venus de Milo Louvre Ma399 n6.jpg",title:"Aphrodite de Mélos",work:"Statue hellénistique vers 130–100 av. J.-C., musée du Louvre, Ma 399.",reading:"Document d’iconographie tardive, non une représentation directe du récit d’Hésiode.",status:"Sculpture antique ; photo non IA.",credit:"Jastrow / Wikimedia Commons ; domaine public."},
heracles:{file:"Herakles lion Louvre F33.jpg",title:"Héraclès et le lion de Némée",work:"Amphore attique à figures noires, v. 540 av. J.-C., Louvre F 33.",reading:"Réception figurée d’un travail héroïque.",status:"Vase antique ; photo non IA.",credit:"Wikimedia Commons ; voir notice de fichier pour le crédit et la licence."},
jason:{file:"Jason Pelias Louvre K127.jpg",title:"Jason apporte la Toison d’or à Pélias",work:"Cratère apulien à figures rouges, v. 340–330 av. J.-C., Louvre K 127.",reading:"Témoignage italiote sur les traditions argonautiques.",status:"Vase antique ; photo non IA.",credit:"Wikimedia Commons ; voir notice de fichier pour le crédit et la licence."},
cadmus:{file:"Kadmos dragon Louvre E707.jpg",title:"Cadmos et le serpent",work:"Amphore eubéenne à figures noires, v. 560–550 av. J.-C., Louvre E 707.",reading:"Image antique d’un motif du cycle thébain.",status:"Vase antique ; photo non IA.",credit:"Wikimedia Commons ; voir notice de fichier pour le crédit et la licence."},
};
const galleries={
"/corpus/civilisations/perse-iran-ancien-behistun.html":["behistun"],
"/corpus/mythologie-grecque/02-dieux-et-divinites/aphrodite-etude-integrale.html":["aphrodite"],
"/corpus/mythologie-grecque/archives/MYTHOS_bibliotheque_navigable.html":["achille","rhea","enuma"],
"/corpus/mythologie-grecque/archives/atlas-mythologique.html":["delphi"],
"/corpus/mythologie-grecque/archives/bibliotheque.html":["achille","sirenes"],
"/corpus/mythologie-grecque/archives/cultes-cites.html":["delphi","rhea"],
"/corpus/mythologie-grecque/archives/historiographie-v6.html":["hunefer","enuma"],
"/corpus/mythologie-grecque/archives/livre-argonautiques.html":["jason"],
"/corpus/mythologie-grecque/archives/livre-dieux.html":["typhon","rhea"],
"/corpus/mythologie-grecque/archives/livre-heracles.html":["heracles"],
"/corpus/mythologie-grecque/archives/livre-thebes.html":["cadmus"],
"/corpus/mythologie-grecque/archives/monographies.html":["achille","rhea"],
"/corpus/mythologie-grecque/archives/sources-methodes.html":["enuma","hunefer"],
"/reconstitutions-3d.html":["delphi","lascaux"],
"/sites/delphes.html":["delphi"],

"/index.html":["achille","sirenes","rhea"],
"/philosophie.html":["achille","sirenes","rhea"],
"/mythologie-grecque.html":["typhon","achille","sirenes"],
"/mythologie-comparee.html":["enuma","rhea","hunefer"],
"/grande-encyclopedie.html":["hunefer","enuma","lascaux"],
"/civilisations.html":["hunefer","enuma"],
"/theatre-grec.html":["masque","priam"],
"/origines-du-sacre.html":["lascaux","hunefer"],
"/sommaire-general.html":["priam","enuma","lascaux"]
};
const chapterGalleries={
"/corpus/mythologie-grecque/archives/livre-troie.html":[["iliade","achille"],["iliade","priam"],["apres","traine"]],
"/corpus/mythologie-grecque/archives/livre-odyssee.html":[["chant-9","cyclope"],["chant-12","sirenes"],["chant-22","pretendants"]],
"/corpus/mythologie-grecque/archives/livre-hesiode.html":[["cronos","rhea"],["typhon","typhon"]]
};
function elt(tag,cls,txt){
 const node=document.createElement(tag);
 if(cls)node.className=cls;
 if(txt!==undefined)node.textContent=txt;
 return node;
}
function fig(key){
 const d=media[key]; if(!d)return null;
 const f=elt("figure","mythos-figure");
 f.dataset.mythosFigure=key;
 const img=elt("img");
 img.src="https://commons.wikimedia.org/wiki/Special:FilePath/"+encodeURIComponent(d.file).replace(/%2F/g,"/")+"?width=1100";
 img.loading="lazy";img.decoding="async";img.alt=d.title+": "+d.work;
 const fallback=elt("p","mythos-fallback","Image indisponible depuis ce navigateur. La notice-source reste accessible ci-dessous.");
 img.addEventListener("error",function(){f.classList.add("mythos-media-unavailable");},{once:true});
 f.append(img,fallback);
 const cap=elt("figcaption");
 cap.append(elt("strong","",d.title));
 cap.append(elt("span","mythos-work",d.work));
 cap.append(elt("span","mythos-reading",d.reading));
 cap.append(elt("span","mythos-status",d.status));
 const credits=elt("span","mythos-credits",d.credit+" ");
 const a=elt("a","mythos-source","Voir la notice et les droits →");
 a.href="https://commons.wikimedia.org/wiki/File:"+encodeURIComponent(d.file.replace(/ /g,"_"));
 a.rel="noopener noreferrer";a.target="_blank";
 credits.append(a);
 if(d.license){const l=elt("a","mythos-license"," · Licence");l.href=d.license;l.target="_blank";l.rel="noopener noreferrer";credits.append(l);}
 cap.append(credits);f.append(cap);
 return f;
}
function run(){
 const path=location.pathname.replace(/\/+/g,"/").replace(/\/$/,"/index.html");
 if(document.querySelector("[data-mythos-illustrations-installed]"))return;
 const head=document.querySelector("main");
 if(!head)return;
 const gall=galleries[path];
 if(gall){
  const s=elt("section","mythos-icono-block");
  s.setAttribute("data-mythos-illustrations-installed","");
  s.setAttribute("aria-label","Repères iconographiques documentés");
  s.append(elt("h2","","Œuvres et documents iconographiques"));
  s.append(elt("p","mythos-icono-intro","Sélection commentée pour une lecture critique. Objets antiques, photographies et répliques modernes sont identifiés séparément ; les notices de provenance et de droits sont consultables sous chaque image."));
  const grid=elt("div","mythos-icono-grid");
  gall.forEach(k=>{const item=fig(k);if(item)grid.append(item);});
  s.append(grid);
  // Le bloc est ajouté dans le flux éditorial sans remplacer aucun texte.
  const toc=head.querySelector(".book-toc"); const t=head.querySelector(".page-title"); if(toc)toc.insertAdjacentElement("afterend",s); else if(t)t.insertAdjacentElement("afterend",s); else head.insertBefore(s,head.firstElementChild);
 }
 const places=chapterGalleries[path]||[];
 places.forEach(pair=>{
  const sec=document.getElementById(pair[0]);
  if(!sec||sec.querySelector('[data-mythos-figure="'+pair[1]+'"]'))return;
  const item=fig(pair[1]);if(!item)return;
  const firstP=sec.querySelector("p");
  const h=sec.querySelector("h2");
  if(firstP) firstP.insertAdjacentElement("afterend",item);
  else if(h)h.insertAdjacentElement("afterend",item);
  else sec.append(item);
  sec.setAttribute("data-mythos-illustrations-installed","");
 });
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",run,{once:true});else run();
})();
