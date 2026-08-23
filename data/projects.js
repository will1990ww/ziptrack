/* =====================================================================
   projects.js  —  EDIT THIS FILE TO MANAGE YOUR PROJECT GALLERY
   ---------------------------------------------------------------------
   Three categories: decking, blinds (zip blinds), grilles.
   Each section = 6 slots = 5 photos + 1 video.
   Item types:
     { type:"image", src:"assets/images/projects/<cat>/<file>.webp", title:"…", meta:"…" }
     { type:"video", src:"assets/videos/projects/<cat>/<file>.mp4",
       poster:"assets/images/projects/<cat>/<file>.webp", title:"…", meta:"…" }
     { type:"empty" }   // placeholder "Add photo/video" box

   ADD MEDIA (no coding):
     1. Drop a photo (.webp/.jpg) into assets/images/projects/<category>/
        or a video (.mp4) into assets/videos/projects/<category>/
     2. Edit the matching entry below (filename + title + meta).
     3. Save, refresh the Projects page.
   ===================================================================== */
window.PROJECTS = {
  decking: [
    { type:"image", src:"assets/images/projects/decking/deck-01.webp", title:"Condo balcony \u2014 capped WPC", meta:"\u2248 9 m\u00b2 \u00b7 aluminium subframe \u00b7 2 days" },
    { type:"image", src:"assets/images/projects/decking/deck-02.webp", title:"Marble-look tiles & stone", meta:"Cool underfoot \u00b7 wet-area ready" },
    { type:"image", src:"assets/images/projects/decking/deck-03.webp", title:"Skyline balcony deck", meta:"Indoor\u2013outdoor flow" },
    { type:"image", src:"assets/images/projects/decking/deck-04.webp", title:"Chengal hardwood patio", meta:"Landed \u00b7 natural grain" },
    { type:"image", src:"assets/images/projects/decking/deck-05.webp", title:"Edge & drainage detail", meta:"Corrosion-resistant fixings" },
    { type:"video", src:"assets/videos/projects/decking/deck-demo.mp4", poster:"assets/images/projects/decking/deck-01.webp", title:"Walkthrough (demo)", meta:"Tap \u25b6 \u00b7 replace with your clip" }
  ],
  blinds: [
    { type:"image", src:"assets/images/projects/blinds/blind-01.webp", title:"Motorised zip blind enclosure", meta:"2 panels \u00b7 solar mesh" },
    { type:"image", src:"assets/images/projects/blinds/blind-02.webp", title:"Condo balcony screen", meta:"Heat & glare control" },
    { type:"image", src:"assets/images/projects/blinds/blind-03.webp", title:"Dusk privacy screen", meta:"5% openness fabric" },
    { type:"image", src:"assets/images/projects/blinds/blind-04.webp", title:"Daytime shade", meta:"Wind-driven rain reduced" },
    { type:"image", src:"assets/images/projects/blinds/blind-05.webp", title:"Corner balcony", meta:"Multi-panel layout" },
    { type:"video", src:"assets/videos/projects/blinds/blind-demo.mp4", poster:"assets/images/projects/blinds/blind-01.webp", title:"Zip blind in action (demo)", meta:"Tap \u25b6 \u00b7 replace with your clip" }
  ],
  grilles: [
    { type:"image", src:"assets/images/projects/grilles/grille-01.webp", title:"Vertical invisible grille", meta:"Balcony \u00b7 city view" },
    { type:"image", src:"assets/images/projects/grilles/grille-02.webp", title:"Nylon-coated cables", meta:"Value option \u00b7 3-yr" },
    { type:"image", src:"assets/images/projects/grilles/grille-03.webp", title:"PTFE / Teflon cables", meta:"High floor \u00b7 5-yr" },
    { type:"image", src:"assets/images/projects/grilles/grille-04.webp", title:"Nano all-weather", meta:"Coastal \u00b7 10-yr" },
    { type:"image", src:"assets/images/projects/grilles/grille-05.webp", title:"Window grille", meta:"Unobstructed view" },
    { type:"video", src:"assets/videos/projects/grilles/grille-demo.mp4", poster:"assets/images/projects/grilles/grille-01.webp", title:"Grille tour (demo)", meta:"Tap \u25b6 \u00b7 replace with your clip" }
  ]
};
