\version "2.24.0"
\header {
  title = "Kicking Stones"
  subtitle = "track 1  ·  apertura del álbum"
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
  a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1 g1 e1:m a1:m f1
}

theMelody = {
  \key a \minor
  \time 4/4
  \tempo 4 = 146
  \mark \markup \column { \box \bold "Intro" \italic \fontsize #-2 "solo pad" } \improvisationOn b'1 \repeat percent 3 { b'1 } \improvisationOff \mark \markup \column { \box \bold "Verso 1" \italic \fontsize #-2 "voz y bajo" }  r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. \mark \markup \column { \box \bold "Verso 2" \italic \fontsize #-2 "voz y bajo" }  r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. \mark \markup \column { \box \bold "Pre-Coro" \italic \fontsize #-2 "entra batería y guitarra" }  r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. \mark \markup \column { \box \bold "Instrumental" \italic \fontsize #-2 "sin voz" }  r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. \mark \markup \column { \box \bold "Coro" \italic \fontsize #-2 "todo" }  e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. \mark \markup \column { \box \bold "Puente" \italic \fontsize #-2 "hablado, batería mínima" }  r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. \mark \markup \column { \box \bold "Coro 2" \italic \fontsize #-2 "todo" }  e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. \mark \markup \column { \box \bold "Post-Coro" \italic \fontsize #-2 "respuesta doblada" }  e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. \mark \markup \column { \box \bold "Instrumental" \italic \fontsize #-2 "sin voz" }  r1 e'8 d'8 c'8 a4 r4. r1 e'8 d'8 c'8 a4 r4. \mark \markup \column { \box \bold "Outro" \italic \fontsize #-2 "entra la guitarra solista" }  e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4. e'8 d'8 c'8 a4 r4.
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
  \line { \bold \fontsize #2 "El groove" }
  \vspace #0.4
  \wordwrap-string #"Medido del MIDI de la versión masterizada, no reconstruido de oído. La guitarra no rasguea: toca un motivo melódico descendente, Mi-Re-Do-La, en la primera mitad del compás. Ese hueco en la segunda mitad es lo que deja respirar al tema a 146. En versos y pre-coro suena un compás de por medio; en coros y outro, todos. El bajo marca 1 y 3."
  \vspace #0.6
}
\score {
  \new StaffGroup <<
    \new RhythmicStaff \with { instrumentName = \markup { \fontsize #-3 "Guit." } } { \improvisationOn b'8 b'8 b'8 b'2 r8 }
    \new Staff \with { instrumentName = \markup { \fontsize #-3 "Bajo" } } { \clef bass a,,2 a,,2 }
    \new DrumStaff \with { instrumentName = \markup { \fontsize #-3 "Batería" } } \drummode { <bd hh>8 hh8 <sn hh>8 hh8 <bd hh>8 hh8 <sn hh>8 hh8 }
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
    \line { \bold "1." \wordwrap-string #"La forma de esta hoja está deducida del máster, cruzando los tiempos de entrada de cada línea cantada contra los compases. No sale de los nombres de sección del generador, que registran la intención del arreglo y no lo que terminó grabándose." }
    \line { \bold "2." \wordwrap-string #"En concreto: las partes que el generador llama 'rapfaster' llevan versos cantados normales, nunca se grabó rap ahí; la que llama 'chorus1' no tiene voz y acá va como Instrumental; y la que llama 'verse1' es el coro." }
    \line { \bold "3." \wordwrap-string #"Progresión i - VI - VII - v en La menor (Am - F - G - Em), un acorde por compás, sin una sola alteración accidental en toda la obra. Las secciones se distinguen por instrumentación y densidad, no por armonía." }
    \line { \bold "4." \wordwrap-string #"Tempo único de 146 para toda la canción. 146 no es un número elegido sino medido: la maqueta vocal cubre 8 compases (32 tiempos) en 13.15s." }
    \line { \bold "5." \wordwrap-string #"El outro lleva guitarra solista sobre la escala de La menor natural. Es una parte improvisada sobre la armonía, no una melodía fija, por eso no va escrita." }
    \line { \bold "6." \wordwrap-string #"La línea vocal todavía no está transcrita; la letra va al final de esta hoja con los tiempos de entrada del máster. Existe además una versión en español de la letra, en el archivo lyrics_es." }
}

\pageBreak
\markup \vspace #0.5
\markup { \bold \fontsize #3 "Letra" }
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Verso 1" }
  \vspace #0.3
      \line { \wordwrap-string #"Singers taunting on pulpit mic" }
      \line { \wordwrap-string #"keep working the show" }
      \line { \wordwrap-string #"While 2nd floor's assessors" }
      \line { \wordwrap-string #"continue the mega-reform" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Verso 2" }
  \vspace #0.3
      \line { \wordwrap-string #"In the shadow of the concrete giants" }
      \line { \wordwrap-string #"where shock ink is warm" }
      \line { \wordwrap-string #"Like people's blood running" }
      \line { \wordwrap-string #"down where only bikes should run" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Pre-Coro" }
  \vspace #0.3
      \line { \wordwrap-string #"Looking at winged solutions" }
      \line { \wordwrap-string #"Watching the model decay" }
      \line { \wordwrap-string #"From 'The Brick' to the rubble" }
      \line { \wordwrap-string #"Just improvising the ruins today" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Coro" }
  \vspace #0.3
      \line { \wordwrap-string #"Winged solutions for a failing frame" }
      \line { \wordwrap-string #"The architect would die of shame" }
      \line { \wordwrap-string #"We have no place in the design" }
      \line { \wordwrap-string #"Just kicking stones against grey walls" }
      \line { \wordwrap-string #"We're just wasting time" }
      \line { \wordwrap-string #"Kicking stones against grey walls..." }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Puente" }
  \vspace #0.3
      \line { \wordwrap-string #"'Those who have power make choises that create poverty'" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Coro" }
  \vspace #0.3
      \line { \wordwrap-string #"Winged solutions for a failing frame" }
      \line { \wordwrap-string #"The architect would die of shame" }
      \line { \wordwrap-string #"We have no place in the design" }
      \line { \wordwrap-string #"Just kicking stones against grey walls" }
      \line { \wordwrap-string #"We're just wasting time" }
      \line { \wordwrap-string #"Kicking stones against grey walls..." }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Post-Coro" }
  \vspace #0.3
      \line { \wordwrap-string #"We're just wasting time" }
      \line { \wordwrap-string #"Kicking stones against grey walls..." }
      \line { \wordwrap-string #"(Kicking stones against grey walls...)" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Outro" }
  \vspace #0.3
      \line { \wordwrap-string #"The masterplan" }
      \line { \wordwrap-string #"The mega-reform" }
      \line { \wordwrap-string #"The architect would die of shame" }
      \line { \wordwrap-string #"Just kicking stones" }
      \line { \wordwrap-string #"Just hitting rocks" }
      \line { \wordwrap-string #"Against grey walls" }
      \line { \wordwrap-string #"They will never stop" }
}

