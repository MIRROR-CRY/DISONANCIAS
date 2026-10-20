\version "2.24.0"
\header {
  title = "Sin titulo"
  subtitle = "indie-folk  ·  track 4"
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
  c1 f1 c1 a1:m c1 f1 c1 a1:m c1 f1 c1 a1:m f1 f1 g1 g1 a1:m g1 c1 f1 a1:m g1 c1 f1 c1 f1 c1 a1:m c1 f1 c1 a1:m f1 f1 g1 g1 a1:m g1 c1 f1 a1:m g1 c1 f1 f1 g1 a1:m g1 a1:m g1 c1 f1 a1:m g1 c1 f1 c1 f1 c1 a1:m
}

theMelody = {
  \key c \major
  \time 4/4
  \tempo 4 = 79
  \mark \markup \column { \box \bold "Intro" \italic \fontsize #-2 "solo guitarra acústica" }  <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 \mark \markup \column { \box \bold "Verse" \italic \fontsize #-2 "despojado" }  <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 \mark \markup \column { \box \bold "Pre Chorus" \italic \fontsize #-2 "entran palmas" }  <f, a, c f a>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <g, b, d g b>8 <g, b, d g b>4 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>4 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 \mark \markup \column { \box \bold "Chorus" \italic \fontsize #-2 "entra el bajo, cello y pisadas" }  <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 \mark \markup \column { \box \bold "Verse" \italic \fontsize #-2 "despojado" }  <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>4 <c e g c' e'>8 <c e g c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 \mark \markup \column { \box \bold "Pre Chorus" \italic \fontsize #-2 "entran palmas" }  <f, a, c f a>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <g, b, d g b>8 <g, b, d g b>4 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>4 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 \mark \markup \column { \box \bold "Chorus" \italic \fontsize #-2 "entra el bajo, cello y pisadas" }  <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 \mark \markup \column { \box \bold "Bridge" \italic \fontsize #-2 "punto más bajo del arco" }  <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>4 <f, a, c f a>8 <f, a, c f a>8 <g, b, d g b>4 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>4 <g, b, d g b>8 <g, b, d g b>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>4 <a, e a c' e'>8 <a, e a c' e'>8 <g, b, d g b>4 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>4 <g, b, d g b>8 <g, b, d g b>8 \mark \markup \column { \box \bold "Chorus Final" \italic \fontsize #-2 "todo: 3 pisadas + 4 palmas + arpegio" }  <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <g, b, d g b>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 \mark \markup \column { \box \bold "Outro" \italic \fontsize #-2 "fade lineal de 4 compases" }  <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <f, a, c f a>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <c e g c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8 <a, e a c' e'>8
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
  \line { \bold \fontsize #2 "El groove: pisadas y palmas" }
  \vspace #0.4
  \wordwrap-string #"El estilo no está en la guitarra, está acá. Pisadas en 1 y 3, palmas en 2 y 4, y en las secciones más llenas las palmas empiezan a rellenar el contratiempo. No es una pista copiada más fuerte: son tres capas de pisadas y cuatro de palmas, cada una con su desfase propio de unos 10ms y su lugar en el estéreo. La dispersión entre capas ES el efecto."
  \vspace #0.6
}
\score {
  \new StaffGroup <<
    \new RhythmicStaff \with { instrumentName = \markup { \fontsize #-3 "Guit." } } { \improvisationOn b'8 b'8 b'8 b'8 b'8 b'8 b'8 b'8 }
    \new DrumStaff \with { instrumentName = \markup { \fontsize #-3 "Pisadas/palmas" } } \drummode { bd4 hc4 bd4 hc8 hc8 }
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
    \line { \bold "1." \wordwrap-string #"Sin melodía vocal ni letra todavía: la canción está en etapa de base. Todas las secciones van como cifrado rítmico." }
    \line { \bold "2." \wordwrap-string #"Acordes en POSICIÓN ABIERTA, sin cejilla. Referencia: 'Ho Hey' de The Lumineers (79 BPM, Do mayor, C-F-C-Am)." }
    \line { \bold "3." \wordwrap-string #"Sin modulación: el crecimiento del final es por acumulación de capas, no por cambio de tono, igual que en la referencia." }
    \line { \bold "4." \wordwrap-string #"El estilo son las pisadas y palmas, no la guitarra: tres capas de pisadas y cuatro de palmas, que entran de a poco. Pisadas en 1 y 3, palmas en 2 y 4. No están en pentagrama todavía y es lo que más falta en esta hoja." }
    \line { \bold "5." \wordwrap-string #"Las secciones se distinguen por densidad, no solo por armonía. El puente es el punto más bajo justo antes del punto más alto." }
}

