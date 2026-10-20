\version "2.24.0"
\header {
  title = "Rescue Us"
  subtitle = "track 2  ·  antes titulada 36@24"
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
  d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1 d1:m g1 c1 f1
}

theMelody = {
  \key c \major
  \time 4/4
  \tempo 4 = 120
  \mark \markup \column { \box \bold "Intro" \italic \fontsize #-2 "sirena de ambulancia antes del primer compás" }  f'1 b'1 e'1 a'1 \mark \markup \column { \box \bold "Verse" \italic \fontsize #-2 "despojado, la voz manda" }  f'1 b'1 e'1 a'1 f'1 b'1 e'1 a'1 \mark \markup \column { \box \bold "Pre Chorus" \italic \fontsize #-2 "construye" }  f'1 b'1 e'1 a'1 \mark \markup \column { \box \bold "Chorus" \italic \fontsize #-2 "hook completo" }  f'1 b'1 e'1 a'1 f'1 b'1 e'1 a'1 \mark \markup \column { \box \bold "Verse" \italic \fontsize #-2 "despojado, la voz manda" }  f'1 b'1 e'1 a'1 f'1 b'1 e'1 a'1 \mark \markup \column { \box \bold "Chorus" \italic \fontsize #-2 "hook completo" }  f'1 b'1 e'1 a'1 f'1 b'1 e'1 a'1 \mark \markup \column { \box \bold "Bridge" \italic \fontsize #-2 "entra el cello" }  f'1 b'1 e'1 a'1 f'1 b'1 e'1 a'1 \mark \markup \column { \box \bold "Chorus Final" \italic \fontsize #-2 "versión más grande, sirena al cerrar" }  f'1 b'1 e'1 a'1 f'1 b'1 e'1 a'1 f'1 b'1 e'1 a'1
  \bar "|."
}

\score {
  <<
    \new ChordNames { \theChords }
    \new Staff = "main" \with {
      instrumentName = \markup { \fontsize #-2.5 "Melodía" }
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

\markup \vspace #1.6
\markup \column {
  \line { \bold \fontsize #1 "Motivo: cita de 'Dame Luz' (Nicole)" }
  \vspace #0.4
  \wordwrap-string #"Aparece de forma espontánea en coros y puente, en guitarra aguda. Cinco tiempos, cruza la línea divisoria, por eso va aparte y sin indicación de compás. ATENCIÓN: es una cita de una obra ajena. No forma parte de lo que se registra como propio."
  \vspace #0.4
}
\score {
  \new Staff { \key c \major \cadenzaOn a'4 a'8 g'8 f'4 a'8 b'8 c''4 \bar "|." }
  \layout { }
}

\pageBreak
\markup \column {
  \line { \bold \fontsize #1 "Notas" }
  \vspace #0.4
    \line { \bold "1." \wordwrap-string #"La melodía escrita es la Gen Alpha Melody: grados 4-7-3-6 de la escala, en Do mayor F-B-E-A. Cada nota pilar es la TERCERA de su acorde. Contorno real: sube un tritono, baja una quinta, sube una cuarta." }
    \line { \bold "2." \wordwrap-string #"Esta melodía está escrita en redondas porque así la sintetiza el generador: es un pedal armónico, no el gancho rítmico definitivo. Cuando exista la línea vocal cantada habrá que transcribirla y reemplazar estas redondas." }
    \line { \bold "3." \wordwrap-string #"Armonía Dm-G-C-F: es un ciclo completo de quintas descendentes, ii-V-I-IV en Do mayor. Hay una V-I auténtica (G a C) en cada vuelta." }
    \line { \bold "4." \wordwrap-string #"Pero la pieza nunca cadencia en el tónico: empieza en Dm, termina en F, y las ocho secciones entran en Dm. La armadura de Do mayor describe el contenido; el énfasis está en Re. Es deliberado, y es lo que produce la sensación de bucle sin descanso." }
    \line { \bold "5." \wordwrap-string #"Las secciones se distinguen por instrumentación y densidad, no por cambio armónico." }
    \line { \bold "6." \wordwrap-string #"El generador mide las secciones en segundos porque sintetiza audio. 2.0s por acorde equivale a un compás de 4/4 a 120." }
    \line { \bold "7." \wordwrap-string #"La línea vocal se canta sobre esta base y todavía no está transcrita. La letra va al final de esta partitura." }
}

\pageBreak
\markup \vspace #0.5
\markup { \bold \fontsize #3 "Letra" }
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Verse 1" }
  \vspace #0.3
      \line { \wordwrap-string #"Bright, clear eyes... no fear in them" }
      \line { \wordwrap-string #"Light brown hair, drifts up to me" }
      \line { \wordwrap-string #"A voice that's calm, a steady hand" }
      \line { \wordwrap-string #"A smile that doesn't lie at all" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Verse 2" }
  \vspace #0.3
      \line { \wordwrap-string #"Funny, but not trying hard" }
      \line { \wordwrap-string #"Smart enough to win the fight" }
      \line { \wordwrap-string #"Kind to strangers, kind to me" }
      \line { \wordwrap-string #"Ambitious, but still has time" }
}
\markup \column {
  \vspace #0.8
  \line { \bold \fontsize #1 "Chorus" }
  \vspace #0.3
      \line { \wordwrap-string #"You'll rescue me" }
      \line { \wordwrap-string #"I'll rescue you" }
      \line { \wordwrap-string #"Please, dear God" }
      \line { \wordwrap-string #"Rescue us all" }
}

