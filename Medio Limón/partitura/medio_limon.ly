\version "2.24.0"
\header {
  title = "Medio Limón"
  subtitle = "tropipop  ·  track 3  ·  antes titulada Patio de los Naranjos"
  composer = "Emmanuel Ángel Blue Norambuena Sepúlveda"
  copyright = "© Emmanuel Ángel Blue Norambuena Sepúlveda. Todos los derechos reservados."
  tagline = ""
}

\paper {
  #(set-paper-size "a4")
  top-margin = 12\mm
  bottom-margin = 12\mm
  ragged-bottom = ##t
  ragged-last-bottom = ##t
}

theChords = \chordmode {
  f1 bes1 d1:m c1 f1 c1 d1:m a1:7 bes1 f1 g1:m c1 g1:m c1 g1:m c1:7 f1 d1:m bes1 bes1:m f1 c1 bes1 c1 f1 d1:m bes1 bes1:m f1 c1 bes1 c1 f1 c1 d1:m a1:7 bes1 f1 g1:m c1 f1 c1 d1:m a1:7 bes1 f1 g1:m c1 g1:m c1 g1:m c1:7 f1 d1:m bes1 bes1:m f1 c1 bes1 c1 f1 d1:m bes1 bes1:m f1 c1 bes1 c1 f1 d1:m bes1 bes1:m f1 c1 bes1 c1
}

theMelody = {
  \key f \major
  \time 4/4
  \tempo 4 = 106
  \mark \markup \column { \box \bold "Intro" \italic \fontsize #-2 "acordeón presenta el hook" }  <f' a' c''>2 <f' a' c''>4. <f' a' c''>8 <f' bes' d''>2 <f' bes' d''>4. <f' bes' d''>8 <d' f' a'>2 <d' f' a'>4. <d' f' a'>8 <e' g' c''>2 <e' g' c''>4. <e' g' c''>8 \mark \markup \column { \box \bold "Verse" \italic \fontsize #-2 "despojado: guitarra, bajo y percusión" }  <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <e' a' des''>8 <e' a' des''>8 \once \override NoteHead.style = #'cross <e' a' des''>8 <e' a' des''>8 <e' a' des''>8 <e' a' des''>8 \once \override NoteHead.style = #'cross <e' a' des''>8 <e' a' des''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 \mark \markup \column { \box \bold "Pre Chorus" \italic \fontsize #-2 "acordeón ascendente" }  <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <e' g' bes'>8 <e' g' bes'>8 \once \override NoteHead.style = #'cross <e' g' bes'>8 <e' g' bes'>8 <e' g' bes'>8 <e' g' bes'>8 \once \override NoteHead.style = #'cross <e' g' bes'>8 <e' g' bes'>8 \mark \markup \column { \box \bold "Chorus" \italic \fontsize #-2 "entra todo" }  <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' des''>8 <f' bes' des''>8 \once \override NoteHead.style = #'cross <f' bes' des''>8 <f' bes' des''>8 <f' bes' des''>8 <f' bes' des''>8 \once \override NoteHead.style = #'cross <f' bes' des''>8 <f' bes' des''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 \mark \markup \column { \box \bold "Chorus" \italic \fontsize #-2 "entra todo" }  <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' des''>8 <f' bes' des''>8 \once \override NoteHead.style = #'cross <f' bes' des''>8 <f' bes' des''>8 <f' bes' des''>8 <f' bes' des''>8 \once \override NoteHead.style = #'cross <f' bes' des''>8 <f' bes' des''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 \mark \markup \column { \box \bold "Verse" \italic \fontsize #-2 "despojado: guitarra, bajo y percusión" }  <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <e' a' des''>8 <e' a' des''>8 \once \override NoteHead.style = #'cross <e' a' des''>8 <e' a' des''>8 <e' a' des''>8 <e' a' des''>8 \once \override NoteHead.style = #'cross <e' a' des''>8 <e' a' des''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <e' a' des''>8 <e' a' des''>8 \once \override NoteHead.style = #'cross <e' a' des''>8 <e' a' des''>8 <e' a' des''>8 <e' a' des''>8 \once \override NoteHead.style = #'cross <e' a' des''>8 <e' a' des''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 \mark \markup \column { \box \bold "Pre Chorus" \italic \fontsize #-2 "acordeón ascendente" }  <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 <d' g' bes'>8 \once \override NoteHead.style = #'cross <d' g' bes'>8 <d' g' bes'>8 <e' g' bes'>8 <e' g' bes'>8 \once \override NoteHead.style = #'cross <e' g' bes'>8 <e' g' bes'>8 <e' g' bes'>8 <e' g' bes'>8 \once \override NoteHead.style = #'cross <e' g' bes'>8 <e' g' bes'>8 \mark \markup \column { \box \bold "Chorus" \italic \fontsize #-2 "entra todo" }  <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' des''>8 <f' bes' des''>8 \once \override NoteHead.style = #'cross <f' bes' des''>8 <f' bes' des''>8 <f' bes' des''>8 <f' bes' des''>8 \once \override NoteHead.style = #'cross <f' bes' des''>8 <f' bes' des''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 \mark \markup \column { \box \bold "Outro" \italic \fontsize #-2 "coro x2 con fade-out" }  <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' des''>8 <f' bes' des''>8 \once \override NoteHead.style = #'cross <f' bes' des''>8 <f' bes' des''>8 <f' bes' des''>8 <f' bes' des''>8 \once \override NoteHead.style = #'cross <f' bes' des''>8 <f' bes' des''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 \mark \markup \column { \box \bold "Outro" \italic \fontsize #-2 "coro x2 con fade-out" }  <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 <d' f' a'>8 \once \override NoteHead.style = #'cross <d' f' a'>8 <d' f' a'>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' des''>8 <f' bes' des''>8 \once \override NoteHead.style = #'cross <f' bes' des''>8 <f' bes' des''>8 <f' bes' des''>8 <f' bes' des''>8 \once \override NoteHead.style = #'cross <f' bes' des''>8 <f' bes' des''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 <f' a' c''>8 \once \override NoteHead.style = #'cross <f' a' c''>8 <f' a' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 <f' bes' d''>8 \once \override NoteHead.style = #'cross <f' bes' d''>8 <f' bes' d''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 <e' g' c''>8 \once \override NoteHead.style = #'cross <e' g' c''>8 <e' g' c''>8
  \bar "|."
}

\score {
  <<
    \new ChordNames { \theChords }
    \new Staff = "main" \with {
      instrumentName = \markup { \fontsize #-2.5 "Guitarra" }
    } <<
      \new Voice = "mel" { \theMelody }
    >>
  >>
  \layout {
    \context { \Score
      \override RehearsalMark.self-alignment-X = #LEFT
      \override RehearsalMark.padding = #3.0
      barNumberVisibility = #(every-nth-bar-number-visible 4)
      \override BarNumber.break-visibility = #'#(#f #t #t)
    }
    \context { \Staff
      \override TextScript.padding = #1.4
      \override TextScript.outside-staff-priority = #250
    }
    \context { \ChordNames
      \override ChordName.padding = #0.8
    }
  }
}

\pageBreak
\markup \column {
  \line { \bold \fontsize #2 "El rasgueo del paseo" }
  \vspace #0.4
  \wordwrap-string #"Esto es lo que hace que suene a paseo y no a cumbia. La cabeza en cruz es el apagado: la mano derecha golpea las cuerdas apagadas contra el diapasón y suena percutido, no afinado. Donde la partitura mostraría un silencio, se golpea. El bajo anticipa la raíz del acorde siguiente en el 'y' del tiempo 4, ligada sobre la línea divisoria: esa síncopa es la que tira hacia adelante. La guacharaca raspa semicorcheas sin parar, unas siete por segundo."
  \vspace #0.6
}
\score {
  \new StaffGroup <<
    \new RhythmicStaff \with { instrumentName = \markup { \fontsize #-3 "Guit." } } { \improvisationOn b'8 b'8 \once \override NoteHead.style = #'cross b'8 b'8 b'8 b'8 \once \override NoteHead.style = #'cross b'8 b'8 }
    \new Staff \with { instrumentName = \markup { \fontsize #-3 "Bajo" } } { \clef bass f,4. f8 c4. bes,8 }
    \new DrumStaff \with { instrumentName = \markup { \fontsize #-3 "Caja/guach." } } \drummode { <bd cabasa>16 cabasa16 cabasa16 cabasa16 <bd sn cabasa>16 cabasa16 cabasa16 cabasa16 <bd cabasa>16 cabasa16 cabasa16 cabasa16 <bd sn cabasa>16 cabasa16 cabasa16 cabasa16 }
  >>
  \layout {
    indent = 2.2\cm
    \context { \Score
      \override StaffGrouper.staff-staff-spacing = #'((basic-distance . 6) (minimum-distance . 5) (padding . 0.5))
      \override SystemStartBar.collapse-height = #1
    }
  }
}

\pageBreak
\markup \column {
  \line { \bold \fontsize #1 "Notas" }
  \vspace #0.4
    \line { \bold "1." \wordwrap-string #"Aire: paseo vallenato, en cuatro tiempos. Ojo que la frase corriente 'el vallenato va en 2/4' es falsa: el son va en 2/4, pero el merengue y la puya van en 6/8. El paseo se escribe en 2/4 y se cuadra en cuatro." }
    \line { \bold "2." \wordwrap-string #"El rasgueo no toca acordes sostenidos: donde la partitura muestra silencio se golpean las cuerdas apagadas con la mano derecha. Ese golpe percutido en 2 y 4 es el motor del ritmo, sin él la canción arrastra a cualquier tempo." }
    \line { \bold "3." \wordwrap-string #"Bbm en el coro es el cuarto grado menor prestado: Bb - Bbm - F es IV - iv - I. Ese giro agridulce sale de las cifras de las referencias, no es invención." }
    \line { \bold "4." \wordwrap-string #"A7 en el compás 4 del verso es V7/vi, pero NO resuelve a Dm: el Dm ya pasó en el compás 3 y el A7 va a Bb. Es una resolución deceptiva a IV, o si se prefiere leerlo local, un acorde cromático de paso con el bajo subiendo La - Si bemol." }
    \line { \bold "5." \wordwrap-string #"El bajo anticipa la raíz del acorde siguiente en el 'y' del tiempo 4, ligada sobre la línea divisoria. Esa síncopa es la que tira hacia adelante. No está cifrada en esta hoja: va escrita en el generador de audio." }
    \line { \bold "6." \wordwrap-string #"Tempo: 105.5. Viene de un conteo del autor sobre la referencia, 22 pulsos en 12.49s. Ojo que 22 pulsos son 21 intervalos, o sea 100.9 por minuto; según cómo se contó, el tempo real está entre 101 y 106 y queda por confirmar." }
    \line { \bold "7." \wordwrap-string #"La línea vocal se canta sobre esta base y todavía no está transcrita." }
    \line { \bold "8." \wordwrap-string #"La canción termina en C, o sea en dominante, con fade-out. Es deliberado: no resuelve." }
}

\pageBreak
\markup \vspace #0.5
\markup { \bold \fontsize #3 "Letra" }
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Intro" }
  \vspace #0.3
      \line { \wordwrap-string #"No se preocupe jefecito yo toi por llegar" }
      \line { \wordwrap-string #"No se preocupen mis pollitos yo toi por llegar" }
      \line { \wordwrap-string #"No se preocupen mis alumnos yo toi por llegar" }
      \line { \wordwrap-string #"No se preocupe mi amorcito yo toi por llegar" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Pre-Chorus" }
  \vspace #0.3
      \line { \wordwrap-string #"Llego, llego a ti!" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Coro" }
  \vspace #0.3
      \line { \wordwrap-string #"Que yo llego por ti" }
      \line { \wordwrap-string #"Que yo bailo por ti" }
      \line { \wordwrap-string #"Que yo gozo por ti" }
      \line { \wordwrap-string #"Que yo vivo por ti" }
      \line { \wordwrap-string #"Que yo canto por ti" }
      \line { \wordwrap-string #"Que yo llego por ti" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Verse 2" }
  \vspace #0.3
      \line { \wordwrap-string #"Todas las historias que contaban" }
      \line { \wordwrap-string #"De la media naranja, medio limón" }
      \line { \wordwrap-string #"Y me preguntaba por qué no llegaban" }
      \line { \wordwrap-string #"Miraba el patio, los naranjos en flor" }
      \line { \wordwrap-string #"Contando los días, contando el reloj" }
      \line { \wordwrap-string #"Hasta que entendí: el que faltaba era yo" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Pre-Chorus" }
  \vspace #0.3
      \line { \wordwrap-string #"Llego, llego a ti!" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Coro (bis)" }
  \vspace #0.3
      \line { \wordwrap-string #"Que yo llego por ti" }
      \line { \wordwrap-string #"Que yo bailo por ti" }
      \line { \wordwrap-string #"Que yo gozo por ti" }
      \line { \wordwrap-string #"Que yo vivo por ti" }
      \line { \wordwrap-string #"Que yo canto por ti" }
      \line { \wordwrap-string #"Que yo llego por ti" }
}

